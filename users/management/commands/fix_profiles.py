from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from users.models import UserProfile


class Command(BaseCommand):
    help = "Create missing UserProfile instances for existing users"

    def handle(self, *args, **options):
        users_without_profiles = 0
        for user in User.objects.all():
            try:
                user.profile
            except UserProfile.DoesNotExist:
                UserProfile.objects.create(user=user)
                users_without_profiles += 1
                self.stdout.write(f"Created profile for user: {user.username}")

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {users_without_profiles} profiles"
            )
        )
