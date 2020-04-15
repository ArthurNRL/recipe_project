from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=100)
    ingredients = models.TextField()
    instructions = models.TextField()
    datePosted = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete = models.DO_NOTHING)

    def ingredientList(self):
        a = self.ingredients.replace(" ","")
        a = a.replace("[","")
        a = a.replace("'", "")
        a = a.replace("]", "")
        return a.split(",")

    def instructionList(self):
        a = self.instructions.replace(" ", "")
        a = a.replace("[", "")
        a = a.replace("'", "")
        a = a.replace("]", "")
        return a.split(",")

    def __str__(self):
        return self.title