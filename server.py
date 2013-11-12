#! /usr/bin/env python
# coding: utf8

import flask
from markov import markov

app = flask.Flask(__name__)
 

@app.route('/')
def index():
    task = markov.generate(3).decode('utf8')
    return flask.render_template('index.html', task=task)


@app.route('/download/', methods=['GET', 'POST'])
def download():
    if flask.request.method != 'POST':
        return flask.redirect(flask.url_for('index'))

    number = flask.request.form['number']
    if not number.isdigit():
        return flask.render_template('error.html',
                                     msg=u'Задано некорректное число задач.')
    else:
        number = int(number)
        if number <= 0:
            return flask.render_template('error.html',
                                         msg=u'Задано слишком маленькое число задач.')
        if number > 100:
            return flask.render_template('error.html',
                                         msg=u'Задано слишком большое число задач.')

    tex = markov.generate_tex(number)
    response = flask.make_response(tex)
    response.headers['Content-Type'] = 'application/x-tex'
    response.headers['Content-Disposition'] = 'attachment; filename="tasks"'
    return response
 

if __name__ == "__main__":
    #app.run(host='0.0.0.0')
    app.debug = True
    app.run()
