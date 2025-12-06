from django.core.management.base import BaseCommand
from devices.models import User


class Command(BaseCommand):
    help = 'Create an initial admin user for the Repair Café system'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, default='admin', help='Admin username')
        parser.add_argument('--password', type=str, default='admin', help='Admin password')
        parser.add_argument('--first-name', type=str, default='Admin', help='First name')
        parser.add_argument('--last-name', type=str, default='User', help='Last name')
        parser.add_argument('--email', type=str, default='admin@repaircafe.com', help='Email address')
        parser.add_argument('--update', action='store_true', help='Update user if already exists')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        first_name = options['first_name']
        last_name = options['last_name']
        email = options['email']

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            if options['update']:
                user = User.objects.get(username=username)
                user.set_password(password)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.is_admin = True
                user.is_staff = True
                user.is_superuser = True
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Admin user "{username}" updated successfully!')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'User "{username}" already exists! Use --update to update it.')
                )
                return
        else:
            # Create admin user
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
                is_admin=True,
                is_staff=True,
                is_superuser=True
            )

            self.stdout.write(
                self.style.SUCCESS(f'Admin user "{username}" created successfully!')
            )
        self.stdout.write(f'Username: {username}')
        self.stdout.write(f'Password: {password}')
        self.stdout.write(f'Full Name: {first_name} {last_name}')
        self.stdout.write(f'Email: {email}')
        self.stdout.write('\nYou can now log in with these credentials.')
