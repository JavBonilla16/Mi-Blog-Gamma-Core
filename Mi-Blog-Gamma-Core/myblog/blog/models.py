from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
import math
from django.utils.html import strip_tags

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Título')
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Autor')
    content = RichTextField(verbose_name='Contenido')
    excerpt = models.TextField(max_length=300, blank=True, verbose_name='Resumen')
    cover_image = models.ImageField(upload_to='posts/', blank=True, null=True, verbose_name='Imagen de portada')
    tags = TaggableManager(verbose_name='Etiquetas')
    created_date = models.DateTimeField(default=timezone.now, verbose_name='Fecha de creación')
    published_date = models.DateTimeField(blank=True, null=True, verbose_name='Fecha de publicación')
    published = models.BooleanField(default=False, verbose_name='Publicado')

    class Meta:
        ordering = ['-created_date']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    @property
    def reading_time(self):
        text = strip_tags(self.content or "")
        word_count = len(text.split())
        minutes = math.ceil(word_count / 200) if word_count > 0 else 1
        return max(1, int(minutes))

    def publish(self):
        self.published_date = timezone.now()
        self.published = True
        self.save()

    def get_average_rating(self):
        """Calcula el promedio de calificaciones del post"""
        reviews = self.reviews.all()
        if reviews:
            return round(sum(review.rating for review in reviews) / len(reviews), 1)
        return 0

    def get_rating_count(self):
        """Obtiene el número total de calificaciones"""
        return self.reviews.count()

    def get_approved_comments_count(self):
        """Obtiene el número de comentarios aprobados"""
        return self.comments.filter(is_approved=True).count()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Autor', null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name='Nombre', blank=True)
    email = models.EmailField(verbose_name='Email', blank=True)
    content = models.TextField(verbose_name='Comentario')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')
    is_approved = models.BooleanField(default=False, verbose_name='Aprobado')
    pinned = models.BooleanField(default=False, verbose_name='Fijado')

    class Meta:
        ordering = ['created_date']
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'

    def __str__(self):
        if self.author:
            return f'Comentario de {self.author.username} en {self.post.title}'
        else:
            return f'Comentario de {self.name} en {self.post.title}'
    
    def get_score(self):
        """Calcula el score del comentario basado en votos"""
        return sum(vote.vote for vote in self.votes.all())
    
    def get_user_vote(self, user):
        """Obtiene el voto del usuario para este comentario"""
        try:
            vote = self.votes.get(user=user)
            return vote.vote
        except CommentVote.DoesNotExist:
            return 0

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuario')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Avatar')
    bio = models.TextField(max_length=500, blank=True, verbose_name='Biografía')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

    def __str__(self):
        return f'Perfil de {self.user.username}'

class Review(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reviews', verbose_name='Post')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Calificación'
    )
    comment = models.TextField(blank=True, verbose_name='Comentario')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')

    class Meta:
        unique_together = ['post', 'user']
        verbose_name = 'Reseña'
        verbose_name_plural = 'Reseñas'

    def __str__(self):
        return f'{self.user.username} - {self.rating} estrellas para {self.post.title}'

class Reaction(models.Model):
    """Modelo para reacciones rápidas como WhatsApp"""
    REACTION_TYPES = [
        ('👍', '👍 Me gusta'),
        ('❤️', '❤️ Me encanta'),
        ('😂', '😂 Divertido'),
        ('😮', '😮 Asombrado'),
        ('😢', '😢 Triste'),
        ('😡', '😡 Enojado'),
    ]
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions', verbose_name='Post')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')
    reaction_type = models.CharField(max_length=2, choices=REACTION_TYPES, verbose_name='Tipo de reacción')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')
    
    class Meta:
        unique_together = ['post', 'user']
        verbose_name = 'Reacción'
        verbose_name_plural = 'Reacciones'
    
    def __str__(self):
        return f'{self.user.username} reaccionó {self.reaction_type} a {self.post.title}'

class CommentVote(models.Model):
    """Modelo para votos de comentarios (upvote/downvote)"""
    VOTE_CHOICES = [
        (1, 'Upvote'),
        (-1, 'Downvote'),
        (0, 'Neutral'),
    ]
    
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='votes', verbose_name='Comentario')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')
    vote = models.IntegerField(choices=VOTE_CHOICES, verbose_name='Voto')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    
    class Meta:
        unique_together = ['comment', 'user']
        verbose_name = 'Voto de Comentario'
        verbose_name_plural = 'Votos de Comentarios'
    
    def __str__(self):
        vote_text = dict(self.VOTE_CHOICES)[self.vote]
        return f'{self.user.username} - {vote_text} en comentario {self.comment.id}'

class Notification(models.Model):
    """Modelo para notificaciones del sistema"""
    NOTIFICATION_TYPES = [
        ('mention', 'Mención'),
        ('comment', 'Nuevo comentario'),
        ('reaction', 'Nueva reacción'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name='Usuario')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, verbose_name='Tipo')
    title = models.CharField(max_length=200, verbose_name='Título')
    message = models.TextField(verbose_name='Mensaje')
    url = models.URLField(blank=True, verbose_name='URL')
    is_read = models.BooleanField(default=False, verbose_name='Leída')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')
    
    class Meta:
        ordering = ['-created_date']
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
    
    def __str__(self):
        return f'{self.user.username} - {self.title}'

class Subscription(models.Model):
    """Modelo para suscripciones por autor o tema"""
    SUBSCRIPTION_TYPES = [
        ('author', 'Autor'),
        ('tag', 'Etiqueta'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions', verbose_name='Usuario')
    subscription_type = models.CharField(max_length=10, choices=SUBSCRIPTION_TYPES, verbose_name='Tipo')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='subscribers', verbose_name='Autor')
    tag = models.CharField(max_length=100, blank=True, verbose_name='Etiqueta')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')
    
    class Meta:
        unique_together = ['user', 'subscription_type', 'author', 'tag']
        verbose_name = 'Suscripción'
        verbose_name_plural = 'Suscripciones'
    
    def __str__(self):
        if self.subscription_type == 'author':
            return f'{self.user.username} suscrito a {self.author.username}'
        else:
            return f'{self.user.username} suscrito a etiqueta {self.tag}'
