# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-17 11:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField(max_length=10000)),
                ('start', models.DateTimeField(default=django.utils.timezone.now)),
                ('end', models.DateTimeField()),
                ('startmode', models.BooleanField(default=False)),
                ('level_ordered', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Contestant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(default=0)),
                ('level_number', models.IntegerField(default=1)),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brain.Contest')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('number', models.IntegerField()),
                ('points', models.IntegerField()),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brain.Contest')),
            ],
        ),
        migrations.CreateModel(
            name='Moderator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isowner', models.BooleanField(default=False)),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brain.Contest')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=20000)),
                ('answer', models.TextField(max_length=50000)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brain.Moderator')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brain.Level')),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('contestant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brain.Contestant')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brain.Question')),
            ],
        ),
    ]
