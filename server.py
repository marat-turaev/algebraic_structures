#! /usr/bin/env python
# coding: utf8

import tex
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
        if number > 200:
            return flask.render_template('error.html',
                                         msg=u'Задано слишком большое число задач.')

    docType = flask.request.form['type']
    if not docType in ['x-tex','pdf']:
        return flask.render_template('error.html',
                                     msg=u'Задан неверный тип документа.')

    data = markov.generate_tex(number)
    if docType == 'pdf':
        data = tex.latex2pdf(data.decode('utf8'))
    response = flask.make_response(data)
    response.headers['Content-Type'] = 'application/%s' % docType
    response.headers['Content-Disposition'] = 'attachment; filename="tasks"'
    return response
 

if __name__ == "__main__":
    #app.run(host='0.0.0.0')
    app.debug = True
    app.run()
