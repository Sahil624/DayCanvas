
from gettext import translation
from rest_framework import serializers
from .models import Journal, JournalImages
from django.db import transaction

class JournalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalImages
        fields = ['id', 'file']

class JournalSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )
    journal_images = JournalImageSerializer(many=True, read_only=True, source='images')

    class Meta:
        model = Journal
        fields = ['id', 'user', 'date', 'updated_on', 'created_on', 'journal', 'images', 'journal_images']
        read_only_fields = ['user', 'updated_on', 'created_on']

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        validated_data['user'] = self.context['request'].user
        
        try:
            with transaction.atomic():
                journal = Journal.objects.create(**validated_data)
                for image in images:
                    JournalImages.objects.create(journal=journal, file=image)
                return journal
        except Exception as e:
            raise serializers.ValidationError(f"Failed to create journal: {str(e)}")

    def update(self, instance, validated_data):
        images = validated_data.pop('images', [])
        
        try:
            with transaction.atomic():
                # Update journal fields
                instance.journal = validated_data.get('journal', instance.journal)
                instance.save()
                
                # Add new images
                for image in images:
                    JournalImages.objects.create(journal=instance, file=image)
                
                return instance
        except Exception as e:
            raise serializers.ValidationError(f"Failed to update journal: {str(e)}")
