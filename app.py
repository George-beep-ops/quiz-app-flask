from flask import Flask, render_template, request, redirect, session, url_for
from questions import questions
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

minigame_points = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}
results = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nickname = request.form['nickname']
        session['nickname'] = nickname
        session['score'] = 0
        session['question_index'] = 0
        session['minigame_index'] = 1
        return redirect(url_for('question'))
    return render_template('start.html')

@app.route('/question', methods=['GET', 'POST'])
def question():
    i = session.get('question_index', 0)

    if request.method == 'POST':
        answer = request.form.get('answer')
        if i > 0:
            correct = questions[i - 1]['correct']
            if answer == correct:
                session['score'] += 1

    # Nach jeder 2. beantworteten Frage → Minispiel
    if i > 0 and i % 2 == 0:
        return redirect(url_for('minigame', num=session['minigame_index']))

    if i >= len(questions):
        nickname = session.get('nickname', 'Unbekannt')
        results.append({'name': nickname, 'score': session['score']})
        return redirect(url_for('results_page'))

    q = questions[i]
    session['question_index'] = i + 1
    return render_template('question.html', q=q, index=i + 1)

@app.route('/minigame/<int:num>', methods=['GET', 'POST'])
def minigame(num):
    if request.method == 'POST':
        try:
            punkte = int(request.form.get('score', 0))
        except:
            punkte = minigame_points.get(num, 0)
        session['score'] += punkte

        # nur minigame index erhöhen, nicht question index!
        session['minigame_index'] = num + 1
        return redirect(url_for('question'))

    return render_template(f'minigame_{num}.html')

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

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


