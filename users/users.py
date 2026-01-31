import os
from dotenv import load_dotenv

load_dotenv()

# Get passwords from environment variables
PRODUCTION_USER_PASSWORD = os.getenv('PROD_SAUCEDEMO_USER_PASSWORD')
CI_USER_PASSWORD = os.getenv('CI_SAUCEDEMO_USER_PASSWORD')

# Production users
PRODUCTION_USERS = {
    "standard_user": {
        "username": "standard_user",
        "password": PRODUCTION_USER_PASSWORD
    },
    "locked_out_user": {
        "username": "locked_out_user",
        "password": PRODUCTION_USER_PASSWORD
    },
    "problem_user": {
        "username": "problem_user",
        "password": PRODUCTION_USER_PASSWORD
    }
}

# CI users (qa, dev, ci environments)
CI_USERS = {
    "standard_user": {
        "username": "standard_user",
        "password": CI_USER_PASSWORD
    },
    "locked_out_user": {
        "username": "locked_out_user",
        "password": CI_USER_PASSWORD
    },
    "problem_user": {
        "username": "problem_user",
        "password": CI_USER_PASSWORD
    }
}