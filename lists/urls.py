from django.urls import path
from lists import views

app_name = 'lists'

urlpatterns = [
    path('', views.home_page, name='home'),
    path('<int:list_id>/', views.view_list, name='view_list'),
    path('new', views.new_list, name='new_list')
]
