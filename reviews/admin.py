from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['reviewer', 'freelancer', 'project', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['comment', 'reviewer__username', 'freelancer__username']
