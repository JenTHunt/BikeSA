from django.db import models

class UserManager(models.Manager):
    def validate(self, postData):
        errors = {}
        if len(postData["first_name"]) < 2:
            errors["first_name"] = "First name must be longer than 2 characters."
        if len(postData["last_name"]) < 2:
            errors["last_name"] = "Last name must be longer than 2 characters."
        if len(postData["password"]) < 2:
            errors["password"] = "Password must be longer than 2 characters."
        if postData["password"] != postData["confirm_password"]:
            errors["password_confirmation"] = "Password and confirm password do not match."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Ride(models.Model):
    date = models.DateField()
    trail = models.CharField(max_length=45)
    distance = models.CharField(max_length=25)
    time = models.TimeField()
    notes = models.CharField(max_length=255)
    rider = models.ForeignKey(User, related_name="user_ride", on_delete=models.CASCADE)

class Post(models.Model):
    message = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name='user_posts', on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='liked_posts')
    #post_comments

class Comment(models.Model):
    comment = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='post_comments', on_delete=models.CASCADE)