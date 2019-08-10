from flask import Flask, render_template, request, redirect, url_for, session
import random
app = Flask(__name__)

#secret key
app.secret_key = 'my_key_is_super_secret'

#The Routes
@app.route('/')
def home_page():
    if 'views' in session:
        print("This returns false on first instance")
    else:
        #establish keys in session dictionary
        session['views'] = 0
        session['game_history'] = []
        session['users'] = []
        set_session()
    
    return render_template('index.html')

@app.route('/process', methods=["POST"])
def process_user_input():
    session['user_guess'] = request.form['user_guess']
    session['show_hint'] = 'inline-block'
    session['hint_color'] = 'red'

    if session['guess_tracker'] < 4:
        if int(session['user_guess']) > session['random_integer']:
            session['guess_tracker'] += 1
            session['hint'] = 'Too High'
        elif int(session['user_guess']) < session['random_integer']:
            session['guess_tracker'] += 1
            session['hint'] = 'Too Low'
        else:
            session['guess_tracker'] += 1
            session['show_guess_tracker'] = 'inline-block'
            session['hint_color'] = 'green'
            session['hint'] = 'YOU WIN!'
            session['win_lose'] = 'win'
            session['show_submit'] = 'none'
            session['show_reset'] = 'inline-block'
            session['show_winner_name_input'] = 'inline-block'
    else:
        session['guess_tracker'] += 1
        session['show_guess_tracker'] = 'inline-block'
        session['show_reset'] = 'inline-block'
        session['hint'] = 'You Lose!'
        session['win_lose'] = 'lose'
        session['show_submit'] = 'none'
    return redirect('/')

@app.route('/reset_game', methods=['POST'])
def reset_game():
    if session['win_lose'] == 'win':
        session['user_name'] = request.form['user_name']
        session['users'].append(session['user_name'])
        session['game_history'].append(session['guess_tracker'])
    set_session()

    return redirect('/')

@app.route('/leaderboards')
def leaderboards():
    return render_template('leaderboards.html')

def set_session():
    session['random_integer'] = random.randint(1, 100)
    session['user_guess'] = 0
    session['user_name'] = ''
    session['guess_tracker'] = 0
    session['show_guess_tracker'] = 'none'
    session['hint'] = ''
    session['show_hint'] = 'none'
    session['hint_color'] = ''
    session['show_submit'] = 'inline-block'
    session['show_reset'] = 'none'
    session['win_lose'] = ''
    session['show_winner_name_input'] = 'none'

if __name__ == '__main__':
    app.run(debug=True)