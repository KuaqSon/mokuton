from django.contrib import admin

from main_app.models import User


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = (
        "name",
        "email",
        "is_active",
        "created_at",
    )

    fields = (
        "name",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    readonly_fields = ["is_superuser"]


admin.site.register(User, UserAdmin)
