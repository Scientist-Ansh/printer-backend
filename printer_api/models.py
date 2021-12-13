from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.


class Department(models.Model):
    def __str__(self):
        return self.name

    id = models.CharField(max_length=10, primary_key=True)
    password = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    page_limit = models.IntegerField(default=100)


class User(models.Model):
    def __str__(self):
        return self.username

    def is_password_correct(self, password):
        return self.password == password

    name = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    department = models.ForeignKey(Department, on_delete=CASCADE)
    pages_printed = models.IntegerField(default=0)

# department means program
# username is users email
