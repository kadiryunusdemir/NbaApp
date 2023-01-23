from flask import current_app, flash, redirect, render_template, abort, request, url_for
from flask_login import current_user, login_required, logout_user, login_user
from psycopg2 import Error, errors
from passlib.hash import pbkdf2_sha256 as hasher

from forms import DraftAddForm, DraftEditForm,DraftCombineAddForm,DraftCombineEditForm, PlayerAttributesAddForm, PlayerAttributesEditForm, PlayerEditForm, TeamEditForm, TeamAttributesEditForm, GameAddForm, GameEditForm, LoginForm
from models.Player import Player
from models.PlayerAttributes import PlayerAttributes
from models.team import Team
from models.team_attributes import TeamAttributes
from models.draft import Draft
from models.draft_combine import Draft_Combine
from models.game import game as Game
from user import get_user

def home_page():
    return render_template("home.html")

################################ TEAM ########################################
def teams_page():
    db = current_app.config["db"]
    if request.method == "GET":
        teams = db.get_teams()
        return render_template("teams.html", teams=sorted(teams))
    else:
        search = request.form.get("search")
        if search:
            teams = db.get_teams_by_search(search)
            if teams == None:
                flash("No result!", "warning")
                teams = db.get_teams()
                return render_template("teams.html", teams=sorted(teams))
            else:
                flash("Search result:", "success")
                return render_template("teams.html", teams=sorted(teams))
        if not current_user.is_admin:
            abort(401) # “Unauthorized” error
        form_team_ids = request.form.getlist("team_ids")
        for form_team_id in form_team_ids:
            db.delete_team(int(form_team_id))
            flash("Team is deleted.", "success")
        return redirect(url_for("teams_page"))

def team_page(team_id):
    db = current_app.config["db"]
    team = db.get_team(team_id)
    if team is None:
        abort(404)  #HTTP “Not Found” (404) error.
    return render_template("team.html", team=team)

@login_required
def team_add_page():
    if not current_user.is_admin:
        abort(401) # “Unauthorized” error
    form = TeamEditForm()
    if form.validate_on_submit():
        full_name = form.data["full_name"]
        abbreviation = form.data["abbreviation"]
        nickname = form.data["nickname"]
        city = form.data["city"]
        state = form.data["state"]
        year_founded = form.data["year_founded"]
        team = Team(0, full_name, abbreviation, nickname, city, state, year_founded)
        db = current_app.config["db"]
        try:
            team_id = db.add_team(team)
        except Error as e:
            if isinstance(e, errors.UniqueViolation):
                flash("Values must be unique!", "danger")
            return render_template("team_edit.html", form=form, type="Add")
        flash("Team is added.", "success")
        return redirect(url_for("team_page", team_id=team_id)) 
    return render_template("team_edit.html", form=form, type="Add")

@login_required
def team_edit_page(team_id):
    if not current_user.is_admin:
        abort(401) # “Unauthorized” error
    db = current_app.config["db"]
    team = db.get_team(team_id)
    if team is None:
        abort(404)
    form = TeamEditForm()
    if form.validate_on_submit():
        full_name = form.data["full_name"]
        abbreviation = form.data["abbreviation"]
        nickname = form.data["nickname"]
        city = form.data["city"]
        state = form.data["state"]
        year_founded = form.data["year_founded"]
        team = Team(0, full_name, abbreviation, nickname, city, state, year_founded)
        try:
            db.update_team(team_id, team)
        except Error as e:
            if isinstance(e, errors.UniqueViolation):
                flash("Values must be unique!", "danger ")
            return render_template("team_edit.html", form=form, type="Edit")
        flash("Team is updated.", "success ")
        return redirect(url_for("team_page", team_id=team_id))
    # if not valid return values
    form.full_name.data = team.full_name
    form.abbreviation.data = team.abbreviation
    form.nickname.data = team.nickname
    form.city.data = team.city
    form.state.data = team.state
    form.year_founded.data = team.year_founded
    return render_template("team_edit.html", form=form, type="Edit")

################################ TEAM ATTRIBUTES ########################################
def teams_attributes_page():
    db = current_app.config["db"]
    if request.method == "GET":
        teams_attributes = db.get_teams_attributes()
        return render_template("teams_attributes.html", teams_attributes=sorted(teams_attributes))
    else:
        search = request.form.get("search")
        if search:
            teams_attributes = db.get_teams_attributes_by_search(search)
            if teams_attributes == None:
                flash("No result!", "warning")
                teams_attributes = db.get_teams_attributes()
                return render_template("teams_attributes.html", teams_attributes=sorted(teams_attributes))
            else:
                flash("Search result:", "success")
                return render_template("teams_attributes.html", teams_attributes=sorted(teams_attributes))
        if not current_user.is_admin:
            abort(401) # “Unauthorized” error
        form_team_attributes_ids = request.form.getlist("team_attributes_ids")
        for form_team_attributes_id in form_team_attributes_ids:
            db.delete_team_attributes(int(form_team_attributes_id))
            flash("Team attributes are deleted.", "success")
        return redirect(url_for("teams_attributes_page"))
    
