from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from main import find_rec, find_notes, find_descriptions, update_liked_perfumes

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('chat'))
    return render_template('login.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        user_input = request.form['user_input']
        session['user_input'] = user_input

        user_data = {
            "username": session['username'],
            "prompt": user_input
        }

        # Call your recommendation functions from main.py
        results, perfumes = find_rec(user_data)
        notes = find_notes(perfumes)

        session['results'] = results
        session['perfumes'] = perfumes
        session['notes'] = notes

        return redirect(url_for('results'))

    return render_template('prompt.html', username=session['username'])

@app.route('/results')
def results():
    if 'username' not in session or 'results' not in session:
        return redirect(url_for('chat'))

    perfumes = session['perfumes']
    selected_perfume = perfumes[0] if perfumes else None
    notes = session['notes']
    descriptions = find_descriptions(notes)

    return render_template(
        'result.html',
        username=session['username'],
        user_input=session['user_input'],
        results=session['results'],
        perfumes=perfumes,
        selected_perfume=selected_perfume,
        top_notes=notes.get(selected_perfume, [])[0] if selected_perfume else [],
        middle_notes=notes.get(selected_perfume, [])[1] if selected_perfume else [],
        base_notes=notes.get(selected_perfume, [])[2] if selected_perfume else [],
        perfume_description=descriptions.get(selected_perfume) if selected_perfume else '',
        all_notes=notes,
        descriptions = descriptions
    )

@app.route('/like', methods=['POST'])
def like():
    data = request.get_json()
    perfume = data.get('perfume')
    action = data.get('action')
    liked = data.get('liked', [])

    # Store in session or process as needed
    session['liked_perfumes'] = liked

    # Call your processing function if needed
    update_liked_perfumes(liked)

    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)
