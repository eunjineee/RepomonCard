from django.urls import path
from .views import repo_card, repo_personal_card, user_card, svg_chart

urlpatterns = [
    path('repo', repo_card),
    path('repo_personal', repo_personal_card),
    path('user', user_card),
    path('chart/', svg_chart, name='chart'),
    # path('chart2/', svg_chart2, name='chart2'),
]
