from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .forms import PaginatorForm
from main.services import ativos_svc


@require_GET
def list_ativos(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'authenticated': False}, status=401)
    sigla = request.GET.get('sigla')
    paginator = request.GET.get('paginator')
    paginator = PaginatorForm.model_validate_json(paginator)

    ativos = ativos_svc.list_ativos(
        sigla=sigla,
        page=paginator.page,
        rows_per_page=paginator.rows_per_page,
        sort_by=paginator.sort_by,
        descending=paginator.descending
    )

    return JsonResponse({})
