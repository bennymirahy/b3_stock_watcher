from typing import Tuple

from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.serializers.base import Serializer
from django.db.models import Q

from main.client.brapi_api import BrapiAPI
from main.models.models_ativos import Ativo
from main.serializers.ativos_serializer import AtivoSerializer


def _get_filtered_ativos_qs(user: User, sigla: str, sort_by: list) -> Serializer:
    qs = Ativo.objects.to_serialize(AtivoSerializer).filter(user=user)
    if sigla:
        qs = qs.filter(Q(name__icontains=sigla))
    qs = qs.order_by(sort_by)

    return qs


def _ativos_paginator(
    ativos_qs: Serializer, page: int, rows_per_page: int, descending: bool
) -> Tuple[list, int]:
    paginator = Paginator(object_list=ativos_qs, per_page=rows_per_page)
    page = paginator.get_page(page)
    total_rows = paginator.count

    return list(page.object_list), total_rows


def list_ativos(
    user: User,
    sigla: str,
    sort_by: list,
    page: str,
    rows_per_page: int,
    descending: bool
) -> Tuple[list, int]:
    ativos_qs = _get_filtered_ativos_qs(user, sigla, sort_by)
    ativos, total_rows = _ativos_paginator(ativos_qs, page, rows_per_page, descending)
    ativos = [a.serialize() for a in ativos]

    return ativos, total_rows


def fetch_all_B3_assets(sigla_str: str):
    response = BrapiAPI().fetch_available_assets().assets
    filtered_assets = filter(lambda sigla: sigla_str in sigla, response)
    return list(filtered_assets)
