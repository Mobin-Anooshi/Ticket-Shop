from django.urls import path
from . import views



app_name='home'
urlpatterns =[
    path('',views.HomeView.as_view(),name='home'),
    path('travels/',views.TravelView.as_view(),name='travels')
]