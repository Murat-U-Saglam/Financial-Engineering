# Packages and functions for loading environment variables
from dotenv import dotenv_values
import os


class Config:
    try:
        # Load environment variables from .env file in root directory
        dotenv_values()
    except FileNotFoundError:
        exit(code="No .env file found in root directory. Please create one.")
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_PORT = os.getenv("MYSQL_PORT")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
