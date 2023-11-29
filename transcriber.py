import os
from dotenv import load_dotenv
import openai
from openai.cli._tools import migrate

from openai import OpenAI
import re
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
# prompt = 'please summarize the transcript below into bullet points \n---\n"{0}"'.format(transcript)


client = openai.OpenAI(
    api_key=os.getenv("api_key")
)
def get_video_transcript(video_id):
    try:
        response = YouTubeTranscriptApi.get_transcript(video_id)
        transcripts = [item['text'] for item in response]
        transcript_string = '  '.join(transcripts)
        return transcript_string
    except TranscriptsDisabled:
        print("TranscriptsDisabled: Transcription not available")
        raise TranscriptsDisabled("Transcription not available")
    except Exception as e:
        print("Error:", str(e))
        raise e



def summarize_transcript(transcript):
    load_dotenv()
    prompt = 'please summarize the transcript below into bullet points \n---\n"{0}"'.format(transcript)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        max_tokens=1000,
        temperature=0.5,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
