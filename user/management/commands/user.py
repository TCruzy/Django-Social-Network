from django.core.management.base import BaseCommand, CommandError
from user.models import User


class Command(BaseCommand):
    help = 'Get user object and print full name'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int)
        parser.add_argument('--email', '-e', action='store_true', help='Get user email')
        parser.add_argument('--fullname', '-f', action='store_true', help='Get user full name')

    def handle(self, *args, **options):
        user_id = options['user_id']
        try:
            user = User.objects.get(id=user_id)
            if options['email']:
                self.stdout.write(self.style.SUCCESS('%s' % user.email))
            elif options['fullname']:
                self.stdout.write(self.style.SUCCESS('%s %s' % (user.first_name, user.last_name)))
            else:
                self.stdout.write(self.style.SUCCESS('%s' % user.first_name))
        except User.DoesNotExist:
            raise CommandError('User does not exist')