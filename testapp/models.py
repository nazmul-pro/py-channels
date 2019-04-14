# Create your models here.
from django.db import models
# from django.template.defaultfilters import slugify
# from django.contrib.auth.models import User


class AppUser(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=75)
    phone = models.TextField()
    password = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    # @models.permalink
    # def get_absolute_url(self):
    #     return ('blog_post_detail', (),
    #             {
    #                'slug': self.slug,
    #             })

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.title)
    #     super(Post, self).save(*args, **kwargs)

    # class Meta:
    #     ordering = ['created_on']

    #     def __unicode__(self):
    #         return self.title
class AppUserInfo(models.Model):
    app_user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    permissions = models.TextField()
    avatar = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

class AppUserToken(models.Model):
    app_user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    jwt = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

class LiveDiscussion(models.Model):
    app_user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    text = models.TextField()
    love = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)