from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),


    path('order/<int:id>/', views.ordering, name='ordering'),

    path('cart/', views.cart, name='cart'),

    path('address/', views.address, name='address'),

   
    path('product/<int:id>/', views.product_detail, name='product-detail'),


    path('about/', views.about, name='about'),


    path('update-quantity/<int:id>/', views.update_quantity, name='update_quantity'),

    path('confirmed-orders/', views.confirmed_orders, name='confirmed-orders'),


    
    path('payment-success/', views.payment_success, name='payment-success'),
    path('payment-cancel/', views.payment_cancel, name='payment-cancel'),




#testing

# urls.py
path("adminorders/", views.admin_orders, name="admin_orders"),

path("mark-delivered/<int:order_id>/", views.mark_delivered, name="mark_delivered"),






path('add_product/', views.add_product, name='add-product'),



path('learning/', views.learning_view, name='learning'),


path("new_arraival/",views.new_arraival,name='new-arraival')

    
    
]