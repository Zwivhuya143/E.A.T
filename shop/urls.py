from django.urls import path

from . import views

urlpatterns = [
    path("", views.emptyIndex, name='index'),
    path("<slug:slug>", views.index, name='index'),
    path("register/", views.sign_up, name='register'),
    path("login/", views.sign_in, name='login'),
    path("logout/", views.sign_out, name='logout'),
    path("my_orders/", views.get_my_orders, name='my_orders'),
    path("order_details/<int:order_id>", views.order_details, name='order_details'),
    path("checkout/", views.checkout, name='checkout'),
    path("menu/", views.get_menu, name='menu'),
    path("blog/", views.get_blog, name='blog'),
    path("cart/", views.cart, name="cart"),
    path("reservations/", views.get_reservations, name="reservations"),
    path("add_to_cart/<int:product_id>", views.add_to_cart, name="add_to_cart"),
    path("remove_from_cart/<int:product_id>", views.remove_from_cart, name="remove_from_cart"),
]
