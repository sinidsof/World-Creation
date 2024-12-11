
from django import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('world_creation.core.urls')),  # Началната страница
    path('tasks/', include('world_creation.tasks.urls')),  # URL за задачите
    path('accounts/', include('world_creation.accounts.urls')),  # URL за акаунтите
    path('dashboards/', include('world_creation.dashboards.urls')),  # URL за обратни връзки
    # path('sharing/', include('sharing.urls')),  # URL за споделяне

 ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Други URL пътища