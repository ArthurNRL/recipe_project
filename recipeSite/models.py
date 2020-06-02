from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
# TODO add time
# TODO add portion
# todo add grupos alimentares
# todo instrumentos


class Post(models.Model):
    title = models.CharField(max_length=60)
    description = models.CharField(max_length=150)
    picture = models.ImageField(default='logo.png', upload_to='post_pics')
    datePosted = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete = models.DO_NOTHING)
    original = models.ForeignKey('self', on_delete=models.SET_NULL, default='', null=True)

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


