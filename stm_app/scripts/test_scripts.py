# -*- coding: utf-8 -*-

#python manage.py runscript test_scr

from stm_app.models import Projects, Tasks
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.contrib.auth.models import User


def run():
    tasks = Tasks.objects.all()
    for task in tasks:
        mail_to = []
        for user in task.task_users.values():
            if not user['is_superuser']:
                mail_to.append(user['email'])
            subject = u'Hello! You have failed task in the project {}'.format(task.id_project.project_name)
            mail_body = u'Task:\n\n{}\n\n{}\n\nUntil the ' \
                        u'end of execution of less than {} day(s).'.format(task.title,
                                                                           task.description,
                                                                           (task.due_date.date() - datetime.today().date()).days
                                                                           )
            mail_from = u'stm@emerline.com'
        send_mail(subject, mail_body, mail_from, mail_to)