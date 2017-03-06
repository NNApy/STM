# -*- coding: utf-8 -*-
import kronos
from django.core.mail import send_mail
from models import Tasks
from datetime import datetime


@kronos.register('0 14 * * *')
def daily():
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


@kronos.register('0 * * * *')
def hourly():
    tasks = Tasks.objects.all()
    for task in tasks:
        if (task.due_date.date() - datetime.today().date()).days == 1:
            mail_to = []
            for user in task.task_users.values():
                if not user['is_superuser']:
                    mail_to.append(user['email'])
                subject = u'Hello! You have failed task in the project {}'.format(task.id_project.project_name)
                mail_body = u'Task:\n\n{}\n\n{}\n\nUntil the ' \
                            u'end of execution of less than 1 day.'.format(task.title,
                                                                               task.description,
                                                                               (task.due_date.date() - datetime.today().date()).days
                                                                               )
                mail_from = u'stm@emerline.com'
            send_mail(subject, mail_body, mail_from, mail_to)