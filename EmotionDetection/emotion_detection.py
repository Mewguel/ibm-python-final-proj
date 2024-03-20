''' Contains the emotion analyzer using watson sentiment api
'''
import json
import requests


def emotion_detector(text_to_analyze):
    '''
    This function performs emotion detection on the given text using the Watson Emotion Detection API.
    Args:
        text_to_analyze (str): The text to be analyzed for emotions. 
    Returns:
        str: The text attribute of the response object received from the Emotion Detection API.
    
    '''
    url = ('https://sn-watson-emotion.labs.skills.network/'
           'v1/watson.runtime.nlp.v1/NlpService/EmotionPredict')
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    myobj = { "raw_document": { "text": text_to_analyze } }

    try:
        response = requests.post(url, json=myobj, headers=headers, timeout=10)

        emotion_dict = {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

        if response.status_code == 200:
            formatted_response = json.loads(response.text)
            emotion_dict = formatted_response['emotionPredictions'][0]['emotion']

            dominant_emotion = ''
            dominant_score = 0
            for emotion, score in emotion_dict.items():
                if score > dominant_score:
                    dominant_score = score
                    dominant_emotion = emotion

            emotion_dict['dominant_emotion'] = dominant_emotion
            return emotion_dict

        elif response.status_code == 400:
            return emotion_dict

        elif response.status_code == 500:
            print("Something went wrong")
            return emotion_dict
                  
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == '__main__':
    print(emotion_detector("I am so happy I am doing this."))