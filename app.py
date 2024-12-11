from flask import Flask, request, render_template
from database import collection
from helper import generation


app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def chat():
  if request.method == 'GET':
    chat = list(collection.find({}, {'prompt':1, 'response':1, 'formatted_time':1, 'tokens':1}))
    return render_template('index.html', chat=chat)
  else:
    prompt = request.form['prompt']
    time, response, token_usage = generation(prompt)
    if not time:
      chat = list(collection.find({}, {'prompt':1, 'response':1, 'formatted_time':1, 'tokens':1}))
      return render_template('index.html', chat=chat, error=response)
    # Create a new message to display (including the user's input)
    chat = list(collection.find({}, {'prompt':1, 'response':1, 'formatted_time':1, 'tokens':1}))
    # Render the template with the updated chat history
    return render_template('index.html', chat=chat)


if __name__=='__main__':
  app.run()
