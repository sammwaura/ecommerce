from django.urls import path
from . import views

urlpatterns = [
    # Leave as empty string for base url
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),

    path('update_item/', views.updateItem, name="update_item"),
     path('process_order/', views.processOrder, name="process_order"),
     path('', views.mpesa, name="mpesa"),
     path('daraja/stk_push', views.stk_push_callback, name="stk_push_callback")
    
]
