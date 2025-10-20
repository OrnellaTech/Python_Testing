import json
from flask import Flask,render_template,request,redirect,flash,url_for
from flask import session
from datetime import datetime

def loadClubs(path='clubs.json'):
    with open(path) as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions(path='competitions.json'):
    with open(path) as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions

def can_book_places(competition, club, places_required):
    available_places = int(competition['numberOfPlaces'])
    club_points = int(club['points'])

    if places_required > available_places:
        return False, f"Il ne reste que {available_places} places disponibles."
    elif places_required > 12:
        return False, "Vous ne pouvez pas réserver plus de 12 places à la fois."
    elif places_required > club_points:
        return False, "Vous n'avez pas assez de points pour réserver autant de places."
    else:
        return True, f"Réservation réussie de {places_required} place(s) !"



def create_app(config=None):
    app = Flask(__name__)
    app.secret_key = 'something_special'
    if config:
        app.config.update(config)


    # app = Flask(__name__)
    # app.secret_key = 'something_special'

    competitions = loadCompetitions()
    clubs = loadClubs()

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            email = request.form['email']
            club = [c for c in clubs if c['email'] == email]
            if not club:
                flash("❌ Email incorrect. Accès refusé", "error")
                return redirect(url_for('index'))
            else:
                # Email correct, redirige vers la page welcome
                return redirect(url_for('showSummary',  email=email))
        return render_template('index.html')


    @app.route('/showSummary')
    def showSummary():
        email = request.args.get('email')
        date_actuelle = datetime.now()
        # Convertir les dates des compétitions en objets datetime
        for comp in competitions:
            comp['date_obj'] = datetime.strptime(comp['date'], "%Y-%m-%d %H:%M:%S")
        
        club = [c for c in clubs if c['email'] == email]
        if not club:
            flash("❌ Email incorrect. Accès refusé", "error")
            return redirect(url_for('index'))
        club = club[0]  # récupère le dictionnaire du club
        return render_template('welcome.html', club=club, competitions=competitions, date_actuelle=date_actuelle)


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
        date_actuelle = datetime.now()
        # Convertir les dates des compétitions en objets datetime
        for comp in competitions:
            comp['date_obj'] = datetime.strptime(comp['date'], "%Y-%m-%d %H:%M:%S")
        
        club = clubs[0]  # ou tu peux récupérer depuis session si besoin
        return render_template('welcome.html', club=club, competitions=competitions,date_actuelle=date_actuelle)

    @app.route('/clubs')
    def displayClubs():
        return render_template('club_displays.html', clubs=clubs)




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
# <<<<<<< HEAD
                # flash("❌ Vous n'avez pas assez de points pour réserver autant de places.", "error")
# =======
                # flash("❌ Vous n'avez pas assez de points pour réserver autant de places.", "error")
                flash("Vous ne pouvez plus réserver de places", "error")

# >>>>>>> test_integration
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

    return app

# if __name__ == '__main__':
#     app = create_app()
#     app.run(host='0.0.0.0', port=5000, debug=True)