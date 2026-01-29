from django.contrib import admin
from django.urls import path
from scanner import views as scanner_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('scan-ticket/', scanner_views.scan_ticket, name='scan_ticket'),
    path('', scanner_views.scanner_view, name='home'),
]