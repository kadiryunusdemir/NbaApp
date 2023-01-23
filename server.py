import os
from flask import Flask
from flask_login import LoginManager
import psycopg2 as dbapi2

import views
from database import Database
from user import get_user

lm = LoginManager()

# creating a user object from the user id in the session
@lm.user_loader
def load_user(user_id):
    return get_user(user_id)

def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")
    
    ## url rules ##
    app.add_url_rule("/", view_func=views.home_page)
    #################### DRAFT ###############################
    app.add_url_rule("/drafts/<int:id>", view_func=views.draft_page)
    app.add_url_rule("/drafts", view_func=views.drafts_page, methods=["GET", "POST"])
    app.add_url_rule("/add_draft", view_func=views.add_draft_page, methods=["GET", "POST"])
    app.add_url_rule("/drafts/<int:id>/edit", view_func=views.draft_edit_page, methods=["GET", "POST"])
    app.add_url_rule("/draft_delete/<int:id>/", view_func=views.draft_delete_page)
    
    app.add_url_rule("/draft_combines/<int:id>", view_func=views.draft_combine_page)
    app.add_url_rule("/draft_combines", view_func=views.draft_combines_page, methods=["GET", "POST"])
    app.add_url_rule("/add_draft_combine", view_func=views.add_draft_combine_page, methods=["GET", "POST"])
    app.add_url_rule("/draft_combines/<int:id>/edit", view_func=views.draft_combine_edit_page, methods=["GET", "POST"])
    app.add_url_rule("/draft_combine_delete/<int:id>/", view_func=views.draft_combine_delete_page)

    #################### TEAMS ###############################
    app.add_url_rule("/teams", view_func=views.teams_page, methods=["GET", "POST"])
    # send the team id part of the route (/team/1) as a integer parameter to the handler.
    app.add_url_rule("/teams/<int:team_id>", view_func=views.team_page)
    app.add_url_rule("/teams/<int:team_id>/edit", view_func=views.team_edit_page, methods=["GET", "POST"])
    # GET/POST, these need to be allowed when registering the route
    app.add_url_rule("/add_team", view_func=views.team_add_page, methods=["GET", "POST"])

    #################### TEAMS ATTRIBUTES ###############################
    app.add_url_rule("/teams_attributes", view_func=views.teams_attributes_page, methods=["GET", "POST"])
    app.add_url_rule("/teams_attributes/<int:team_id>", view_func=views.team_attributes_page)
    app.add_url_rule("/teams_attributes/<int:team_id>/edit", view_func=views.team_attributes_edit_page, methods=["GET", "POST"])
    app.add_url_rule("/add_team_attributes", view_func=views.team_attributes_add_page, methods=["GET", "POST"])

    #######################   PLAYERS   ########################
    app.add_url_rule("/players", view_func=views.players_page, methods=["GET", "POST"])
    app.add_url_rule("/players/<int:player_id>", view_func=views.player_page)
    app.add_url_rule("/add_player", view_func=views.add_player_page, methods=["GET", "POST"])
    app.add_url_rule("/players/<int:player_id>/edit", view_func=views.edit_player_page, methods=["GET", "POST"])
    app.add_url_rule("/player_delete/<int:id>/", view_func=views.delete_player_page)
    
    #######################   PLAYER ATTRIBUTES   ########################
    app.add_url_rule("/players_attributes", view_func=views.players_attributes_page,  methods=["GET", "POST"])
    app.add_url_rule("/player_attributes/<int:player_id>", view_func=views.player_attributes_page)
    app.add_url_rule("/add_player_attributes", view_func=views.add_player_attributes_page, methods=["GET", "POST"])
    app.add_url_rule("/players_attributes/<int:player_attributes_id>/edit", view_func=views.edit_player_attributes_page, methods=["GET", "POST"])
    app.add_url_rule("/players_attributes_delete/<int:id>/", view_func=views.delete_player_attributes_page)
    
    #######################   PLAYER PHOTOS   ########################
    app.add_url_rule("/players_photos", view_func=views.players_photos_page)
    
    #######################   PLAYER BIOS   ########################
    app.add_url_rule("/players_bios", view_func=views.players_bios_page)
    
    #######################   GAMES   ########################
    app.add_url_rule("/games", view_func=views.games_page, methods=["GET", "POST"])
    app.add_url_rule("/games/<int:gameID>", view_func=views.game_page)
    app.add_url_rule("/games/<int:gameID>/edit", view_func=views.game_edit_page, methods=["GET", "POST"])
    app.add_url_rule("/add_game", view_func=views.game_add_page, methods=["GET", "POST"])

    ####################### LOGIN / LOGOUT ########################
    app.add_url_rule("/login", view_func=views.login_page, methods=["GET", "POST"])
    app.add_url_rule("/logout", view_func=views.logout_page)
    
    ## user ##
    lm.init_app(app)
    # If a visitor makes a request to a protected page without logging in, we can redirect the request
    # to the login page by setting the login_view property of the login manager 
    lm.login_message = "Please log in to access this page."
    lm.login_message_category = "warning"
    lm.login_view = "login_page"
    
    ## DB connection ##
    db = Database(db_url)
    app.config["db"] = db

    return app

if __name__ == "__main__":
    db_url = os.getenv("DATABASE_URL")
    if db_url is None:
        print("Bash Usage: DATABASE_URL=connectionString python server.py")
        exit(1)
    print("Successfull connection")
    app = create_app()
    port = app.config.get("PORT")
    host = app.config.get("HOST")
    app.run(host=host, port=port)