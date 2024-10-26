from argparse import Action
from itertools import count
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import action

from models.ai_images.story_to_image import story_to_image
from models.ai_story.ai_story import journal_to_story
from models.models import Frame, ImageGenBatch, StoryLine
from models.serializers import FrameSerializer, StoryLineSerializer
from story.models import Journal


# class StoryLineViewSet(viewsets.ModelViewSet):
#     serializer_class = StoryLineSerializer
#     permission_classes = [IsAuthenticated]
    
#     def get_queryset(self):
#         return StoryLine.objects.filter(
#             user=self.request.user
#         ).annotate(
#             frame_count=count('frame')
#         ).select_related('user', 'journal')

#     @Action(detail=False, methods=['GET'])
#     def by_journal(self, request):
#         """Get story for a specific journal"""
#         journal_id = request.query_params.get('journal_id')
#         if not journal_id:
#             return Response(
#                 {"error": "journal_id is required"}, 
#                 status=status.HTTP_400_BAD_REQUEST
#             )
            
#         story = self.get_queryset().filter(journal_id=journal_id).first()
#         if not story:
#             return Response(
#                 {"error": "Story not found"}, 
#                 status=status.HTTP_404_NOT_FOUND
#             )
            
#         serializer = self.get_serializer(story)
#         return Response(serializer.data)


# class FrameViewSet(viewsets.ModelViewSet):
#     serializer_class = FrameSerializer
#     permission_classes = [IsAuthenticated]
    
#     def get_queryset(self):
#         return Frame.objects.filter(
#             storyline__user=self.request.user
#         ).select_related('storyline')
        
#     @action(detail=False, methods=['GET'])
#     def by_story(self, request):
#         """Get all frames for a specific story"""
#         story_id = request.query_params.get('story_id')
#         if not story_id:
#             return Response(
#                 {"error": "story_id is required"}, 
#                 status=status.HTTP_400_BAD_REQUEST
#             )
            
#         frames = self.get_queryset().filter(storyline_id=story_id)
#         serializer = self.get_serializer(frames, many=True)
#         return Response(serializer.data)


class GenerateStory(APIView):

    def post(self, request, journal_id):
        try:
            journal = Journal.objects.get(id=journal_id)
            story = journal_to_story(journal)

            serial = StoryLineSerializer(story)
            return Response(serial.data)
        except Journal.DoesNotExist:
            raise NotFound("Journal Not Found")
        
class BatchStatus(APIView):

    def get(self, request, batch_id):
        try:
            batch = ImageGenBatch.objects.get(id=batch_id)
            
            return Response({
                "batch_id": batch.id,
                "completed_count": batch.completed_count,
                "is_completed": ImageGenBatch.is_complete(batch_id)
            })
        except ImageGenBatch.DoesNotExist:
            raise NotFound("Batch not found!")

        
class GenerateEpisode(APIView):

    def get(self, request, story_id):
        story = StoryLine.objects.get(id=story_id)
        serial = StoryLineSerializer(story)
        return Response(serial.data)

    def post(self, request, story_id):
        try:
            story = StoryLine.objects.get(id=story_id)

            batch = story_to_image(story)
            return Response({
                "batch_id": batch.id,
                "completed_count": batch.completed_count
            })

        except StoryLine.DoesNotExist:
            raise NotFound("Storyline not found")