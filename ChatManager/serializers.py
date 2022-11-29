from rest_framework import serializers
from .models import Message
from ProfileManager.models import UserProfile
from django.contrib.sites.shortcuts import get_current_site
from django.core.validators import ValidationError

class MessageSerializer(serializers.ModelSerializer):

    sender_full_name = serializers.SerializerMethodField()
    sender_image = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'text', "sent_by", "sender_full_name", "sender_image", "is_seen", "sent_at", "seen_at"]

        extra_kwargs = {
            'sent_by': {'read_only': True},
        }

    def get_sender_full_name(self, obj):
        print("obj :", obj)
        return obj.sent_by.last_name + " " + obj.sent_by.first_name

    def get_sender_image(self, message_obj):
        if message_obj.sent_by.image:
            current_site = get_current_site(self.context["request"])

            return current_site.domain + message_obj.sent_by.image.url
        else:
            return None

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