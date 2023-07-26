from dotenv import load_dotenv
import os
load_dotenv("../../.env")

DATABASE_URL = os.getenv("DATABASE_URL")
EMAIL_ADDR = os.getenv("EMAIL_ADDR")
EMAIL_PASS = os.getenv("EMAIL_PASS")