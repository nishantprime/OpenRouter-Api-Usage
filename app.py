from flask import Flask, request
from database import collection
from helper import generation


app = Flask(__name__)


@app.route('/', methods = ['GET', 'POST'])
def chat():
  if request.method == 'GET':
    chat = collection.find()
    return render_template('index.html', chat=chat)
  else:
    prompt = request.form['prompt']
    response = generation(prompt)
    return render_template('index.html', response = response)


if __name__=='__main__':
  app.run()
