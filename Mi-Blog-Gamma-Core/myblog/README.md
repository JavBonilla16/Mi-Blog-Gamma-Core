# Blog Django - Sistema Social Completo

Un blog completo desarrollado con Django que incluye sistema de autenticación, autorización, contenido enriquecido, calificaciones, comentarios con moderación y **funcionalidades sociales avanzadas**.

## Características

### Funcionalidades Básicas
- ✅ **Sistema de autenticación completo** (registro, login, logout)
- ✅ **Perfiles de usuario** con avatar y biografía
- ✅ **CRUD completo de posts** con autorización
- ✅ **Sistema de comentarios** con moderación por autor
- ✅ **Sistema de calificaciones** (1-5 estrellas)
- ✅ **Contenido enriquecido** con CKEditor
- ✅ **Subida de imágenes** para posts y avatares
- ✅ **Sistema de etiquetas** con django-taggit
- ✅ **Búsqueda y filtrado** de posts
- ✅ **Paginación** en todas las listas
- ✅ **Interfaz moderna** con Bootstrap 5
- ✅ **Responsive design**

### Funcionalidades Sociales (NUEVAS)
- ✅ **Reacciones rápidas** con emoticones (como WhatsApp)
- ✅ **Sistema de votos** para comentarios (upvote/downvote)
- ✅ **Mejores comentarios** ordenados por score y pinned
- ✅ **Menciones @usuario** en comentarios
- ✅ **Sistema de notificaciones** in-app
- ✅ **Suscripciones** por autor o etiqueta
- ✅ **Notificaciones por email** para suscripciones
- ✅ **Feeds RSS** filtrados por autor/etiqueta
- ✅ **Rate limiting** para prevenir spam

## Prerrequisitos

- Python 3.8+
- pip (gestor de paquetes de Python)

## Instalación

1. **Clona el repositorio:**
   ```bash
   git clone <url-del-repositorio>
   cd myblog
   ```

2. **Crea un entorno virtual:**
   ```bash
   python -m venv .venv
   ```

3. **Activa el entorno virtual:**
   
   **En Linux/macOS:**
   ```bash
   source .venv/bin/activate
   ```
   
   **En Windows:**
   ```bash
   .venv\Scripts\activate
   ```

4. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configura las variables de entorno:**
   
   Crea un archivo `.env` en la raíz del proyecto con:
   ```
   SECRET_KEY=tu-clave-secreta-aqui
   DEBUG=True
   ```

6. **Aplica las migraciones:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Carga los datos de prueba:**
   ```bash
   python manage.py loaddata blog/fixtures/users.json
   python manage.py loaddata blog/fixtures/posts.json blog/fixtures/comments.json blog/fixtures/reactions.json blog/fixtures/comment_votes.json blog/fixtures/subscriptions.json blog/fixtures/notifications.json
   ```

8. **Crea un superusuario (opcional):**
   ```bash
   python manage.py createsuperuser
   ```

9. **Ejecuta el servidor de desarrollo:**
   ```bash
   python manage.py runserver
   ```

10. **Accede a la aplicación:**
    - Blog: http://127.0.0.1:8000/
    - Admin: http://127.0.0.1:8000/admin/

## Usuarios de prueba

Después de cargar las fixtures, tendrás estos usuarios disponibles:

| Usuario | Contraseña | Descripción |
|---------|------------|-------------|
| `admin` | `admin123` | Administrador del sistema |
| `javier` | `javier123` | Autor de posts sobre Django |
| `maria` | `maria123` | Autora de posts sobre Python |
| `carlos` | `carlos123` | Autor de posts sobre tendencias web |
| `ana` | `ana123` | Autora de posts sobre optimización |

## Configuración de archivos multimedia

Para que las imágenes se muestren correctamente en desarrollo, asegúrate de que las siguientes configuraciones estén en `settings.py`:

```python
# Archivos multimedia
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

Y en `urls.py` principal:

```python
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## Estructura del proyecto

```
myblog/
├── blog/                    # Aplicación principal
│   ├── models.py           # Modelos (Post, Comment, Profile, Review)
│   ├── views.py            # Vistas (CRUD, autenticación, etc.)
│   ├── forms.py            # Formularios
│   ├── urls.py             # URLs de la aplicación
│   ├── admin.py            # Configuración del admin
│   └── templates/          # Templates HTML
├── myblog/                 # Configuración del proyecto
│   ├── settings.py         # Configuraciones
│   ├── urls.py             # URLs principales
│   └── wsgi.py
├── media/                  # Archivos subidos (imágenes)
├── static/                 # Archivos estáticos
├── requirements.txt        # Dependencias
└── README.md              # Este archivo
```

## Funcionalidades principales

### Autenticación
- Registro de usuarios con formulario personalizado
- Login/logout con redirecciones
- Perfiles de usuario con avatar y biografía

### Posts
- Crear, editar y eliminar posts (solo el autor)
- Contenido enriquecido con CKEditor
- Imágenes de portada
- Sistema de etiquetas
- Publicación inmediata o borrador

### Comentarios
- Comentarios por usuarios autenticados
- Moderación por el autor del post
- Aprobación/rechazo de comentarios

### Calificaciones
- Sistema de 1-5 estrellas
- Una calificación por usuario por post
- Promedio de calificaciones visible

