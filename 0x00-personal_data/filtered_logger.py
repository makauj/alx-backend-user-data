#!/usr/bin/env python3
"""Filter_datum function that returns an obfuscated log message"""
import re
import logging
import csv
from typing import Dict, List
from os import environ
import mysql.connector  # type: ignore


PII_FIELDS = ("name", "phone", "ssn", "email", "address")


def filter_datum(fields: List[str],
                 redaction: str,
                 msg: str,
                 separator: str) -> str:
    """Filter_datum function that returns an obfuscated log message
    Args:
        feilds (dict): A list of strings to obfuscate
        redaction (str): The string to replace the sensitive data with
        message (str): String representing the log line
        separator (str): The separator between fields in the log line
    The function should a regex to repkace occurences of certain field values
    with the redaction value.
    """
    regex = r"(?i)({})".format("|".join(fields))
    return re.sub(regex, redaction, msg, flags=re.IGNORECASE)


def get_logger() -> logging.Logger:
    """Get a logger object with a specific format and level"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - /"
                                  "%(name)s - /"
                                  "%(levelname)s - /"
                                  "%(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Get a database connection"""
    username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    database = environ.get("PERSONAL_DATA_DB_NAME", "personal_data")
    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )


def get_data() -> List[Dict[str, str]]:
    """Get data from the database"""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM personal_data")
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Method to filter values in incoming log records using filter_datum.
        Values for fields in fields should be filtered.
        """
        record.msg = filter_datum(
            self.fields,
            self.REDACTION,
            record.msg,
            self.SEPARATOR
        )
        return super(RedactingFormatter, self).format(record)


def main():
    """Main function to set up logging and process data"""
    logger = get_logger()
    data = get_data()
    formatter = RedactingFormatter(PII_FIELDS)  # type: ignore
    for record in data:
        msg = "; ".join(f"{key}={value}" for key, value in record.items())
        log_record = logging.LogRecord(
            name=logger.name,
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg=msg,
            args=None,
            exc_info=None
        )
        formatter.format(log_record)
        logger.info(log_record.msg)


if __name__ == "__main__":
    main()
