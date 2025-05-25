from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model 

class Command(BaseCommand):

    def handle(self, *args, **options):
        user = get_user_model()
        if not user.objects.filter(username='admin').exists():
            user.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin',
            )
            print("Admin created successfully!")
        else:
            print("Admin already exists.")

