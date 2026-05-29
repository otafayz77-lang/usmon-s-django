from django.shortcuts import redirect, render, get_object_or_404
from .models import Basket, Category, CustomUser, Product, Transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404

def home(request):
    products = Product.objects.all()
    return render(request, 'product.html', {'products': products})

def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not email or not password or not confirm_password:
            return render(request, "register.html", {"error": "Barcha maydonlarni to'ldiring"})
        
        if password != confirm_password:
            return render(request, "register.html", {"error": "Parollar mos emas"})

        if CustomUser.objects.filter(email=email).exists():
            return render(request, "register.html", {"error": "Bu email allaqachon ro'yxatdan o'tgan"})

        try:
            CustomUser.objects.create_user(
                email=email,
                password=password
            )
            return redirect('login')
        except Exception as e:
            return render(request, "register.html", {"error": f"Xatolik yuz berdi: {str(e)}"})

    return render(request, "register.html")


def detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'detail.html', {'product': product})


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        
        return render(request, 'login.html', {'error': 'Email yoki parol xato'})
    
    return render(request, 'login.html')
    
def logout_user(request):
    logout(request)
    return redirect('login')    


def profil(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    user_products = Product.objects.filter(user=request.user)
    user_orders = Transaction.objects.filter(user=request.user)
    
    return render(request, 'profile.html', {
        'user_products': user_products,
        'user_orders': user_orders
    })

@login_required(login_url='login')
def add_product(request):
    if request.method == "POST":
        nomi = request.POST.get("nomi")

        if not nomi:
            categories = Category.objects.all()
            return render(request, "add_product.html", {
                "error": "Mahsulot nomi kiritilmagan",
                "categories": categories
            })

        Product.objects.create(
            Nomi=nomi,
            Narxi=request.POST.get("narxi"),
            Malumoti=request.POST.get("malumoti"),
            Rasmi=request.FILES.get("rasmi"),
            Yili=request.POST.get("yili"),
            Holati="Yangi",
            Kategoriya_id=int(request.POST.get("kategoriya")),
            user=request.user
        )

        return redirect("profil")

    categories = Category.objects.all()
    return render(request, "add_product.html", {"categories": categories})


@login_required(login_url='login')
def add_basket(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise Http404("Mahsulot topilmadi")
    
    basket_item, created = Basket.objects.get_or_create(
        product=product,
        user=request.user,
        defaults={'count': 1}
    )
    
    if not created:
        basket_item.count += 1
        basket_item.save()
    
    return redirect('basket')


@login_required(login_url='login')
def basket(request):
    basket_items = Basket.objects.filter(user=request.user)
    total = sum(item.total_price for item in basket_items)
    
    return render(request, 'basket.html', {
        'basket_items': basket_items,
        'total': total
    })


@login_required(login_url='login')
def remove_from_basket(request, basket_id):
    try:
        basket_item = Basket.objects.get(id=basket_id, user=request.user)
        basket_item.delete()
    except Basket.DoesNotExist:
        pass
    
    return redirect('basket')


@login_required(login_url='login')
def update_basket(request, basket_id):
    if request.method == "POST":
        count = request.POST.get("count", 1)
        try:
            count = int(count)
            if count < 1:
                count = 1
            
            basket_item = Basket.objects.get(id=basket_id, user=request.user)
            basket_item.count = count
            basket_item.save()
        except (Basket.DoesNotExist, ValueError):
            pass
    
    return redirect('basket')


@login_required(login_url='login')
def buy_now(request):
    if request.method == "POST":
        location = request.POST.get("location")
        payment = request.POST.get("payment")
        
        if not location or not payment:
            return render(request, 'buy_now.html', {
                'error': 'Barcha maydonlarni to\'ldiring'
            })
        
        basket_items = Basket.objects.filter(user=request.user)
        
        if not basket_items.exists():
            return redirect('basket')
        
        for item in basket_items:
            Transaction.objects.create(
                product=item.product,
                user=request.user,
                location=location,
                payment=payment
            )
        
        basket_items.delete()
        
        return render(request, 'order_success.html', {
            'message': 'Buyurtma muvaffaqiyatli yaratildi!'
        })
    
    return render(request, 'buy_now.html')