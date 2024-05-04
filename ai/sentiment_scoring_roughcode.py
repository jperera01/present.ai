import base64
import requests

import os
import re  #to parse gpt response string

import openai
from nltk.sentiment import SentimentIntensityAnalyzer

#------------------------------------------------------
#CONST DATA & PATHS
#------------------------------------------------------
#environment variables
api_key = 'API KEY GOES HERE'
os.environ['OPENAI_API_KEY'] = api_key

#video frames folder
folder_path = ".\\snapshots"
files = sorted([f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.png'))])
analyses = [] #list to store analyses

#------------------------------------------------------
#FUNCTIONS
#------------------------------------------------------
#encode images to base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

#split gpt message using regex patterns
def parse_message(message):
    pattern = r'(?<=\.)\s+(?=In the second)' #preserves parsing phrase
    parts = re.split(pattern, message)
    description1 = parts[0].strip() if len(parts) > 1 else None
    description2 = parts[1].strip() if len(parts) > 1 else None    
    return description1, description2

#stores evaluation in dictionary format
def store_analysis(description1, description2, confidence_change, confidence_current, evaluation_statement):
    is_unconfident = confidence_change < -20 or confidence_current < 50

    return {
        'description1': description1,
        'description2': description2,
        'evaluation_statement': evaluation_statement,
        'confidence_change': confidence_change,
        'current_confidence': confidence_current,
        'is_unconfident': is_unconfident
    }

#------------------------------------------------------
#IMAGE PROCESSING
#process consecutive pairs of images
#------------------------------------------------------
client = openai.OpenAI() #client instance

#headers for HTTP request
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

for i in range(5):#len(files) - 1):
    image1_path = os.path.join(folder_path, files[i])
    image2_path = os.path.join(folder_path, files[i + 1])
    image1_base64 = encode_image(image1_path)
    image2_base64 = encode_image(image2_path)

    #payload with base64 images
    payload = {
        "model": "gpt-4-turbo", #"gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Use two sentences to describe difference or similarity in demeanor of the person in these two photos. Sentence 1 should start with, \'in the first photo\' and sentence 2 should start with \'in the second photo\'",
                    },
                    {
                      "type": "image_url",
                      "image_url": {
                        "url": f"data:image/jpeg;base64,{image1_base64}"
                      }
                    },
                    {
                      "type": "image_url",
                      "image_url": {
                        "url": f"data:image/jpeg;base64,{image2_base64}"
                      }
                    }
                ],
            }
        ],
        "max_tokens": 300
    }

    # Send request
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    all_text = response.json().get('choices')[0].get('message').get('content')
    
    # Parse response
    description1, description2 = parse_message(all_text)

    #------------------------------------------------------
    #SENTIMENT ANALYSIS
    #------------------------------------------------------
    sia = SentimentIntensityAnalyzer()     #initialize sentiment intensity analyzer

    confidence_score1 = (sia.polarity_scores(description1)['compound'] + 1) * 50
    confidence_score2 = (sia.polarity_scores(description2)['compound'] + 1) * 50
    confidence_difference = confidence_score2 - confidence_score1
    confidence_change = round((confidence_difference / confidence_score1) * 100, 2)
    current_confidence = round(confidence_score2, 2)

    #create evaluation statement
    evaluation_statement = f"The person in these photos has experienced a {confidence_change}% change in confidence for a final score of {current_confidence}%."
    
    #store the analysis
    analysis = store_analysis(description1, description2, confidence_change, current_confidence, evaluation_statement)
    print(analysis, "\n")
    analyses.append(analysis)

# print(analyses)