from rest_framework import serializers
from .models import Message
from ProfileManager.models import UserProfile
from django.contrib.sites.shortcuts import get_current_site
from django.core.validators import ValidationError


class InboxSerializer(serializers.ModelSerializer):

    inbox_name = serializers.SerializerMethodField()
    inbox_image = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'text', "sent_by", "user", "inbox_name", "inbox_image", "is_seen", "sent_at", "seen_at"]

        extra_kwargs = {
            'sent_by': {'read_only': True},
        }

    def get_user(self, message_obj):
        if message_obj.group:
            return None
        else:
            if self.context["request"].user != message_obj.sent_by:
                return message_obj.sent_by.id
            else:
                return message_obj.sent_to.id

    def get_inbox_name(self, message_obj):
        if message_obj.group:
            return message_obj.group.name
        else:
            if self.context["request"].user != message_obj.sent_by:
                return message_obj.sent_by.last_name + " " + message_obj.sent_by.first_name
            else:
                return message_obj.sent_to.last_name + " " + message_obj.sent_to.first_name

    def get_inbox_image(self, message_obj):
        if message_obj.group:
            return None
        else:
            current_site = get_current_site(self.context["request"])
            if self.context["request"].user != message_obj.sent_by:
                if message_obj.sent_by.image:
                    return current_site.domain + message_obj.sent_by.image.url
                else:
                    return None
            else:
                if message_obj.sent_to.image:
                    return current_site.domain + message_obj.sent_to.image.url
                else:
                    return None


class MessageSerializer(serializers.ModelSerializer):


    class Meta:
        model = Message
        fields = ['id', 'text', "sent_by", "is_seen", "sent_at", "seen_at"]

        extra_kwargs = {
            'sent_by': {'read_only': True},
        }

    def create(self, validated_data):
        if not "sent_to" in validated_data or not validated_data["sent_to"]:
            return ValidationError({"sent_to": "This field is required."})
        else:
            try:
                receiver = UserProfile.objects.get(id=validated_data["sent_to"])
                validated_data["sent_to"] = receiver
            except:
                return ValidationError({"Error": "Unknown user receiver."})
            message_obj = Message.objects.create(
                            sent_by=self.context["request"].user, **validated_data
                         )

        return message_obj

