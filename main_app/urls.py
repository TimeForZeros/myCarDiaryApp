from django.urls import path, include 
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cars/', views.cars_index, name='index'),
    path('cars/<int:car_id>/', views.cars_detail, name='detail'),
    path('cars/create/', views.CarCreate.as_view(), name='cars_create'),
    path('cars/<int:pk>/update/', views.CarUpdate.as_view(), name='cars_update'),
    path('cars/<int:pk>/delete/', views.CarDelete.as_view(), name='cars_delete'),
    path('cars/<int:car_id>/add_maintenance/', views.add_maintenance, name='add_maintenance'),
    path('cars/<int:car_id>/add_photo/', views.add_photo, name='add_photo'),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('features/', views.FeaturesList.as_view(), name='features_index'),
    path('features/<int:pk>/', views.FeaturesDetail.as_view(), name='features_detail'),
    path('features/create/', views.FeaturesCreate.as_view(), name='features_create'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup', views.signup, name='signup'),
#     path('features/<int:pk>/update/', views FeaturesUpdate.as_view(), name='features_update'),
#     path('features/<int:pk>/delete/', views.FeaturesDelete.as_view(), name='features_delete'),

  path('cars/<int:car_id>/assoc_feature/<int:feature_id>/', views.assoc_feature, name='assoc_feature'),
  path('cars/<int:car_id>/unassoc_feature/<int:feature_id>/', views.unassoc_feature, name='unassoc_feature'),


    path('maintenance/', views.MaintenanceList.as_view(), name='maintenance_index'),
    path('maintenance/<int:pk>/', views.MaintenanceDetail.as_view(), name='maintenance_detail'),
    path('maintenance/create/', views.MaintenanceCreate.as_view(), name='maintenance_create'),
    # path('maintenance/<int:pk>/update/', views MaintenanceUpdate.as_view(), name='maintenance_update'),
    # path('maintenance/<int:pk>/delete/', views.MaintenanceDelete.as_view(), name='maintenance_delete'),

]