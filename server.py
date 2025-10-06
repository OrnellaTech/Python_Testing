import json
from flask import Flask,render_template,request,redirect,flash,url_for
from flask import session

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
    club = [club for club in clubs if club['email'] == request.form['email']][0]
    

    # Lors de showSummary
    session['club_name'] = club['name']

    return render_template('welcome.html',club=club,competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/welcome')
def welcome():
    club = clubs[0]  # ou tu peux récupérer depuis session si besoin
    return render_template('welcome.html', club=club, competitions=competitions)

# @app.route('/welcome')
# def welcome():
#     club_name = session.get('club_name', clubs[0]['name'])
#     club = [c for c in clubs if c['name'] == club_name][0]
#     return render_template('welcome.html', club=club, competitions=competitions)



@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    

    action_type = request.form.get('action_type')

    if action_type == "purshase":
        # placesRequired = int(request.form['places'])
        # competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
        # flash('Great-booking complete!')
        # return render_template('booking.html', club=club, competition=competition)
        placesRequired = int(request.form['places'])
        available_places = int(competition['numberOfPlaces'])
        club_points = int(club['points'])

        if placesRequired > available_places:
            flash(f"❌ Il ne reste que {available_places} places disponibles.", "error")
        elif placesRequired > 12:
            flash("⚠️ Vous ne pouvez pas réserver plus de 12 places à la fois.", "warning")
        elif placesRequired > club_points:
            flash("❌ Vous n'avez pas assez de points pour réserver autant de places.", "error")
        else:
            # ✅ Tout est OK, on met à jour les valeurs dans le dictionnaire en mémoire
            competition['numberOfPlaces'] = available_places - placesRequired
            club['points'] = club_points - placesRequired
            flash(f"✅ Réservation réussie de {placesRequired} place(s) !", "success")
        
        return redirect(url_for('book', competition=competition['name'], club=club['name']))


    elif action_type == "return":
        flash("")
        # return render_template('welcome.html', club=club, competitions=competitions)
        return redirect(url_for('welcome'))
    else:
        flash('')
        # return render_template('welcome.html', club=club, competitions=competitions)
        return redirect(url_for('welcome'))
# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))