from django.contrib import admin
from .models import Store

# Register your models here.
class StoreAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'country', 'currency', 'seller', 'is_verified')
    fieldsets = (
        (None, {
            'fields': ('seller','store_name', 'country', 'currency', 'is_verified','description'),
        }),
        ('Image Details', {
            'classes': ('collapse',),
            'fields': ('logo', 'banner_image'),
        }),
        ('Contact Details', {
            'classes': ('collapse',),
            'fields': ('contact_no', 'email', 'website_link', 'facebook_link', 'instagram_link'),   
        }),
        ('Additional Details', {
            'classes': ('collapse',),
            'fields': ('terms_and_conditions', 'return_policy'),
        })

    )

admin.site.register(Store, StoreAdmin)
