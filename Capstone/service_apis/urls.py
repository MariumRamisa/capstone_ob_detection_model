from django.urls import path
from .views import InsertInfo, GetInfo, GetAllInfo, StoreDetectionResults, GetInfoByDateRange


urlpatterns = [
    path('insert-info/', InsertInfo.as_view(), name='insert-info'),
    path('get-info/', GetInfo.as_view(), name='get-info'),
    path('get-all-info/', GetAllInfo.as_view(), name='get-all-info'), 
    path('store-detection-results/', StoreDetectionResults.as_view(), name='store-detection-results'),  
    path('get-info-by-date-range/', GetInfoByDateRange.as_view(), name='get-info-by-date-range'),
]
