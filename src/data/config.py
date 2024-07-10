# Packages and functions for loading environment variables
from dotenv import dotenv_values


class Config:
    try:
        # Load environment variables from .env file in root directory
        dotenv_values()
    except FileNotFoundError:
        exit("No .env file found in root directory. Please create one.")
    MYSQL_PASSWORD = dotenv_values("MYSQL_PASSWORD")
    MYSQL_USER = dotenv_values("MYSQL_USER")
    MYSQL_HOST = dotenv_values("MYSQL_HOST")
    MYSQL_PORT = dotenv_values("MYSQL_PORT")
    MYSQL_DATABASE = dotenv_values("MYSQL_DATABASE")
