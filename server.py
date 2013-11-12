#! /usr/bin/env python
# coding: utf8

import flask


app = flask.Flask(__name__)
 

@app.route('/')
def index():
    return flask.render_template('index.html', task='Text of the task')


@app.route('/download/', methods=['GET', 'POST'])
def download():
    if flask.request.method != 'POST':
        return flask.redirect(flask.url_for('index'))

    tex = 'text'
    response = flask.make_response(tex)
    #response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Type'] = 'application/x-tex'
    response.headers['Content-Disposition'] = 'attachment; filename="tasks"'
    return response
 

if __name__ == "__main__":
    #app.run(host='0.0.0.0')
    app.debug = True
    app.run()
