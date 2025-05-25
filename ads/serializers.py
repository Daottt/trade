from rest_framework import serializers
from ads import models

class AdSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)

    class Meta:
        model = models.Ad
        fields = ("id", "user", "title", "description", "image_url", "category", "condition", "created_at")

class ProposalSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ExchangeProposal
        fields = ("id", "ad_sender", "ad_receiver", "comment", "status", "created_at")

    def validate(self, data):
        user = self.context['request'].user
        if not user:
            raise serializers.ValidationError("User not found in request context.")
        if data['ad_sender'].user == data['ad_receiver'].user:
            raise serializers.ValidationError("Sender and receiver cannot be the same user.")
        if data['ad_sender'].user != user:
            raise serializers.ValidationError("Sender cannot be other user.")
        return data
