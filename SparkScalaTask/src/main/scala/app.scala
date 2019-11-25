import org.apache.spark.sql.expressions._
import org.apache.spark.sql.functions._
import org.apache.spark.sql.{DataFrame, SparkSession}


object app extends App {

  // Paths to files
  val us_cities_file: String = "uscitiesv1.5.csv"
  val parking_file: String = "parking-violations-issued-fiscal-year-2014-august-2013-june-2014.csv"

  // Define spark session
  val spark: SparkSession = SparkSession.builder()
    .master("local[*]")
    .appName("Recruitment-Task")
    .getOrCreate()

  import spark.implicits._

  // Load us cities file to data frame
  var cities_df: DataFrame = spark.read.format("csv").option("header", "true").load(us_cities_file)

  // Making mapping for state name and shortcut
  val replacements_state: scala.collection.Map[String, String] = cities_df.select("state_id", "state_name").rdd
    .map(row => (row.getString(0), row.getString(1))).collectAsMap()

  //Making mapping for population in each state
  val population_in_state: scala.collection.Map[String, String] = cities_df.select("state_id", "population")
    .na.drop().withColumn("population", $"population".cast("Int"))
    .groupBy("state_id").sum("population").rdd
    .map(row => (row.getString(0), row.getLong(1).toString)).collectAsMap()
  cities_df = null

  // Load second file to data frame
  val parking_df: DataFrame = spark.read.format("csv").option("header", "true").load(parking_file)

  // Defining window partitioner
  val windowSpec = Window.partitionBy("State Name").orderBy("Year-Month")

  // Making list with dictionary keys
  val stateIdsSequence = population_in_state.keys.toList

  // Calculate result data frame
  var result: DataFrame = parking_df
    .select($"Registration State".as("State Name"), $"Issue Date"as("Year-Month"))
    .withColumn("Year-Month", concat_ws("-", slice(split($"Year-Month", "-"), 1, 2)))
    .groupBy($"State Name", $"Year-Month").count().withColumnRenamed("count", "Ratio")
    .withColumn("helper", $"State Name")
    .na.replace("helper", population_in_state.toMap)
    .withColumn("Ratio", format_number($"Ratio".cast("Float") / $"helper".cast("Float"), 8)).drop("helper")
    .where($"State Name".isin(stateIdsSequence:_*))
    .na.replace("State Name", replacements_state.toMap)
    .orderBy(desc("State Name"), asc("Year-Month"))
    .withColumn("help-100", lit(100.00))
    .withColumn("Difference (%)", $"help-100" - when((lag("Ratio", 1)
      .over(windowSpec)).isNull, null).otherwise(when($"Ratio" === lag("Ratio", 1).over(windowSpec), 100.00)
      .otherwise(when($"Ratio" > lag("Ratio", 1).over(windowSpec), (lag("Ratio", 1).over(windowSpec)*$"help-100")/$"Ratio")
        .otherwise(($"Ratio"*$"help-100"/lag("Ratio", 1).over(windowSpec)))))).drop("help-100")
    .withColumn("Difference (%)", when($"Difference (%)".isNull, null).otherwise(format_number($"Difference (%)", 2)))

  // Creating connection to database
  val jdbcHostname = "localhost"
  val jdbcPort = 3306
  val jdbcDatabase = "spark_task"
  val jdbcUsername = "root"
  val jdbcPassword = ""
  val jdbcDriver = "com.mysql.jdbc.Driver"

  val jdbcUrl = s"jdbc:mysql://${jdbcHostname}:${jdbcPort}/${jdbcDatabase}"

  import java.util.Properties
  val connectionProperties = new Properties()

  connectionProperties.put("user", s"${jdbcUsername}")
  connectionProperties.put("password", s"${jdbcPassword}")
  connectionProperties.put("jdbcDriver", s"${jdbcDriver}")

  Class.forName(jdbcDriver)

  result.write.jdbc(jdbcUrl, "US_cities_tickets_stats", connectionProperties)

}
