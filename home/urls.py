from django.urls import path
from django.contrib.auth.views import LogoutView, login_required

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', login_required(LogoutView.as_view(next_page='login')), name='logout'),
    path('lista_formulario/', login_required(views.lista_formulario), name='lista_formulario'),
    path('crear_formulario/', login_required(views.crear_formulario), name='crear_formulario'),

    path('editar_formulario/<int:id>/', login_required(views.editar_formulario), name='editar_formulario'),
    path('eliminar_formulario/<int:id>/', login_required(views.eliminar_formulario), name='eliminar_formulario'), 
    path('detalle_formulario/<int:id>/', login_required(views.detalle_formulario), name='detalle_formulario'),
    path('eliminar_pregunta/<int:id>/', login_required(views.eliminar_pregunta), name='eliminar_pregunta'),
    path('analisis_formulario/<int:id>/', login_required(views.analisis_formulario), name='analisis_formulario'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('completar_formulario/<int:id>/', views.completar_formulario, name='completar_formulario'),
    path('log_formulario/<int:id>/', views.log_formulario, name='log_formulario'),
]