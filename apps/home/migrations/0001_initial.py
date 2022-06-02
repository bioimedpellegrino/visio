# Generated by Django 3.2.6 on 2022-04-09 09:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Param',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('detection', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('recognition', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('emotion_agegender', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('saveimage', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('useaudio', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('framelapse', models.PositiveRealField(blank=True, default=0, null=True)),
            ],
            options={
                'verbose_name': 'Impostazione',
                'verbose_name_plural': 'Impostazioni',
            },
        ),
        migrations.CreateModel(
            name='Camera',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, default='Visio standard camera', max_length=1024, null=True)),
                ('desc', models.TextField(blank=True, null=True)),
                ('user_selection', models.CharField(blank=True, default='', max_length=200, null=True)),
            ],
            options={
                'verbose_name': 'Videocamera',
                'verbose_name_plural': 'Videocamere',
            },
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, default='', max_length=1024, null=True)),
                ('desc', models.TextField(blank=True, null=True)),
                ('site', models.CharField(blank=True, max_length=2048, null=True)),
                ('camera', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.camera')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(default='', max_length=1024, null=True)),
                ('last_name', models.CharField(default='', max_length=1024, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('face_image', models.FileField(upload_to='picture/portraits')),
            ],
        ),
        migrations.CreateModel(
            name='VisioRecognition',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('age', models.CharField(blank=True, default='', max_length=1024, null=True)),
                ('gender', models.CharField(blank=True, default='', max_length=10, null=True)),
                ('emotion', models.CharField(blank=True, default='', max_length=1024, null=True)),
                ('entity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.entity')),
                ('person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.person')),
            ],
        ),
        migrations.CreateModel(
            name='ImageData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('face_num', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('image', models.FileField(upload_to='pictures/acquisition')),
                ('entity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.entity')),
            ],
            options={
                'verbose_name': 'Metadati',
                'verbose_name_plural': 'Immagini - Metadati',
            },
        ),
    ]
