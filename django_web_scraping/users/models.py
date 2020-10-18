from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.files.storage import default_storage as storage
from scraping.models import News
from scrap.models import Scrap


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')


    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)
        #img = Image.open(storage.open(self.image.path))

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        if img.height > 180 or img.width > 180:
            output_size = (180, 180)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Contact(models.Model):
    user = models.ForeignKey(Profile, related_name='topics', on_delete=models.CASCADE)
    topic = models.ForeignKey(Scrap, related_name='users', on_delete=models.CASCADE)

    def __str__(self):
        return '{} follows {}'.format(self.user, self.topic)


  