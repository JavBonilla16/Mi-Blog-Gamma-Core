from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Posts
    path('', views.post_list, name='post_list'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    
    # Autenticación
    path('signup/', views.signup, name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    # Perfil
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    
    # Moderación
    path('comment/<int:comment_id>/<str:action>/', views.moderate_comment, name='moderate_comment'),
    
    # Etiquetas
    path('tag/<slug:tag_slug>/', views.posts_by_tag, name='posts_by_tag'),
    
    # Funcionalidades sociales
    path('post/<slug:slug>/react/', views.add_reaction, name='add_reaction'),
    path('comment/<int:comment_id>/vote/', views.vote_comment, name='vote_comment'),
    path('comment/<int:comment_id>/pin/', views.toggle_comment_pin, name='toggle_comment_pin'),
    path('notifications/', views.notifications, name='notifications'),
    path('notification/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/count/', views.notification_count, name='notification_count'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('rss/', views.rss_feed, name='rss_feed'),
    path('rss/<str:feed_type>/<str:feed_id>/', views.rss_feed, name='rss_feed_filtered'),
]