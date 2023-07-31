from memoize import memoize

from main.client import brapi_forms as forms
from main.client.brapi_base import BaseRequest


class ListB3Assets(BaseRequest):
    # Buscar por todos os ativos listados na B3
    method = 'GET'
    endpoint = 'available'
    output_form = forms.AvailableAssets

    def __repr__(self):
        # Mesmo cache para todas as intancias
        return f'ListB3Assets_{self.endpoint}'

    @memoize(timeout=5 * 60)
    def send(self):
        return super().send()

    def clean_response(self, resp: dict) -> dict:
        return {'assets': resp['indexes'] + resp['stocks']}

    def parse_response(self, clean_resp: dict) -> forms.AvailableAssets:
        return self.output_form.model_validate(clean_resp)


class ConsultAssetQuote(BaseRequest):
    # Consultar cotacao de um ativo
    method = 'GET'
    output_form = forms.AssetPrices

    def __init__(self, client: dict, sigla: str):
        self.endpoint = f'quote/{sigla}'
        super().__init__(client)

    def __repr__(self):
        # Cache por sigla
        return f'ConsultAssetQuote_{self.endpoint}'

    @memoize(timeout=3 * 60)
    def send(self, interval):
        params = {
            'interval': f'{interval}m',
            'range': '1d',
            'fundamental': False,
            'dividends': False
        }
        return super().send(params=params)

    def clean_response(self, resp: dict) -> dict:
        clean_prices = [
            data for data in resp['results'][0]['historicalDataPrice'] if data['close'] is not None
        ]
        return {'prices': clean_prices}

    def parse_response(self, clean_resp: dict) -> forms.AssetPrices:
        return self.output_form.model_validate(clean_resp)
