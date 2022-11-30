from django.core.management.base import BaseCommand, CommandError
from blog_post.models import Post, PostLikes
from user.models import User


class Command(BaseCommand):
    help = 'Create like for post by user'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int)
        parser.add_argument('post_id', type=int)

    def handle(self, *args, **options):
        user_id = options['user_id']
        post_id = options['post_id']
        try:
            post = Post.objects.get(id=post_id)
            user = User.objects.get(id=user_id)
            post_likes = PostLikes.objects.create(user=user, post=post)
            post_likes.save()
            self.stdout.write(self.style.SUCCESS('Successfully created like for post by user'))
            self.stdout.write(self.style.SUCCESS(f'{post_likes}'))
        except Post.DoesNotExist:
            raise CommandError('Post does not exist')
        except User.DoesNotExist:
            raise CommandError('User does not exist')