from django.urls import path

from.import views
urlpatterns = [
    path('main/', views.main, name='main'),
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('accounts/', views.accounts, name='accounts'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='update_item'),
]