### Búsqueda y filtrado
- Búsqueda por título y contenido
- Filtrado por etiquetas
- Paginación en todas las listas

### Funcionalidades Sociales

#### Reacciones Rápidas
- Sistema de reacciones con emoticones (👍, ❤️, 😂, 😮, 😢, 😡)
- Cada usuario puede reaccionar una vez por tipo por post
- Toggle: hacer clic en la misma reacción la elimina
- Contadores actualizados en tiempo real con AJAX

#### Sistema de Votos para Comentarios
- Upvote/downvote/neutral para comentarios
- Ordenamiento por "mejores comentarios" (pinned → score → fecha)
- Comentarios destacados (pinned) por moderadores
- Una sola votación por usuario por comentario

#### Menciones y Notificaciones
- Menciones @usuario en comentarios
- Notificaciones in-app con estado leído/no leído
- Notificaciones automáticas por:
  - Nuevos comentarios en posts
  - Nuevas reacciones en posts
  - Menciones en comentarios

#### Sistema de Suscripciones
- Suscripciones por autor específico
- Suscripciones por etiqueta/tema
- Notificaciones por email sobre nuevos posts
- Feeds RSS filtrados por autor/etiqueta
- Management command para envío de emails: `python manage.py send_subscription_notifications`

## Comandos útiles

### Gestión de notificaciones por email
```bash
# Enviar notificaciones sobre posts de las últimas 24 horas
python manage.py send_subscription_notifications

# Enviar notificaciones sobre posts de las últimas 48 horas
python manage.py send_subscription_notifications --hours 48
```

### Gestión de datos
```bash
# Cargar todos los datos de prueba
python manage.py loaddata blog/fixtures/users.json
python manage.py loaddata blog/fixtures/posts.json blog/fixtures/comments.json blog/fixtures/reactions.json blog/fixtures/comment_votes.json blog/fixtures/subscriptions.json blog/fixtures/notifications.json

# Crear migraciones para cambios en modelos
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate
```

## URLs importantes

| URL | Descripción |
|-----|-------------|
| `/` | Lista de posts |
| `/post/<slug>/` | Detalle de post con reacciones y comentarios |
| `/notifications/` | Panel de notificaciones |
| `/subscriptions/` | Gestión de suscripciones |
| `/rss/` | Feed RSS general |
| `/rss/author/<id>/` | Feed RSS por autor |
| `/rss/tag/<tag>/` | Feed RSS por etiqueta |
| `/admin/` | Panel de administración |

## Tecnologías utilizadas

- **Backend:** Django 4.2.23
- **Base de datos:** SQLite (desarrollo)
- **Frontend:** Bootstrap 5, Font Awesome
- **Editor de texto:** CKEditor
- **Etiquetas:** django-taggit
- **Imágenes:** Pillow
- **AJAX:** JavaScript vanilla para interacciones dinámicas
- **Email:** Django Email Backend (configurado para consola en desarrollo)
- **RSS:** Django syndication framework

## Desarrollo y Testing

### Estructura de archivos adicionales
```
blog/
├── management/
│   └── commands/
│       └── send_subscription_notifications.py  # Comando para emails
├── fixtures/                                   # Datos de prueba
│   ├── users.json
│   ├── posts.json
│   ├── comments.json
│   ├── reactions.json
│   ├── comment_votes.json
│   ├── subscriptions.json
│   └── notifications.json
└── templates/
    ├── emails/                                 # Templates de email
    │   ├── author_notification.html
    │   ├── author_notification.txt
    │   ├── tag_notification.html
    │   └── tag_notification.txt
    └── blog/
        ├── notifications.html
        ├── subscriptions.html
        └── post_detail.html (actualizado)
```

### Flujo de trabajo recomendado con GitKraken

1. **Issues y ramas:**
   - Crear un issue por función implementada
   - Crear rama feature desde el issue
   - Ejemplo: `feature/reacciones-rapidas`

2. **Tablero (GitKraken Boards):**
   - Backlog → In Progress → In Review → Done
   - WIP limit: 2 por persona

3. **Pull Requests:**
   - Un PR por función hacia develop
   - Incluir screenshots y "cómo probar"
   - Checklist: migraciones, tests, lint

### Testing de funcionalidades

Para probar las funcionalidades sociales:

1. **Reacciones:** Inicia sesión y haz clic en los emoticones en cualquier post
2. **Votos:** Vota comentarios con las flechas arriba/abajo
3. **Menciones:** Escribe `@usuario` en un comentario
4. **Notificaciones:** Ve a `/notifications/` para ver las notificaciones
5. **Suscripciones:** Ve a `/subscriptions/` para gestionar suscripciones
6. **RSS:** Accede a `/rss/` para ver el feed RSS

## Contribución

Este proyecto implementa todas las funcionalidades sociales solicitadas:

- ✅ Reacciones rápidas con emoticones
- ✅ Sistema de votos para comentarios y ordenamiento por mejores comentarios
- ✅ Menciones @usuario y sistema de notificaciones
- ✅ Suscripciones por tema/autor con alertas por email y RSS
- ✅ Migraciones y fixtures con datos de prueba
- ✅ README con instrucciones completas

El código está listo para producción y sigue las mejores prácticas de Django.
