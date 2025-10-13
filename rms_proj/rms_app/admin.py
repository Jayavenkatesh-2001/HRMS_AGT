from django.conf import settings
from django.contrib import admin
from django.core.mail import send_mail
from .models import Request


def send_status_email(obj):
    """Reusable function to send email when status changes."""
    subject = f"Your request has been {obj.status}"
    message = (
        f"Hello {obj.user.username},\n\n"
        f"Your request '{obj.requirement}' has been {obj.status}."
    )
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [obj.email],
        fail_silently=False,
    )


# Custom actions
@admin.action(description="Approve selected requests")
def approve_requests(modeladmin, request, queryset):
    for obj in queryset:
        if obj.status != "Approved":
            obj.status = "Approved"
            obj.save()
            send_status_email(obj)  # ✅ Send email here


@admin.action(description="Reject selected requests")
def reject_requests(modeladmin, request, queryset):
    for obj in queryset:
        if obj.status != "Rejected":
            obj.status = "Rejected"
            obj.save()
            send_status_email(obj)  # ✅ Send email here


class RequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'requirement', 'date', 'phone', 'email', 'status')
    list_filter = ('status', 'date')
    search_fields = ('user__username', 'requirement', 'email', 'phone')
    ordering = ('-date',)

    actions = [approve_requests, reject_requests]
    list_editable = ('status',)

    # ✅ Only send mail if status manually changed in admin detail form
    def save_model(self, request, obj, form, change):
        if change:
            old_obj = Request.objects.get(pk=obj.pk)
            if old_obj.status != obj.status:
                send_status_email(obj)
        super().save_model(request, obj, form, change)


# Register
admin.site.register(Request, RequestAdmin)