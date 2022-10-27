# from django.test import TestCase
import pytest

from django.contrib.auth.models import User

from api.models import Task, Image

# Check write data to Driver model
@pytest.mark.django_db
@pytest.mark.parametrize('title', 'description', 'user', 'executors', 'images',\
    [('task1', 'description1', 'user1', 'user2', 'img1'),
     ('task2', 'description2', 'user2', 'user1', 'img1'),
    #  ('task3', 'description3', 'user3', ['user1', 'user2']),
    #  ('task4', 'description4', 'user4', ['user1', 'user2', 'user3'])
     ])

def test_task_create(title, description, user, executors, images):
    if User.objects.filter(username=user).exists():
        user=User.objects.get(username=user)
    else:
        user=User.objects.get(username=user)
    if User.objects.filter(username=executors).exists():
        executors=User.objects.get(username=executors)
    else:
        executors=User.objects.create(username=executors)
    if Image.objects.filter(image=images).exists():
        images=Image.objects.get(image=images)
    else:
        images=Image.objects.create(image=images)

    task = Task.objects.create(
        title=title,
        description=description,
        user=user,
        executors=executors,
        images=images)

    assert task.title == title
    assert task.description == description
    assert task.user == user
    assert task.executors == executors
    assert task.images == images
    assert Task.objects.count() == 1
