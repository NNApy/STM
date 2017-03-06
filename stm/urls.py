from django.conf.urls import url, include
from stm_app.views import start, control_redirect, general, user_logout, users, projects, add_edit_user, \
    reset_pass, change_pass, delete_user, add_edit_project, del_project, add_edit_task, del_task, tasks
from rest_framework import routers
from stm_app import views

router = routers.DefaultRouter()

router.register(r'tasks', views.TasksViewSet)
router.register(r'projects', views.ProjectsViewSet)
router.register(r'users', views.UsersViewSet)


urlpatterns = [
    url(r'^accounts/', include('django.contrib.auth.urls'), name='accounts'),
    url(r'^control', control_redirect, name='control_redirect'),
    url(r'^$', start, name='start'),
    url(r'^general/', general, name='general'),
    url(r'^logout', user_logout, name='logout'),
    url(r'^users/', users, name='users'),
    url(r'^add_edit_user/', add_edit_user, name='add_edit_user'),
    url(r'^reset_pass/', reset_pass, name='reset_pass'),
    url(r'^change_pass/', change_pass, name='change_pass'),
    url(r'^delete_user/', delete_user, name='delete_user'),
    url(r'^projects/', projects, name='projects'),
    url(r'^add_edit_project/', add_edit_project, name='add_edit_project'),
    url(r'^del_project/', del_project, name='del_project'),
    url(r'^add_edit_task/', add_edit_task, name='add_edit_task'),
    url(r'^del_task/', del_task, name='del_task'),
    url(r'^tasks/', tasks, name='tasks'),

    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]
