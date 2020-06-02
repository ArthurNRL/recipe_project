from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from os import remove
from django.utils import timezone
from django.urls import reverse
from recipeSite.models import Post

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='logo.png', upload_to='profile_pics')
    favoritePosts = models.ManyToManyField(Post, blank=True, null=True)
    dateJoined = models.DateTimeField(default = timezone.now)

    def defaultImage(self):
        if not self.image == 'logo.png':
            remove(self.image.path)
            self.image = 'logo.png'
            self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            img.thumbnail((300, 300))
            img.save(self.image.path)

    def __str__(self):
        return f'{self.user.username}`s Profile'
