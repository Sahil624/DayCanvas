import json
import logging
import os
from typing import Dict
from models.ai_story.prompt import get_user_prompt
from models.ai_story.tags import extract_tags
from models.models import Frame, StoryLine
from story.models import Journal
import anthropic
from django.db import transaction


def parse_and_save_story(response_text: str, journal: Journal) -> StoryLine:
    """
    Parse the API response and save it to StoryLine and Frame models.
    
    Args:
        response_text (str): The XML response from the Anthropic API
        journal (Journal): The associated Journal instance
        
    Returns:
        StoryLine: The created StoryLine instance
    """
    try:
        # Ensure response text is string
        if not isinstance(response_text, str):
            raise ValueError(f"Expected string response, got {type(response_text)}")
            
        tags = [
            'title',
            'summary',
            'analysis_and_planning',
            'frames'
        ]

        tags = extract_tags(response_text, tags)

        logging.debug(f"Parent Tags \n {json.dumps(tags, indent=4)}")
        
        # Direct access to title and summary based on the provided XML structure
        title = tags['title']
        summary = tags['summary']
        
        if title is None or summary is None:
            raise ValueError("Missing required title or summary elements")
            
        with transaction.atomic():
            # Create StoryLine
            storyline = StoryLine.objects.create(
                user=journal.user,
                journal=journal,
                response=response_text,
                title=title.strip(),
                summary=summary.strip()
            )
            
            # Process frames - direct access to frame elements
            frames = extract_tags(tags['frames'], ['frame'])['frame']
            if not frames:
                raise ValueError("No frames found in response")
                
            for frame_elem in frames:
                frame_tags = extract_tags(frame_elem, ['story', 'image_gen_prompt'])
                story = frame_tags.get('story')
                image_prompt = frame_tags.get('image_gen_prompt')
                
                if story is not None and image_prompt is not None:
                    Frame.objects.create(
                        storyline=storyline,
                        story=story.strip(),
                        image_gen_prompt=image_prompt.strip()
                    )
            
            return storyline

    except Exception as e:
        raise e
        raise ValueError(f"Error processing response: {str(e)}")


def journal_to_story(journal: Journal) -> StoryLine:
    client = anthropic.Anthropic(
        api_key=os.getenv('ANTHROPIC_KEY'),
    )

    user_prompt = get_user_prompt(journal)

    print(user_prompt)

    message = client.messages.create(
        # model="claude-3-haiku-20240307",
        model="claude-3-5-sonnet-20241022",
        max_tokens=2595,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text":  user_prompt
                    }
                ]
            }
        ]
    )
    print(message.content[0].text)

    storyline = parse_and_save_story(message.content[0].text, journal)

    return storyline
