import boto3
import pandas as pd
import logging
from src.logger import logging
from io import StringIO

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

class s3_operations:
    def __init__(self, bucket_name, aws_access_key, aws_secret_key, region_name="us-east-1"):
        """
        Initalize the S3_operations class with AWS credentials and S3 bucket details
        """
        self.bucket_name = bucket_name
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region_name
        )
        logging.info("Data Ingestion from S3 bucket initalized")


    def fetch_file_from_s3(self, file_key):
        """
        Fetches the CSV file from the s3 bucket naf returns it as a Pandas Dataframe
        :param file_key: s3 file path (e.g.: 'data/data.csv')
        :return: Pandas Dataframe
        """
        try:
            logging.info(f"Fetching the file '{file_key}' from s3 bucket '{self.bucket_name}'...")
            obj = self.s3_client.get_object(Bucket = self.bucket_name, Key = file_key)
            df = pd.read_csv(StringIO(obj['Body'].read().decode('utf-8')))
            logging.info(f"Successfully fetched and loaded '{file_key}' from the s3 bucket that has {len(df)} records")
            return df
        except Exception as e:
            logging.exception(f"Failed to fetch '{file_key}' from s3: {e}")
            return None
        