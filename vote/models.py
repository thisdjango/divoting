from django.contrib.auth.models import User
from django.db import models


class Voting(models.Model):
    from_date = models.DateTimeField()
    till_date = models.DateTimeField()
    descr = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)


class Variant(models.Model):
    voting = models.ForeignKey(to=Voting, on_delete=models.CASCADE)
    text = models.CharField(max_length=10)


class Vote(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    variant = models.ForeignKey(to=Variant, on_delete=models.CASCADE)
    date = models.DateTimeField()


