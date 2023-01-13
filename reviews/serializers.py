from rest_framework import serializers
from .models import Review


class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def get_image(self, data):
        request = self.context.get("request")
        if data.image:
            return request.build_absolute_uri(data.image.url)
        return None

    def create(self, validated_data):
        return Review.objects.create_review(**validated_data)
