from django.contrib import admin
from django.urls import path
from odam import views
from odam.views import add_basket, basket, home, register, detail, login_user, logout_user, profil, add_product, remove_from_basket, update_basket, buy_now
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('detail/<int:product_id>/', detail, name='detail'),
    path('logout/', logout_user, name='logout'),
    path('profil/', profil, name='profil'),
    path('add_product/', add_product, name='add_product'),
    path('basket/', basket, name='basket'),
    path('add-to-cart/<int:product_id>/', add_basket, name='add_basket'),
    path('remove-from-basket/<int:basket_id>/', remove_from_basket, name='remove_basket'),
    path('update-basket/<int:basket_id>/', update_basket, name='update_basket'),
    path('buy-now/', buy_now, name='buy_now'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)