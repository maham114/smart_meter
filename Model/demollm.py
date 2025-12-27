from dotenv import dotenv_values
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, "token.env")

print("Script directory:", BASE_DIR)
print("Env path:", ENV_PATH)
print("Env exists:", os.path.exists(ENV_PATH))

config = dotenv_values(ENV_PATH)
HF_TOKEN = config.get("HF_TOKEN")

print("HF_TOKEN:", HF_TOKEN)
