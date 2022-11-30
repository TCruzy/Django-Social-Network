from django.core.management.base import BaseCommand, CommandError
from user.models import User
from blog_post.models import Post


class Command(BaseCommand):
    help = 'List all posts of a user'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int)

    def handle(self, *args, **options):
        user_id = options['user_id']
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise CommandError('User with id "%s" does not exist' % user_id)
        posts = Post.objects.filter(author_id=user)

        posts_list = []
        for post in posts:
            posts_list.append(post.title)

        if len(posts_list) == 0:
            self.stdout.write(self.style.SUCCESS('User %s has no posts' % user))
        else:
            self.stdout.write(self.style.SUCCESS('User %s has the following posts: %s' % (user, posts_list)))
