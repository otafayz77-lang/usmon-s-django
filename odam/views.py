from django.shortcuts import redirect, render
from .models import Category, CustomUser, Product
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request, 'product.html', {'products': products})
def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        CustomUser.objects.create_user(
            # username=email,
            email=email,
            password=password
        )

        return redirect('home')

    return render(request, "register.html")


def detail(request, product_id):
    products = Product.objects.get(id=product_id)
    return render(request, 'detail.html', {'product': products})


def login_user(request):


    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)

            print("User logged in successfully.")

            return redirect('home')
        print("User tizimda yo'q")

        return render(request, 'register.html')
    else:
        return render(request, 'login.html')
    
def logout_user(request):
    logout(request)
    return redirect('login')    



def profil(request):
    return render(request, 'profile.html')

def profile(request):
    products = Product.objects.all()
    return render(request, 'profile.html', {'products': products} )

def add_product(request):
    if request.method == "POST":
        print(request.POST)

        nomi = request.POST.get("nomi")

        if not nomi:
            return render(request, "add_product.html", {
                "error": "Mahsulot nomi kiritilmagan"
            })

        Product.objects.create(
            Nomi=nomi,
            Narxi=request.POST.get("narxi"),
            Malumoti=request.POST.get("malumoti"),
            Rasmi=request.FILES.get("rasmi"),
            Yili=request.POST.get("yili"),
            Holati="Yangi",
            Kategoriya=request.POST.get("kategoriya"),
        )

        return redirect("home")

    categories = Category.objects.all()
    return render(request, "add_product.html", {"categories": categories})

