from rest_framework import serializers
from rest_framework.exceptions import APIException


from api.models import Task


def is_task_owner(request) -> bool:
    """Is the user a task owner?"""
    task_id = request.data.get("id", None)
    if task_id:
        task = Task.objects.get(id=task_id)
        if task.user != request.user:
            return False

    return True

def is_task_executor(request) -> bool:
    """Is the user a task executor?"""
    # print(request.parser_context.get('kwargs').get('pk'))
    task_id = request.parser_context.get('kwargs', None).get('pk', None)
    if task_id:
        task = Task.objects.get(id=task_id)
        if request.user not in task.executors.all():
            return False

    return True
