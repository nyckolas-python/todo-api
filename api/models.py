from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

# Create your models here.
class Image(models.Model):

    image = models.ImageField(
        upload_to="",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg', 'tiff', 'gif'])]
        ) 

class Task(models.Model):
    NEW = 'N'
    PROGRESS = 'P'
    COMPLETED = 'C'
    STATUS_CHOICES = [
        (NEW, '💡 New task'),
        (PROGRESS, '🚀 In progress'),
        (COMPLETED, '✔️ Completed'),
    ]

    title = models.CharField(max_length=255, null=True)
    description =models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=2, choices=STATUS_CHOICES, default=NEW, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tasks", null=True,
        verbose_name="Task manager:"
        )
    executors = models.ManyToManyField(
        User, verbose_name="Responsible for completing:")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    task_images = models.ManyToManyField(
        Image, verbose_name="Attached images:", blank=True)
    
    def _get_status_display(self):
        status_display = [_ for s,_ in self.status_choices if s==self.status]
        return f"{status_display[0]}"
    
    def _get_user_display(self):
        pass
    
    def _get_task_image_urls(self):
        pass
    
    def save(self, *args, **kwargs) -> None:
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return f"{self.user}: {self.id}.{self.title}"
    