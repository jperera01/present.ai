import re
from app.ai.model import client
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import time

sia = SentimentIntensityAnalyzer()

def create_analysis(description1, description2, confidence_change, confidence_current):
    is_unconfident = confidence_change < -20 or confidence_current < 70

    return {
        'description1': description1,
        'description2': description2,
        'confidence_change': confidence_change,
        'current_confidence': confidence_current,
        'is_unconfident': is_unconfident
    }

def parse_message(message):
    pattern = r'(?<=\.)\s+(?=In the second)'
    parts = re.split(pattern, message)
    description1 = parts[0].strip() if len(parts) > 1 else None
    description2 = parts[1].strip() if len(parts) > 1 else None    
    return description1, description2

def get_sentiment(base64Image1, base64Image2):
    # start_time = time.time()
    completion = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system","content": "Use two sentences to describe difference or similarity in demeanor of the person in these two photos. Sentence 1 should start with, 'in the first photo' and sentence 2 should start with 'in the second photo'"},
            {
                "role": "user", 
                "content": [
                    {
                        "type": 'text',
                        "text": "The first image is this."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"{base64Image1}"
                        }
                    },
                    {
                        "type": 'text',
                        "text": "The second image is this."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"{base64Image2}"
                        }
                    },
                ]
            }
        ]
    )

    # end_time = time.time()

    # execution_time = end_time - start_time
    # print(f"Execution time: {execution_time:.5f} seconds")

    # start_time = time.time()
    response_text = completion.choices[0].message.content
    description1, description2 = parse_message(response_text)
    confidence_score1 = (sia.polarity_scores(description1)['compound'] + 1) * 50
    confidence_score2 = (sia.polarity_scores(description2)['compound'] + 1) * 50
    confidence_difference = confidence_score2 - confidence_score1
    confidence_change = round((confidence_difference / confidence_score1) * 100, 2)
    current_confidence = round(confidence_score2, 2)
    # end_time = time.time()

    # execution_time = end_time - start_time
    # print(f"Execution time 2: {execution_time:.5f} seconds")

    return create_analysis(description1, description2, confidence_change, current_confidence)