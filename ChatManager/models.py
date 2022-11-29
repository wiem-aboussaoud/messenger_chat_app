from django.db import models
from MessengerApp.settings import *


class ChatGroup(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class UserChatGroup(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="chat_groups")
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + "_" + self.group.name


class Message(models.Model):
    text = models.TextField()
    sent_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="message_sent", related_query_name="sender")
    sent_to = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="message_received", related_query_name="receiver")
    to_group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, null=True, blank=True, related_name="related_messages")
    is_seen = models.BooleanField(default=False)

    seen_at = models.DateTimeField(null=True, blank=True)

    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text