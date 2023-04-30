from django.urls import path
from . import views

urlpatterns = [
    path('menu-items', views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>', views.MenuItemsRUDView.as_view()),
    path('groups/manager/users', views.ManagerLCView.as_view()),
    path('groups/manager/users/<int:pk>', views.ManagerDView.as_view()),
    path('groups/delivery-crew/users', views.DeliveryCrewLCView.as_view()),
    path('groups/delivery-crew/users/<int:pk>', views.DeliveryCrewDView.as_view()),
    path('cart/menu-items', views.CartLCView.as_view()),
    path('cart/menu-items/<int:pk>', views.CartDView.as_view()),
    path('orders', views.OrderLCView.as_view()),
    path('orders/<int:pk>', views.OrderRUDView.as_view()),
    path('category', views.CategoryLCView.as_view()),
    path('category/<int:pk>', views.CategoryRUDView.as_view()),
    ]
