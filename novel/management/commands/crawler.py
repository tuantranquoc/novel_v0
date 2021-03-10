from django.core.management.base import BaseCommand
from django.utils import timezone
from novel import crawler


class Command(BaseCommand):
    help = 'run crawler'

    def handle(self, *args, **kwargs):
        crawler.get_url_from_main_page("href")
        # crawler.craw_01("href")
        # crawler.get_url_from_main_page_01()
        self.stdout.write("done crawling")
