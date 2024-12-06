"""
Este archivo contiene todas las vistas (views) del sistema de encuestas.
Las vistas son funciones que procesan las peticiones HTTP y retornan respuestas.
"""

# Importaciones necesarias
import datetime
from django.http import JsonResponse  # Para retornar respuestas JSON
from django.shortcuts import render, redirect, get_object_or_404  # Funciones de utilidad de Django
from django.contrib.auth import authenticate, login  # Para autenticación
from django.contrib import messages  # Para mostrar mensajes al usuario
from django.contrib.auth.forms import UserCreationForm  # Formulario de registro
from django.db.models import Count, Avg  # Para operaciones de agregación
from django.db.models.functions import Round  # Para redondear números
from .models import *  # Importa todos los modelos
from .forms import *  # Importa todos los formularios

def home(request):
    """
    Vista de la página principal.
    Simplemente renderiza la plantilla home.html
    """
    return render(request, 'home.html')

def lista_formulario(request):
    """
    Muestra la lista de todas las encuestas disponibles.
    
    Ejemplo de uso:
    /lista_formulario/ -> Muestra todas las encuestas en una tabla
    """
    formularios = Encuesta.objects.all()  # Obtiene todas las encuestas de la base de datos
    return render(request, 'lista_formulario.html', {'formularios': formularios})

def crear_formulario(request):
    """
    Permite crear una nueva encuesta.
    Solo usuarios autenticados pueden crear encuestas.
    
    Flujo:
    1. Verifica que el usuario esté autenticado
    2. Si es POST, procesa el formulario
    3. Si es GET, muestra el formulario vacío
    
    Ejemplo:
    POST /crear_formulario/ 
    {
        'titulo': 'Mi encuesta',
        'descripcion': 'Una encuesta de ejemplo'
    }
    """
    # Verifica autenticación
    if not request.user.is_authenticated:
        messages.error(request, 'Debe iniciar sesión para crear una encuesta')
        return redirect('login')
        
    if request.method == 'POST':
        form = EncuestaForm(request.POST)
        if form.is_valid():
            encuesta = form.save(commit=False)
            # Asocia la encuesta con el administrador actual
            administrador = Administrador.objects.get(ID_Administrador=request.user)
            encuesta.ID_Administrador = administrador
            encuesta.save()
            
            # Registra la creación en el log
            log = Log(
                ID_Encuesta=encuesta,
                ID_Administrador=administrador,
                ID_Encuestado=None,
                ID_Respuesta=None,
                Modificacion="Creación de nueva encuesta"
            )
            log.save()
            messages.success(request, 'Encuesta creada exitosamente')
            return redirect('lista_formulario')
        else:
            messages.error(request, 'Error al crear la encuesta. Por favor revise los datos ingresados.')
    else:
        form = EncuestaForm()
    return render(request, 'formulario.html', {'form': form})

def login_view(request):
    """
    Maneja el inicio de sesión de usuarios.
    
    Ejemplo de uso:
    POST /login/
    {
        'username': 'usuario',
        'password': 'contraseña'
    }
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido {username}!')
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'login.html')

def register(request):
    """
    Maneja el registro de nuevos usuarios.
    Crea tanto un usuario Django como un registro en la tabla Administrador.
    
    Ejemplo:
    POST /register/
    {
        'username': 'nuevo_usuario',
        'password1': 'contraseña',
        'password2': 'contraseña'
    }
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Crea el registro de administrador asociado
            administrador = Administrador(
                ID_Administrador=user,
                Nombre=user.username,
                Usuario=user.username,
            )
            administrador.save()
            
            messages.success(request, f'Cuenta creada exitosamente para {user.username}')
            return redirect('login')
        else:
            messages.error(request, 'Error en el formulario. Por favor revise los datos ingresados.')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def lista_establecimiento(request):
    """
    Muestra la lista de todos los establecimientos registrados.
    """
    establecimientos = Establecimiento.objects.all()
    return render(request, 'lista_establecimiento.html', {'establecimientos': establecimientos})

def crear_establecimiento(request):
    """
    Permite crear un nuevo establecimiento.
    
    Ejemplo:
    POST /crear_establecimiento/
    {
        'nombre': 'Mi Establecimiento',
        'direccion': 'Calle Principal 123'
    }
    """
    if request.method == 'POST':
        form = EstablecimientoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Establecimiento creado exitosamente')
            return redirect('lista_establecimiento')
        else:
            messages.error(request, 'Error al crear el establecimiento. Por favor revise los datos ingresados.')
    else:
        form = EstablecimientoForm()
    return render(request, 'establecimiento.html', {'form': form})

