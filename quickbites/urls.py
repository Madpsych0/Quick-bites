from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin URLs
    path('admin/', admin.site.urls),

    # Authentication URLs
    path('', views.splash_screen, name='splash'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Main app URLs
    path('menu/', views.menu_view, name='menu'),
    path('cart/', views.cart_view, name='cart'),
    path('offers/', views.offers_view, name='offers'),
    path('customer-support/', views.customer_support_view, name='customer_support'),

    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('get-cart-count/', views.get_cart_count, name='get_cart_count'),

    path('payment/', views.payment_view, name='payment'),
    path('process-payment/', views.process_payment, name='process_payment'),
    path('payment-success/<uuid:order_id>/', views.payment_success, name='payment_success'),

    path('profile/', views.profile_view, name='profile'),
    path('ticket/<uuid:order_id>/', views.ticket_view, name='ticket'),

    path('api/redeem-ticket/', views.redeem_ticket, name='redeem_ticket'),
]

# --- Add this conditional statement at the end of the file ---
# This serves media files during development (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)