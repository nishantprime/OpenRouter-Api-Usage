from flask import Flask, request, render_template
from helper import generation, get_messages


app = Flask(__name__)



@app.route('/', methods = ['GET', 'POST'])
def chat():
  if request.method == 'GET':
    chat = get_messages()
    
    return render_template('index.html', chat=chat)
  else:
    prompt = request.form['prompt']
    time, response, token_usage = generation(prompt)
    if not time:
      chat = get_messages()
      return render_template('index.html', chat=chat, error=response)
    # Create a new message to display (including the user's input)
    chat = get_messages()
    # Render the template with the updated chat history
    return render_template('index.html', chat=chat)


if __name__=='__main__':
  app.run()
