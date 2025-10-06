
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/chartsofaccounts/', include('chartsofaccounts.urls')),
    path('api/transactions/', include('transactions.urls')),
    path('api/business/', include('business.urls')),
    path('api/reports/', include('reports.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)