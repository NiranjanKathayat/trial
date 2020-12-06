
from django.urls import path
from store import views

urlpatterns = [
    path('', views.store, name='store'),
    path('detail_view/<int:id>/', views.detail_view, name="detail_view"),
    path('update_item/', views.update_item, name="update_item"),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('add_product/', views.product_form, name="product_form"),
    path('payment/', views.payment, name='payment'),
]