def team_attributes_page(team_id):
    db = current_app.config["db"]
    team_attributes = db.get_team_attributes(team_id)
    if team_attributes is None:
        return redirect(url_for("team_attributes_edit_page", team_id=team_id))
        # abort(404)  #HTTP “Not Found” (404) error.
    abbreviation = db.get_team_abbr(team_id)
    return render_template("team_attributes.html", team_attributes=team_attributes, abbr=abbreviation)

@login_required
def team_attributes_add_page():
    if not current_user.is_admin:
        abort(401) # “Unauthorized” error
    form = TeamAttributesEditForm()
    db = current_app.config["db"]
    form.teams.choices = db.get_teams_with_empty_attributes()
    if form.teams.choices is None:
        flash("All teams has attributes!", "danger")
        return redirect(url_for("teams_attributes_page"))
    if form.validate_on_submit():
        team_id = form.teams.data
        arena = form.data["arena"]
        arena_capacity = form.data["arena_capacity"]
        owner = form.data["owner"]
        general_manager = form.data["general_manager"]
        head_coach= form.data["head_coach"]
        d_league_affiliation = form.data["d_league_affiliation"]
        facebook_website_link = form.data["facebook_website_link"]
        instagram_website_link = form.data["instagram_website_link"]
        twitter_website_link = form.data["twitter_website_link"]
        team_attributes = TeamAttributes(team_id, arena, arena_capacity, owner, general_manager, head_coach, 
                                         d_league_affiliation, facebook_website_link, instagram_website_link, 
                                         twitter_website_link)
        try:
            team_id = db.add_team_attributes(team_attributes)
        except Error as e:
            if isinstance(e, errors.ForeignKeyViolation):
                flash("There is no related team!", "danger")
            return render_template("team_attributes_add.html", form=form)
        flash("Team attributes are added.", "success")
        return redirect(url_for("team_attributes_page", team_id=team_id))
    return render_template("team_attributes_add.html", form=form)

@login_required
def team_attributes_edit_page(team_id):
    if not current_user.is_admin:
        abort(401) # “Unauthorized” error
    db = current_app.config["db"]
    team_attributes = db.get_team_attributes(team_id)
    isNew = False
    if team_attributes is None:
        team = db.get_team(team_id)
        if team is None:
            abort(404)  #HTTP “Not Found” (404) error.
        else:
            isNew = True
    form = TeamAttributesEditForm()
    form.abbreviation = db.get_team_abbr(team_id)
    form.teams.choices=[(team_id, "temp")]
    form.teams.data = team_id
    if form.validate_on_submit():
        arena = form.data["arena"]
        arena_capacity = form.data["arena_capacity"]
        owner = form.data["owner"]
        general_manager = form.data["general_manager"]
        head_coach= form.data["head_coach"]
        d_league_affiliation = form.data["d_league_affiliation"]
        facebook_website_link = form.data["facebook_website_link"]
        instagram_website_link = form.data["instagram_website_link"]
        twitter_website_link = form.data["twitter_website_link"]
        team_attributes = TeamAttributes(team_id, arena, arena_capacity, owner, general_manager, head_coach, 
                                         d_league_affiliation, facebook_website_link, instagram_website_link, 
                                         twitter_website_link)
        # team_id cannot be changed so no need for try, catch for foreign key error
        if isNew is True:
            team_id = db.add_team_attributes(team_attributes)
            flash("Team attributes are added.", "success")
            return redirect(url_for("team_attributes_page", team_id=team_id))
        else:
            db.update_team_attributes(team_id, team_attributes)
            flash("Team attributes are updated.", "success")
            return redirect(url_for("team_attributes_page", team_id=team_id))
    # if not valid return values
    form.team_id.data = team_id
    if team_attributes is None:
        return render_template("team_attributes_edit.html", form=form)
    form.arena.data = team_attributes.arena
    form.arena_capacity.data = team_attributes.arena_capacity
    form.owner.data = team_attributes.owner
    form.general_manager.data = team_attributes.general_manager
    form.head_coach.data = team_attributes.head_coach
    form.d_league_affiliation.data = team_attributes.d_league_affiliation
    form.facebook_website_link.data = team_attributes.facebook_website_link
    form.instagram_website_link.data = team_attributes.instagram_website_link
    form.twitter_website_link.data = team_attributes.twitter_website_link
    return render_template("team_attributes_edit.html", form=form)

