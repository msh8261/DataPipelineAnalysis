from secrets import token_bytes
from base64 import b64encode

FEATURE_FLAGS = {
    "ENABLE_TEMPLATE_PROCESSING": True,
}

ENABLE_PROXY_FIX = True
TALISMAN_ENABLED = False

SECRET_KEY = b64encode(token_bytes(42)).decode()