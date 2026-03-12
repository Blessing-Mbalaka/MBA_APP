from django.apps import AppConfig


class MbamainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mbamain'

    def ready(self):
        """Auto-populate ResearchInterest table if empty on app startup"""
        try:
            from mbamain.models import ResearchInterest
            if ResearchInterest.objects.count() == 0:
                from django.core.management import call_command
                call_command('populate_disciplines', verbosity=0)
        except Exception:
            # Silently ignore errors during app initialization
            pass
        
        # Connect signal handlers for auto profile creation
        import mbamain.signals
