from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from stm_app.models import Projects, Tasks

from rest_framework import viewsets
from stm_app.serializers import TasksSerializer, ProjectsSerializer, UsersSerializer

default_pass = 123456


def start(request):
    """
    function on the first run
    """
    if User.objects.filter(is_superuser=1).count() == 0:
        if request.method == "GET":
            return render(request, 'create_manager.html')
        else:
            try:
                User.objects.create_user(first_name=request.POST.get('fname'),
                                         last_name=request.POST.get('lname'),
                                         email=request.POST.get('email'),
                                         username=request.POST.get('username'),
                                         password=request.POST.get('password'),
                                         is_superuser=1
                                         )
                user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
                request.session['access_key'] = 'manager'
                login(request, user)
                return redirect(general)
            except Exception as error:
                messages.warning(request, error)
                return redirect(start)
    else:
        return redirect(control_redirect)


@login_required()
def control_redirect(request):
    if request.user.check_password(default_pass):
        return redirect(change_pass)
    else:
        if request.user.is_superuser:
            return redirect(general)
        else:
            return redirect(tasks)


@login_required()
def general(request):
    """
    tasks list for managers
    """
    if request.user.is_superuser:
        if request.method == 'GET':
            tasks_list = Tasks.objects.all()
            context = {'tasks': tasks_list.order_by('due_date')}
            return render(request, 'tasks.html', context)
    else:
        return redirect(control_redirect)


@login_required()
def users(request):
    """
    users list
    """
    if request.user.is_superuser:
        if request.method == 'GET':
            context = {'users': User.objects.all()}
            return render(request, 'users.html', context)
    else:
        return redirect(control_redirect)


@login_required()
def add_edit_user(request):
    """
    add or edit user
    """
    if request.user.is_superuser:
        if request.method == 'GET':
            if request.GET.get('u_id'):
                context = {'user_data': User.objects.filter(id=request.GET.get('u_id')).get()}
                return render(request, 'add_edit_user.html', context)
            else:
                return render(request, 'add_edit_user.html')
        else:
            position = 0
            if request.POST.get('position') == 'manager':
                position = 1
            if request.POST.get('u_id'):
                try:
                    User.objects.filter(id=request.POST.get('u_id')).update(
                        first_name=request.POST.get('fname'),
                        last_name=request.POST.get('lname'),
                        email=request.POST.get('email'),
                        username=request.POST.get('username'),
                        is_superuser=position
                    )
                    messages.success(request, 'User {} was successfully changed'.format(request.POST.get('username')))
                    return redirect(users)
                except Exception as error:
                    messages.warning(request, error)
                    return redirect(start)
            else:
                try:
                    User.objects.create_user(first_name=request.POST.get('fname'),
                                             last_name=request.POST.get('lname'),
                                             email=request.POST.get('email'),
                                             username=request.POST.get('username'),
                                             password=default_pass,
                                             is_superuser=position
                                             )
                    messages.success(request, 'User {} created successfully'.format(request.POST.get('username')))
                    return redirect(users)
                except Exception as error:
                    messages.warning(request, error)
                    return redirect(start)
    else:
        return redirect(control_redirect)


@login_required()
def reset_pass(request):
    """
    Reser user password to the default password
    """
    if request.user.is_superuser:
        try:
            user = User.objects.get(id=request.GET.get('u_id'))
            user.set_password(default_pass)
            user.save()
            messages.success(request,
                             'The password for this user has been successfully changed to the standard password ('
                             '123456)')
            return redirect('/add_edit_user/?id={}'.format(request.GET.get('u_id')))
        except Exception as error:
            messages.warning(request, error)
            return redirect('/add_edit_user/?id={}'.format(request.GET.get('u_id')))
    else:
        return redirect(control_redirect)


@login_required()
def change_pass(request):
    """
    Changing the default password
    """
    if request.method == 'GET':
        return render(request, 'change_pass.html')
    else:
        try:
            if request.user.check_password(request.POST.get('password')):
                messages.warning(request, 'Password must be different from the standard')
                return redirect(change_pass)
            request.user.set_password(request.POST.get('password'))
            request.user.save()
            user = authenticate(username=request.user.username, password=request.POST.get('password'))
            login(request, user)
            messages.success(request, 'The password was successfully changed')
            return redirect(control_redirect)
        except Exception as error:
            messages.warning(request, error)
            return redirect(control_redirect)


@login_required()
def user_logout(request):
    """
    user logout
    """
    if request.session.has_key('access_key'):
        del request.session['access_key']
    logout(request)
    return redirect('login')


@login_required()
def delete_user(request):
    """
    delete some user
    """
    if request.user.is_superuser:
        try:
            user = User.objects.get(id=request.POST.get('u_id'))
            user.delete()
            messages.success(request, "The user was deleted")
            return redirect(users)
        except User.DoesNotExist:
            messages.warning(request, "User does not exist")
            return redirect(users)
        except Exception as error:
            messages.warning(request, error)
            return redirect(users)
    else:
        return redirect('/')


@login_required()
def projects(request):
    """
    projects list
    """
    if request.user.is_superuser:
        if request.method == 'GET':
            context = {'projects': Projects.objects.all(),
                       'users': User.objects.all()
                       }
            return render(request, 'projects.html', context)
    else:
        return redirect(control_redirect)


