import requests
import logging
import json
import os

LOGGER = logging.getLogger(__name__)

LOGIN_MICROSOFT_URL = "https://login.microsoftonline.com"
AUTH_URL = f"{LOGIN_MICROSOFT_URL}/common/oauth2/v2.0/authorize"
REDIRECT_URI = f"{LOGIN_MICROSOFT_URL}/common/oauth2/nativeclient"
REQUEST_TOKEN_URL = f"{LOGIN_MICROSOFT_URL}/common/oauth2/v2.0/token"
AUTH_SCOPES = [
    "Files.ReadWrite",
    "Files.ReadWrite.All",
    "Sites.ReadWrite.All",
    "offline_access",
]
RESPONSE_TYPE = "code"
PROMPT = "login"
GRANT_TYPE = "authorization_code"
CONFIG_FILE = "config.json"


def get_authorization_url(client_id: str) -> None:
    response = requests.get(
        AUTH_URL,
        params={
            "client_id": client_id,
            "response_type": RESPONSE_TYPE,
            "redirect_uri": REDIRECT_URI,
            "scope": " ".join(AUTH_SCOPES),
            "prompt": PROMPT,
        },
    )
    response.raise_for_status()
    LOGGER.info(f"Authorization URL: {response.url}")


def extract_code_from_url(url: str) -> str:
    return url.split("code=")[1].split("&")[0]


def save_auth_code(code: str) -> None:
    with open(CONFIG_FILE, "w") as file:
        raw = json.dumps({"code": code})
        file.write(raw)


def save_refresh_token(refresh_token: str) -> None:
    if not os.path.exists(CONFIG_FILE):
        return None
    data = {}
    with open(CONFIG_FILE, "r") as file:
        data = json.loads(file.read())
        if "code" not in data:
            LOGGER.error("Authorization code not found.")
            return None
    with open(CONFIG_FILE, "w") as file:
        data["refresh_token"] = refresh_token
        raw = json.dumps(data)
        file.write(raw)


def get_auth_code() -> str:
    if not os.path.exists(CONFIG_FILE):
        LOGGER.warn("Authorization code not found.")
        return None

    with open(CONFIG_FILE, "r") as file:
        content = file.read()
        data = json.loads(content)
        if "code" not in data:
            LOGGER.warn("Authorization code not found.")
            return None
        return data["code"]


def get_refresh_token() -> str:
    if not os.path.exists(CONFIG_FILE):
        LOGGER.error("Refresh token not found.")
        return None
    with open(CONFIG_FILE, "r") as file:
        content = file.read()
        data = json.loads(content)
        if "refresh_token" not in data:
            LOGGER.error("Refresh token not found.")
            return None
        return data["refresh_token"]


def new_token(client_id: str, refresh_token: str) -> str:
    response = requests.post(
        REQUEST_TOKEN_URL,
        data={
            "client_id": client_id,
            "refresh_token": refresh_token,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "refresh_token",
        },
    )
    data = response.json()
    LOGGER.debug(f"New Token Response: {data}")
    response.raise_for_status()
    return data["access_token"]


def request_tokens(client_id: str, auth_code: str) -> dict:
    response = requests.post(
        REQUEST_TOKEN_URL,
        data={
            "client_id": client_id,
            "code": auth_code,
            "redirect_uri": REDIRECT_URI,
            "grant_type": GRANT_TYPE,
        },
    )
    data = response.json()
    LOGGER.debug(f"Request Token Response: {data}")
    response.raise_for_status()
    LOGGER.info(f"Tokens: {data}")
    return data


def list_files(access_token: str):
    url = "https://graph.microsoft.com/v1.0/me/drive/root/children"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    data = response.json()
    LOGGER.debug(f"List Files Response: {data}")
    response.raise_for_status()
    return data["value"]