def players_page():
    db = current_app.config["db"]
        
    if request.method == "GET":
        players = db.get_players()
        return render_template("players.html", players=players)
    else:
        player_to_delete = request.form.get("player_to_delete")
        db.delete_player(int(player_to_delete))
        flash("Player is deleted.", "success")
        return redirect(url_for("players_page"))

def player_page(player_id):
    db = current_app.config["db"]
    player = db.get_player(player_id)
    if player is None:
        abort(404)  #HTTP “Not Found” (404) error.
    return render_template("player.html", player=player)

@login_required
def add_player_page():
    if not current_user.is_admin:
        abort(401) # “Unauthorized” error
    form = PlayerEditForm()
    db = current_app.config["db"]
    form.is_active.choices = [('0', '0'), ('1', '1')]
    if form.validate_on_submit():
        full_name = form.data["full_name"]
        first_name = form.data["first_name"]
        last_name = form.data["last_name"]
        is_active = form.is_active.data
        player = Player(0, full_name, first_name, last_name, is_active)
        try:
            player = db.add_player(player)
        except Error as e:
            if isinstance(e, errors.ForeignKeyViolation):
                flash("There is no related team!", "danger")
            return render_template("add_player.html", form=form)
        flash("Player is added.", "success")
        return redirect(url_for("players_page")) 
    return render_template("add_player.html", form=form)

@login_required
def delete_player_page(id):
    if not current_user.is_admin:
        abort(401) # “Unauthorized” error
    db = current_app.config["db"]
    db.delete_player(id)
    players = db.get_players()
    flash("Player deleted","success ")
    return render_template("players.html", players = players)

@login_required
def edit_player_page(player_id):
    if not current_user.is_admin:
        abort(401) # “Unauthorized” error
    db = current_app.config["db"]
    player = db.get_player(player_id)
    if player is None:
        abort(404)
    form = PlayerEditForm()
    form.is_active.choices = [('0', '0'), ('1', '1')]
    if form.validate_on_submit():
        full_name = form.data["full_name"]
        first_name = form.data["first_name"]
        last_name = form.data["last_name"]
        is_active = form.is_active.data
        player = Player(0, full_name, first_name, last_name, is_active)
        try:
            db.update_player(player_id, player)
        except Error as e:
            if isinstance(e, errors.UniqueViolation):
                flash("Values must be unique!", "danger ")
            return render_template("player_edit.html", form=form)
        flash("Player is updated.", "success ")
        return redirect(url_for("player_page", player_id=player_id))
    form.full_name.data = player.full_name
    form.first_name.data = player.first_name
    form.last_name.data = player.last_name
    form.is_active.data = player.is_active
    return render_template("player_edit.html", form=form)

def drafts_page():
    db = current_app.config["db"]
    drafts = db.get_drafts()
    return render_template("drafts.html", drafts=drafts)

def draft_page(id):
    db = current_app.config["db"]
    draft = db.get_draft(id)
    if draft is None:
        abort(404)  #HTTP “Not Found” (404) error.
    return render_template("draft.html", draft=draft)

@login_required
def add_draft_page():
    if not current_user.is_admin:
        abort(401) # “Unauthorized” error
    form = DraftAddForm()
    db = current_app.config["db"]
    if form.validate_on_submit():
        yearDraft = form.data["yearDraft"]
        numberPickOverAll = form.data["numberPickOverAll"]
        numberRound = form.data["numberRound"]
        numberRoundPick = form.data["numberRoundPick"]
        nameOrganizationFrom = form.data["nameOrganizationFrom"]
        typeOrganizationFrom = form.data["typeOrganizationFrom"]
        idPlayer = form.data["idPlayer"]
        team_id = form.data["team_id"]
        Player_Profile_Flag = form.data["Player_Profile_Flag"]
        slugOrganizationTypeFrom = form.data["slugOrganizationTypeFrom"]
        locationOrganizationFrom = form.data["locationOrganizationFrom"]
        draft = Draft(0, yearDraft, numberPickOverAll, numberRound, numberRoundPick,nameOrganizationFrom,typeOrganizationFrom,idPlayer,team_id,Player_Profile_Flag,slugOrganizationTypeFrom,locationOrganizationFrom)
        try:
            draft = db.add_draft(draft)
        except Error as e:
            if isinstance(e, errors.ForeignKeyViolation):
                flash("There is no related team or player!", "danger")
            return render_template("add_draft.html", form=form)
        flash("Draft is added.", "success")
        # that creates a problem, calls /team_attributess/0 
        # return redirect(url_for("team_attributes_page", team_id=team_id)) 
        return redirect(url_for("drafts_page")) 
    return render_template("add_draft.html", form=form)

