from django_qserializer import BaseSerializer

from main.models.models_ativos import Ativo
from commons.utils import to_tz

class AtivoSerializer(BaseSerializer):
    select_related = ['user']

    def serialize_object(self, obj: Ativo) -> dict:
        updated_at = to_tz(obj.updated_at, 'America/Sao_Paulo').strftime('%d/%m/%Y às %H:%M')

        return {
            'id': obj.id,
            'username': obj.user.username,
            'sigla': obj.sigla,
            'ref_price': obj.ref_price,
            'lower_limit': obj.lower_limit,
            'upper_limit': obj.upper_limit,
            'interval': obj.interval,
            'updated_at': updated_at
        }
