from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('login'), name='home'),
    path('admin/', admin.site.urls),
    path('school_app/',include('school_app.urls')),
    # path('api-auth/', include('rest_framework.urls')),  # DRF's login/logout views

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)