@login_required
def draft_edit_page(id):
    if not current_user.is_admin:
        abort(401) # “Unauthorized” error
    db = current_app.config["db"]
    draft = db.get_draft(id)
    if draft is None:
        abort(404)  #HTTP “Not Found” (404) error.
    form = DraftEditForm()
    if form.validate_on_submit():
        yearDraft = form.data["yearDraft"]
        numberPickOverAll = form.data["numberPickOverAll"]
        numberRound = form.data["numberRound"]
        numberRoundPick = form.data["numberRoundPick"]
        nameOrganizationFrom = form.data["nameOrganizationFrom"]
        typeOrganizationFrom = form.data["typeOrganizationFrom"]
        Player_Profile_Flag = form.data["Player_Profile_Flag"]
        slugOrganizationTypeFrom = form.data["slugOrganizationTypeFrom"]
        locationOrganizationFrom = form.data["locationOrganizationFrom"]
        draft = Draft(id, yearDraft, numberPickOverAll, numberRound, numberRoundPick,nameOrganizationFrom,typeOrganizationFrom,draft.idPlayer,draft.team_id,Player_Profile_Flag,slugOrganizationTypeFrom,locationOrganizationFrom)
        try:
            db.update_draft(id, draft)
        except Error as e:
            if isinstance(e, errors.UniqueViolation):
                flash("Values must be unique!", "danger ")
            flash("Hİ")
            return render_template("draft_edit.html", form=form)
        flash("Draft is updated.", "success ")
        return redirect(url_for("draft_page", id = draft.id))
    # if not valid return values
    form.yearDraft.data = draft.yearDraft
    form.numberPickOverAll.data = draft.numberPickOverAll
    form.numberRound.data = draft.numberRound
    form.numberRoundPick.data = draft.numberRoundPick
    form.nameOrganizationFrom.data = draft.nameOrganizationFrom
    form.typeOrganizationFrom.data = draft.typeOrganizationFrom
    form.Player_Profile_Flag.data = draft.Player_Profile_Flag
    form.slugOrganizationTypeFrom.data = draft.slugOrganizationTypeFrom
    form.locationOrganizationFrom.data = draft.locationOrganizationFrom
    form.idPlayer.data = draft.idPlayer
    form.team_id.data = draft.team_id
    return render_template("draft_edit.html", form=form)

@login_required
def draft_delete_page(id):
    if not current_user.is_admin:
        abort(401) # “Unauthorized” error
    db = current_app.config["db"]
    deleted_draft = db.get_draft(id)
    db.delete_draft(id,deleted_draft)
    drafts = db.get_drafts()
    flash("Draft deleted","success ")
    return render_template("drafts.html", drafts = drafts)

def draft_combines_page():
    db = current_app.config["db"]
    draft_combines = db.get_draft_combines()
    return render_template("draft_combines.html", draft_combines=draft_combines)

def draft_combine_page(id):
    db = current_app.config["db"]
    draft_combine = db.get_draft_combine(id)
    if draft_combine is None:
        abort(404)  #HTTP “Not Found” (404) error.
    return render_template("draft_combine.html", draft_combine=draft_combine)

@login_required
def add_draft_combine_page():
    if not current_user.is_admin:
        abort(401) # “Unauthorized” error
    form = DraftCombineEditForm()
    db = current_app.config["db"]
    if form.validate_on_submit():
        yearCombine = form.data["yearCombine"]
        idPlayer = form.data["idPlayer"]
        slugPosition = form.data["slugPosition"]
        heightWOShoesInches = form.data["heightWOShoesInches"]
        heightWOShoes = form.data["heightWOShoes"]
        weightLBS = form.data["weightLBS"]
        wingspanInches = form.data["wingspanInches"]
        wingspan = form.data["wingspan"]
        reachStandingInches = form.data["reachStandingInches"]
        reachStandingO = form.data["reachStandingO"]
        verticalLeapStandingInches = form.data["verticalLeapStandingInches"]
        verticalLeapMaxInches = form.data["verticalLeapMaxInches"]
        timeLaneAgility = form.data["timeLaneAgility"]
        timeThreeQuarterCourtSprint = form.data["timeThreeQuarterCourtSprint"]
        repsBenchPress135 = form.data["repsBenchPress135"]
        draft_combine = Draft_Combine(0, yearCombine,idPlayer,slugPosition ,heightWOShoesInches,heightWOShoes,weightLBS,wingspanInches,wingspan,reachStandingInches ,reachStandingO,verticalLeapStandingInches,verticalLeapMaxInches,timeLaneAgility,timeThreeQuarterCourtSprint,repsBenchPress135)
        try:
            draft_combine = db.add_draft_combine(draft_combine)
        except Error as e:
            if isinstance(e, errors.ForeignKeyViolation):
                flash("There is no related player!", "danger")
            return render_template("draft_combine_add.html", form=form)
        flash("Draft Combine is added.", "success")
        return redirect(url_for("draft_combines_page")) 
    return render_template("draft_combine_add.html", form=form)

