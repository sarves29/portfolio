from django.contrib import admin
from .models import Project, Resume

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'featured', 'order', 'created_at')
    list_editable = ('featured', 'order')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')
