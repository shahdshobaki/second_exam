from django.db import models
import re
import bcrypt
from django.core.exceptions import ObjectDoesNotExist

class UserManager(models.Manager):
    def basic_register(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First Name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last Name should be at least 2 characters"

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if User.objects.filter(email=postData['email']).exists():
            errors['email_used'] = "Email already in use!"

        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData['password'] != postData['confirm_pw']:
            errors["confirm_pw"] = "Passwords do not match"

        return errors

    def basic_login(self, postData):
        errors = {}
        try:
            user = User.objects.get(email=postData['email'])
        except ObjectDoesNotExist:
            errors['email'] = "Email not found."
            return errors

        if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
            errors['password'] = "Invalid password."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=225)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Idea(models.Model):
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ideas")

def check_email(POST):
    return User.objects.filter(email=POST['email'])

def create_user(POST):
    password = POST['password']
    return User.objects.create(
        first_name=POST['first_name'],
        last_name=POST['last_name'],
        email=POST['email'],
        password=bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode(),
    )

def create_idea(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    Idea.objects.create(
        description=request.POST['description'],
        user=user
    )

def get_ideas(user_id):
    return Idea.objects.filter(user_id=user_id)

def delete_idea(POST):
    idea = Idea.objects.get(id=POST['id_idea'])
    idea.delete()

def update_idea(POST, idea_id, user_id):
    idea = Idea.objects.get(id=idea_id, user_id=user_id)
    idea.description = POST['description']
    idea.save()
