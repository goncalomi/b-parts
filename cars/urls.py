from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('add-plate', views.CreateCustomerView.as_view(), name='add_plate'),
    path('list-plates', views.ListPlatesView.as_view(), name='list_plates'),
    path('customers/<int:pk>/', views.UpdateCustomerView.as_view(), name='edit_customer'),
]
