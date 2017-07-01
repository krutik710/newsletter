from django.contrib import admin
from mailmonikapp.models import Newsletter,Subscription
# Register your models here.

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email','is_active')
    list_filter = ('is_active',)
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('is_active',)
        return self.readonly_fields

class NewsletterAdmin(admin.ModelAdmin):
    search_fields = ('subject','body')


admin.site.register(Newsletter,NewsletterAdmin)
admin.site.register(Subscription,SubscriptionAdmin)

