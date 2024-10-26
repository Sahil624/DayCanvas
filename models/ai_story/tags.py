
import re
from typing import Dict, List, Union


def extract_tags(response: str, response_tags: List[str]) -> Dict[str, Union[str, List[str]]]:
    """
    Extract content from tags in the response text. If multiple instances of a tag are found,
    returns a list of values for that tag.

    Args:
        response (str): The response text containing tags
        response_tags (List[str]): List of tag names to extract

    Returns:
        Dict[str, Union[str, List[str]]]: Dictionary with tag names as keys and either
        single strings or lists of strings as values
    """
    # Initialize the result dictionary
    result = {}

    # Extract content for each tag
    for tag in response_tags:
        pattern = f"<{tag}>(.*?)</{tag}>"
        matches = re.finditer(pattern, response, re.DOTALL | re.IGNORECASE)
        
        # Collect all matches for this tag
        values = []
        for match in matches:
            # Strip leading/trailing whitespace and remove extra newlines
            content = re.sub(r'\n+', '\n', match.group(1).strip())
            values.append(content)

        # If we found any matches, add them to the result
        if values:
            # If only one value found, store it as a string
            # If multiple values found, store as a list
            result[tag] = values[0] if len(values) == 1 else values

    return result

if __name__ == '__main__':
    tags = [
        'title',
        'summary',
        'analysis_and_planning',
        'frames'
    ]

    content = ''

    with open('response_sample.txt') as f:
        content = f.read()
    
    tags = extract_tags(content, tags)

    print("TAGS")
    print(tags)

    tags = extract_tags(tags['frames'], ['frame'])

    for frame in tags['frame']:
        print("--------- FRAME ------------")
        tag = extract_tags(frame, ['story', 'image_gen_prompt'])
        print(tag)
