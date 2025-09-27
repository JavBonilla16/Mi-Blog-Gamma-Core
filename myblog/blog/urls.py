from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Posts
    path('', views.post_list, name='post_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
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
]