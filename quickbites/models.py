from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db import models
from django.utils import timezone
import uuid


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, uprn, name, email=None, password=None, **extra_fields):
        """
        Create and save a regular User with UPRN as the login field
        """
        if not uprn:
            raise ValueError("The UPRN must be set")
        email = self.normalize_email(email)
        user = self.model(uprn=uprn, name=name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, uprn, name, email=None, password=None, **extra_fields):
        """
        Create and save a SuperUser with UPRN as the login field
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(uprn, name, email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser
    Uses UPRN as the username field
    """
    uprn = models.CharField(
        max_length=20, unique=True, help_text="University Personal Registration Number"
    )
    name = models.CharField(max_length=100, help_text="Full name of the user")

    USERNAME_FIELD = "uprn"
    REQUIRED_FIELDS = ["name", "email"]

    objects = UserManager()

    def __str__(self):
        return f"{self.name} ({self.uprn})"


class MenuItem(models.Model):
    """
    Model for food items in the menu
    """
    CATEGORY_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('beverage', 'Beverage'),
        ('special', 'Today\'s Special'),
        ('offer', 'Offers'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - ₹{self.price}"

class Cart(models.Model):
    """
    Shopping cart for users
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_total(self):
        return sum(item.get_subtotal() for item in self.cartitem_set.all())

class CartItem(models.Model):
    """
    Individual items in the cart
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def get_subtotal(self):
        return self.menu_item.price * self.quantity

class Order(models.Model):
    """
    Order model for completed purchases
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    qr_code = models.TextField(blank=True)  # Store QR code data
    is_redeemed = models.BooleanField(default=False)
    redeemed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Order {self.id} - {self.user.name}"

class OrderItem(models.Model):
    """
    Individual items in an order
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)  # Store price at time of order
    
    def get_subtotal(self):
        return self.price * self.quantity

class Feedback(models.Model):
    """
    Customer feedback model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Feedback from {self.user.name} - {self.subject}"

class MenuSection(models.Model):
    """
    Model to control which menu sections are active
    """
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - {'Active' if self.is_active else 'Inactive'}"
