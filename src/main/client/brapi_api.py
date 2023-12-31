import logging

from main.client import brapi_endpoints as endpoints

logger = logging.getLogger()


class BrapiAPI():
    client = {
        'logger': logger,
        'base_url': 'https://brapi.dev/api'
    }

    def fetch_available_assets(self):
        assets = endpoints.ListB3Assets(self.client).send()
        return assets.parsed

    def fetch_asset_quote(self, sigla: str, interval: int) -> dict:
        prices = endpoints.ConsultAssetQuote(self.client, sigla).send(interval)
        return prices.parsed.dict()
