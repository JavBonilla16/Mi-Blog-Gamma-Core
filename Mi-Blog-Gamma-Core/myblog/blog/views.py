from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.db.models import Q, Sum
from django.db import models
from django.http import JsonResponse
from django.utils import timezone
from .models import Post, Comment, Profile, Review, Reaction, CommentVote, Notification, Subscription
from .utils import detect_mentions, send_reaction_notification, send_comment_notification
from .forms import CommentForm, CustomUserCreationForm, ProfileForm, PostForm, ReviewForm

def post_list(request):
    """Vista para mostrar la lista de posts publicados con búsqueda"""
    posts = Post.objects.filter(published=True).order_by('-published_date')
    
    # Búsqueda
    search_query = request.GET.get('q')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query) |
            Q(excerpt__icontains=search_query)
        )
    
    # Paginación
    paginator = Paginator(posts, 10)  # 10 posts por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog/post_list.html', {
        'page_obj': page_obj,
        'search_query': search_query
    })

def post_detail(request, slug):
    """Vista para mostrar un post específico con sus comentarios y reseñas"""
    post = get_object_or_404(Post, slug=slug, published=True)
    
    # Obtener comentarios ordenados por mejores comentarios
    comments = post.comments.filter(is_approved=True).annotate(
        score=models.Sum('votes__vote')
    ).order_by('-pinned', '-score', 'created_date')
    
    new_comment = None
    user_review = None
    user_reaction = None
    can_moderate = False

    # Verificar si el usuario puede moderar comentarios
    if request.user.is_authenticated and request.user == post.author:
        can_moderate = True
        # Mostrar todos los comentarios para moderación
        comments = post.comments.all().annotate(
            score=models.Sum('votes__vote')
        ).order_by('-pinned', '-score', 'created_date')

    # Obtener reseña del usuario actual si existe
    if request.user.is_authenticated:
        try:
            user_review = Review.objects.get(post=post, user=request.user)
        except Review.DoesNotExist:
            user_review = None
        
        # Obtener reacción del usuario actual si existe
        try:
            user_reaction = Reaction.objects.get(post=post, user=request.user)
        except Reaction.DoesNotExist:
            user_reaction = None

    if request.method == 'POST':
        # Manejar comentarios
        if 'comment' in request.POST:
            if not request.user.is_authenticated:
                messages.error(request, 'Debes iniciar sesión para comentar.')
                return redirect('blog:login')
            
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.author = request.user
                new_comment.save()
                
                # Detectar menciones y crear notificaciones
                detect_mentions(new_comment.content, post, request.user)
                
                # Enviar notificación al autor del post
                send_comment_notification(post, request.user)
                
                messages.success(request, '¡Tu comentario ha sido añadido y está pendiente de aprobación!')
                return redirect('blog:post_detail', slug=post.slug)
        else:
            comment_form = CommentForm()

        # Manejar reseñas
        if 'review' in request.POST:
            if not request.user.is_authenticated:
                messages.error(request, 'Debes iniciar sesión para calificar.')
                return redirect('blog:login')
            
            review_form = ReviewForm(data=request.POST)
            if review_form.is_valid():
                review, created = Review.objects.get_or_create(
                    post=post, 
                    user=request.user,
                    defaults=review_form.cleaned_data
                )
                if not created:
                    review.rating = review_form.cleaned_data['rating']
                    review.comment = review_form.cleaned_data['comment']
                    review.save()
                    messages.success(request, '¡Tu calificación ha sido actualizada!')
                else:
                    messages.success(request, '¡Gracias por tu calificación!')
                return redirect('blog:post_detail', slug=post.slug)
        else:
            review_form = ReviewForm()
    else:
        comment_form = CommentForm()
        review_form = ReviewForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'approved_comments_count': post.get_approved_comments_count(),
        'new_comment': new_comment,
        'comment_form': comment_form,
        'review_form': review_form,
        'user_review': user_review,
        'user_reaction': user_reaction,
        'can_moderate': can_moderate,
        'reaction_types': Reaction.REACTION_TYPES
    })

