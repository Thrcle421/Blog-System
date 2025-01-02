from django.core.management.base import BaseCommand
from blog.models import BlogCategory


class Command(BaseCommand):
    help = 'Initialize blog categories'

    def handle(self, *args, **kwargs):
        categories = ['Technology', 'Life', 'Programming', 'Other']
        for category in categories:
            BlogCategory.objects.get_or_create(name=category)
        self.stdout.write(self.style.SUCCESS(
            'Successfully initialized categories'))
