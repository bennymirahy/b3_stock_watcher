from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST

from main.service import ativos_svc

from .views_forms import PaginatorForm


@require_GET
def list_ativos(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'authenticated': False}, status=401)

    sigla = request.GET.get('sigla')
    paginator = request.GET.get('paginator')
    paginator = PaginatorForm.model_validate_json(paginator)
    ativos, total_rows = ativos_svc.list_ativos(
        user=user,
        sigla=sigla,
        sort_by=paginator.sort_by,
        page=paginator.page,
        rows_per_page=paginator.rows_per_page,
        descending=paginator.descending
    )

    return JsonResponse({
        'ativos': ativos,
        'count': total_rows
    })


@require_POST
def save_ativo(request, sigla):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'authenticated': False}, status=401)
    pass


@require_GET
def fetch_ativos(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'authenticated': False}, status=401)

    sigla_str = request.GET.get('sigla')
    assets = ativos_svc.fetch_all_B3_assets(sigla_str)

    return JsonResponse({'assets': assets})
