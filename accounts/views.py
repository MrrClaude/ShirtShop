from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def indexSport(request):
    return render(request, "sports/index.html")
def aboutSport(request):
    return render(request, "sports/about.html")
def cartSport(request):
    return render(request, "sports/cart.html")
def contactSport(request):
    return render(request, "sports/contact.html")
def blogSport(request):
    return render(request, "sports/blog.html")
def blogsingleSport(request):
    return render(request, "sports/blog-single.html")
def shopSport(request):
    return render(request, "sports/shop.html")
def productsingleSport(request):
    return render(request, "sports/product-single.html")
def checkoutSport(request):
    return render(request, "sports/checkout.html")
    return render(request, "sports/service.html")