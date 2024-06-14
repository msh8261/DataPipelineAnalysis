import csv
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s:%(funcName)s:%(levelname)s:%(message)s"
)

def generate_data(data_path, topic) -> dict:
        try:
            file_path = f"{data_path}/{topic}.csv"
            with open(file_path, encoding="utf-8-sig") as csvfile:
                csvreader = csv.DictReader(csvfile)
                list_of_rows = []
                for rows in csvreader:
                    list_of_rows.append(rows)


            return list_of_rows
        except FileNotFoundError:
            logging.error(f"file {data_path}/{topic} not found.")
        except Exception as e:
            logging.error(
                f"Failed to process the file and \
                                sending messages."
            )
            return 'not-ready'