@login_required
def draft_combine_edit_page(id):
    if not current_user.is_admin:
        abort(401) # “Unauthorized” error
    db = current_app.config["db"]
    draft_combine = db.get_draft_combine(id)
    if draft_combine is None:
        abort(404)  #HTTP “Not Found” (404) error.
    form = DraftCombineEditForm()
    if form.validate_on_submit():
        yearCombine = form.data["yearCombine"]
        slugPosition = form.data["slugPosition"]
        heightWOShoesInches = form.data["heightWOShoesInches"]
        heightWOShoes = form.data["heightWOShoes"]
        weightLBS = form.data["weightLBS"]
        wingspanInches = form.data["wingspanInches"]
        wingspan = form.data["wingspan"]
        reachStandingInches = form.data["reachStandingInches"]
        reachStandingO = form.data["reachStandingO"]
        verticalLeapStandingInches = form.data["verticalLeapStandingInches"]
        verticalLeapMaxInches = form.data["verticalLeapMaxInches"]
        timeLaneAgility = form.data["timeLaneAgility"]
        timeThreeQuarterCourtSprint = form.data["timeThreeQuarterCourtSprint"]
        repsBenchPress135 = form.data["repsBenchPress135"]
        draft_combine = Draft_Combine(id, yearCombine,draft_combine.idPlayer,slugPosition ,heightWOShoesInches,heightWOShoes,weightLBS,wingspanInches,wingspan,reachStandingInches ,reachStandingO,verticalLeapStandingInches,verticalLeapMaxInches,timeLaneAgility,timeThreeQuarterCourtSprint,repsBenchPress135)
        try:
            db.update_draft_combine(id, draft_combine)
        except Error as e:
            if isinstance(e, errors.UniqueViolation):
                flash("Values must be unique!", "danger ")
            flash("Hİ")
            return render_template("draft_combine_edit.html", form=form)
        flash("Draft is updated.", "success ")
        return redirect(url_for("draft_combine_page", id = draft_combine.id))
    # if not valid return values
    form.yearCombine.data = draft_combine.yearCombine
    form.idPlayer.data = draft_combine.idPlayer
    form.slugPosition.data = draft_combine.slugPosition
    form.heightWOShoesInches.data = draft_combine.heightWOShoesInches
    form.heightWOShoes.data = draft_combine.heightWOShoes
    form.weightLBS.data = draft_combine.weightLBS
    form.wingspanInches.data = draft_combine.wingspanInches
    form.wingspan.data = draft_combine.wingspan
    form.reachStandingInches.data = draft_combine.reachStandingInches
    form.idPlayer.data = draft_combine.idPlayer
    form.reachStandingO.data = draft_combine.reachStandingO
    form.verticalLeapStandingInches.data = draft_combine.verticalLeapStandingInches
    form.timeLaneAgility.data = draft_combine.timeLaneAgility
    form.timeThreeQuarterCourtSprint.data = draft_combine.timeThreeQuarterCourtSprint
    form.repsBenchPress135.data = draft_combine.repsBenchPress135
    return render_template("draft_combine_edit.html", form=form)

@login_required
def draft_combine_delete_page(id):
    if not current_user.is_admin:
        abort(401) # “Unauthorized” error
    db = current_app.config["db"]
    deleted_draft_combine = db.get_draft_combine(id)
    db.delete_draft_combine(id,deleted_draft_combine)
    draft_combines = db.get_draft_combines()
    flash("Draft Combine deleted","success ")
    return render_template("draft_combines.html", draft_combines = draft_combines)

def players_attributes_page():
    db = current_app.config["db"]
    if request.method == "GET":
        player_attributes = db.get_players_attributes()
        return render_template("player_attributes.html", player_attributes=player_attributes)
    else:
        player_attributes_to_delete = request.form.get("player_attributes_to_delete")
        db.delete_player_attributes(int(player_attributes_to_delete))
        flash("Player attributes are deleted.", "success")
        return redirect(url_for("players_attributes_page"))

def player_attributes_page(player_id):
    db = current_app.config["db"]
    player_attributes = db.get_player_attributes(player_id)
    if player_attributes is None:
        abort(404)  #HTTP “Not Found” (404) error.
    return render_template("individual_player_attributes.html", player_attributes=player_attributes)

