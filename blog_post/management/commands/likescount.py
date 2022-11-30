from django.core.management.base import BaseCommand, CommandError
from blog_post.models import PostLikes


class Command(BaseCommand):
    help = 'Likes count on post by given post id'

    def add_arguments(self, parser):
        parser.add_argument('post_id', type=int, nargs='?', default=None)

    def handle(self, *args, **options):
        post_id = options['post_id']
        if post_id:
            try:
                post_likes = PostLikes.objects.filter(post__id=post_id)
                self.stdout.write(self.style.SUCCESS(f'Post: {post_likes[0].post}'))
                self.stdout.write(self.style.SUCCESS(f'Likes count on post by given post id: {post_likes.count()}'))
            except IndexError:
                raise CommandError('Post does not exist')
        else:
            post_likes = PostLikes.objects.all()
            self.stdout.write(self.style.SUCCESS(f'Likes count on post by given post id: {post_likes.count()}'))