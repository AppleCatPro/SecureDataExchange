from django.contrib import admin
from .models import CustomUser, ConfidentialData, Message, AuditLog

admin.site.register(CustomUser)
admin.site.register(ConfidentialData)
admin.site.register(Message)
admin.site.register(AuditLog)