@login_required
def edit_player_attributes_page(player_attributes_id):
    if not current_user.is_admin:
        abort(401) # “Unauthorized” error
    form = PlayerAttributesEditForm()
    
    db = current_app.config["db"]
    form.teams.choices = db.get_teams_for_player_attributes()
    player_attributes = db.get_player_attributes(player_attributes_id)
    if player_attributes is None:
        abort(404)  #HTTP “Not Found” (404) error.
    
    if form.validate_on_submit():
        first_name = form.data["first_name"]
        last_name = form.data["last_name"]
        display_fi_last = form.data["display_fi_last"]
        player_slug = form.data["player_slug"]
        birthdate = form.data["birthdate"]
        country = form.data["country"]
        last_affiliation = form.data["last_affiliation"]
        height = form.data["height"]
        weight = form.data["weight"]
        season_exp = form.data["season_exp"]
        jersey = form.data["jersey"]
        position = form.data["position"]
        rosterstatus = form.data["rosterStatus"]
        games_played_current_season_flag = form.data["games_played_current_season_flag"]
        teams = form.teams.data
        team_name = db.get_team_name(teams)
        playercode = form.data["playerCode"]
        from_year = form.data["from_year"]
        to_year = form.data["to_year"]
        dleague_flag = form.data["dleague_flag"]
        nba_flag = form.data["nba_flag"]
        games_played_flag = form.data["games_played_flag"]
        draft_year = form.data["draft_year"]
        draft_round = form.data["draft_round"]
        draft_number = form.data["draft_number"]
        pts = form.data["pts"]
        ast = form.data["ast"]
        reb = form.data["reb"]
        all_star_appearances = form.data["all_star_appearances"]
        pie = form.data["pie"]
        if(form.data["weight"] == ''):
            weight = 0
        if(form.data["pts"] == ''):
            pts = 0
        if(form.data["ast"] == ''):
            ast = 0
        if(form.data["reb"] == ''):
            reb = 0
        if(form.data["all_star_appearances"] == ''):
            all_star_appearances = 0
        if(form.data["pie"] == ''):
            pie = 0
        player_attributes = PlayerAttributes(player_attributes_id, first_name, last_name, display_fi_last, player_slug, birthdate, country, last_affiliation, height, weight, season_exp, jersey, position, rosterstatus, games_played_current_season_flag, teams, team_name, playercode, from_year, to_year, dleague_flag, nba_flag, games_played_flag, draft_year, draft_round, draft_number, pts, ast, reb, all_star_appearances, pie)
        db.update_player_attributes(player_attributes_id, player_attributes)
        flash("Player attributes are updated.", "success")
        return redirect(url_for("player_attributes_page", player_id=player_attributes_id))
    if player_attributes is None:
        return render_template("player_attributes_edit.html", form=form)
    form.first_name.data = player_attributes.first_name
    form.last_name.data = player_attributes.last_name
    form.display_fi_last.data = player_attributes.display_fi_last  
    form.player_slug.data = player_attributes.player_slug
    form.birthdate.data = player_attributes.birthdate
    form.country.data = player_attributes.country
    form.last_affiliation.data = player_attributes.last_affiliation
    form.height.data = player_attributes.height
    form.weight.data = player_attributes.weight
    form.season_exp.data = player_attributes.season_exp
    form.jersey.data = player_attributes.jersey
    form.position.data = player_attributes.position
    form.rosterStatus.data = player_attributes.rosterStatus
    form.games_played_current_season_flag.data = player_attributes.games_played_current_season_flag
    form.teams.data = player_attributes.team_name
    form.playerCode.data = player_attributes.playerCode
    form.from_year.data = player_attributes.from_year
    form.to_year.data = player_attributes.to_year
    form.dleague_flag.data = player_attributes.dleague_flag
    form.nba_flag.data = player_attributes.nba_flag
    form.games_played_flag.data = player_attributes.games_played_flag
    form.draft_year.data = player_attributes.draft_year
    form.draft_round.data = player_attributes.draft_round
    form.draft_number.data = player_attributes.draft_number
    form.pts.data = player_attributes.pts
    form.ast.data = player_attributes.ast
    form.reb.data = player_attributes.reb
    form.all_star_appearances.data = player_attributes.all_star_appearances
    form.pie.data = player_attributes.pie
    return render_template("player_attributes_edit.html", form=form)

