from django.urls import path
from .views import generate_badge, svg_chart

urlpatterns = [
    path('generate_badge', generate_badge),

    path('chart/', svg_chart, name='chart'),
]
