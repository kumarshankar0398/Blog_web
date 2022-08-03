from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.template.defaultfilters import slugify

from .managers import UserManager

USER_TYPE = (
    ("Publisher", "Publisher"),
    ("Reader", "Reader")
)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=40, unique=True)
    password = models.CharField(max_length=200)
    date_joined = models.DateTimeField(verbose_name='datejoined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last_login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    ifLogged = models.BooleanField(default=False)
    profile = models.ImageField(null=True, blank=True, upload_to='profile1', default=None)
    UserType = models.CharField(max_length=20, choices=USER_TYPE, default="Reader")

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


# class Post(models.Model):
#     def user_directory_path(instance, filename):
#         # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#         return 'user_{0}/{1}'.format('aaa', filename)
#
#     title = models.CharField(max_length=200, unique=True)
#     author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='blog_posts')
#     updated_on = models.DateTimeField(auto_now=True)
#     content = models.TextField()
#     created_on = models.DateTimeField(auto_now_add=True)
#     status = models.IntegerField(choices=STATUS, default=0)
#     postImg = models.FileField(null=True, upload_to=user_directory_path)
#
#     def save(self, *args, **kwargs):
#         self.url = slugify(self.title)
#         super(Post, self).save(*args, **kwargs)
#
#     class Meta:
#         ordering = ['-created_on']
#
#     def __str__(self):
#         return self.title



class Post(models.Model):
    def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'user_{0}/{1}'.format('aaa', filename)

    title = models.CharField(max_length=200, unique=True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    postImg = models.FileField(null=True, upload_to=user_directory_path)
    # likes = models.IntegerField(default=0)
    # dislikes = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.url = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)


VOTE = (
    (1, "Like"),
    (0, "Dislike")
)


class Like_Dislike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    vote = models.IntegerField(choices=VOTE, null=True, default="")
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user) + ':' + str(self.post) + ':' + str(self.vote)

    class Meta:
        unique_together = ("user", "post", "vote")


# class Preference(models.Model):
#     user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     value = models.IntegerField()
#     date = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return str(self.user) + ':' + str(self.post) + ':' + str(self.value)
#
#     class Meta:
#         unique_together = ("user", "post", "value")
