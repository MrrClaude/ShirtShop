from django.shortcuts import render ,redirect
from .forms import ItemForm ,ProductForm
from .models import *
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Min, Max
from .models import *
from django.http import HttpResponse ,JsonResponse
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
    # Get the product (must exist)
    product = get_object_or_404(Product, id=pk)

    # Try to get product detail, but allow missing
    product_detail = ProductDetail.objects.filter(productID=pk).first()

    # Get sizes
    sizes = product.sizes.all() 

    context = {
        'ObjProductDetail': product,
        'ObjDTProductDetailInfo': product_detail,  # could be None
        'sizes': sizes, 
    }

    return render(request, "sports/product-single.html", context)
def checkoutSport(request):
    return render(request, "sports/checkout.html")

def create_book(request):
    if request.method == "POST":
        title = request.POST['title']
        author = request.POST['author']
        published_date = request.POST['published_date']
        Book.objects.create(title=title, author=author, published_date=published_date)
        return redirect('book_list')
    return render(request, 'sports/create_book.html')

def book_list(request):
    books = Book.objects.all()
    return render(request, 'sports/book_list.html', {'books': books})

def update_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        book.title = request.POST['title']
        book.author = request.POST['author']
        book.published_date = request.POST['published_date']
        book.save()
        return redirect('book_list')
    return render(request, 'sports/update_book.html', {'book': book})

def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        book.delete()
        return redirect('book_list')
    return render(request, 'sports/delete_book.html', {'book': book})

def create_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_list')  # Redirect to the list view
    else:
        form = ItemForm()
    return render(request, 'sports/create_item.html', {'form': form})

def item_list(request):
    items = Item.objects.all()
    return render(request, 'sports/item_list.html', {'items': items})

def create_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            # return redirect('item_list')  # Redirect to the list view
    else:
        form = ItemForm()
    return render(request, 'sports/create_item.html', {'ProductForm': form})


def update_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_list')  # Redirect to the list view
    else:
        form = ItemForm(instance=item)
    return render(request, 'sports/update_item.html', {'form': form, 'item': item})

def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')  # Redirect to the list view after deletion
    return render(request, 'sports/delete_item.html', {'item': item})


def add_to_cart(request, product_id):
    # Get the selected size from query string
    selected_size_id = request.GET.get('size')  

    product = Product.objects.get(id=product_id)
    quantity = int(request.GET.get("qty", 1))  # Use the quantity from the page
    size_name = ''

    if selected_size_id:
        try:
            size = product.sizes.get(id=selected_size_id)
            size_name = size.name
        except Size.DoesNotExist:
            size_name = ''
    else:
        # Default to SMALL if it exists
        small_size = product.sizes.filter(name__iexact='SMALL').first()
        if small_size:
            selected_size_id = small_size.id
            size_name = small_size.name
        else:
            # Fallback if no size available
            selected_size_id = None
            size_name = ''

    # Unique key for cart to handle same product with different sizes
    key = f"{product_id}_{selected_size_id}" if selected_size_id else str(product_id)

    cart = request.session.get('cart', {})

    if key in cart:
        # Add the selected quantity instead of always +1
        cart[key]['quantity'] += quantity
        cart[key]['total'] = cart[key]['quantity'] * cart[key]['price']
    else:
        cart[key] = {
            'productName': product.productName,
            'size': size_name,
            'price': float(product.price),
            'quantity': quantity,  # Use selected quantity
            'total': float(product.price) * quantity,  # Correct total
            'image': product.productImage.url if product.productImage else ''
        }

    request.session['cart'] = cart
    return redirect('view_cart')




def view_cart(request):
    cart = request.session.get('cart', {})
    
    # recompute totals
    for item in cart.values():
        item['total'] = item['price'] * item['quantity']

    total_price = sum(item['total'] for item in cart.values())

    request.session['cart'] = cart

    return render(request, 'sports/cart.html', {
        'cart': cart,
        'total_price': total_price
    })


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('view_cart')

def checkout_view(request):
    cart = request.session.get('cart', {})
    total_price = sum(item['total'] for item in cart.values())

    return render(request, 'sports/checkout.html', {
        'cart': cart,
        'total_price': total_price,
    })

def update_cart_quantity(request):
    product_id = request.POST.get('product_id')
    new_quantity = int(request.POST.get('quantity', 1))

    cart = request.session.get('cart', {})

    if product_id in cart:
        cart[product_id]['quantity'] = new_quantity
        cart[product_id]['total'] = new_quantity * cart[product_id]['price']

    request.session['cart'] = cart

    # Calculate new subtotal
    total_price = sum(item['total'] for item in cart.values())

    return JsonResponse({
        'status': 'success',
        'new_total': cart[product_id]['total'],
        'cart_total': total_price
    })

def billing_add(request):
    cart = request.session.get('cart', {})
    total_price = sum(item['total'] for item in cart.values())

    if request.method == "POST":
        data = request.POST
        qr_image = request.FILES.get('qr_code_image')

        billing = BillingDetail(
            first_name=data['first_name'],
            last_name=data['last_name'],
            country=data['country'],
            address=data['address'],
            town=data['town'],
            postcode=data['postcode'],
            phone=data['phone'],
            email=data['email'],
            qr_code_image=qr_image,
            total=data['total']
        )
        billing.save()
        return redirect('billing_list')
    
    return render(request, 'sports/checkout.html', {
        'cart': cart,
        'total_price': total_price,
    })

def billing_list(request):
    billings = BillingDetail.objects.all()
    return render(request, 'sports/BillingList.html', {'billings': billings})








