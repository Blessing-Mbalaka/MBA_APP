# apps.py
from django.apps import AppConfig
from django.core.signals import request_started
from django.dispatch import receiver

class MbaadminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mbaAdmin'