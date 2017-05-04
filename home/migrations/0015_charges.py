# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-04 08:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0014_pledges_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Charges',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('ptime', models.DateTimeField()),
                ('charge_time', models.DateTimeField()),
                ('status', models.CharField(choices=[('succeeded', 'succeeded'), ('failed', 'failed')], default='succeeded', max_length=40)),
                ('cnum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.CreditCards')),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Projects')),
                ('uid', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]