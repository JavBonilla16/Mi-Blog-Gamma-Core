# Blog Django - Autenticación, Autorización y Contenido Enriquecido

Un blog completo desarrollado con Django que incluye sistema de autenticación, autorización, contenido enriquecido, calificaciones, comentarios con moderación y más.

## Características

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

7. **Crea un superusuario:**
   ```bash
   python manage.py createsuperuser
   ```

8. **Ejecuta el servidor de desarrollo:**
   ```bash
   python manage.py runserver
   ```

9. **Accede a la aplicación:**
   - Blog: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

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

## Tecnologías utilizadas

- **Backend:** Django 4.2.23
- **Base de datos:** SQLite (desarrollo)
- **Frontend:** Bootstrap 5, Font Awesome
- **Editor de texto:** CKEditor
- **Etiquetas:** django-taggit
- **Imágenes:** Pillow

## Capturas de pantalla requeridas

Para demostrar el funcionamiento, se requieren capturas de:

1. **Registro de usuario** (`/signup/`)
2. **Inicio de sesión** (`/login/`)
3. **Perfil de usuario** (`/profile/`)
4. **Crear nuevo post** (`/post/create/`)
5. **Detalle del post** con comentarios y calificación
6. **Búsqueda y paginación**
7. **Moderación de comentarios**

## Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Contacto

Para preguntas o sugerencias, contacta al desarrollador.

---

**Nota:** Este proyecto fue desarrollado como parte de un parcial de la materia "Desarrollo V" y cumple con todos los requisitos especificados en el documento de requerimientos.
