from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    # API
    path('api-token-auth/', obtain_auth_token),

    # path('category', views.CategoryView.as_view()),

    # Menu-items
    # path('menu-items', views.MenuItemsView.as_view()),
    # path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),

    # User group management
    # path('groups/manager/users', permissions.manager_view),
    # path('groups/manager/users/<int:pk>', ),
    # path('groups/delivery-crew/users', ),
    # path('groups/delivery-crew/users/<int:pk>', ),

    # Cart management
    # path('cart/menu-items', views.CartView.as_view()),

    # Order management
    # path('orders', views.OrderView.as_view()),
    # path('orders/<int:pk>', views.OrderItemView.as_view()),
]