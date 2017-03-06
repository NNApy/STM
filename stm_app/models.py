from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


class Projects(models.Model):
    class Meta:
        db_table = "Projects"

    users = models.ManyToManyField(User)
    project_name=models.CharField(max_length=35)
    description=models.CharField(max_length=100)



class Tasks(models.Model):
    class Meta:
        db_table = "Tasks"

    id_project=models.ForeignKey(Projects)
    title=models.CharField(max_length=50)
    description=models.CharField(max_length=250)
    due_date=models.DateTimeField(null=False,default=datetime.now)
    task_users = models.ManyToManyField(User)
    # manager=models.CharField(max_length=20, null=False)
    # developer=models.CharField(max_length=20, null=False)

# class Person(models.Model):
#     name = models.CharField(max_length=200)
#     age = models.IntegerField(null=True)
#     height = models.IntegerField(null=True)
#
# class Project(models.Model):
#     title = models.CharField(max_length=100, default='')
#     isbn = models.CharField(max_length=20, default='')
#     persons = models.ManyToManyField(Person)




# class Split(models.Model):
#     split = models.OneToOneField(User)