# Vistas de autenticación
def signup(request):
    """Vista de registro de usuarios"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'¡Bienvenido {username}! Tu cuenta ha sido creada exitosamente.')
            return redirect('blog:post_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/signup.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'blog/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('blog:post_list')

# Vistas de perfil
@login_required
def profile(request):
    """Vista del perfil del usuario"""
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
    
    return render(request, 'blog/profile.html', {'profile': profile})

@login_required
def profile_edit(request):
    """Vista para editar el perfil"""
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Tu perfil ha sido actualizado!')
            return redirect('blog:profile')
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'blog/profile_edit.html', {'form': form})

# Vistas CRUD para posts
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        if form.instance.published:
            form.instance.published_date = timezone.now()
        messages.success(self.request, '¡Tu post ha sido creado exitosamente!')
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def form_valid(self, form):
        if form.instance.published and not form.instance.published_date:
            form.instance.published_date = timezone.now()
        messages.success(self.request, '¡Tu post ha sido actualizado!')
        return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, '¡El post ha sido eliminado!')
        return super().delete(request, *args, **kwargs)

# Vista para moderar comentarios
@login_required
def moderate_comment(request, comment_id, action):
    """Vista para aprobar/rechazar comentarios"""
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Verificar que el usuario es el autor del post
    if request.user != comment.post.author:
        messages.error(request, 'No tienes permisos para moderar este comentario.')
        return redirect('blog:post_detail', slug=comment.post.slug)
    
    if action == 'approve':
        comment.is_approved = True
        comment.save()
        messages.success(request, 'Comentario aprobado.')
    elif action == 'reject':
        comment.is_approved = False
        comment.save()
        messages.success(request, 'Comentario rechazado.')
    
    return redirect('blog:post_detail', slug=comment.post.slug)

# Vista para posts por etiqueta
def posts_by_tag(request, tag_slug):
    """Vista para mostrar posts filtrados por etiqueta"""
    from taggit.models import Tag
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(published=True, tags=tag).order_by('-published_date')
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog/posts_by_tag.html', {
        'tag': tag,
        'page_obj': page_obj
    })

# Vistas para funcionalidades sociales

@login_required
def add_reaction(request, slug):
    """Vista para agregar/quitar reacciones a posts"""
    if request.method == 'POST':
        post = get_object_or_404(Post, slug=slug, published=True)
        reaction_type = request.POST.get('reaction_type')
        
        if reaction_type in [choice[0] for choice in Reaction.REACTION_TYPES]:
            reaction, created = Reaction.objects.get_or_create(
                post=post,
                user=request.user,
                defaults={'reaction_type': reaction_type}
            )
            
            if not created:
                if reaction.reaction_type == reaction_type:
                    # Si es la misma reacción, la eliminamos (toggle)
                    reaction.delete()
                    action = 'removed'
                else:
                    # Si es diferente, la actualizamos
                    reaction.reaction_type = reaction_type
                    reaction.save()
                    action = 'updated'
            else:
                action = 'added'
                # Enviar notificación solo cuando se agrega una nueva reacción
                send_reaction_notification(post, request.user, reaction_type)
            
            # Obtener contadores actualizados
            reaction_counts = {}
            for choice in Reaction.REACTION_TYPES:
                count = Reaction.objects.filter(post=post, reaction_type=choice[0]).count()
                reaction_counts[choice[0]] = count
            
            return JsonResponse({
                'success': True,
                'action': action,
                'reaction_counts': reaction_counts,
                'user_reaction': reaction_type if action != 'removed' else None
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
def vote_comment(request, comment_id):
    """Vista para votar comentarios"""
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id)
        vote_value = int(request.POST.get('vote', 0))
        
        if vote_value in [-1, 0, 1]:
            vote, created = CommentVote.objects.get_or_create(
                comment=comment,
                user=request.user,
                defaults={'vote': vote_value}
            )
            
            if not created:
                vote.vote = vote_value
                vote.save()
            
            # Obtener score actualizado
            score = comment.get_score()
            
            return JsonResponse({
                'success': True,
                'score': score,
                'user_vote': vote_value
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
def toggle_comment_pin(request, comment_id):
    """Vista para fijar/desfijar comentarios (solo moderadores)"""
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Verificar que el usuario es el autor del post
    if request.user != comment.post.author and not request.user.is_staff:
        messages.error(request, 'No tienes permisos para fijar este comentario.')
        return redirect('blog:post_detail', slug=comment.post.slug)
    
    comment.pinned = not comment.pinned
    comment.save()
    
    action = 'fijado' if comment.pinned else 'desfijado'
    messages.success(request, f'Comentario {action}.')
    
    return redirect('blog:post_detail', slug=comment.post.slug)

@login_required
def notifications(request):
    """Vista para mostrar notificaciones del usuario"""
    notifications_list = request.user.notifications.all()[:20]  # Últimas 20
    unread_count = request.user.notifications.filter(is_read=False).count()
    
    return render(request, 'blog/notifications.html', {
        'notifications': notifications_list,
        'unread_count': unread_count
    })

@login_required
def mark_notification_read(request, notification_id):
    """Vista para marcar notificación como leída"""
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    
    return redirect('blog:notifications')

@login_required
def notification_count(request):
    """Vista para obtener el contador de notificaciones no leídas"""
    count = request.user.notifications.filter(is_read=False).count()
    return JsonResponse({'count': count})

@login_required
def subscriptions(request):
    """Vista para gestionar suscripciones"""
    user_subscriptions = request.user.subscriptions.all()
    
    if request.method == 'POST':
        subscription_type = request.POST.get('subscription_type')
        
        if subscription_type == 'author':
            author_id = request.POST.get('author_id')
            author = get_object_or_404(User, id=author_id)
            subscription, created = Subscription.objects.get_or_create(
                user=request.user,
                subscription_type='author',
                author=author
            )
            if not created:
                subscription.delete()
                messages.success(request, f'Ya no estás suscrito a {author.username}.')
            else:
                messages.success(request, f'Te has suscrito a {author.username}.')
        
        elif subscription_type == 'tag':
            tag_name = request.POST.get('tag_name')
            subscription, created = Subscription.objects.get_or_create(
                user=request.user,
                subscription_type='tag',
                tag=tag_name
            )
            if not created:
                subscription.delete()
                messages.success(request, f'Ya no estás suscrito a la etiqueta {tag_name}.')
            else:
                messages.success(request, f'Te has suscrito a la etiqueta {tag_name}.')
        
        return redirect('blog:subscriptions')
    
    # Obtener autores que han publicado posts
    authors = User.objects.filter(post__published=True).distinct().order_by('first_name', 'last_name')
    
    return render(request, 'blog/subscriptions.html', {
        'subscriptions': user_subscriptions,
        'authors': authors
    })

def rss_feed(request, feed_type=None, feed_id=None):
    """Vista para generar feeds RSS filtrados"""
    from django.http import HttpResponse
    from django.contrib.syndication.views import Feed
    from django.utils.feedgenerator import Rss201rev2Feed
    
    # Obtener posts según el tipo de feed
    if feed_type == 'author' and feed_id:
        posts = Post.objects.filter(published=True, author_id=feed_id).order_by('-published_date')[:20]
        feed_title = f"Posts de {User.objects.get(id=feed_id).username}"
    elif feed_type == 'tag' and feed_id:
        from taggit.models import Tag
        tag = get_object_or_404(Tag, slug=feed_id)
        posts = Post.objects.filter(published=True, tags=tag).order_by('-published_date')[:20]
        feed_title = f"Posts sobre {tag.name}"
    else:
        posts = Post.objects.filter(published=True).order_by('-published_date')[:20]
        feed_title = "Todos los posts"
    
    # Generar RSS
    feed = Rss201rev2Feed(
        title=feed_title,
        link=request.build_absolute_uri('/'),
        description="Feed RSS del blog"
    )
    
    for post in posts:
        feed.add_item(
            title=post.title,
            link=request.build_absolute_uri(post.get_absolute_url()),
            description=post.excerpt or post.content[:200],
            pubdate=post.published_date
        )
    
    response = HttpResponse(feed.writeString('utf-8'), content_type='application/rss+xml')
    response['Content-Disposition'] = 'attachment; filename="feed.xml"'
    return response