def editar_establecimiento(request, id):
    """
    Permite editar un establecimiento existente.
    
    Parámetros:
    id -- ID del establecimiento a editar
    """
    establecimiento = get_object_or_404(Establecimiento, ID_Establecimiento=id)
    if request.method == 'POST':
        form = EstablecimientoForm(request.POST, instance=establecimiento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Establecimiento actualizado exitosamente')
            return redirect('lista_establecimiento')
        else:
            messages.error(request, 'Error al actualizar el establecimiento. Por favor revise los datos ingresados.')
    else:
        form = EstablecimientoForm(instance=establecimiento)
    return render(request, 'establecimiento.html', {'form': form})

def eliminar_establecimiento(request, id):
    """
    Elimina un establecimiento existente.
    
    Parámetros:
    id -- ID del establecimiento a eliminar
    """
    establecimiento = get_object_or_404(Establecimiento, ID_Establecimiento=id)
    if request.method == 'POST':
        try:
            establecimiento.delete()
            messages.success(request, 'Establecimiento eliminado exitosamente')
            return redirect('lista_establecimiento')
        except Exception as e:
            messages.error(request, 'Error al eliminar el establecimiento. Es posible que tenga datos asociados.')
    return render(request, 'confirmar_eliminar.html', {'objeto': establecimiento})

def editar_formulario(request, id):
    """
    Permite editar una encuesta existente.
    Solo usuarios autenticados pueden editar encuestas.
    
    Parámetros:
    id -- ID de la encuesta a editar
    """
    encuesta = get_object_or_404(Encuesta, id=id)
    
    if not request.user.is_authenticated:
        messages.error(request, 'Debe iniciar sesión para editar una encuesta')
        return redirect('login')
        
    if request.method == 'POST':
        form = EncuestaForm(request.POST, instance=encuesta)
        if form.is_valid():
            encuesta = form.save(commit=False)
            administrador = Administrador.objects.get(ID_Administrador=request.user)
            encuesta.ID_Administrador = administrador
            encuesta.save()
            
            # Registra la edición en el log
            log = Log(
                ID_Encuesta=encuesta,
                ID_Administrador=administrador,
                Modificacion="Edición de encuesta"
            )
            log.save()
            
            messages.success(request, 'Encuesta actualizada exitosamente')
            return redirect('lista_formulario')
        else:
            messages.error(request, 'Error al actualizar la encuesta. Por favor revise los datos ingresados.')
    else:
        form = EncuestaForm(instance=encuesta)
    
    return render(request, 'formulario.html', {'form': form, 'edicion': True})

def eliminar_formulario(request, id):
    """
    Elimina una encuesta existente.
    Solo usuarios autenticados pueden eliminar encuestas.
    
    Parámetros:
    id -- ID de la encuesta a eliminar
    
    Retorna:
    JsonResponse con el resultado de la operación
    """
    encuesta = get_object_or_404(Encuesta, id=id)
    
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Debe iniciar sesión para eliminar una encuesta'})
        
    if request.method == 'POST':
        try:
            administrador = Administrador.objects.get(ID_Administrador=request.user)
            
            # Registra la eliminación en el log
            log = Log(
                ID_Encuesta=encuesta,
                ID_Administrador=administrador,
                Modificacion="Eliminación de encuesta"
            )
            log.save()
            
            encuesta.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Error al eliminar la encuesta'})
            
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

def detalle_formulario(request, id):
    """
    Muestra el detalle de una encuesta y permite agregar preguntas.
    
    Parámetros:
    id -- ID de la encuesta a mostrar
    """
    encuesta = get_object_or_404(Encuesta, id=id)
    preguntas = Pregunta.objects.filter(ID_Encuesta=encuesta)
    
    if request.method == 'POST':
        pregunta_form = PreguntaForm(request.POST)
        if pregunta_form.is_valid():
            pregunta = pregunta_form.save(commit=False)
            pregunta.ID_Encuesta = encuesta
            pregunta.save()
            
            # Registra la nueva pregunta en el log
            administrador = Administrador.objects.get(ID_Administrador=request.user)
            log = Log(
                ID_Encuesta=encuesta,
                ID_Administrador=administrador,
                Modificacion=f"Agregada nueva pregunta: {pregunta.Titulo}"
            )
            log.save()
            
            messages.success(request, 'Pregunta agregada exitosamente')
            return redirect('detalle_formulario', id=id)
    else:
        pregunta_form = PreguntaForm()
    
    context = {
        'encuesta': encuesta,
        'preguntas': preguntas,
        'pregunta_form': pregunta_form
    }
    return render(request, 'detalle_formulario.html', context)

def eliminar_pregunta(request, id):
    """
    Elimina una pregunta de una encuesta.
    Solo usuarios autenticados pueden eliminar preguntas.
    
    Parámetros:
    id -- ID de la pregunta a eliminar
    
    Retorna:
    JsonResponse con el resultado de la operación
    """
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'No autorizado'})
        
    if request.method == 'POST':
        try:
            pregunta = get_object_or_404(Pregunta, id=id)
            encuesta = pregunta.ID_Encuesta
            administrador = Administrador.objects.get(ID_Administrador=request.user)
            
            # Registra la eliminación en el log
            log = Log(
                ID_Encuesta=encuesta,
                ID_Administrador=administrador,
                Modificacion=f"Eliminada pregunta: {pregunta.Titulo}"
            )
            log.save()
            
            pregunta.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
            
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

