from django.core.management.base import BaseCommand
from devices.models import User


class Command(BaseCommand):
    help = 'Sync is_staff field with is_admin field for all users'

    def handle(self, *args, **options):
        users = User.objects.all()
        updated_count = 0

        for user in users:
            if user.is_staff != user.is_admin:
                user.is_staff = user.is_admin
                user.save()
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Updated {user.username}: is_staff={user.is_staff}, is_admin={user.is_admin}'
                    )
                )

        if updated_count == 0:
            self.stdout.write(
                self.style.SUCCESS('All users are already in sync.')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'\nSuccessfully synced {updated_count} user(s).'
                )
            )
