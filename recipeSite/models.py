from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# TODO add post images

class Post(models.Model):
    title = models.CharField(max_length=100)
    datePosted = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete = models.DO_NOTHING)

    def get_absolute_url(self):
        return reverse('postDetail', kwargs={'pk': self.pk})

    def ingredientList(self):
        ingredients = Ingredients.objects.filter(post=self)
        for ingredient in ingredients:
            yield ingredient.ingredients

    def instructionList(self):
        instructions = Instructions.objects.filter(post=self)
        for instruction in instructions:
            yield instruction.instructions

    def __str__(self):
        return self.title

class Ingredients(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    ingredients = models.TextField()


class Instructions(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    instructions = models.TextField()


