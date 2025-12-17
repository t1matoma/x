from rest_framework import serializers

from ..models.message import Message


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(read_only=True)
    sender_username = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'sender_username', 'content', 'chat', 'timestamp']

class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['content', 'chat']
        read_only_fields = ['id', 'timestamp']
        
class MessageEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['content']
        read_only_fields = ['id', 'timestamp']