@login_required
def add_player_attributes_page():
    if not current_user.is_admin:
        abort(401) # “Unauthorized” error
    form = PlayerAttributesAddForm()
    db = current_app.config["db"]
    form.players.choices = db.get_players_with_empty_attributes()
    form.teams.choices = db.get_teams_for_player_attributes()
    
    if form.validate_on_submit():
        player = form.players.data
        first_name = form.data["first_name"]
        last_name = form.data["last_name"]
        display_fi_last = form.data["display_fi_last"]
        player_slug = form.data["player_slug"]
        birthdate = form.data["birthdate"]
        country = form.data["country"]
        last_affiliation = form.data["last_affiliation"]
        height = form.data["height"]
        weight = form.data["weight"]
        season_exp = form.data["season_exp"]
        jersey = form.data["jersey"]
        position = form.data["position"]
        rosterstatus = form.data["rosterStatus"]
        games_played_current_season_flag = form.data["games_played_current_season_flag"]
        teams = form.teams.data
        team_name = db.get_team_name(teams)
        playercode = form.data["playerCode"]
        from_year = form.data["from_year"]
        to_year = form.data["to_year"]
        dleague_flag = form.data["dleague_flag"]
        nba_flag = form.data["nba_flag"]
        games_played_flag = form.data["games_played_flag"]
        draft_year = form.data["draft_year"]
        draft_round = form.data["draft_round"]
        draft_number = form.data["draft_number"]
        pts = form.data["pts"]
        ast = form.data["ast"]
        reb = form.data["reb"]
        all_star_appearances = form.data["all_star_appearances"]
        pie = form.data["pie"]
        if(form.data["height"] == ''):
            height = 0
        if(form.data["season_exp"] == ''):
            season_exp = 0
        if(form.data["weight"] == ''):
            weight = 0
        if(form.data["pts"] == ''):
            pts = 0
        if(form.data["ast"] == ''):
            ast = 0
        if(form.data["reb"] == ''):
            reb = 0
        if(form.data["all_star_appearances"] == ''):
            all_star_appearances = 0
        if(form.data["pie"] == ''):
            pie = 0
        player_attributes = PlayerAttributes(player, first_name, last_name, display_fi_last, player_slug, birthdate, country, last_affiliation, height, weight, season_exp, jersey, position, rosterstatus, games_played_current_season_flag, teams, team_name, playercode, from_year, to_year, dleague_flag, nba_flag, games_played_flag, draft_year, draft_round, draft_number, pts, ast, reb, all_star_appearances, pie)
        try:
            player_attributes_id = db.add_player_attributes(player_attributes)
        except Error as e:
            flash(e, "danger")
            if isinstance(e, errors.ForeignKeyViolation):
                flash("There is no related Player!", "danger")
            return render_template("player_attributes_add.html", form=form)
        flash("Player attributes are added.", "success")
        return redirect(url_for("players_attributes_page"))
    return render_template("player_attributes_add.html", form=form)

@login_required
def delete_player_attributes_page(id):
    if not current_user.is_admin:
        abort(401) # “Unauthorized” error
    db = current_app.config["db"]
    db.delete_player_attributes(id)
    players_attributes = db.get_players_attributes()
    flash("Draft deleted","success ")
    return render_template("player_attributes.html", player_attributes=players_attributes)

def players_photos_page():
    db = current_app.config["db"]
    player_photos = db.get_players_photos()
    return render_template("player_photos.html", player_photos=player_photos)

def players_bios_page():
    db = current_app.config["db"]
    player_bios = db.get_players_bios()
    return render_template("player_bios.html", player_bios=player_bios)

def games_page():
    db = current_app.config["db"]
    if (request.method == "GET"):
        games = db.get_games()
        return render_template("game.html", games=games)
    else:
        wanted = request.form.get("search")
        if wanted:
            games = db.get_games_with_search(wanted)
            if games == None:
                flash("Can't find anything!", "warning")
                games = db.get_games()
                return render_template("game.html", games = games)
            else:
                return render_template("game.html", games = games)
        if not current_user.is_admin:
            abort(401)
        deletedMatches = request.form.getlist("deletedMatch")
        for eachMatch in deletedMatches:
            db.delete_game(int(eachMatch))

        flash("Match is deleted.", "success")
        return redirect(url_for("games_page"))
def game_page(gameID):
    db = current_app.config["db"]
    game = db.get_game(gameID)
    if game is None:
        abort(404)
    return render_template("game_single.html", game = game)

