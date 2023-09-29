from django.urls import path
from .views import *


app_name = 'searchengine_processor'

urlpatterns = [
    path('search_processor', WebSearchProcessor.as_view()),
    path('trend_processor', TrendAnalyser.as_view()),
    ]