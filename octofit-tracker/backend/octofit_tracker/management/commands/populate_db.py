from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models


from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB directly for index creation
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        db.users.create_index([('email', 1)], unique=True)

        # Clear collections
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Teams
        marvel_team = {'name': 'Team Marvel', 'members': []}
        dc_team = {'name': 'Team DC', 'members': []}
        marvel_team_id = db.teams.insert_one(marvel_team).inserted_id
        dc_team_id = db.teams.insert_one(dc_team).inserted_id

        # Users
        users = [
            {'name': 'Spider-Man', 'email': 'spiderman@marvel.com', 'team_id': marvel_team_id},
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team_id': marvel_team_id},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team_id': dc_team_id},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team_id': dc_team_id},
        ]
        user_ids = db.users.insert_many(users).inserted_ids

        # Update teams with members
        db.teams.update_one({'_id': marvel_team_id}, {'$set': {'members': user_ids[:2]}})
        db.teams.update_one({'_id': dc_team_id}, {'$set': {'members': user_ids[2:]}})

        # Activities
        activities = [
            {'user_id': user_ids[0], 'activity': 'Running', 'duration': 30},
            {'user_id': user_ids[1], 'activity': 'Cycling', 'duration': 45},
            {'user_id': user_ids[2], 'activity': 'Swimming', 'duration': 25},
            {'user_id': user_ids[3], 'activity': 'Yoga', 'duration': 40},
        ]
        db.activities.insert_many(activities)

        # Leaderboard
        leaderboard = [
            {'user_id': user_ids[0], 'score': 100},
            {'user_id': user_ids[1], 'score': 90},
            {'user_id': user_ids[2], 'score': 95},
            {'user_id': user_ids[3], 'score': 85},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Workouts
        workouts = [
            {'user_id': user_ids[0], 'workout': 'Pushups', 'reps': 50},
            {'user_id': user_ids[1], 'workout': 'Situps', 'reps': 60},
            {'user_id': user_ids[2], 'workout': 'Squats', 'reps': 70},
            {'user_id': user_ids[3], 'workout': 'Plank', 'duration': 120},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
