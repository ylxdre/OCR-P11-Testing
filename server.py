import json
from flask import Flask,render_template,request,redirect,flash,url_for,session
from datetime import datetime


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']]
    current_compet = [compet for compet in competitions if datetime.strptime(compet['date'], '%Y-%m-%d %H:%M:%S') > datetime.now()]
    print(current_compet)
    if club:
        return render_template('welcome.html', club=club[0], competitions=current_compet)
    flash("The email isn't found")
    return redirect(url_for('index'))

@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    if competition['name'] in session:
        places = {competition['name']: session[competition['name']] + placesRequired}
    else:
        places = {competition['name']: placesRequired}
    points = int(club['points'])
    print("booked", places)
    if placesRequired <= 12:
        if places[competition['name']] <= 12:
            if placesRequired <= points:
                competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
                club['points'] = int(club['points']) - placesRequired
                if not competition['name'] in session:
                    session[competition['name']] = placesRequired
                flash('Great-booking complete!')
            else:
                flash("You don't have enough points")
        else:
            flash(f"You already booked 12 places for {competition['name']}")
    else:
        flash("You can't book more than 12 places")
    return render_template('welcome.html', club=club,
                           competitions=competitions)

# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if (__name__ == "__main__"):
    app.run(debug=True)
