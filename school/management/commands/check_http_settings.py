from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.termcolors import colorize


class Command(BaseCommand):
    help = "Check basic Django settings configuration"

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.NOTICE("Checking Django settings configuration...")
        )

        # Check DEBUG setting
        self.stdout.write(
            f"DEBUG mode: {colorize('ON' if settings.DEBUG else 'OFF', fg='green' if settings.DEBUG else 'red')}"
        )

        # Display basic settings
        self.stdout.write(f"SECRET_KEY: {'*' * 10} (hidden)")
        self.stdout.write(f"ALLOWED_HOSTS: {', '.join(settings.ALLOWED_HOSTS)}")
        self.stdout.write(f"DATABASE ENGINE: {settings.DATABASES['default']['ENGINE']}")
        self.stdout.write(f"STATIC_URL: {settings.STATIC_URL}")
        self.stdout.write(f"MEDIA_URL: {settings.MEDIA_URL}")

        # Display middleware
        self.stdout.write("\nMiddleware:")
        for middleware in settings.MIDDLEWARE:
            self.stdout.write(f"  - {middleware}")

        # Display installed apps
        self.stdout.write("\nInstalled Apps:")
        for app in settings.INSTALLED_APPS:
            self.stdout.write(f"  - {app}")

        self.stdout.write(self.style.SUCCESS("\nSettings check complete!"))
