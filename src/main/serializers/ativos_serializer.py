from datetime import datetime

import pytz
from django_qserializer import BaseSerializer

from commons.utils import to_tz
from main.models.models_ativos import Ativo, AtivoHistory


class AtivoSerializer(BaseSerializer):
    select_related = ['user']
    prefetch_related = ['ativohistory_set']

    def get_last_update(self, obj: Ativo):
        last_history = obj.ativohistory_set.order_by('timestamp').last()
        return last_history.timestamp

    def serialize_object(self, obj: Ativo) -> dict:
        last_update_unix = self.get_last_update(obj)
        updated_at = to_tz(datetime.fromtimestamp(last_update_unix, tz=pytz.UTC), 'America/Sao_Paulo')
        return {
            'id': obj.id,
            'username': obj.user.username,
            'sigla': obj.sigla,
            'ref_price': round(obj.ref_price, 3),
            'lower_limit': obj.lower_limit,
            'upper_limit': obj.upper_limit,
            'interval': obj.interval,
            'updated_at': updated_at.strftime('%d/%m/%Y às %H:%M')
        }

class HistorySerializer(BaseSerializer):
    def serialize_object(self, obj: AtivoHistory) -> dict:
        date_time = to_tz(
            datetime.fromtimestamp(obj.timestamp, tz=pytz.UTC), 'America/Sao_Paulo'
        ).isoformat()
        return {
            'id': obj.id,
            'price': obj.close_price,
            'datetime': date_time
        }
