from django.urls import path
from .views import generate_badge, svg_chart, svg_chart2

urlpatterns = [
    path('generate_badge', generate_badge),

    path('chart/', svg_chart, name='chart'),
    path('chart2/', svg_chart2, name='chart2'),
]
