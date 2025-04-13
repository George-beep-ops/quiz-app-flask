# -*- coding: utf-8 -*-
"""
Created on Sat Apr 12 18:14:06 2025

@author: nilsc
"""

from flask import Flask, render_template, request, redirect, session, url_for
from questions import questions
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Für Sicherheit (z. B. Sitzungen)

# Punktevergabe für Minispiele (je nach Schwierigkeit)
minigame_points = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}

# Ergebnisliste (nur in RAM – verschwindet bei Neustart)
results = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nickname = request.form['nickname']
        session['nickname'] = nickname
        session['score'] = 0
        session['current'] = 0
        return redirect(url_for('question'))
    return render_template('start.html')

@app.route('/question', methods=['GET', 'POST'])
def question():
    i = session.get('current', 0)

    # Wenn vorherige Frage beantwortet wurde
    if request.method == 'POST':
        answer = request.form.get('answer')
        correct = questions[i - 1]['correct']
        if answer == correct:
            session['score'] += 1

    # Quiz vorbei?
    if i >= len(questions):
        nickname = session.get('nickname', 'Unbekannt')
        results.append({'name': nickname, 'score': session['score']})
        return redirect(url_for('results_page'))

    # Minigame nach jeder 2. Frage
    if i > 0 and i % 2 == 0:
        return redirect(url_for('minigame', num=i // 2))

    session['current'] = i + 1
    q = questions[i]
    return render_template('question.html', q=q, index=i + 1)

@app.route('/minigame/<int:num>', methods=['GET', 'POST'])
def minigame(num):
    if request.method == 'POST':
        punkte = 0
        try:
            punkte = int(request.form.get('score', 0))
        except:
            pass
        session['score'] += punkte if punkte > 0 else minigame_points.get(num, 0)

        # WICHTIG: Erhöhe den Fragenzähler nach dem Minispiel!
        session['current'] = session.get('current', 0) + 1

        return redirect(url_for('question'))
    return render_template(f'minigame_{num}.html')

@app.route('/results')
def results_page():
    sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)
    return render_template('results.html', results=sorted_results)

# Wichtig für Render: Portbindung
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
