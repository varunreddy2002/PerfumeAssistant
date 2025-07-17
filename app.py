# from flask import Flask, render_template, request, redirect, url_for, session

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
    
#     if request.method == 'POST':
#         description = request.form['description']
#         return render_template('chat.html', submitted=True, description=description)
    
#     return render_template('chat.html', submitted=False)

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, session
 
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
 
    user_input = None
    results = []
 
    if request.method == 'POST':
        user_input = request.form['user_input']
        results = generate_recommendations(user_input)
 
    return render_template('chat.html', username=session['username'], user_input=user_input, results=results)
 
def generate_recommendations(prompt_text):
    # Dummy logic - replace with your own
    return [
        f"Analyzing: {prompt_text}",
        "Suggestion: Dior Homme",
        "Suggestion: Tom Ford Black Orchid",
        "Suggestion: Versace Eros"
    ]
 
if __name__ == '__main__':
    app.run(debug=True)