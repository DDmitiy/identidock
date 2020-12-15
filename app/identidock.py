from flask import Flask, Response, request
import requests
import redis
import hashlib
import html


app = Flask(__name__)
cache = redis.StrictRedis(host='redis', port=6379, db=0)

DEFAULT_NAME = 'Joe Bloggs'
SALT = 'SOME_UNIQUE_SALT'


@app.route('/', methods=['GET', 'POST'])
def mainpage():
    name = DEFAULT_NAME

    if request.method == 'POST':
        name = html.escape(request.form['name'], quote=True)
    salted_name = name + SALT
    hashed_name = hashlib.sha256(salted_name.encode()).hexdigest()

    header = '<html><head><title>Identidock</title></head><body>'

    body = '''<form method="POST"> 
	Hello <input type='text' name='name' value='{name}'>
	<input type='submit' value='submit'>
	<form/>
	<p>You look like a:<p/>
	<img src='/monster/{hashed_name}'/>
    '''.format(name=name, hashed_name=hashed_name)

    footer = '</body></html>'
    return header + body + footer


@app.route('/monster/<name>')
def get_identicon(name):
    name = html.escape(name, quote=True)

    image = cache.get(name)
    if image:
        return Response(image, mimetype='image/png')

    resp = requests.get('http://dnmonster:8080/monster/{name}?size=160'.format(name=name))
    image = resp.content
    cache.set(name, image)

    return Response(image, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

