from django.contrib import admin


from webhook.models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "content", "timestamp", "status", "mobile_no")
    search_fields = ("sender", "receiver", "mobile_no")
    list_filter = ("status", "timestamp")
