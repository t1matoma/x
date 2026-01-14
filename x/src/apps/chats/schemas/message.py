from rest_framework import serializers

from ..models.message import Message


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(read_only=True)
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    file_url = serializers.URLField(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'sender_username', 'content', 'file_url', 'chat', 'timestamp']

class MessageCreateSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False, allow_null=True)
    class Meta:
        model = Message
        fields = ['content', 'file']
        read_only_fields = ['id', 'timestamp']
        
class MessageEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['content']
        read_only_fields = ['id', 'timestamp']