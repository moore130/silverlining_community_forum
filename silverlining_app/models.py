from django.db import models
import re

class UserManager(models.Manager):
    def validator(self,postData):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['password']) < 5:
            errors['password'] = 'Your password must be at least 5 characters.'
        if len(postData['user_name']) < 2:
            errors['user_name'] = 'Your username must be at least 2 characters.'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Invalid email address. Please enter a valid email.'
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = 'Passwords do not match. Please try again.'
        return errors

class User(models.Model):
    user_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects=UserManager()


class Todo(models.Model):
    title = models.CharField(max_length=250)
    poster = models.ForeignKey(User, related_name='user_title', on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title