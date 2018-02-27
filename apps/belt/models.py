from __future__ import unicode_literals
from django.db import models
import re, bcrypt

class BlogManager(models.Manager):
    def simple_validator(self, postData):
        errors = {}
        if len(postData['fname']) < 2:
            errors["fname"] = "First name shouldn't be empty."
        if len(postData['lname']) < 2:
            errors["lname"] = "Last name shouldn't be empty."
        if len(postData['username']) < 2:
            errors['username'] = "User name to short."
        if len(postData['pw']) < 8:
            errors['pw'] = "Passwords must be longer."
        elif postData['pw'] != postData['cpw']:
            errors['match'] = "Your password didn't match up."
        if User.objects.filter(username = postData['username']):
            errors['username'] = "Invalid username."
        if len(postData['hire_date']) < 1:
            errors['hire'] = "Please fill out Hired form."
        if not errors:
            pass1 = bcrypt.hashpw(postData['pw'].encode(), bcrypt.gensalt())
            User.objects.create(first_name=postData['fname'], last_name=postData['lname'], username=postData['username'],password=pass1,hire_date=postData['hire_date'])
        return errors

    def login_validator(self, POSTS):
        errors = {}
        if len(POSTS['username']) < 1 or len(POSTS['pw']) < 1:
            errors['empty'] = "Fill out Login"
        if not User.objects.filter(username = POSTS['username']):
            errors['username'] = "Wrong Username/Password"
        else:
            passs = User.objects.get(username=POSTS['username'])
            if not bcrypt.checkpw(POSTS['pw'].encode(), passs.password.encode()):
                errors['passs'] = "Wrong Username/Password"
        if not errors:
            id = User.objects.get(username=POSTS['username']).id
            name = User.objects.get(username=POSTS['username']).first_name
            print id, name
        return errors

    def wish_validator(self, POSTS):
        errors = {}
        if len(POSTS['item']) < 3:
            errors['empty'] = "Invalid Item/Product"
        if Wishlist.objects.filter(name = POSTS['item']):
            errors['here'] = "Item/Product exsists already"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    hire_date = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = BlogManager() 

class Wishlist(models.Model):
    name = models.CharField(max_length=255)
    uploader = models.ForeignKey(User, related_name="Users_item")
    liked_users = models.ManyToManyField(User, related_name="liked_items")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = BlogManager() 