# notifications/serializers.py
from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.StringRelatedField()
    recipient = serializers.StringRelatedField()
    target = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'actor', 'verb', 'target', 'unread', 'timestamp']

    def get_target(self, obj):
        if obj.target is None:
            return None
        return {
            'type': obj.target_content_type.model,
            'id': obj.target_object_id,
            'repr': str(obj.target)
        }
