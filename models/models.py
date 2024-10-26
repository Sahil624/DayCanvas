from django.db import models
from django.contrib.auth import get_user_model

from story.models import Journal


class StoryLine(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    journal = models.OneToOneField(Journal, on_delete=models.CASCADE)

    response = models.TextField()

    title = models.CharField(max_length=500)
    summary = models.TextField()


class Frame(models.Model):
    storyline = models.ForeignKey(StoryLine, on_delete=models.CASCADE)
    story = models.TextField()
    image_gen_prompt = models.TextField()


class ImageGenBatch(models.Model):
    storyline = models.ForeignKey(StoryLine, on_delete=models.CASCADE)
    completed_count = models.PositiveSmallIntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def is_complete(batch_id):
        batch = ImageGenBatch.objects.only('completed_count', 'storyline').get(id=batch_id)
        return batch.completed_count == batch.storyline.frame_set.count()
    

class FrameImages(models.Model):
    frame = models.OneToOneField(Frame, on_delete=models.CASCADE)
    batch = models.ForeignKey(ImageGenBatch, on_delete=models.CASCADE)
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
