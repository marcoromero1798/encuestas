import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count, Avg
from django.db.models.functions import Round
from .models import *  
from .forms import *

def home(request):
    return render(request, 'home.html')

def lista_formulario(request):
    formularios = Encuesta.objects.all()  # Obtiene todas las encuestas
    return render(request, 'lista_formulario.html', {'formularios': formularios})

def crear_formulario(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Debe iniciar sesión para crear una encuesta')
        return redirect('login')
        
    if request.method == 'POST':
        form = EncuestaForm(request.POST)
        if form.is_valid():
            encuesta = form.save(commit=False)
            # Obtener el administrador del usuario actual
            administrador = Administrador.objects.get(ID_Administrador=request.user)
            encuesta.ID_Administrador = administrador
            encuesta.save()
            
            # Crear registro en el log
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
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido {username}!')
            return redirect('home')  # Redirige a la página principal después del login
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Crear registro en la tabla Administrador
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
    establecimientos = Establecimiento.objects.all()
    return render(request, 'lista_establecimiento.html', {'establecimientos': establecimientos})

def crear_establecimiento(request):
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
            
            # Crear registro en el log
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
    encuesta = get_object_or_404(Encuesta, id=id)
    
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Debe iniciar sesión para eliminar una encuesta'})
        
    if request.method == 'POST':
        try:
            administrador = Administrador.objects.get(ID_Administrador=request.user)
            
            # Crear registro en el log antes de eliminar
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
    encuesta = get_object_or_404(Encuesta, id=id)
    preguntas = Pregunta.objects.filter(ID_Encuesta=encuesta)
    
    if request.method == 'POST':
        pregunta_form = PreguntaForm(request.POST)
        if pregunta_form.is_valid():
            pregunta = pregunta_form.save(commit=False)
            pregunta.ID_Encuesta = encuesta
            pregunta.save()
            
            # Registro en el log
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
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'No autorizado'})
        
    if request.method == 'POST':
        try:
            pregunta = get_object_or_404(Pregunta, id=id)
            encuesta = pregunta.ID_Encuesta
            administrador = Administrador.objects.get(ID_Administrador=request.user)
            
            # Registro en el log
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
                
                # Registro en el log
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
    encuesta = get_object_or_404(Encuesta, id=id)
    preguntas = Pregunta.objects.filter(ID_Encuesta=encuesta)
    
    analisis_preguntas = []
    total_respuestas = 0
    
    for pregunta in preguntas:
        respuestas = Respuesta.objects.filter(ID_Pregunta=pregunta)
        total_respuestas = respuestas.count()
        
        # Calcular estadísticas
        stats = {
            'promedio': Round(Avg('Respuesta'), 2),
            'distribucion': Count('Respuesta'),
        }
        
        # Distribución de respuestas
        distribucion = respuestas.values('Respuesta').annotate(
            total=Count('id')
        ).order_by('Respuesta')
        
        # Convertir a porcentajes
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
    encuesta = get_object_or_404(Encuesta, id=id)
    logs = Log.objects.filter(ID_Encuesta=encuesta).order_by('-Fecha')
    
    return render(request, 'log_formulario.html', {
        'encuesta': encuesta,
        'logs': logs
    })
