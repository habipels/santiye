from django.db import models
from users.models import CustomUser

class Group(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(CustomUser, related_name='chat_groups')
    image = models.FileField(upload_to='chatgrup_resimleri/', verbose_name="Profile", blank=True, null=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='chat_messages')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='messages')
    file = models.FileField(upload_to='uploads/', blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"
