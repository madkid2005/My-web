from django.contrib import admin
from .models import Category, Product
from django.contrib.staticfiles.storage import staticfiles_storage
from django.utils.html import format_html

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller', 'category', 'price', 'sku', 'color', 'created_at', 'updated_at')
    list_filter = ('category', 'color', 'seller')
    search_fields = ('name', 'description', 'seller__user__username')
    ordering = ('-created_at',)
    fields = ('name', 'description', 'price', 'sku', 'color', 'category', 'seller', 'image')
    readonly_fields = ('created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        if not change:
            # Additional logic when creating a new object
            pass
        super().save_model(request, obj, form, change)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')



class CustomAdminSite(admin.AdminSite):
    def each_context(self, request):
        context = super().each_context(request)
        context['custom_css'] = staticfiles_storage.url('css/custom_admin.css')
        return context

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['custom_css'] = self.each_context(request).get('custom_css', '')
        return super().index(request, extra_context)

admin_site = CustomAdminSite(name='custom_admin')



admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)

