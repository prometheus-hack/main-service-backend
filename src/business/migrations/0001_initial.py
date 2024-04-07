# Generated by Django 5.0.4 on 2024-04-07 02:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organizations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.organization')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QRCodeUsing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('used_dt', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.organization')),
            ],
        ),
    ]