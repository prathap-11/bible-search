import random
from django.core.management.base import BaseCommand
from myapp.models import BibleDb, DailyVerse
from django.utils import timezone

class Command(BaseCommand):
    help = 'Generate a daily Bible verse'

    def handle(self, *args, **kwargs):
        # Get all verses from the BibleDb
        all_verses = list(BibleDb.objects.all())
        
        if not all_verses:
            self.stdout.write(self.style.ERROR('No verses found in the database.'))
            return
        
        # Select a random verse
        selected_verse = random.choice(all_verses)

        # Save or update the daily verse
        DailyVerse.objects.update_or_create(
            date=timezone.now().date(),
            defaults={'verse': selected_verse}
        )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully generated daily verse: {selected_verse}'))