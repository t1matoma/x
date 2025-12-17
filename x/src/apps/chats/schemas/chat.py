from rest_framework import serializers

from ..models.chat import Chat


class ChatSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Chat
        fields = ['id', 'members', 'timestamp']

class ChatCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['members']
        read_only_fields = ['id', 'timestamp']

    def validate_members(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("A chat must have at least two members.")
        return value