from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, MenuItem, Cart, CartItem, Order, OrderItem, Feedback, MenuSection

class CustomUserAdmin(UserAdmin):
    """
    Custom admin interface for User model
    """
    list_display = ('uprn', 'name', 'email', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('uprn', 'name', 'email')
    ordering = ('uprn',)
    
    fieldsets = (
        (None, {'fields': ('uprn', 'password')}),
        ('Personal info', {'fields': ('name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('uprn', 'name', 'email', 'password1', 'password2'),
        }),
    )

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    """
    Admin interface for managing menu items
    """
    list_display = ('name', 'category', 'price', 'is_available', 'created_at')
    list_filter = ('category', 'is_available', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('is_available', 'price')
    ordering = ('category', 'name')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'price', 'category')
        }),
        ('Availability', {
            'fields': ('is_available',)
        }),
        ('Image', {
            'fields': ('image',)
        }),
    )

@admin.register(MenuSection)
class MenuSectionAdmin(admin.ModelAdmin):
    """
    Admin interface for controlling menu sections
    """
    list_display = ('name', 'is_active')
    list_editable = ('is_active',)
    ordering = ('name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin interface for managing orders and tickets
    """
    list_display = ('id', 'user', 'total_amount', 'status', 'is_redeemed', 'created_at')
    list_filter = ('status', 'is_redeemed', 'created_at')
    search_fields = ('user__name', 'user__uprn')
    list_editable = ('status',)
    readonly_fields = ('id', 'qr_code', 'created_at', 'redeemed_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Order Information', {
            'fields': ('id', 'user', 'total_amount', 'status', 'created_at')
        }),
        ('Ticket Information', {
            'fields': ('is_redeemed', 'redeemed_at', 'qr_code')
        }),
    )

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """
    Admin interface for viewing customer feedback
    """
    list_display = ('user', 'subject', 'rating', 'is_read', 'created_at')
    list_filter = ('rating', 'is_read', 'created_at')
    search_fields = ('user__name', 'subject', 'message')
    list_editable = ('is_read',)
    readonly_fields = ('user', 'created_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Feedback Information', {
            'fields': ('user', 'subject', 'message', 'rating', 'created_at')
        }),
        ('Admin Actions', {
            'fields': ('is_read',)
        }),
    )

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('menu_item', 'quantity', 'price')
    extra = 0

# Update OrderAdmin to include OrderItems
OrderAdmin.inlines = [OrderItemInline]

# Register the custom user admin
admin.site.register(User, CustomUserAdmin)

# Register other models with basic admin
admin.site.register(Cart)
admin.site.register(CartItem)
