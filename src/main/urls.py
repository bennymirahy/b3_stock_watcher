from django.urls import path

from main.views import views_ativos, views_auth

urlpatterns = [
    path('api/whoami', views_auth.whoami),
    path('api/login', views_auth.login),
    path('api/logout', views_auth.logout),

    path('api/ativos/list', views_ativos.list_ativos),
    path('api/ativos/<str:sigla>/save', views_ativos.save_ativo),
    path('api/ativos/<str:sigla>/delete', views_ativos.delete_ativo),
    path('api/ativos/fetch', views_ativos.fetch_ativos)
]
