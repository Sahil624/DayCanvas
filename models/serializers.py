from rest_framework import serializers
from .models import StoryLine, Frame

class FrameSerializer(serializers.ModelSerializer):
    """
    Serializer for Frame model with all its fields
    """
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        if hasattr(obj, 'frameimages'):
            return obj.frameimages.image.url
        return None

    class Meta:
        model = Frame
        fields = ['id', 'story', 'image_gen_prompt', 'image']
        read_only_fields = ('image', )


class StoryLineSerializer(serializers.ModelSerializer):
    """
    Serializer for StoryLine model with nested frames
    """
    frames = FrameSerializer(source='frame_set', many=True, read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = StoryLine
        fields = [
            'id', 
            'user',
            'user_name',
            'journal',
            'response',
            'title',
            'summary',
            'frames'
        ]
        read_only_fields = ['user', 'frames']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def to_representation(self, instance):
        """
        Customize the representation to include frame count
        """
        representation = super().to_representation(instance)
        representation['frame_count'] = len(representation['frames'])
        return representation
