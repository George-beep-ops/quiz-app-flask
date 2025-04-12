# -*- coding: utf-8 -*-
"""
Created on Sat Apr 12 18:14:06 2025

@author: nilsc
"""

from flask import Flask, render_template, request, redirect

app = Flask(__name__)
responses = []

@app.route('/')
def question():
    return render_template("question.html")

@app.route('/submit', methods=["POST"])
def submit():
    answer = request.form.get("answer")
    responses.append(answer)
    print("Antwort erhalten:", answer)
    return redirect('/')

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False)
