from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('home.urls')),
    path('vendor/', include('Vendor.urls')),
    path('users/', include('Users.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
