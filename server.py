import json
from flask import Flask,render_template,request,redirect,flash,url_for,session


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
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html', club=club, competitions=competitions)
    except IndexError:
        flash("Sorry, that email wasn't found")
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
    if placesRequired <= 12:
        if places[competition['name']] <= 12:
            if placesRequired <= points:
                competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
                if not competition['name'] in session:
                    session[competition['name']] = placesRequired
                flash(f"Great ! {placesRequired} places booked for {competition['name']}")
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
