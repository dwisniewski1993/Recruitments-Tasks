import os
import logging as log
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from exceptions import *
from config import *


def main():
    log.basicConfig(level=log.INFO)
    log.info('Pandas data-frame to PDF converter starting')

    # detect working directory
    current_path = os.path.dirname(os.path.abspath(__file__))

    # set directory for input data files like .xls and .json schemas files
    input_file_path = "/".join([current_path, INPUT_DATA_DIRECTORY])

    output_file_path = "/".join([current_path, OUTPUT_DATA_DIRECTORY])

    if not os.path.exists(output_file_path):
        os.makedirs(output_file_path)

    # detecting schemas files
    schemas = [file for file in os.listdir(input_file_path) if os.path.isfile(os.path.join(input_file_path, file))
               and file.split('.')[-1] == 'json']

    log.info(f"{len(schemas)} schemas file detected")

    # parsing each schema file - if more than one - each after another
    for schema in schemas:
        log.info(f"Start parsing {schema} file...")

        # absolute path to schema file
        schema_path = "/".join([input_file_path, schema])

        # read schema file
        with open(schema_path, 'r') as f:
            schema_json = json.loads(f.read())

        # check valid schema
        if 'file_name' in schema_json:
            data_file_name = schema_json['file_name']
            data_file_path = "/".join([input_file_path, data_file_name])

            # check if data file exist
            if os.path.exists(data_file_path):
                log.info(f"File {data_file_name} founded")

                # loading data file to pandas ExcelFile
                xls_file = pd.ExcelFile(f"{current_path}/{INPUT_DATA_DIRECTORY}/{data_file_name}")

                file_output_dir = f"{output_file_path}/{data_file_name}_results"

                if not os.path.exists(file_output_dir):
                    os.makedirs(file_output_dir)

                if 'sheets' in schema_json:
                    # check num sheets in schema and data file
                    num_sheets_schema = schema_json['sheets']['num_sheets']
                    num_sheets_file = len(xls_file.sheet_names)

                    if num_sheets_schema == num_sheets_file:

                        # load each sheet to pandas DF
                        for item in schema_json['sheets']['sheets_items']:
                            if item['name'] in xls_file.sheet_names:
                                log.info(f"Start generating PDF for {item['name']} sheet from {data_file_name} file...")

                                item_path = f"{file_output_dir}/{item['name']}"

                                if not os.path.exists(item_path):
                                    os.makedirs(item_path)

                                df = pd.read_excel(xls_file, sheet_name=item['name'], header=None)

                                # split sheet to tables
                                df_list = np.split(df, df[df.isnull().all(1)].index)

                                if len(df_list) != item['num_tables']:
                                    raise SchemaNotValid(f"According to schema data file should contain "
                                                         f"{item['num_tables']}, {len(df_list)} founded!")
                                else:

                                    # each table going to be display in next PDF page for convenience
                                    with PdfPages(f"{item_path}/{item['name']}.pdf") as pdf:

                                        for i in range(len(df_list)):
                                            fig = plt.figure(dpi=100)
                                            fig.suptitle(f"{item['name']} sheet tables", fontsize=16)
                                            fig.set_size_inches([20, 5])

                                            dfr = df_list[i].dropna(axis=1, how='all')\
                                                .dropna(axis=0, how='all')\
                                                .replace(np.nan, '', regex=True)

                                            ax = fig.add_subplot('111')
                                            ax.axis('tight')
                                            ax.axis('off')
                                            ax.set_title(label=item['tables_titles'][i])
                                            ax.table(cellText=dfr.values, loc='center')

                                            pdf.savefig()

                            else:
                                raise SchemaNotValid(
                                    f"Data file should contain sheet {item['name']} but sheet not exist!")
                    else:
                        raise SchemaNotValid(f"Schema suppose to have {num_sheets_schema}, {num_sheets_file} founded")
                else:
                    f"'sheets' key not found in schema {schema}"
            else:
                raise FileNotFoundError(f"File {data_file_path} not founded!")
        else:
            raise SchemaNotValid(f"'file_name' key not found in schema {schema}")


if __name__ == '__main__':
    main()
