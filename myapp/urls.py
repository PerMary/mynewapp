from django.urls import path
from . import views

urlpatterns = [
	path('', views.demand_list, name='demand_list'),
	path('demand/<int:pk>/', views.demand_detail, name='demand_detail'),
	path('demand/new/', views.demand_new, name='demand_new'),
	path('demand/<int:pk>/edit/', views.demand_edit, name='demand_edit'),
	path('demand/<pk>/remove/', views.demand_remove, name='demand_remove'),
	path('demand/<pk>/position_new', views.position_new, name='position_new'),
	path('demand/<pk>/remove/', views.demand_remove, name='demand_remove'),
	path('demand/<pk>/position_edit', views.position_edit, name='position_edit'),
	path('demand/<pk>/position_remove/', views.position_remove, name='position_remove'),
]