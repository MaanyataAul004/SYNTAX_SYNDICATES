from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.sites.models import Site

class AuctionsConfig(AppConfig):
    name = 'auctions'

    def ready(self):
        from django.contrib.sites.models import Site  # Import inside ready to avoid circular imports
        post_migrate.connect(create_default_site, sender=self)

def create_default_site(sender, **kwargs):
    Site.objects.update_or_create(
        id=1,
        defaults={
            'domain': '127.0.0.1:8000',  # Replace with your actual domain
            'name': 'Your Site Name'
        }
    )
