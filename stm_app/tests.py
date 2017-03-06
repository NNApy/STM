from django.test import TestCase
from django.contrib.auth.models import User
from stm_app.models import Projects, Tasks
from datetime import datetime


class CreateFirstManager(TestCase):
    def test_ok_create_first_manager(self):
        """Check the first time the system is started"""
        data = {'fname': 'nikita', 'lname': 'narkevitch', 'email': 'nnarkevitch@emerline.com',
                'username': 'nnarkevitch',
                'password': '123456'
                }
        response = self.client.post('', data)
        manager = User.objects.last()
        self.assertEquals(manager.first_name, data['fname'])
        self.assertEquals(manager.last_name, data['lname'])
        self.assertEquals(manager.email, data['email'])
        self.assertEquals(manager.username, data['username'])
        self.assertTrue(manager.password)
        self.assertEquals(manager.is_superuser, 1)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/general/')


class STMTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_manager', email='test_manager@emerline.com',
                                             password='123456', is_superuser=1)

    def test_ok_create_new_user(self):
        """Create new user"""
        self.client.login(username='test_manager', password='123456')
        users = User.objects.all()
        data = {'fname': 'nikita', 'lname': 'narkevitch', 'email': 'nnarkevitch@emerline.com',
                'username': 'test_user', 'position': 'manager'
                }
        response = self.client.post('/add_edit_user/', data)
        manager = users.last()
        self.assertEquals(manager.first_name, data['fname'])
        self.assertEquals(manager.last_name, data['lname'])
        self.assertEquals(manager.email, data['email'])
        self.assertEquals(manager.username, data['username'])
        self.assertEquals(manager.is_superuser, 1)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/users/')

    def test_ok_delete_new_user(self):
        """Delete new user"""
        self.client.login(username='test_manager', password='123456')
        data = {'fname': 'nikita', 'lname': 'narkevitch', 'email': 'nnarkevitch@emerline.com',
                'username': 'test_user', 'position': 'manager'
                }
        self.client.post('/add_edit_user/', data)
        users = User.objects.all()
        self.assertEquals(users.count(), 2)
        response = self.client.post('/delete_user/', {'u_id': users.last().id})
        self.assertEquals(users.count(), 1)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/users/')

    def test_ok_edit_new_user(self):
        """Edit new user"""
        self.client.login(username='test_manager', password='123456')
        data = {'fname': 'nikita', 'lname': 'narkevitch', 'email': 'nnarkevitch@emerline.com',
                'username': 'test_user', 'position': 'manager'
                }
        self.client.post('/add_edit_user/', data)
        users = User.objects.all()
        self.assertEquals(users.count(), 2)
        new_data = {'u_id': users.last().id, 'fname': 'new_fname', 'lname': 'new_lname',
                    'email': 'new_email@emerline.com',
                    'username': 'new_username', 'position': 'developer'
                    }
        response = self.client.post('/add_edit_user/', new_data)
        self.assertEquals(users.last().first_name, new_data['fname'])
        self.assertEquals(users.last().last_name, new_data['lname'])
        self.assertEquals(users.last().email, new_data['email'])
        self.assertEquals(users.last().username, new_data['username'])
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/users/')

    def test_ok_change_pass(self):
        """Change password"""
        self.client.login(username='test_manager', password='123456')
        data = {'fname': 'nikita', 'lname': 'narkevitch', 'email': 'nnarkevitch@emerline.com',
                'username': 'test_user', 'position': 'manager'
                }
        self.client.post('/add_edit_user/', data)
        users = User.objects.all()
        self.assertEquals(users.count(), 2)
        response = self.client.post('/change_pass/', {'password': 123456})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/change_pass/')
        response = self.client.post('/change_pass/', {'password': 1234567})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/control')

    def test_ok_create_project(self):
        """Create new project"""
        self.client.login(username='test_manager', password='123456')
        projects = Projects.objects.all()
        data = {'project_name': 'prodject', 'description': 'description',
                'users': [1]
                }
        response = self.client.post('/add_edit_project/', data)
        project = projects.last()
        project_users = projects.get().users.count()
        self.assertEquals(project_users, 1)
        self.assertEquals(project.project_name, data['project_name'])
        self.assertEquals(project.description, data['description'])
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/projects/')

    def test_ok_edit_new_project(self):
        """Edit new project"""
        self.client.login(username='test_manager', password='123456')
        data = {'project_name': 'project', 'description': 'description'
                }
        self.client.post('/add_edit_project/', data)
        projects = Projects.objects.all()
        self.assertEquals(projects.count(), 1)
        new_data = {'p_id': projects.last().id, 'project_name': 'new_project_name', 'description': 'new_description'
                    }
        response = self.client.post('/add_edit_project/', new_data)
        self.assertEquals(projects.last().project_name, new_data['project_name'])
        self.assertEquals(projects.last().description, new_data['description'])
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/projects/')

    def test_ok_delete_new_project(self):
        """Delete new project"""
        self.client.login(username='test_manager', password='123456')
        data = {'project_name': 'project', 'description': 'description'
                }
        self.client.post('/add_edit_project/', data)
        projects = Projects.objects.all()
        self.assertEquals(projects.count(), 1)
        response = self.client.post('/del_project/', {'p_id': projects.last().id})
        self.assertEquals(projects.count(), 0)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/projects/')

    def test_ok_create_task(self):
        """Create new task"""
        self.client.login(username='test_manager', password='123456')
        tasks = Tasks.objects.all()
        data = {'project': 1, 'title': 'task_title', 'description': 'task_description',
                'due_date': '2017-02-26 00:00:00'
                }
        response = self.client.post('/add_edit_task/', data)
        task = tasks.last()
        self.assertEquals(task.id_project_id, data['project'])
        self.assertEquals(task.title, data['title'])
        self.assertEquals(task.description, data['description'])
        self.assertEquals(task.due_date, task.due_date)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/add_edit_task/?t_id={}'.format(task.id))

    def test_ok_delete_new_task(self):
        """Delete new task"""
        self.client.login(username='test_manager', password='123456')
        tasks = Tasks.objects.all()
        data = {'project': 1, 'title': 'task_title', 'description': 'task_description',
                'due_date': '2017-02-26 00:00:00'
                }
        self.client.post('/add_edit_task/', data)
        task = tasks.last()
        self.assertEquals(tasks.count(), 1)
        response = self.client.post('/del_task/', {'t_id': task.id})
        self.assertEquals(tasks.count(), 0)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/general/')

    def test_ok_edit_new_task(self):
        """Edit new task"""
        self.client.login(username='test_manager', password='123456')
        tasks = Tasks.objects.all()
        data = {'project': 1, 'title': 'task_title', 'description': 'task_description',
                'due_date': datetime.now()
                }
        self.client.post('/add_edit_task/', data)
        self.assertEquals(tasks.count(), 1)
        new_data = {'t_id': tasks.last().id, 'title': 'new_task_title', 'description': 'new_task_description',
                    'due_date': datetime.now(), 'users': [1]
                    }
        response = self.client.post('/add_edit_task/', new_data)
        task = tasks.last()
        self.assertEquals(task.title, new_data['title'])
        self.assertEquals(task.description, new_data['description'])
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/general/')
