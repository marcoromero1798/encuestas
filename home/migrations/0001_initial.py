# Generated by Django 4.2.16 on 2024-12-06 13:50

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0013_merge_20241206_1049'),
    ]

    operations = [
        migrations.CreateModel(
            name='Administrador',
            fields=[
                ('ID_Administrador', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('Nombre', models.CharField(max_length=35)),
                ('Usuario', models.CharField(max_length=40, unique=True)),
                ('Contraseña', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Encuesta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Titulo', models.CharField(max_length=60)),
                ('Descripcion', models.CharField(blank=True, max_length=60, null=True)),
                ('ID_Administrador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.administrador')),
            ],
        ),
        migrations.CreateModel(
            name='Encuestado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Correo', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Establecimiento',
            fields=[
                ('ID_Establecimiento', models.AutoField(primary_key=True, serialize=False)),
                ('Nombre', models.CharField(max_length=35)),
                ('Direccion', models.CharField(max_length=30)),
                ('Telefono', models.IntegerField(validators=[django.core.validators.MinValueValidator(100000000), django.core.validators.MaxValueValidator(999999999)])),
                ('Correo', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Titulo', models.CharField(max_length=60)),
                ('ID_Encuesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.encuesta')),
            ],
        ),
        migrations.CreateModel(
            name='Respuesta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Respuesta', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(9)])),
                ('ID_Pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.pregunta')),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Fecha', models.DateTimeField(auto_now_add=True)),
                ('Modificacion', models.CharField(max_length=256)),
                ('ID_Administrador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.administrador')),
                ('ID_Encuesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.encuesta')),
                ('ID_Encuestado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.encuestado')),
                ('ID_Respuesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.respuesta')),
            ],
        ),
        migrations.AddField(
            model_name='administrador',
            name='ID_Establecimiento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.establecimiento'),
        ),
    ]
