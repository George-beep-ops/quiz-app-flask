from flask import Flask, render_template, request, redirect, session, url_for
from questions import questions
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Sicherheits-Schlüssel

# Punktevergabe für Minispiele
minigame_points = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}

# Ergebnisse (nur im RAM)
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

    # Antwort auswerten
    if request.method == 'POST':
        answer = request.form.get('answer')
        correct = questions[i - 1]['correct']
        if answer == correct:
            session['score'] += 1

    # Quiz zu Ende?
    if i >= len(questions):
        nickname = session.get('nickname', 'Unbekannt')
        results.append({'name': nickname, 'score': session['score']})
        return redirect(url_for('results_page'))

    # Minigame nach jeder zweiten Frage
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
        return redirect(url_for('question'))
    return render_template(f'minigame_{num}.html')

@app.route('/results')
def results_page():
    return render_template('results.html')

# ✅ Admin-Auswertung mit Passwort
@app.route('/admin_results', methods=['GET', 'POST'])
def admin_results():
    correct_password = 'nilsquiz2025'

    if 'admin_authenticated' not in session:
        if request.method == 'POST':
            entered_password = request.form.get('password')
            if entered_password == correct_password:
                session['admin_authenticated'] = True
                return redirect(url_for('admin_results'))
            else:
                return render_template('admin_results.html', error='Falsches Passwort!')
        return render_template('admin_results.html')

    sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)
    score_distribution = {}
    for result in results:
        score = result['score']
        score_distribution[score] = score_distribution.get(score, 0) + 1

    return render_template('admin_results.html', results=sorted_results, distribution=score_distribution)

# ⚙️ Port für Render setzen
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

