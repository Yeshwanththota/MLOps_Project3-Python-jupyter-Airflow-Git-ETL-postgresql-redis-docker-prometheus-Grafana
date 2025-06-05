import psycopg2
import pandas as pd
from src.logger import get_logger
from src.custom_exception import CustomException
import os
from sklearn.model_selection import train_test_split
import sys
from config.database_config import DB_CONFIG
from config.paths_config import * 

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self, db_params, output_dir):

        self.db_params = db_params
        self.output_dir = output_dir

        os.makedirs(self.output_dir, exist_ok=True)
        logger.info(f"Output directory created at: {self.output_dir}")
    def connect_to_db(self):
        try:
            conn = psycopg2.connect(
                host=self.db_params['HOST'],
                port=self.db_params['PORT'],
                dbname=self.db_params['dbname'],
                user=self.db_params['USER'],
                password=self.db_params['PASSWORD']
            )
            logger.info("Database connection established successfully.")
            return conn
        except Exception as e:
            logger.error(f"Error connecting to the database: {e}")
            raise CustomException(f"Database connection failed: {e}")
    def extact_data(self):
        try:
            conn = self.connect_to_db()
            query = "SELECT * FROM public.titanic"
            df = pd.read_sql_query(query, conn)
            conn.close()
            logger.info("Data extracted successfully from the database.")
            return df
        except Exception as e:
            logger.error(f"Error extracting data: {e}")
            raise CustomException(f"Data extraction failed: {e}")
    def save_data(self, df):
        try:
            train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
            train_df.to_csv(TRAIN_PATH, index=False)

            test_df.to_csv(TEST_PATH, index=False)

            logger.info(f"Data saved to {TRAIN_PATH} and {TEST_PATH}.")
        except Exception as e:
            logger.error(f"Error saving data: {e}")
            raise CustomException(f"Data saving failed: {e}")
    def run(self):
        try:
            logger.info("Starting data ingestion process...")
            df = self.extact_data()
            self.save_data(df)
            logger.info("Data ingestion process completed successfully.")
        except Exception as e:
            logger.error(f"Data ingestion process failed: {e}")
            raise CustomException(f"Data ingestion failed: {e}")
if __name__ == "__main__":
    
    data_ingestion = DataIngestion(DB_CONFIG, RAW_DIR)
    data_ingestion.run()