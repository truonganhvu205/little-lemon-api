from django.urls import path
from . import views

urlpatterns = [
    # API
    # path('users', ),
    # path('users/users/me/', ),
    # path('/token/login/', ),

    path('category', views.CategoryView.as_view()),

    # Menu-items
    path('menu-items', views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),

    # User group management
    # path('groups/manager/users', ),
    # path('groups/manager/users/<int:pk>', ),
    # path('groups/delivery-crew/users', ),
    # path('groups/delivery-crew/users/<int:pk>', ),

    # Cart management
    # path('cart/menu-items', ),

    # # Order management
    # path('orders', ),
    # path('orders/<int:pk>', ),
]