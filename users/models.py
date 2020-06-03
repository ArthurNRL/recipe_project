from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from os import remove
from django.utils import timezone
from django.urls import reverse
from recipeSite.models import Post
import io
from django.core.files.storage import default_storage as storage

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

        img_read = storage.open(self.image.name, 'r')
        img = Image.open(img_read)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            in_mem_file = io.BytesIO()
            img.save(in_mem_file, format='JPEG')
            img_write = storage.open(self.image.name, 'w+')
            img_write.write(in_mem_file.getvalue())
            img_write.close()

        img_read.close()

    def __str__(self):
        return f'{self.user.username}`s Profile'
