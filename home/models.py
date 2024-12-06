from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
# Create your models here.

class Establecimiento(models.Model):
    ID_Establecimiento = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=35)
    Direccion = models.CharField(max_length=30)
    Telefono = models.IntegerField(validators=[MinValueValidator(100000000), MaxValueValidator(999999999)])
    Correo = models.CharField(max_length=40)

    class Meta:
        db_table = 'establecimiento'

    def __str__(self):
        return self.Nombre


class Administrador(models.Model):
    ID_Administrador = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    Nombre = models.CharField(max_length=35)
    Usuario = models.CharField(max_length=40, unique=True)
    ID_Establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE ,blank=True, null=True)

    class Meta:
        db_table = 'administrador'

    def __str__(self):
        return self.Nombre


class Encuesta(models.Model):
    Titulo = models.CharField(max_length=60)
    Descripcion = models.CharField(max_length=60, blank=True, null=True)
    ID_Administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE,blank=True, null=True)

    class Meta:
        db_table = 'encuesta'

    def __str__(self):
        return self.Titulo

class Pregunta(models.Model):
    
    Titulo = models.CharField(max_length=60)
    ID_Encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)

    class Meta:
        db_table = 'pregunta'

    def __str__(self):
        return self.Titulo

class Respuesta(models.Model):
    Respuesta = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)])

    ID_Pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)

    class Meta:
        db_table = 'respuesta'

    def __str__(self):
        return str(self.Respuesta)

class Encuestado(models.Model):
    Correo = models.CharField(max_length=40)

    class Meta:
        db_table = 'encuestado'

    def __str__(self):
        return self.Correo

class Log(models.Model):
    ID_Encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE,blank=True, null=True)
    ID_Encuestado = models.ForeignKey(Encuestado, on_delete=models.CASCADE,blank=True, null=True)
    ID_Respuesta = models.ForeignKey(Respuesta, on_delete=models.CASCADE,blank=True, null=True)
    ID_Administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE,blank=True, null=True)
    Fecha = models.DateTimeField(auto_now_add=True)
    Modificacion = models.CharField(max_length=256)

    class Meta:
        db_table = 'log'

    def __str__(self):
        return str(self.ID_Log)
