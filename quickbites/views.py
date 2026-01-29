from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
import qrcode
import io
import base64
from .models import User, MenuItem, Cart, CartItem, Order, OrderItem, Feedback, MenuSection
from .forms import UserRegistrationForm, UserLoginForm, FeedbackForm

def splash_screen(request):
    """
    Display splash screen with QuickBites branding
    """
    return render(request, 'quickbites/splash.html')

def register_view(request):
    """
    User registration view
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.name}! Your account has been created.')
            return redirect('menu')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'quickbites/register.html', {'form': form})

def login_view(request):
    """
    User login view
    """
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            uprn = form.cleaned_data['uprn']
            password = form.cleaned_data['password']
            user = User.objects.get(uprn=uprn)
            login(request, user)
            messages.success(request, f'Welcome back, {user.name}!')
            return redirect('menu')
        else:
            messages.error(request, 'Invalid credentials.')
    else:
        form = UserLoginForm()
    
    return render(request, 'quickbites/login.html', {'form': form})

@login_required
def logout_view(request):
    """
    User logout view
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('splash')

@login_required
def menu_view(request):
    """
    Menu page showing all available food items
    """
    # Get active menu sections
    active_sections = MenuSection.objects.filter(is_active=True).values_list('name', flat=True)
    
    # Get menu items for active sections
    menu_items = MenuItem.objects.filter(
        is_available=True,
        category__in=active_sections
    ).order_by('category', 'name')
    
    # Group items by category
    menu_by_category = {}
    for item in menu_items:
        if item.category not in menu_by_category:
            menu_by_category[item.category] = []
        menu_by_category[item.category].append(item)
    
    return render(request, 'quickbites/menu.html', {
        'menu_by_category': menu_by_category,
        'user_name': request.user.name
    })

@login_required
def add_to_cart(request, item_id):
    """
    Add item to user's cart
    """
    if request.method == 'POST':
        menu_item = get_object_or_404(MenuItem, id=item_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            menu_item=menu_item,
            defaults={'quantity': 1}
        )
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        
        return JsonResponse({
            'success': True,
            'message': f'{menu_item.name} added to cart',
            'cart_count': cart.cartitem_set.count()
        })
    
    return JsonResponse({'success': False})

@login_required
def cart_view(request):
    """
    Display user's cart
    """
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.cartitem_set.all()
        total = cart.get_total()
    except Cart.DoesNotExist:
        cart_items = []
        total = 0
    
    return render(request, 'quickbites/cart.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required
def offers_view(request):
    """
    Display current offers
    """
    offers = MenuItem.objects.filter(category='offer', is_available=True)
    return render(request, 'quickbites/offers.html', {'offers': offers})

@login_required
def customer_support_view(request):
    """
    Handle customer support requests (renamed from feedback)
    """
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
            return redirect('customer_support')
    else:
        form = FeedbackForm()
    
    return render(request, 'quickbites/customer_support.html', {'form': form})

@login_required
def update_cart_item(request, item_id):
    """
    Update quantity of item in cart
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        quantity = int(data.get('quantity', 1))
        
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(cart=cart, id=item_id)
            
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
            else:
                cart_item.delete()
            
            return JsonResponse({
                'success': True,
                'cart_total': cart.get_total(),
                'item_subtotal': cart_item.get_subtotal() if quantity > 0 else 0
            })
        except (Cart.DoesNotExist, CartItem.DoesNotExist):
            return JsonResponse({'success': False})
    
    return JsonResponse({'success': False})

@login_required
def remove_from_cart(request, item_id):
    """
    Remove item from cart
    """
    if request.method == 'POST':
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(cart=cart, id=item_id)
            cart_item.delete()
            
            return JsonResponse({
                'success': True,
                'cart_total': cart.get_total(),
                'message': 'Item removed from cart'
            })
        except (Cart.DoesNotExist, CartItem.DoesNotExist):
            return JsonResponse({'success': False})
    
    return JsonResponse({'success': False})

@login_required
def payment_view(request):
    """
    Mockup payment gateway
    """
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.cartitem_set.all()
        total = cart.get_total()
        
        if not cart_items:
            messages.error(request, 'Your cart is empty!')
            return redirect('cart')
            
    except Cart.DoesNotExist:
        messages.error(request, 'Your cart is empty!')
        return redirect('cart')
    
    return render(request, 'quickbites/payment.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required
def process_payment(request):
    """
    Process payment and create order
    """
    if request.method == 'POST':
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.cartitem_set.all()
            
            if not cart_items:
                messages.error(request, 'Your cart is empty!')
                return redirect('cart')
            
            # Create order
            order = Order.objects.create(
                user=request.user,
                total_amount=cart.get_total(),
                status='confirmed'
            )
            
            # Create order items
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    menu_item=cart_item.menu_item,
                    quantity=cart_item.quantity,
                    price=cart_item.menu_item.price
                )
            
            # Generate QR code for the order
            qr_data = f"ORDER:{order.id}:{request.user.uprn}"
            order.qr_code = generate_qr_code(qr_data)
            order.save()
            
            # Clear cart
            cart.delete()
            
            return redirect('payment_success', order_id=order.id)
            
        except Cart.DoesNotExist:
            messages.error(request, 'Your cart is empty!')
            return redirect('cart')
    
    return redirect('cart')

@login_required
def payment_success(request, order_id):
    """
    Payment confirmation page
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'quickbites/payment_success.html', {'order': order})

@login_required
def profile_view(request):
    """
    User profile with order history and tickets
    """
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'quickbites/profile.html', {'orders': orders})

@login_required
def ticket_view(request, order_id):
    """
    Display digital ticket with QR code
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.orderitem_set.all()
    
    return render(request, 'quickbites/ticket.html', {
        'order': order,
        'order_items': order_items
    })

@csrf_exempt
def redeem_ticket(request):
    """
    API endpoint for redeeming tickets via QR scan
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            qr_data = data.get('qr_data', '')
            
            # Parse QR data: "ORDER:order_id:uprn"
            if qr_data.startswith('ORDER:'):
                parts = qr_data.split(':')
                if len(parts) == 3:
                    order_id = parts[1]
                    uprn = parts[2]
                    
                    order = Order.objects.get(id=order_id, user__uprn=uprn)
                    
                    if order.is_redeemed:
                        return JsonResponse({
                            'success': False,
                            'message': 'Ticket already redeemed'
                        })
                    
                    # Mark as redeemed
                    order.is_redeemed = True
                    order.redeemed_at = timezone.now()
                    order.status = 'completed'
                    order.save()
                    
                    return JsonResponse({
                        'success': True,
                        'message': f'Order {order_id} redeemed successfully',
                        'customer_name': order.user.name,
                        'total_amount': str(order.total_amount)
                    })
            
            return JsonResponse({
                'success': False,
                'message': 'Invalid QR code'
            })
            
        except Order.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Order not found'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Error processing request'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required
def get_cart_count(request):
    """
    Get current cart item count
    """
    try:
        cart = Cart.objects.get(user=request.user)
        count = cart.cartitem_set.count()
    except Cart.DoesNotExist:
        count = 0
    
    return JsonResponse({'count': count})

def generate_qr_code(data):
    """
    Generate QR code for order
    """
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    return base64.b64encode(buffer.getvalue()).decode()
