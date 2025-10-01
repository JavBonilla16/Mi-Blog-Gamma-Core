# 📌 Mi Blog - Gamma Core  

**Mi Blog** es un proyecto desarrollado en equipo por *Gamma Core* con **Django** y **HTML**, cuyo objetivo es crear un blog dinámico y colaborativo que integre autenticación, gestión de contenidos, comentarios moderados y calificaciones.  

---

## 🚀 Funcionalidades  

### 🔑 Autenticación y perfiles  
- Registro con formulario personalizado (`/signup/`)  
- Login y logout con redirecciones (`/login/`, `/logout/`)  
- Mensajes de éxito/error  
- Perfil de usuario con **avatar** y **biografía**  
- Vistas: `/profile/` y `/profile/edit/`  
- Avatar visible en la barra de navegación  

### 📝 Gestión de posts (CRUD)  
- Crear, editar y eliminar posts (solo el autor)  
- Restricción con `login_required` y verificación de propiedad  
- Formularios con validación  

### 💬 Comentarios con moderación  
- Solo usuarios autenticados pueden comentar  
- Campo `is_approved` para moderación  
- El autor del post aprueba/rechaza comentarios desde el detalle  

### ⭐ Sistema de calificaciones  
- Calificación de **1 a 5 estrellas**  
- Una reseña por usuario y post (`UniqueConstraint`)  
- Promedio visible en listas y detalle  
- Comentario opcional en la reseña  

### 🎨 Contenido enriquecido y multimedia  
- **CKEditor** para redacción avanzada  
- Imagen de portada (`ImageField`)  
- Resumen/excerpt automático  
- Configuración de `MEDIA_URL` y `MEDIA_ROOT`  

### 🔍 Búsqueda, etiquetas y paginación  
- Búsqueda por título y contenido (`/search/?q=...`)  
- Filtros por etiquetas (`/tag/<slug>/`) con **django-taggit**  
- Paginación de 10 posts por página  

### 💻 UI/UX  
- **Bootstrap 5** + **Font Awesome**  
- Diseño responsive  
- Barra de navegación con estado de sesión  
- Mensajes dinámicos (`django.contrib.messages`)  

---

## 🛠️ Archivos principales  
- **Modelos:** `Post`, `Comment`, `Profile`, `Review`  
- **Vistas:** autenticación, CRUD de posts, perfil de usuario, moderación, búsqueda y filtrado  
- **Templates:** base, autenticación, perfiles, lista/detalle de posts, formularios  
- **Configuración:** `settings.py` (CKEditor, taggit, media), `urls.py`, `requirements.txt`, `README.md`  

---

## ⚙️ Instalación  

1. Clonar el repositorio:  
   ```bash
   git clone <URL_DEL_REPO>
   cd mi-blog
2. Instalar dependencias:
    ``` bash
   pip install -r requirements.txt
3. Migrar base de datos:
    ``` bash
    python manage.py migrate
4. Crear superusuario:
   ``` bash
   
5. Ejecutar servidor:
   ``` bash
   python manage.py createsuperuser
6. Acceder en: http://127.0.0.1:8000/

## 🌟 Características destacadas
   -**Autorización:** solo el autor puede editar/eliminar sus posts
   -**Moderación:** el autor gestiona los comentarios de sus posts
   -**Calificaciones:** promedio dinámico en listas y detalle
   -**Contenido enriquecido:** editor avanzado con imágenes
   -**Búsqueda y filtrado:** títulos, contenido y etiquetas
   -**Interfaz moderna:** Bootstrap 5 y responsive design
