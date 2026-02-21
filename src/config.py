import os
from dotenv import load_dotenv

load_dotenv()

# --- URLs ---
BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")
INVENTORY_URL = f"{BASE_URL}/inventory.html"
CART_URL = f"{BASE_URL}/cart.html"

# --- Credentials ---
STANDARD_USER = os.getenv("STANDARD_USER", "standard_user")
LOCKED_OUT_USER = os.getenv("LOCKED_OUT_USER", "locked_out_user")
PROBLEM_USER = os.getenv("PROBLEM_USER", "problem_user")
STANDARD_PASSWORD = os.getenv("STANDARD_PASSWORD", "secret_sauce")