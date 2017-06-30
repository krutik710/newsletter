from django.contrib import admin
from mailmonikapp.models import Newsletter,Subscription
# Register your models here.

class SubscriptionAdmin(admin.ModelAdmin):
    
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('is_active',)
        return self.readonly_fields


admin.site.register(Newsletter)
admin.site.register(Subscription,SubscriptionAdmin)
