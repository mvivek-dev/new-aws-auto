import os
import boto3
import pymysql
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET = os.getenv("S3_BUCKET_NAME")

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


def upload_log_to_s3():
    s3 = boto3.client("s3", region_name=AWS_REGION)

    log_content = f"Log generated at {datetime.utcnow()}"
    file_name = "app_log.txt"

    with open(file_name, "w") as f:
        f.write(log_content)

    s3.upload_file(file_name, S3_BUCKET, file_name)
    print("Log uploaded to S3")


def write_log_to_rds():
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            message VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute(
        "INSERT INTO logs (message) VALUES (%s)",
        ("Log uploaded to S3 successfully",)
    )

    connection.commit()
    cursor.close()
    connection.close()
    print("Log written to RDS")


def main():
    print("Starting automation")
    upload_log_to_s3()
    write_log_to_rds()
    print("Automation completed")


if __name__ == "__main__":
    main()
