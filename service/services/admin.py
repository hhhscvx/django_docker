from django.contrib import admin

from services.models import Service, Plan, Subscription

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price_to_subscribe']
    list_filter = ['name']
    search_fields = ['name']

admin.site.register(Plan)
admin.site.register(Subscription)