def completar_formulario(request, id):
    """
    Permite a un usuario completar una encuesta.
    
    Parámetros:
    id -- ID de la encuesta a completar
    
    Ejemplo de uso:
    POST /completar_formulario/1/
    {
        'correo': 'usuario@ejemplo.com',
        'pregunta_1': '8',
        'pregunta_2': '7'
    }
    """
    encuesta = get_object_or_404(Encuesta, id=id)
    preguntas = Pregunta.objects.filter(ID_Encuesta=encuesta)
    
    if request.method == 'POST':
        # Validar correo del encuestado
        correo = request.POST.get('correo')
        if not correo:
            messages.error(request, 'El correo es requerido')
            return redirect('completar_formulario', id=id)
            
        # Crear o obtener encuestado
        encuestado, created = Encuestado.objects.get_or_create(Correo=correo)
        
        # Guardar respuestas
        for pregunta in preguntas:
            respuesta_valor = request.POST.get(f'pregunta_{pregunta.id}')
            if respuesta_valor:
                respuesta = Respuesta.objects.create(
                    Respuesta=respuesta_valor,
                    ID_Pregunta=pregunta
                )
                
                # Registra la respuesta en el log
                log = Log(
                    ID_Encuesta=encuesta,
                    ID_Encuestado=encuestado,
                    ID_Respuesta=respuesta,
                    Modificacion=f"Respuesta registrada: {respuesta_valor}"
                )
                log.save()
        
        messages.success(request, '¡Gracias por completar la encuesta!')
        return redirect('home')
        
    return render(request, 'completar_formulario.html', {
        'encuesta': encuesta,
        'preguntas': preguntas
    })

def analisis_formulario(request, id):
    """
    Muestra el análisis estadístico de una encuesta.
    
    Parámetros:
    id -- ID de la encuesta a analizar
    
    Calcula:
    - Promedio de respuestas por pregunta
    - Distribución de respuestas
    - Porcentajes de cada respuesta
    """
    encuesta = get_object_or_404(Encuesta, id=id)
    preguntas = Pregunta.objects.filter(ID_Encuesta=encuesta)
    
    analisis_preguntas = []
    total_respuestas = 0
    
    for pregunta in preguntas:
        respuestas = Respuesta.objects.filter(ID_Pregunta=pregunta)
        total_respuestas = respuestas.count()
        
        # Calcular estadísticas básicas
        stats = {
            'promedio': Round(Avg('Respuesta'), 2),
            'distribucion': Count('Respuesta'),
        }
        
        # Obtener distribución de respuestas
        distribucion = respuestas.values('Respuesta').annotate(
            total=Count('id')
        ).order_by('Respuesta')
        
        # Calcular porcentajes
        distribucion_porcentaje = []
        for d in distribucion:
            porcentaje = (d['total'] / total_respuestas * 100) if total_respuestas > 0 else 0
            distribucion_porcentaje.append({
                'valor': d['Respuesta'],
                'total': d['total'],
                'porcentaje': round(porcentaje, 1)
            })
        
        analisis_preguntas.append({
            'pregunta': pregunta,
            'promedio': respuestas.aggregate(promedio=Round(Avg('Respuesta'), 2))['promedio'] or 0,
            'total_respuestas': total_respuestas,
            'distribucion': distribucion_porcentaje
        })
    
    return render(request, 'analisis_formulario.html', {
        'encuesta': encuesta,
        'analisis': analisis_preguntas,
        'total_respuestas': total_respuestas
    })

def log_formulario(request, id):
    """
    Muestra el historial de actividades (log) de una encuesta.
    
    Parámetros:
    id -- ID de la encuesta
    """
    encuesta = get_object_or_404(Encuesta, id=id)
    logs = Log.objects.filter(ID_Encuesta=encuesta).order_by('-Fecha')
    
    return render(request, 'log_formulario.html', {
        'encuesta': encuesta,
        'logs': logs
    })
