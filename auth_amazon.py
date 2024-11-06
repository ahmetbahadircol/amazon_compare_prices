from dotenv import load_dotenv
import os


load_dotenv()

lwa_app_id = os.getenv("LWA_APP_ID")
lwa_client_secret = os.getenv("LWA_CLIENT_SECRET")
sp_api_refresh_token = os.getenv("SP_API_REFRESH_TOKEN")


credentials = dict(
    refresh_token=sp_api_refresh_token,
    lwa_app_id=lwa_app_id,
    lwa_client_secret=lwa_client_secret,
)


def auth():
    from sp_api.base import Client

    try:
        print("Authotication is successful...")
        return Client(credentials=credentials)
    except TypeError as e:
        print(f"Error auth: {e}")
