from django.shortcuts import render
from .models import *
from django.http import HttpResponse
# Create your views here.
def indexSport(request):
    DTProduct= Product.objects.all()
    context={
        'ObjDTProduct':DTProduct
    }
    return render(request, "sports/index.html",context)
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
    DTProduct= Product.objects.all()
    context={
        'ObjDTProduct':DTProduct
    }
    return render(request, "sports/shop.html",context)
def productsingleSport(request, pk):
    DTProductDetail = Product.objects.get(id=pk)
    DTProductDetailInfo = ProductDetail.objects.get(productID=pk)

    context = {
        'ObjProductDetail': DTProductDetail,
        'ObjDTProductDetailInfo': DTProductDetailInfo,
    }

    return render(request, "sports/product-single.html", context)
def checkoutSport(request):
    return render(request, "sports/checkout.html")