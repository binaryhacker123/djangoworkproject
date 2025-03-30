from django.contrib import admin
from .models import Feature, Service, TimeSlot, ContactMessage

# Register your models here.
admin.site.register(Feature)

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'email', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)



class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'is_available')
    list_filter = ('date', 'is_available')

# Register your models
admin.site.register(Service)
admin.site.register(TimeSlot, TimeSlotAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)