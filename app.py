from flask import Flask, render_template, request, redirect, session, url_for
from questions import questions
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Punktevergabe für Minispiele (Fallback bei Fehlern)
minigame_points = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}

# Ergebnisse (nur im RAM gespeichert)
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

    # Bei POST: Antwort überprüfen
    if request.method == 'POST':
        answer = request.form.get('answer')
        if i > 0:  # Vorherige Frage auswerten
            correct = questions[i - 1]['correct']
            if answer == correct:
                session['score'] += 1

    # Quiz beendet?
    if i >= len(questions):
        nickname = session.get('nickname', 'Unbekannt')
        results.append({'name': nickname, 'score': session['score']})
        return redirect(url_for('results_page'))

    # Nach jeder 2. Frage ein Minigame
    if i > 0 and i % 2 == 0:
        return redirect(url_for('minigame', num=i // 2))

    # Nächste Frage anzeigen
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
        session['current'] += 1  # Weiter zur nächsten Frage
        return redirect(url_for('question'))
    return render_template(f'minigame_{num}.html')

@app.route('/results')
def results_page():
    score = session.get('score', 0)  # Score aus Session holen
    return render_template('results.html', score=score)

@app.route('/admin_results', methods=['GET'])
def admin_results():
    if request.args.get('pw') != 'nilsquiz2025':
        return "Zugriff verweigert", 403
    sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)
    return render_template('admin_results.html', results=sorted_results)

# Für Render: Portbindung
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

