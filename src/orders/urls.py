from django.urls import path

from . import views

app_name = 'order'

urlpatterns = [
    path('', views.ListOrder.as_view(), name='list'),
    path('user', views.MyOrder.as_view(), name='user'),
    path('<int:pk>/create', views.CreateOrder.as_view(), name='create'),
    path('<int:pk>/detail', views.ShowOrder.as_view(), name='detail'),
    path('<int:pk>/delete', views.DeleteOrder.as_view(), name='delete'),
    path('<int:pk>/append', views.AddCustomer.as_view(), name='append'),
    path('<int:pk>/drop/<int:ck>', views.DropCustomer.as_view(), name='drop'),
    path('<int:pk>/update/<int:ck>', views.ChangeCustomer.as_view(), name='update'),
    path('<int:pk>/status/<str:status>', views.ChangeOrderStatus.as_view(), name='status'),
]
