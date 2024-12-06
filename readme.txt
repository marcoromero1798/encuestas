# Sistema de Encuestas

encuestas/              # Directorio raíz del proyecto
├── encuestas/         # Configuración principal del proyecto
│   ├── settings.py    # Configuraciones de Django
│   ├── urls.py        # URLs principales
│   └── wsgi.py        # Configuración para despliegue
├── home/              # Aplicación principal
│   ├── models.py      # Modelos de la base de datos
│   ├── views.py       # Vistas y lógica de negocio
│   ├── forms.py       # Formularios
│   └── urls.py        # URLs de la aplicación
└── manage.py          # Script de administración de Django

## Descripción
Sistema web desarrollado en Django para la gestión de encuestas, permitiendo crear, administrar y analizar encuestas con un sistema de puntuación del 1 al 9.

## Características Principales
- Gestión de usuarios y autenticación
- Creación y edición de encuestas
- Sistema de preguntas con escala del 1 al 9
- Análisis estadístico de resultados
- Registro de actividades (logs)
- Gestión de establecimientos
- Interfaz responsive con Bootstrap 5

## Estructura del Proyecto

### Modelos (models.py)
- Establecimiento: Gestión de instituciones
- Administrador: Usuarios con privilegios administrativos
- Encuesta: Formularios de evaluación
- Pregunta: Elementos individuales de cada encuesta
- Respuesta: Registros de respuestas de usuarios
- Encuestado: Información de participantes
- Log: Registro de actividades del sistema

### Vistas Principales (views.py)
- home: Página principal
- lista_formulario: Visualización de encuestas
- crear_formulario: Creación de nuevas encuestas
- completar_formulario: Interfaz para responder encuestas
- analisis_formulario: Estadísticas y resultados
- log_formulario: Historial de actividades

### Formularios (forms.py)
- EstablecimientoForm: Gestión de establecimientos
- EncuestaForm: Creación/edición de encuestas
- PreguntaForm: Gestión de preguntas
- RespuestaForm: Registro de respuestas

## Requisitos Técnicos
- Python 3.x
- Django 4.2.16
- Base de datos SQLite
- Bootstrap 5.3.0
- SweetAlert2 para notificaciones
- Bootstrap Icons

## Configuración del Entorno
1. Instalar dependencias:
   ```
   pip install django
   ```

2. Configurar base de datos:
   ```
   python manage.py migrate
   ```

3. Crear superusuario:
   ```
   python manage.py createsuperuser
   ```

4. Iniciar servidor:
   ```
   python manage.py runserver
   ```

## Estructura de URLs
- /: Página principal
- /login/: Inicio de sesión
- /register/: Registro de usuarios
- /lista_formulario/: Lista de encuestas
- /crear_formulario/: Creación de encuestas
- /detalle_formulario/<id>/: Vista detallada
- /analisis_formulario/<id>/: Análisis estadístico
- /log_formulario/<id>/: Historial de actividades

## Características de Seguridad
- Autenticación requerida para acciones administrativas
- Protección CSRF en formularios
- Validación de datos en formularios
- Registro de actividades y modificaciones

## Interfaz de Usuario
- Diseño responsive
- Navegación intuitiva
- Mensajes de confirmación
- Modales para acciones críticas
- Gráficos estadísticos
- Historial de actividades

## Mantenimiento
- Respaldos regulares de la base de datos
- Monitoreo de logs
- Actualización de dependencias
- Revisión de seguridad

## Notas Adicionales
- El sistema utiliza Bootstrap para el diseño responsive
- Implementa SweetAlert2 para mejores interacciones
- Incluye sistema de logs para auditoría
- Soporte para múltiples establecimientos


Sistema de Encuestas - Documentación
Descripción
Este es un sistema de encuestas desarrollado con Django que permite crear, gestionar y analizar encuestas con preguntas de valoración numérica (1-9).
Características Principales
Gestión de usuarios (registro, inicio de sesión)
Creación y edición de encuestas
Gestión de preguntas
Análisis de resultados con estadísticas
Registro de actividad (logs)
Interfaz responsive con Bootstrap 5
Requisitos Técnicos
Python 3.8+
Django 4.2.16
Base de datos SQLite (incluida)
Navegador web moderno
Instalación
Clonar el repositorio:
Crear y activar entorno virtual:
Instalar dependencias:
Realizar migraciones:
Crear superusuario:
Iniciar servidor:
Estructura del Proyecto
Aplicaciones
encuestas/: Proyecto principal
home/: Aplicación principal con la lógica de negocio
Modelos Principales
Establecimiento: Gestiona información de establecimientos
Administrador: Extiende el modelo de usuario de Django
Encuesta: Almacena encuestas
Pregunta: Preguntas de las encuestas
Respuesta: Respuestas numéricas (1-9)
Log: Registro de actividades
Vistas Principales
Lista de encuestas
Creación/edición de encuestas
Detalle de encuesta
Análisis de resultados
Registro de actividad
Uso del Sistema
Acceder a http://localhost:8000
Iniciar sesión o registrarse
Crear una nueva encuesta desde el panel
Agregar preguntas a la encuesta
Compartir el enlace para completar la encuesta
Ver análisis y resultados
Personalización
Estilos
Los estilos se encuentran en:
Plantillas
Las plantillas principales están en home/templates/
Consideraciones de Seguridad
La clave secreta debe cambiarse en producción
DEBUG debe desactivarse en producción
Revisar ALLOWED_HOSTS según el entorno
Solución de Problemas Comunes
Error de migraciones:
Problemas de estáticos:
Error de permisos:
Verificar que el usuario tenga los permisos correctos
Revisar la asignación de roles en el admin
Contribución
Hacer fork del repositorio
Crear rama para nuevas características
Realizar cambios siguiendo el estilo del código
Enviar pull request