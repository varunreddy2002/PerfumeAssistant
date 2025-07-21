# from flask import Flask, render_template, request, redirect, url_for, session
# from main import find_rec, find_notes
# from google import genai

 
# app = Flask(__name__)
# app.secret_key = 'your_secret_key'
# @app.route('/', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         session['username'] = request.form['username']
#         return redirect(url_for('chat'))
#     return render_template('login.html')
 
# @app.route('/chat', methods=['GET', 'POST'])
# def chat():
#     if 'username' not in session:
#         return redirect(url_for('login'))
 
#     user_input = None
#     results = []
#     perfumes = []
#     notes = {}
#     selected_perfume = None
 
#     if request.method == 'POST':
#         user_input = request.form['user_input']
#         user_data = {
#         "username":session['username'],
#         "prompt":user_input
#         }
#         results, perfumes = find_rec(user_data)
#         notes = find_notes(perfumes)
#         selected_perfume = perfumes[0] if perfumes else None

 
#     return render_template('chat.html', username=session['username'], user_input=user_input, results=results,
#         perfumes=perfumes,
#         selected_perfume=selected_perfume,
#         top_notes=notes.get(selected_perfume, [])[0] if selected_perfume else [],
#         middle_notes=notes.get(selected_perfume, [])[1] if selected_perfume else [],
#         base_notes=notes.get(selected_perfume, [])[2] if selected_perfume else [],
#         all_notes=notes  # optional for dynamic JS update)
#     )
 
# def generate_recommendations(prompt_text):
#     # Dummy logic - replace with your own
#     return [
#         f"Analyzing: {prompt_text}",
#         "Suggestion: Dior Homme",
#         "Suggestion: Tom Ford Black Orchid",
#         "Suggestion: Versace Eros"
#     ]
 
# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, session
from main import find_rec, find_notes

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
        all_notes=notes
    )

# ✅ New route to handle individual perfume detail pages
@app.route('/perfume/<perfume_name>')
def perfume_detail(perfume_name):
    if 'notes' not in session or 'username' not in session:
        return redirect(url_for('chat'))

    notes = session['notes']
    top, middle, base = notes.get(perfume_name, ([], [], []))

    return render_template(
        'perfume_detail.html',  # make sure this template exists!
        perfume_name=perfume_name,
        top_notes=top,
        middle_notes=middle,
        base_notes=base,
        username=session['username']
    )

if __name__ == '__main__':
    app.run(debug=True)
