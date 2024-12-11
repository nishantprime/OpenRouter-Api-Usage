import requests
import json
import os
from database import collection
from datetime import datetime, timedelta


openrouter_api = os.getenv('openrouter_api')


def format_time(unixtime):
  dt_object = datetime.fromtimestamp(unixtime)
  # Add 5 hours and 30 minutes (for IST value)
  new_dt_object = dt_object + timedelta(hours=5, minutes=30)
  return new_dt_object.strftime("%Y-%m-%d %H:%M:%S")

def generation(prompt):
  try:
    response = requests.post(
      url="https://openrouter.ai/api/v1/chat/completions",
      headers={"Authorization": f"Bearer {openrouter_api}"},
      data=json.dumps({
        "model": "meta-llama/llama-3.2-3b-instruct:free",
        "messages": [
          {
            "role": "user",
            "content": prompt
          }]}))
    result = json.loads(response.text)
    output = result['choices'][0]
    
    collection.insert_one({
      'prompt': prompt,
      'id': result['id'],
      'model': result['model'],
      'created': result['created'],
      'formatted_time': format_time(result['created']),
      'response': output['message']['content'],
      'finish_reason': output['finish_reason'],
      'refusal': output['message']['refusal'],
      'tokens': str(result['usage'])
    })

    user_output = [format_time(result['created']), output['message']['content'], str(result['usage'])]
    return user_output
  except Exception as e:
    return [None,str(e),None]

def get_messages():
  chat = list(collection.find({}, {'prompt': 1, 'response': 1, 'formatted_time': 1, 'tokens': 1}).sort('created',-1).limit(20))
  chat.reverse()
  return chat




