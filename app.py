from flask import Flask, request, render_template
from database import collection
from helper import generation


app = Flask(__name__)


@app.route('/', methods = ['GET', 'POST'])
def chat():
  if request.method == 'GET':
    chat = list(collection.find({},{'prompt':1, 'response':1, 'formatted_time':1}))
    return render_template('index.html', chat=chat)
  else:
    prompt = request.form['prompt']
    time, response, token_usage = generation(prompt)
    if not time :
      return  render_template('index.html', error=response)
    return render_template('index.html', time=time, response=response, token_usage=token_usage)


if __name__=='__main__':
  app.run()
