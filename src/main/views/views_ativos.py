from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST

from main.service import ativos_svc
from main.service.exceptions import AtivoNotFoundException, BrapiBaseException

from .views_forms import PaginatorForm, AssetForm


@require_GET
def list_ativos(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'ativos': [], 'count': 0}, status=401)

    sigla = request.GET.get('sigla')
    paginator = request.GET.get('paginator')
    paginator = PaginatorForm.model_validate_json(paginator)
    ativos, total_rows = ativos_svc.list_ativos(
        user=user,
        sigla=sigla,
        sort_by=paginator.sort_by,
        page=paginator.page,
        rows_per_page=paginator.rows_per_page,
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

    data = AssetForm.model_validate_json(request.body)
    action = ativos_svc.update_or_create_ativo(
        user=user,
        sigla=sigla,
        asset_data=data.model_dump()
    )

    return JsonResponse({'result': action})


@require_POST
def delete_ativo(request, sigla):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'authenticated': False}, status=401)
    pass

    try:
        ativos_svc.delete_ativo(user=user, sigla=sigla)
    except AtivoNotFoundException:
        return JsonResponse({'result': 'ativo nao encontrado'}, status=404)
    else:
        return JsonResponse({}, status=204)



@require_GET
def fetch_ativos(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'authenticated': False}, status=401)

    sigla_str = request.GET.get('sigla').upper()
    try:
        assets = ativos_svc.fetch_all_B3_assets(sigla_str)
    except BrapiBaseException:
        return JsonResponse({'error': 'erro ao conectar-se com a api da Brapi'}, status=503)
    else:
        return JsonResponse({'assets': assets})
