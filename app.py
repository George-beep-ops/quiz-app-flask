from flask import Flask, render_template, request, redirect, session, url_for
from questions import questions
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Punkte für Minispiele
minigame_points = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}

# Ergebnisse nur temporär im RAM
results = []

# Fester Ablauf: jede Frage und jedes Minispiel ist ein Schritt
flow = [
    'question_1', 'question_2', 'minigame_1',
    'question_3', 'question_4', 'minigame_2',
    'question_5', 'question_6', 'minigame_3',
    'question_7', 'question_8', 'minigame_4',
    'question_9', 'question_10', 'minigame_5',
    'question_11', 'question_12', 'results'
]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nickname = request.form['nickname']
        session['nickname'] = nickname
        session['score'] = 0
        session['step'] = 0
        return redirect(url_for('next_step'))
    return render_template('start.html')

@app.route('/next', methods=['GET', 'POST'])
def next_step():
    step = session.get('step', 0)

    # Wenn Ablauf abgeschlossen ist
    if step >= len(flow):
        return redirect(url_for('results_page'))

    current = flow[step]

    if current.startswith('question'):
        question_index = int(current.split('_')[1]) - 1
        if request.method == 'POST':
            answer = request.form.get('answer')
            correct = questions[question_index]['correct']
            if answer == correct:
                session['score'] += 1
            session['step'] += 1
            return redirect(url_for('next_step'))
        return render_template('question.html', q=questions[question_index], index=question_index + 1)

    elif current.startswith('minigame'):
        game_num = int(current.split('_')[1])
        if request.method == 'POST':
            try:
                punkte = int(request.form.get('score', 0))
            except:
                punkte = minigame_points.get(game_num, 0)
            session['score'] += punkte
            session['step'] += 1
            return redirect(url_for('next_step'))
        return render_template(f'minigame_{game_num}.html')

    elif current == 'results':
        nickname = session.get('nickname', 'Unbekannt')
        results.append({'name': nickname, 'score': session['score']})
        session['step'] += 1
        return redirect(url_for('results_page'))

@app.route('/results')
def results_page():
    score = session.get('score', 0)
    return render_template('results.html', score=score)

@app.route('/admin_results', methods=['GET'])
def admin_results():
    if request.args.get('pw') != 'nilsquiz2025':
        return "Zugriff verweigert", 403
    sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)
    return render_template('admin_results.html', results=sorted_results)

@app.route('/favicon.ico')
def favicon():
    return '', 204

# Für Render-Deployment
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


