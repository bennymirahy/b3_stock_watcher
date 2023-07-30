from memoize import memoize

from main.client import brapi_forms as forms
from main.client.brapi_base import BaseRequest


class ListB3Assets(BaseRequest):
    # Buscar por todos os ativos listados na B3
    method = 'GET'
    endpoint = 'available'
    output_form = forms.AvailableAssets

    def __repr__(self):
        # Mesma representacao para todas as intancias para o cache fucionar
        return f"ListB3Assets({self.endpoint})"

    @memoize(timeout=5 * 60)
    def send(self):
        return super().send()

    def clean_response(self, response: dict):
        return {'assets': response['indexes'] + response['stocks']}

    def parse_response(self, response: dict):
        return self.output_form.model_validate(response)


class ConsultAssetQuote(BaseRequest):
    # Consultar cotacao de um ativo
    pass
