from django.urls import path
from . import views
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('categories', views.CategoryView.as_view(
        {
          'get': 'list',
          'post': 'create',
        })
       ),
    path('categories/<int:pk>', views.CategoryView.as_view(
        {
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        })
    ),
    path('menu-items', views.MenuItemView.as_view(
        {
            'get': 'list',
            'post': 'create',
        })
    ),
    path('menu-items/<int:pk>', views.MenuItemView.as_view(
        {
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        })
    ),
    path('groups/manager/users', views.ManagerView.as_view(
        {
            'get': 'list',
            'post': 'create',
        })
    ),
    path('groups/manager/users/<int:pk>', views.ManagerView.as_view(
        {
            'delete': 'destroy',
        })
    ),
    path('groups/delivery-crew/users', views.DeliveryCrewView.as_view(
        {
            'get': 'list',
            'post': 'create',
        })
    ),
    path('groups/delivery-crew/users/<int:pk>', views.DeliveryCrewView.as_view(
        {
            'delete': 'destroy',
        })
    ),
    path('cart/menu-items', views.CartView.as_view(
        {
            'get': 'list',
            'post': 'create',
            'delete': 'destroy',
        })
    ),
    path('orders', views.OrderView.as_view(
        {
            'get': 'list',
            'post': 'create',
        })
    ),
    path('orders/<int:pk>', views.OrderView.as_view(
        {
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        })
    ),
]
