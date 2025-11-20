from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Deleting old data...'))
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        Leaderboard.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Creating teams...'))
        marvel = Team.objects.create(name='Marvel', description='Marvel superheroes')
        dc = Team.objects.create(name='DC', description='DC superheroes')

        self.stdout.write(self.style.SUCCESS('Creating users...'))
        users = [
            User.objects.create(email='tony@stark.com', name='Tony Stark', team=marvel, is_superhero=True),
            User.objects.create(email='steve@rogers.com', name='Steve Rogers', team=marvel, is_superhero=True),
            User.objects.create(email='bruce@wayne.com', name='Bruce Wayne', team=dc, is_superhero=True),
            User.objects.create(email='clark@kent.com', name='Clark Kent', team=dc, is_superhero=True),
        ]

        self.stdout.write(self.style.SUCCESS('Creating activities...'))
        Activity.objects.create(user=users[0], type='Iron Suit Training', duration=60, date=timezone.now())
        Activity.objects.create(user=users[1], type='Shield Throwing', duration=45, date=timezone.now())
        Activity.objects.create(user=users[2], type='Detective Work', duration=90, date=timezone.now())
        Activity.objects.create(user=users[3], type='Flight', duration=120, date=timezone.now())

        self.stdout.write(self.style.SUCCESS('Creating workouts...'))
        w1 = Workout.objects.create(name='Super Strength', description='Strength workout for heroes', suggested_for=[marvel.name, dc.name])
        w2 = Workout.objects.create(name='Agility Training', description='Agility and speed', suggested_for=[marvel.name])

        self.stdout.write(self.style.SUCCESS('Creating leaderboard...'))
        Leaderboard.objects.create(team=marvel, points=200)
        Leaderboard.objects.create(team=dc, points=180)

        self.stdout.write(self.style.SUCCESS('Ensuring unique index on email...'))
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        db.user.create_index('email', unique=True)
        self.stdout.write(self.style.SUCCESS('Database populated with test data!'))
