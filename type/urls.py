from django.urls import path
from type import views

urlpatterns = [
    path('', views.allTypes, name='all-types'),
    path('add_new/', views.add_new, name='add_new'),
    path('add_new_category/', views.add_new_category, name='add_new_category'),
    path('add_new_branch_category/', views.add_new_branch_category, name='add_new_branch_category'),
]