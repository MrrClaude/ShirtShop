from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home),
    # path('products/', views.products),
    # path('customer/', views.customer)
    path ('', views.indexSport, name='indexSport'),
    path ('aboutSport/', views.aboutSport, name='aboutSport'),
    path ('blogsingleSport/', views.blogsingleSport, name='blogsingleSport'),
    path ('shopSport/', views.shopSport, name='shopSport'),
    path ('cartSport/', views.cartSport, name='cartSport'),
    path ('contactSport/', views.contactSport, name='contactSport'),
    path ('blogSport/', views.blogSport, name='blogSport'),
    path ('productsingleSport/', views.productsingleSport, name='productsingleSport'),
    path ('checkoutSport/', views.checkoutSport, name='checkoutSport'),
   
    
]