from django.contrib import admin
from .models import Movie, Comment

class CommentAdminInline(admin.StackedInline):
    model = Comment
    can_delete = True

class CommentAdmin(admin.ModelAdmin):
    inlines = (CommentAdminInline,) 

admin.site.register(Movie, CommentAdmin)