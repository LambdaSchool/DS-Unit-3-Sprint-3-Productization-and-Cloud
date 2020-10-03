from flask import Flask, render_template, request
from flask import jsonify
from joblib import load
import numpy as np
from string import ascii_lowercase
from model import DB

'''Features we use ['RANK','GP','MIN','FG_PCT','FG3_PCT','REB','STL','BLK']
    1. RANK...Last thing you ate
    2. GP...The last role you played in a group project
    3. Mins... Do you stay for the whole party or irish exit often?"
    4. FG_PCT...Last time you took a trip
    5. FG3_PCT... Do you go for big wins or little wins?",
    6. REB...Do you join the mosh pit or take a seat?
    7. STL...Would you rather have your team win or you have all the glory!",
    8. BLK...Last time you used a ladder?'''

#create flask web server
app = Flask(__name__)
app.config['SQLAlCHEMY_DATABASE_URI'] = 'sqlite:///sql.db'
DB.init_app(app)


def create_x(post_response):
    feats = []
    # last ate

    LETTERS = {letter: str(index) for index, 
                letter in enumerate(ascii_lowercase, start=1)} 
    feats.append(int(LETTERS[str.lower(post_response['rank'][0])]))
    #games played
    if post_response['gp'] == 'low':
        feats.append(73)
    if post_response['gp'] == 'mid_low':
        feats.append(77)
    if post_response['gp'] == 'mid_high':
        feats.append(80)
    if post_response['gp'] == 'high':
        feats.append(82)
    
    # mins
    if post_response['mins'] == 'low':
        feats.append(2462.0)
    if post_response['mins'] == 'mid_low':
        feats.append(2641.5)
    if post_response['mins'] == 'mid_high':
        feats.append(2804.0)
    if post_response['mins'] == 'high':
        feats.append(3125.0)
    #fg_pct
    if post_response['fg_pct'] == 'low':
        feats.append(0.44150)
    if post_response['fg_pct'] == 'mid_low':
        feats.append(0.46250)
    if post_response['fg_pct'] == 'mid_high':
        feats.append(0.49425)
    if post_response['fg_pct'] == 'high':
        feats.append(0.57800)
    
    #fg3_pct
    if post_response['fg3_pct'] == 'low':
        feats.append(0.3625)
    if post_response['fg3_pct'] == 'high':
        feats.append(0.3880)
        
    #reb
    if post_response['reb'] == 'low':
        feats.append(411.50)
    if post_response['reb'] == 'high':
        feats.append(700)
    
    #stl
    if post_response['stl'] == 'low':
        feats.append(85.00)
    if post_response['stl'] == 'high':
        feats.append(116.50)
    
    #blk
    if post_response['fg_pct'] == 'low':
        feats.append(22.75)
    if post_response['fg_pct'] == 'mid_low':
        feats.append(35.00)
    if post_response['fg_pct'] == 'mid_high':
        feats.append(61.75)
    if post_response['fg_pct'] == 'high':
        feats.append(193.00)
    return np.array(feats).reshape(1,-1)


def get_preds(X):
    pipeline = load('player.joblib')
    y_pred = pipeline.predict(X)
    return y_pred

@app.route('/')
@app.route("/index")
def home():
    return render_template('home.html')

@app.route("/result", methods=["POST"])
def result():
    if request.method == 'POST':
        response = request.form.to_dict()
    feats = create_x(response)

    preds = get_preds(feats)[0]
    return render_template("results.html", preds = preds)


if __name__ == '__main__':
    app.run(debug=True)
