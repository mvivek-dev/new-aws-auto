import os
import logging
import json
from typing import Dict, Any, List

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from boto3.exceptions import S3UploadFailedError
import pymysql  # for MySQL RDS


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger("devops_assignment")


def load_config() -> Dict[str, Any]:
    """
    Load configuration from environment variables.
    In practice these will come from a .env file (or similar) loaded before running.
    """
    config = {
        "aws_region": os.getenv("AWS_REGION", "ap-south-1"),
        "s3_bucket_name": os.getenv("S3_BUCKET_NAME"),
        "db_host": os.getenv("DB_HOST"),
        "db_user": os.getenv("DB_USER"),
        "db_password": os.getenv("DB_PASSWORD"),
        "db_name": os.getenv("DB_NAME"),
        "ec2_private_ip": os.getenv("EC2_PRIVATE_IP"),
    }
    logger.info("Configuration loaded")
    return config


def upload_log_to_s3(
    s3_client,
    bucket_name: str,
    log_file_path: str = "app.log",
) -> None:
    """
    Create a sample log file and upload it to the given S3 bucket.
    """
    if not bucket_name:
        logger.error(
            "S3 bucket name is not configured (S3_BUCKET_NAME is missing).",
        )
        return

    try:
        # Create a simple sample log file
        with open(log_file_path, "w", encoding="utf-8") as f:
            f.write("This is a sample application log entry.\n")

        # Upload file to S3
        s3_client.upload_file(log_file_path, bucket_name, log_file_path)
        logger.info("Uploaded %s to S3 bucket %s", log_file_path, bucket_name)

    except (BotoCoreError, ClientError, S3UploadFailedError, Exception) as e:
        logger.error("Failed to upload log file to S3: %s", e)


def list_s3_objects(
    s3_client,
    bucket_name: str,
    output_file: str = "s3_objects.txt",
) -> List[str]:
    """
    List objects in S3 bucket and write them to a text file.
    """
    object_keys: List[str] = []

    if not bucket_name:
        logger.error("S3 bucket name is missing.")
        return object_keys

    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)

        if "Contents" not in response:
            logger.info("No objects found in the bucket yet.")
            return object_keys

        for obj in response["Contents"]:
            object_keys.append(obj["Key"])

        with open(output_file, "w", encoding="utf-8") as f:
            for key in object_keys:
                f.write(f"{key}\n")

        logger.info("Listed %d objects into %s", len(object_keys), output_file)
        return object_keys

    except (BotoCoreError, ClientError, Exception) as e:
        logger.error("Failed to list S3 objects: %s", e)
        return object_keys


def rds_db_operations(config: Dict[str, Any]) -> None:
    """
    Connect to RDS MySQL, create table 'logs', insert a row, and query it.
    This is written as if it is talking to a real RDS instance, but can be
    treated as mock in this assignment.
    """
    host = config.get("db_host")
    user = config.get("db_user")
    password = config.get("db_password")
    db_name = config.get("db_name")

    if not all([host, user, password, db_name]):
        logger.error(
            "RDS configuration is incomplete. "
            "Check DB_HOST/DB_USER/DB_PASSWORD/DB_NAME.",
        )
        return

    try:
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
            connect_timeout=5,
        )
        logger.info("Connected to RDS MySQL at %s", host)

        with conn.cursor() as cursor:
            # 1. Create table
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                message VARCHAR(255) NOT NULL
            );
            """
            cursor.execute(create_table_sql)

            # 2. Insert sample row
            insert_sql = "INSERT INTO logs (message) VALUES (%s);"
            cursor.execute(
                insert_sql,
                ("This is a sample log row from automation script.",),
            )

            # 3. Query rows
            select_sql = "SELECT id, message FROM logs;"
            cursor.execute(select_sql)
            rows = cursor.fetchall()
            logger.info("Fetched %d rows from logs table", len(rows))
            for row in rows:
                logger.info("Row: id=%s, message=%s", row[0], row[1])

        conn.commit()
        conn.close()
        logger.info("RDS operations completed successfully.")

    except pymysql.MySQLError as e:
        logger.error("MySQL error during RDS operations: %s", e)


def get_ec2_metadata(ec2_client, private_ip: str) -> Dict[str, Any]:
    """
    Retrieve EC2 metadata (instance ID, type, region, private IP)
    using the private IP.
    """
    if not private_ip:
        logger.error(
            "EC2 private IP is not configured (EC2_PRIVATE_IP missing).",
        )
        return {}

    try:
        response = ec2_client.describe_instances(
            Filters=[{"Name": "private-ip-address", "Values": [private_ip]}],
        )

        reservations = response.get("Reservations", [])
        if not reservations or not reservations[0].get("Instances"):
            logger.warning(
                "No EC2 instance found with private IP %s",
                private_ip,
            )
            return {}

        instance = reservations[0]["Instances"][0]

        metadata = {
            "instance_id": instance.get("InstanceId"),
            "instance_type": instance.get("InstanceType"),
            "region": ec2_client.meta.region_name,
            "private_ip": instance.get("PrivateIpAddress"),
        }
        return metadata

    except (BotoCoreError, ClientError, Exception) as e:
        logger.error("Failed to retrieve EC2 metadata: %s", e)
        return {}


def main() -> None:
    config = load_config()

    # Initialize AWS clients
    s3 = boto3.client("s3", region_name=config["aws_region"])
    ec2 = boto3.client("ec2", region_name=config["aws_region"])

    logger.info("Starting automation tasks")

    upload_log_to_s3(s3, config["s3_bucket_name"])
    list_s3_objects(s3, config["s3_bucket_name"])
    rds_db_operations(config)

    metadata = get_ec2_metadata(ec2, config["ec2_private_ip"])
    if metadata:
        logger.info("EC2 metadata: %s", json.dumps(metadata, indent=2))

    logger.info("Automation script finished")


if __name__ == "__main__":
    main()
