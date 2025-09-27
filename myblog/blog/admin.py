from django.contrib import admin
from .models import Post, Comment, Profile, Review

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'created_date', 'published')
    list_filter = ('created_date', 'published_date', 'author', 'published')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_date'
    ordering = ('created_date',)
    list_editable = ('published',)
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'content')
        }),
        ('Opciones de publicación', {
            'fields': ('published', 'published_date'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_date', 'is_approved')
    list_filter = ('is_approved', 'created_date')
    search_fields = ('author__username', 'content')
    actions = ['approve_comments']
    list_editable = ('is_approved',)

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f'{queryset.count()} comentarios aprobados.')
    approve_comments.short_description = 'Aprobar comentarios seleccionados'

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_date')
    search_fields = ('user__username', 'user__email')
    list_filter = ('created_date',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'rating', 'created_date')
    list_filter = ('rating', 'created_date')
    search_fields = ('user__username', 'post__title', 'comment')