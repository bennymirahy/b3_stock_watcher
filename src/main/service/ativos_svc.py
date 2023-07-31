import logging
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Tuple

from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.serializers.base import Serializer
from django.db.models import Max, Q

from commons.utils import to_tz
from main.client.brapi_api import BrapiAPI
from main.models.models_ativos import Ativo, AtivoHistory
from main.serializers.ativos_serializer import AtivoSerializer
from main.service.exceptions import AtivoNotFoundException, BrapiBaseException

# Logging config
logging.basicConfig(
    level=logging.INFO,
    filename='main.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()


def _get_filtered_ativos_qs(user: User, sigla: str, sort_by: str) -> Serializer:
    qs = Ativo.objects.to_serialize(AtivoSerializer).filter(user=user)
    if sigla:
        qs = qs.filter(Q(name__icontains=sigla))
    if sort_by:
        qs = qs.order_by(sort_by)
    return qs


def _ativos_paginator(
    ativos_qs: Serializer, page: int, rows_per_page: int
) -> Tuple[list, int]:
    if (rows_per_page == -1):
        rows_per_page = len(ativos_qs) if len(ativos_qs) > 0 else 1
    paginator = Paginator(object_list=list(ativos_qs), per_page=rows_per_page)
    page = paginator.get_page(page)
    total_rows = paginator.count
    return page.object_list, total_rows


def list_ativos(
    user: User,
    sigla: str,
    sort_by: str,
    page: str,
    rows_per_page: int
) -> Tuple[list, int]:
    ativos_qs = _get_filtered_ativos_qs(user, sigla, sort_by)
    ativos, total_rows = _ativos_paginator(ativos_qs, page, rows_per_page)
    ativos = [a.serialize() for a in ativos]
    return ativos, total_rows


def update_or_create_ativo(
    user: User,
    sigla: str,
    asset_data: dict
) -> str:
    _, created = Ativo.objects.update_or_create(
        user=user,
        sigla=sigla,
        defaults=asset_data
    )
    action = 'created' if created else 'updated'
    msg = f"Asset {sigla} {action} by user {user.username} with parameters: {asset_data}"
    logger.info(msg)
    return action


def delete_ativo(user: User, sigla: str):
    try:
        Ativo.objects.get(user=user, sigla=sigla).delete()
    except Ativo.DoesNotExist as ex:
        raise AtivoNotFoundException from ex
    else:
        msg = f"Asset {sigla} deleted by user {user.username}"
        logger.info(msg)


def fetch_all_B3_assets(sigla_str: str) -> list[str]:
    try:
        response = BrapiAPI().fetch_available_assets().assets
    except BrapiBaseException as ex:
        logger.error(msg=f'{repr(ex)}')
    else:
        filtered_assets = filter(lambda sigla: sigla_str in sigla, response)
        return list(filtered_assets)


def _fetch_asset_quote(sigla: str, interval: int):
    try:
        response = BrapiAPI().fetch_asset_quote(sigla, interval)
    except BrapiBaseException as ex:
        logger.error(msg=f'{repr(ex)}')
        raise
    else:
        return response['prices']


def _bulk_create_histories(ativos:list[Ativo], price_quote: dict):
    to_create = []
    for a in ativos:
        to_create.append(
            AtivoHistory(
                ativo=a,
                close_price=price_quote['close'],
                timestamp=price_quote['date']
            )
        )
    AtivoHistory.objects.bulk_create(to_create)


def _update_histories(ativos: list[Ativo]):
    to_update = defaultdict(list)
    # Monta dict com sigla x ativos (evita repeticao de logica para varios usuarios)
    for a in ativos:
        to_update[a.sigla].append(a)

    for sigla, ativos in to_update.items():
        prices = _fetch_asset_quote(sigla=sigla, interval=5)
        latest_price = prices[-1]
        # Cria historicos para todos os ativos de mesma sigla (diferentes usuarios)
        _bulk_create_histories(ativos, latest_price)


def monitor_ativos():
    # History mais recente de cada ativo
    histories = AtivoHistory.objects.values('ativo_id').annotate(latest_time=Max('created_at'))
    # Monta dict ativo_id x historico mais recente
    ativos_hist_time = {
        h['ativo_id']: h['latest_time']
        for h in histories
    }
    ativos = Ativo.objects.in_bulk()

    # Monta dict de ativos a serem atualizados
    to_update = []
    for id, ativo in ativos.items():
        try:
            hist_time = ativos_hist_time[id]
        except KeyError:  # Ativo sem historico
            to_update.append(ativo)
        else:
            interval = ativo.interval
            time_diff = to_tz(datetime.now(), 'UTC') - hist_time
            if time_diff >= timedelta(minutes=interval):
                to_update.append(ativo)

    _update_histories(to_update)
    # _check_price_tunels()
