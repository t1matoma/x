from rest_framework import serializers
from ..models.chat import Chat


class ChatSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    members_usernames = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ['id', 'members', 'members_usernames', 'timestamp']

    def get_members_usernames(self, obj):
        return [member.username for member in obj.members.all()]

class ChatCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['members']
        read_only_fields = ['id', 'timestamp']

    def validate_members(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("A chat must have at least two members.")
        return value