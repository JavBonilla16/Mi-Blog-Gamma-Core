import re
from django.contrib.auth.models import User
from .models import Notification

def detect_mentions(text, post, comment_author):
    """
    Detecta menciones @usuario en el texto y crea notificaciones
    """
    # Patrón para encontrar menciones @username
    mention_pattern = r'@(\w+)'
    mentions = re.findall(mention_pattern, text)
    
    created_notifications = []
    
    for username in mentions:
        try:
            # Buscar el usuario mencionado
            mentioned_user = User.objects.get(username=username)
            
            # No crear notificación si el usuario se menciona a sí mismo
            if mentioned_user != comment_author:
                # Crear notificación
                notification = Notification.objects.create(
                    user=mentioned_user,
                    notification_type='mention',
                    title=f'Te mencionaron en un comentario',
                    message=f'{comment_author.first_name} {comment_author.last_name} te mencionó en un comentario del post "{post.title}"',
                    url=post.get_absolute_url()
                )
                created_notifications.append(notification)
                
        except User.DoesNotExist:
            # Usuario no existe, ignorar silenciosamente
            continue
    
    return created_notifications

def send_reaction_notification(post, user, reaction_type):
    """
    Envía notificación al autor del post cuando alguien reacciona
    """
    # No notificar si es el propio autor
    if user != post.author:
        Notification.objects.create(
            user=post.author,
            notification_type='reaction',
            title=f'Nueva reacción en tu post',
            message=f'{user.first_name} {user.last_name} reaccionó con {reaction_type} a tu post "{post.title}"',
            url=post.get_absolute_url()
        )

def send_comment_notification(post, comment_author):
    """
    Envía notificación al autor del post cuando alguien comenta
    """
    # No notificar si es el propio autor
    if comment_author != post.author:
        Notification.objects.create(
            user=post.author,
            notification_type='comment',
            title=f'Nuevo comentario en tu post',
            message=f'{comment_author.first_name} {comment_author.last_name} comentó en tu post "{post.title}"',
            url=post.get_absolute_url()
        )
