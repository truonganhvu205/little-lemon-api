from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    # API
    path('api-token-auth/', obtain_auth_token),

    path('category', views.CategoryView.as_view()),

    # Menu-items
    path('menu-items', views.MenuItemView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),

    # User group management
    path('groups/manager/users', views.ManagerUserView.as_view()),
    path('groups/manager/users/<int:pk>', views.SingleManagerUserView.as_view()),
    path('groups/delivery-crew/users', views.DeliveryCrewUserView.as_view()),
    path('groups/delivery-crew/users/<int:pk>', views.SingleDeliveryCrewUserView.as_view()),

    # Cart management
    path('cart/menu-items', views.CartView.as_view()),

    # Order management
    path('orders', views.OrderView.as_view()),
    path('orders/<int:pk>', views.SingleOrderView.as_view()),
]
