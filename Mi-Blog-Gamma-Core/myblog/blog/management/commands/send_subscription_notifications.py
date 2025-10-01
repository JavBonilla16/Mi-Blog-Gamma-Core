from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
from blog.models import Post, Subscription

class Command(BaseCommand):
    help = 'Envía notificaciones por email a usuarios suscritos sobre nuevos posts'

    def add_arguments(self, parser):
        parser.add_argument(
            '--hours',
            type=int,
            default=24,
            help='Número de horas hacia atrás para buscar posts nuevos (default: 24)'
        )

    def handle(self, *args, **options):
        hours = options['hours']
        cutoff_time = timezone.now() - timedelta(hours=hours)
        
        # Buscar posts nuevos
        new_posts = Post.objects.filter(
            published=True,
            published_date__gte=cutoff_time
        ).order_by('-published_date')
        
        if not new_posts.exists():
            self.stdout.write(
                self.style.WARNING(f'No hay posts nuevos en las últimas {hours} horas')
            )
            return
        
        self.stdout.write(f'Encontrados {new_posts.count()} posts nuevos')
        
        # Procesar suscripciones por autor
        author_subscriptions = Subscription.objects.filter(
            subscription_type='author'
        ).select_related('user', 'author')
        
        emails_sent = 0
        
        for subscription in author_subscriptions:
            # Buscar posts del autor en el período
            author_posts = new_posts.filter(author=subscription.author)
            
            if author_posts.exists():
                self.send_author_notification(subscription, author_posts)
                emails_sent += 1
        
        # Procesar suscripciones por etiqueta
        tag_subscriptions = Subscription.objects.filter(
            subscription_type='tag'
        ).select_related('user')
        
        for subscription in tag_subscriptions:
            # Buscar posts con la etiqueta en el período
            tag_posts = new_posts.filter(tags__name=subscription.tag)
            
            if tag_posts.exists():
                self.send_tag_notification(subscription, tag_posts)
                emails_sent += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Se enviaron {emails_sent} notificaciones por email')
        )

    def send_author_notification(self, subscription, posts):
        """Envía notificación por email sobre nuevos posts de un autor"""
        subject = f'Nuevos posts de {subscription.author.first_name} {subscription.author.last_name}'
        
        context = {
            'user': subscription.user,
            'author': subscription.author,
            'posts': posts,
            'subscription_type': 'autor'
        }
        
        message = render_to_string('emails/author_notification.txt', context)
        html_message = render_to_string('emails/author_notification.html', context)
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=None,  # Usa DEFAULT_FROM_EMAIL
                recipient_list=[subscription.user.email],
                html_message=html_message,
                fail_silently=False,
            )
            self.stdout.write(f'Email enviado a {subscription.user.email} sobre {posts.count()} posts de {subscription.author.username}')
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error enviando email a {subscription.user.email}: {str(e)}')
            )

    def send_tag_notification(self, subscription, posts):
        """Envía notificación por email sobre nuevos posts con una etiqueta"""
        subject = f'Nuevos posts sobre "{subscription.tag}"'
        
        context = {
            'user': subscription.user,
            'tag': subscription.tag,
            'posts': posts,
            'subscription_type': 'etiqueta'
        }
        
        message = render_to_string('emails/tag_notification.txt', context)
        html_message = render_to_string('emails/tag_notification.html', context)
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=None,  # Usa DEFAULT_FROM_EMAIL
                recipient_list=[subscription.user.email],
                html_message=html_message,
                fail_silently=False,
            )
            self.stdout.write(f'Email enviado a {subscription.user.email} sobre {posts.count()} posts con etiqueta "{subscription.tag}"')
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error enviando email a {subscription.user.email}: {str(e)}')
            )
