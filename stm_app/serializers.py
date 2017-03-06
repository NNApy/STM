from django.contrib.auth.models import User
from stm_app.models import Tasks, Projects
from rest_framework import serializers


class TasksSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tasks
        fields = ('url', 'title', 'description', 'due_date', 'id_project')


class ProjectsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Projects
        fields = ('url', 'project_name', 'description')


class UsersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'first_name', 'last_name', 'is_superuser', 'last_login')
