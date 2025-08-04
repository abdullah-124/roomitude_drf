from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from roomitude_backend.views import my_function

urlpatterns = [
    path('admin/', admin.site.urls),
    path('my_function/', my_function),
    path('', include('site_admin.urls')),
    path('api/account/', include('account.urls')),
    path('api/categories/', include('category.urls')),
    path('api/products/', include('products.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)