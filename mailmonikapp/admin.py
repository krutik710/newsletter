from django.contrib import admin
from mailmonikapp.models import Subscription, Newsletter,SubscriptionComplete_Email,Welcome_Email
# Register your models here.

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email','is_active')
    list_filter = ('is_active',)
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('is_active',)
        return self.readonly_fields

class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('subject','sent_at')
    search_fields = ('subject','body')


admin.site.register(Newsletter,NewsletterAdmin)
admin.site.register(Subscription,SubscriptionAdmin)
admin.site.register(Welcome_Email)
admin.site.register(SubscriptionComplete_Email)

