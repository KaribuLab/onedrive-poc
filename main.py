import dotenv
import os
import logging
import onedrive

dotenv.load_dotenv()

LOG_LEVEL = int(os.getenv("LOG_LEVEL", "INFO"))

# Dict config for logger

LOGGING_CONFIG = {
    "level": LOG_LEVEL,
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
}

logging.basicConfig(**LOGGING_CONFIG)

LOGGER = logging.getLogger(__name__)
CLIENT_ID = os.getenv("CLIENT_ID")


def main():
    LOGGER.info(f"Client ID: {CLIENT_ID}")
    auth_code = onedrive.get_auth_code()
    if auth_code is None:
        onedrive.get_authorization_url(CLIENT_ID)
        url = input("Please enter the URL: ")
        code = onedrive.extract_code_from_url(url)
        onedrive.save_auth_code(code)
        LOGGER.info("Authorization code saved.")
        LOGGER.info("You can now run the script again.")
        return
    refresh_token = onedrive.get_refresh_token()
    if refresh_token is None:
        tokens = onedrive.request_tokens(CLIENT_ID, auth_code)
        refresh_token = tokens["refresh_token"]
        onedrive.save_refresh_token(refresh_token)
    access_token = onedrive.new_token(CLIENT_ID, refresh_token)
    files = onedrive.list_files(access_token)
    for file in files:
        LOGGER.info(f"File: {file['name']}")


if __name__ == "__main__":
    main()
