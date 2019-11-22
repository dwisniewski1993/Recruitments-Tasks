import org.apache.spark.sql.catalyst.encoders.RowEncoder
import org.apache.spark.sql.types.{StringType, StructField, StructType}
import org.apache.spark.sql.{DataFrame, Row, SparkSession}


object app extends App {

  val us_cities_file: String = "uscitiesv1.5.csv"
  val parking_file: String = "parking-violations-issued-fiscal-year-2014-august-2013-june-2014.csv"

  val spark: SparkSession = SparkSession.builder()
    .master("local[*]")
    .appName("Recruitment-Task")
    .getOrCreate()

  import spark.implicits._

  val cities_df: DataFrame = spark.read.format("csv").option("header", "true").load(us_cities_file)
  val parking_df: DataFrame = spark.read.format("csv").option("header", "true").load(parking_file)

  println(cities_df.columns.toSeq)
  println(parking_df.columns.toSeq)

  val replacements_state = cities_df.select("state_id", "state_name").rdd
    .map(row => (row.getString(0), row.getString(1))).collectAsMap()

  val schema = StructType(Seq(
    StructField("State Name", StringType),
    StructField("Year_Month", StringType),
    StructField("Ratio", StringType)
  ))

  val encoder = RowEncoder(schema)

  val population_in_state = cities_df.select("state_id", "population")
    .na.drop().withColumn("population", $"population".cast("Int"))
    .groupBy("state_id").sum("population").rdd
    .map(row => (row.getString(0), row.getLong(1).toInt)).collectAsMap()

  val result: DataFrame = parking_df
    .select("Registration State", "Issue Date")
    .groupBy($"Registration State".alias("State_Id"), $"Issue Date".alias("Date")).count()
    .orderBy("Issue Date").map(row => {
    val row1 = row.getString(0)
    val row2 = row.getString(1)
    val row3 = row.getLong(2)

    var state_name: String = null
    val year_month = row2.split('-').slice(0, 2).mkString("-")
    var rate: Float = 0.0.toFloat

    if (replacements_state.contains(row1)) {
      state_name = replacements_state(row1)
      rate = (row3.toFloat / population_in_state(row1).toFloat)
    }
    else {
      state_name = "Route " + row1
      rate = 0
    }
    Row(state_name, year_month, f"$rate%1.8f")
  }
  )(encoder)

  result.show()

}
