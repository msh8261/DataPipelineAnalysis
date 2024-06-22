import csv
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s:%(funcName)s:%(levelname)s:%(message)s"
)

def generate_data(data_path, topic) -> dict:
        try:
            file_path = f"{data_path}/{topic}.csv"
            list_of_rows = []
            #encoding="utf-8-sig"
            with open(file_path, newline='', encoding='utf-8' ) as csvfile:
                csvreader = csv.DictReader(csvfile)                
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
