from djongo import models

class Team(models.Model):
    name = models.CharField(max_length=100)
    members = models.ArrayReferenceField(to='User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    team = models.ForeignKey(Team, related_name='users', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Activity(models.Model):
    user = models.ForeignKey(User, related_name='activities', on_delete=models.CASCADE)
    activity = models.CharField(max_length=100)
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.user.name} - {self.activity}"

class Leaderboard(models.Model):
    user = models.ForeignKey(User, related_name='leaderboard', on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return f"{self.user.name} - {self.score}"

class Workout(models.Model):
    user = models.ForeignKey(User, related_name='workouts', on_delete=models.CASCADE)
    workout = models.CharField(max_length=100)
    reps = models.IntegerField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.name} - {self.workout}"
