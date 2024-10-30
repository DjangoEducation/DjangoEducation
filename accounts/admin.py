from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Course
from .models import UserLoginAttempt
from .models import CoursParticiperParUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'diplomes', 'experience', 'specialite', 'about', 'avatar')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'specialites', 'niveau']
    list_filter = ['specialites', 'niveau']
    search_fields = ['title', 'specialites', 'niveau']
    list_per_page = 10
    list_editable = ['specialites', 'niveau']
    image = ['image']
    pdf = ['pdf']

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'image', 'pdf')
        }),
        ('Spécialités', {
            'fields': ('specialites', 'niveau')
        }),
    )

    ordering = ['title']

    @admin.action(description="Mark selected courses as published")
    def make_published(self, request, queryset):
        updated = queryset.update(published=True)
        self.message_user(request, f"{updated} course(s) successfully marked as published.")

    actions = ['make_published']

@admin.register(UserLoginAttempt)
class UserLoginAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'timestamp', 'ip_address', 'successful']
    list_filter = ['successful']
    search_fields = ['user__username', 'ip_address']
    ordering = ['-timestamp']

@admin.register(CoursParticiperParUser)
class CoursParticiperParUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'date_participation']
    list_filter = ['date_participation']
    search_fields = ['user_username', 'course_title']