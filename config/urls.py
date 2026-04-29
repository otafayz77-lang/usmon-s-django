from django.contrib import admin
from django.urls import path
from odam.views import home, register, detail, login_user, logout_user, profil, add_product
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
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)