@login_required
def game_add_page():
    db = current_app.config["db"]
    if not current_user.is_admin:
        abort(401) # “Unauthorized” error
    form = GameAddForm()
    if form.validate_on_submit():
        teamIDHome = form.data["teamIDHome"]
        teamNameHome = form.data["teamNameHome"]
        gameDate = form.data["gameDate"]
        WLHome = form.data["WLHome"]
        pointsHome = form.data["pointsHome"]
        teamIDAway = form.data["teamIDAway"]
        teamNameAway = form.data["teamNameAway"]
        WLAway = form.data["WLAway"]
        pointsAway = form.data["pointsAway"]
        num = db.get_max_gameID() + 1
        num2 = db.get_min_gameID()
        game = Game(num, teamIDHome, teamNameHome, gameDate, WLHome, pointsHome, teamIDAway, teamNameAway, WLAway, pointsAway)
        db = current_app.config["db"]
        if ((WLHome == "W" and pointsAway > pointsHome) or (WLHome == "L" and pointsHome > pointsAway)):
            flash("The given Win - Lose situation doesn't comply with the score!", "danger")
            return render_template("game_add.html", form=form, type="Add")
        if(WLHome == WLAway and WLHome =="W"):
            flash("How come both teams won the match :)", "danger")
            return render_template("game_add.html", form=form, type="Add")
        if (WLHome == WLAway and WLHome == "L"):
            flash("How come both teams lost the match :)", "danger")
            return render_template("game_add.html", form=form, type="Add")
        if (teamIDHome < num2 or teamIDHome > num or teamIDAway < num2 or teamIDAway > num):
            flash("Please enter a valid Team ID", "danger")
            return render_template("game_add.html", form=form, type="Add")
        team1Name = db.get_team_name(teamIDHome)
        team2Name = db.get_team_name(teamIDAway)
        if(team1Name != teamNameHome or team2Name != teamNameAway):
            flash("Team name(s) should be in compliance with team ID(s)", "danger")
            return render_template("game_add.html", form=form, type="Add")
        try:
            gameID = db.add_game(game)
        except Error as e:
            if isinstance(e, errors.UniqueViolation):
                flash("Games must have unique IDs!", "danger")
            if isinstance(e,errors.ForeignKeyViolation):
                flash("There is no related team(s)", "danger")
            return render_template("game_add.html", form=form, type="Add")
        flash("Game is added.", "success")
        return redirect(url_for("game_page", gameID=gameID))
    return render_template("game_add.html", form=form, type="Add")

@login_required
def game_edit_page(gameID):

    db = current_app.config["db"]
    game = db.get_game(gameID)
    if game is None:
        abort(404)
    if not current_user.is_admin:
        abort(401) # “Unauthorized” error
    form = GameEditForm()
    if form.validate_on_submit():

        teamIDHome = form.data["teamIDHome"]
        teamNameHome = form.data["teamNameHome"]
        gameDate = form.data["gameDate"]
        WLHome = form.data["WLHome"]
        pointsHome = form.data["pointsHome"]
        teamIDAway = form.data["teamIDAway"]
        teamNameAway = form.data["teamNameAway"]
        WLAway = form.data["WLAway"]
        pointsAway = form.data["pointsAway"]
        selectedGame = Game(gameID, teamIDHome, teamNameHome, gameDate, WLHome, pointsHome, teamIDAway, teamNameAway, WLAway, pointsAway)
        if (WLHome == "W" and pointsAway > pointsHome):
            flash("The given Win - Lose situation doesn't comply with the score!", "danger")
            return render_template("game_edit.html", form=form, type="Edit")
        if(WLHome == WLAway and WLHome =="W"):
            flash("How come both teams won the match :)", "danger")
            return render_template("game_edit.html", form=form, type="Edit")
        if (WLHome == WLAway and WLHome == "L"):
            flash("How come both teams lost the match :)", "danger")
            return render_template("game_edit.html", form=form, type="Edit")
        try:
            db.update_game2(gameID, selectedGame, game)
        except Error as e:
            if isinstance(e,errors.UniqueViolation):
                flash("Values must be unique!", "danger ")
            return render_template("game_edit.html", form=form, type="Edit")
        flash("Game is updated.", "success ")
        return redirect(url_for("games_page"))


    # if not valid return values
    form.teamIDHome.data = game.teamIDHome
    form.teamNameHome.data = game.teamNameHome
    form.gameDate.data = game.gameDate
    form.WLHome.data = game.WLHome
    form.pointsHome.data = game.pointsHome
    form.teamIDAway.data = game.teamIDAway
    form.teamNameAway.data = game.teamNameAway
    form.WLAway.data = game.WLAway
    form.pointsAway.data = game.pointsAway
    return render_template("game_edit.html", form=form, type="Edit")

def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.data["username"]
        user = get_user(username)
        if user is not None:
            password = form.data["password"]
            if hasher.verify(password, user.password):
                login_user(user)
                # flash function registers a message that the user will see on the next page
                flash("You have logged in.", "success")
                # if an anonymous user visits the /movies/add page, they will be redirected 
                # to the login page (because of the login_view setting, 
                # and after successfully logging in, this part will redirect the user back to
                #  the movie addition page.
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)
        flash("Invalid credentials!", "danger")
    return render_template("login.html", form=form)


def logout_page():
    logout_user()
    flash("You have logged out.", "warning")
    return redirect(url_for("home_page"))