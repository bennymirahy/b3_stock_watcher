import logging

from main.client import brapi_endpoints as endpoints

# Logging config
logging.basicConfig(
    level=logging.DEBUG,
    filename='api.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()


class BrapiAPI():
    client = {
        'logger': logger,
        'base_url': 'https://brapi.dev/api'
    }

    def fetch_available_assets(self):
        assets = endpoints.ListB3Assets(self.client).send()
        return assets.parsed