@login_required()
def add_edit_project(request):
    """
    add or edit some project
    """
    if request.user.is_superuser:
        if request.method == 'GET':
            if request.GET.get('p_id'):
                select_user_is = []
                for user in User.objects.filter(projects__id=request.GET.get('p_id')):
                    select_user_is.append(user.id)
                context = {'project_data': Projects.objects.filter(id=request.GET.get('p_id')).get(),
                           'select_user_is': select_user_is,
                           'all_users': User.objects.all()
                           }
                return render(request, 'add_edit_project.html', context)
            else:
                context = {'all_users': User.objects.all(),
                           }
                return render(request, 'add_edit_project.html', context)
        else:
            if request.POST.get('p_id'):
                try:
                    Projects.objects.filter(id=request.POST.get('p_id')).update(
                        project_name=request.POST.get('project_name'),
                        description=request.POST.get('description'),
                    )
                    project = Projects.objects.filter(id=request.POST.get('p_id')).get()

                    project.users.clear()

                    for user_id in request.POST.getlist('users'):
                        user = User.objects.filter(id=user_id).get()
                        project.users.add(user)

                    messages.success(request,
                                     'Project {} was successfully changed'.format(request.POST.get('project_name')))
                    return redirect(projects)
                except Exception as error:
                    messages.warning(request, error)
                    return redirect(projects)
            else:
                try:
                    project = Projects.objects.create(project_name=request.POST.get('project_name'),
                                                      description=request.POST.get('description'),
                                                      )

                    for user_id in request.POST.getlist('users'):
                        user = User.objects.filter(id=user_id).get()
                        project.users.add(user)
                    messages.success(request,
                                     'Project {} created successfully'.format(request.POST.get('project_name')))
                    return redirect(projects)
                except Exception as error:
                    messages.warning(request, error)
                    return redirect(projects)
    else:
        return redirect(control_redirect)


@login_required()
def del_project(request):
    """
    delete some project
    """
    if request.user.is_superuser:
        if request.POST.get('p_id'):
            try:
                project = Projects.objects.filter(id=request.POST.get('p_id')).get()
                project_name = project.project_name
                project_tasks = Tasks.objects.filter(id_project=request.POST.get('p_id'))
                tasks_list = []
                for task in project_tasks:
                    tasks_list.append(task.title)
                project.users.clear()
                project_tasks.delete()
                project.delete()
                messages.success(request,
                                 'Project {} was successfully deleted with all tasks'.format(project_name))
                messages.warning(request,
                                 'Tasks was deleted: {}'.format(', '.join(tasks_list)))
                return redirect(projects)
            except Exception as error:
                messages.warning(request, error)
                return redirect(projects)
        else:
            return redirect(projects)
    else:
        return redirect(control_redirect)


@login_required()
def add_edit_task(request):
    """
    add or edit some task
    """
    if request.user.is_superuser:
        if request.method == 'GET':
            if request.GET.get('t_id'):

                task = Tasks.objects.filter(id=request.GET.get('t_id')).get()
                project = Projects.objects.filter(id=task.id_project_id).get()
                project_users = User.objects.filter(projects__id=task.id_project_id)

                select_user_is = []
                for user in User.objects.filter(tasks__id=task.id):
                    select_user_is.append(user.id)

                context = {'project_users': project_users, 'task_data': task, 'project': project,
                           'select_user_is': select_user_is
                           }
                if not select_user_is:
                    messages.warning(request, 'Please select the task managers and developers')

                return render(request, 'add_edit_task.html', context)

            context = {'projects': Projects.objects.all()
                       }
            return render(request, 'add_edit_task.html', context)
        elif request.POST.get('project'):
            task = Tasks.objects.create(id_project_id=request.POST.get('project'),
                                        title=request.POST.get('title'),
                                        description=request.POST.get('description'),
                                        due_date=request.POST.get('due_date')
                                        )
            return redirect('/add_edit_task/?t_id={}'.format(task.id))

        else:
            if request.POST.get('t_id'):
                try:
                    Tasks.objects.filter(id=request.POST.get('t_id')).update(title=request.POST.get('title'),
                                                                             description=request.POST.get(
                                                                                 'description'),
                                                                             due_date=request.POST.get('due_date')
                                                                             )
                    task = Tasks.objects.filter(id=request.POST.get('t_id')).get()
                    task.task_users.clear()

                    for user_id in request.POST.getlist('users'):
                        user = User.objects.filter(id=user_id).get()
                        task.task_users.add(user)

                    messages.success(request,
                                     'Task for project {} was successfully changed'.format(
                                         task.id_project.project_name))
                    return redirect(general)
                except Exception as error:
                    messages.warning(request, error)
                    return redirect(general)
    else:
        return redirect(control_redirect)


@login_required()
def del_task(request):
    """
    delete some task
    """
    if request.user.is_superuser:
        if request.POST.get('t_id'):
            try:
                task = Tasks.objects.filter(id=request.POST.get('t_id')).get()
                task_name = task.title
                task.task_users.clear()
                task.delete()
                messages.success(request,
                                 'Task {} was successfully deleted'.format(task_name))
                return redirect(general)
            except Exception as error:
                messages.warning(request, error)
                return redirect(general)
        else:
            return redirect(projects)
    else:
        return redirect(control_redirect)


@login_required()
def tasks(request):
    """
    tasks list for developers
    """
    if request.method == 'GET':
        tasks_list = Tasks.objects.all()
        context = {'tasks': tasks_list.order_by('due_date')}
        return render(request, 'user_tasks.html', context)


# ------------------------------------------------------------------------------------
# -------------------------------------- API -----------------------------------------
# ------------------------------------------------------------------------------------

class TasksViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tasks to be viewed or edited.
    """
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer


class ProjectsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows projects to be viewed or edited.
    """
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer


class UsersViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UsersSerializer
