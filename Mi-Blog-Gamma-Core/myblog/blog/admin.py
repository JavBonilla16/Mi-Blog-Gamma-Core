from django.contrib import admin
from .models import Post, Comment, Profile, Review, Reaction, CommentVote, Notification, Subscription

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
    list_display = ('author', 'post', 'created_date', 'is_approved', 'pinned', 'get_score')
    list_filter = ('is_approved', 'pinned', 'created_date')
    search_fields = ('author__username', 'content')
    actions = ['approve_comments', 'pin_comments', 'unpin_comments']
    list_editable = ('is_approved', 'pinned')

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f'{queryset.count()} comentarios aprobados.')
    approve_comments.short_description = 'Aprobar comentarios seleccionados'
    
    def pin_comments(self, request, queryset):
        queryset.update(pinned=True)
        self.message_user(request, f'{queryset.count()} comentarios fijados.')
    pin_comments.short_description = 'Fijar comentarios seleccionados'
    
    def unpin_comments(self, request, queryset):
        queryset.update(pinned=False)
        self.message_user(request, f'{queryset.count()} comentarios desfijados.')
    unpin_comments.short_description = 'Desfijar comentarios seleccionados'

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

@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'reaction_type', 'created_date')
    list_filter = ('reaction_type', 'created_date')
    search_fields = ('user__username', 'post__title')

@admin.register(CommentVote)
class CommentVoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'vote', 'created_date')
    list_filter = ('vote', 'created_date')
    search_fields = ('user__username', 'comment__content')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'title', 'is_read', 'created_date')
    list_filter = ('notification_type', 'is_read', 'created_date')
    search_fields = ('user__username', 'title', 'message')
    actions = ['mark_as_read']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f'{queryset.count()} notificaciones marcadas como leídas.')
    mark_as_read.short_description = 'Marcar como leídas'

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription_type', 'author', 'tag', 'created_date')
    list_filter = ('subscription_type', 'created_date')
    search_fields = ('user__username', 'author__username', 'tag')