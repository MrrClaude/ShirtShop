from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Min, Max
from .models import *
from django.http import HttpResponse
# Create your views here.
def indexSport(request):
    DTProduct= Product.objects.all()
    sliders = HomeSlider.objects.all()
    deal = DealOfTheMonth.objects.last()
    context={
        "sliders": sliders,
        'ObjDTProduct':DTProduct,
        "deal": deal,
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
from django.shortcuts import render
from .models import Product, Category

def shopSport(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    # Get filter parameters
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    category_id = request.GET.get('category')
    sort = request.GET.get('sort')

    # ==========================
    # Filter by category
    # ==========================
    if category_id:
        products = products.filter(categoryID__id=category_id)

    # ==========================
    # Filter by price
    # ==========================
    if price_from:
        products = products.filter(price__gte=price_from)
    if price_to:
        products = products.filter(price__lte=price_to)

    # ==========================
    # Sorting
    # ==========================
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')

    # ================================
    # Pagination (must be OUTSIDE sort)
    # ================================
    paginator = Paginator(products, 6)  # Show 6 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # ================================
    # Get price range for filter UI
    # ================================
    min_price = Product.objects.order_by('price').first().price if Product.objects.exists() else 0
    max_price = Product.objects.order_by('-price').first().price if Product.objects.exists() else 1000

    context = {
        'categories': categories,
        'page_obj': page_obj,          # use this to loop products
        'price_from': price_from,
        'price_to': price_to,
        'sort': sort,
        'category_id': category_id,
        'min_price': min_price,
        'max_price': max_price,
    }

    return render(request, "sports/shop.html", context)



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

