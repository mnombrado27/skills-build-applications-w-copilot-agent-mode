from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Clear existing data (delete individually for Djongo compatibility)
        for model in [Leaderboard, Activity, Workout, User, Team]:
            for obj in model.objects.all():
                if getattr(obj, 'id', None) is not None:
                    obj.delete()

        # Create teams
        marvel = Team.objects.create(name='Marvel', description='Marvel superheroes')
        dc = Team.objects.create(name='DC', description='DC superheroes')

        # Create users
        tony = User.objects.create(name='Tony Stark', email='tony@marvel.com', team=marvel)
        steve = User.objects.create(name='Steve Rogers', email='steve@marvel.com', team=marvel)
        bruce = User.objects.create(name='Bruce Wayne', email='bruce@dc.com', team=dc)
        clark = User.objects.create(name='Clark Kent', email='clark@dc.com', team=dc)

        # Create activities
        Activity.objects.create(user=tony, type='Run', duration=30, date=timezone.now().date())
        Activity.objects.create(user=steve, type='Swim', duration=45, date=timezone.now().date())
        Activity.objects.create(user=bruce, type='Cycle', duration=60, date=timezone.now().date())
        Activity.objects.create(user=clark, type='Fly', duration=120, date=timezone.now().date())

        # Create workouts
        workout1 = Workout.objects.create(name='Pushups', description='Upper body strength')
        workout2 = Workout.objects.create(name='Sprints', description='Speed training')
        workout1.suggested_for.set([tony, bruce])
        workout2.suggested_for.set([steve, clark])

        # Create leaderboard
        Leaderboard.objects.create(user=tony, score=100, rank=1)
        Leaderboard.objects.create(user=steve, score=90, rank=2)
        Leaderboard.objects.create(user=bruce, score=80, rank=3)
        Leaderboard.objects.create(user=clark, score=70, rank=4)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data!'))
