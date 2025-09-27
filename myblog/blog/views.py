from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from .models import Post, Comment, Profile, Review
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
    comments = post.comments.filter(is_approved=True)
    new_comment = None
    user_review = None
    can_moderate = False

    # Verificar si el usuario puede moderar comentarios
    if request.user.is_authenticated and request.user == post.author:
        can_moderate = True
        # Mostrar todos los comentarios para moderación
        comments = post.comments.all()

    # Obtener reseña del usuario actual si existe
    if request.user.is_authenticated:
        try:
            user_review = Review.objects.get(post=post, user=request.user)
        except Review.DoesNotExist:
            user_review = None

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
        'can_moderate': can_moderate
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