import psycopg2 as dbapi2
from models.PlayerAttributes import PlayerAttributes
from models.PlayerPhoto import PlayerPhoto
from models.PlayerBio import PlayerBio

from models.team import Team
from models.team_attributes import TeamAttributes
from models.Player import Player
from models.draft import Draft
from models.draft_combine import Draft_Combine
from models.game import game as Game

class Database:
    def __init__(self, db_url):
        self.db_url = db_url
            
    def get_team(self, team_id):
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "SELECT full_name, abbreviation, nickname, city, state, year_founded FROM team WHERE (id = %s);"
                cursor.execute(query, (team_id,))
                if cursor.rowcount == 0:
                    return None
                full_name, abbreviation, nickname, city, state, year_founded = cursor.fetchone()
        team = Team(team_id, full_name, abbreviation, nickname, city, state, year_founded)
        return team
        
    def get_team_abbr(self, team_id):
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "SELECT abbreviation FROM team WHERE (id = %s);"
                cursor.execute(query, (team_id,))
                abbreviation = cursor.fetchone()[0]
        return abbreviation
    
    def get_teams(self):
        teams = []
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "SELECT id, full_name, abbreviation, nickname, city, state, year_founded FROM team ORDER BY id;"
                cursor.execute(query)
                for id, full_name, abbreviation, nickname, city, state, year_founded in cursor:
                    teams.append((id, Team(id, full_name, abbreviation, nickname, city, state, year_founded)))
        return teams
    
    def get_teams_by_search(self, search_string):
        teams = []
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = """SELECT id, full_name, abbreviation, nickname, city, state, year_founded FROM team 
                        WHERE id::text LIKE %s OR full_name LIKE %s OR abbreviation LIKE %s OR nickname LIKE %s OR 
                        city LIKE %s OR state LIKE %s OR year_founded::text LIKE %s 
                        ORDER BY id;"""
                search_string = "%" + search_string + "%"
                cursor.execute(query, (search_string, search_string, search_string, search_string, search_string, 
                                       search_string, search_string,))
                if cursor.rowcount == 0:
                    return None
                for id, full_name, abbreviation, nickname, city, state, year_founded in cursor:
                    teams.append((id, Team(id, full_name, abbreviation, nickname, city, state, year_founded)))
        return teams
    
    def get_teams_for_player_attributes(self):
        teams = []
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "SELECT id, full_name FROM team ORDER BY id;"
                cursor.execute(query)
                for id, full_name in cursor:
                    teams.append((id, full_name))
        return teams
    
    def get_team_name(self, team_id):
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "SELECT full_name FROM team WHERE (id = %s);"
                cursor.execute(query, (team_id,))
                name = cursor.fetchone()[0]
        return name

    def add_team(self, team):
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = """INSERT INTO team (full_name, abbreviation, nickname, city, state, year_founded) VALUES 
                (%s, %s, %s, %s, %s, %s) RETURNING id"""
                cursor.execute(query, (team.full_name, team.abbreviation, team.nickname, team.city, team.state,
                                       team.year_founded))
                team_key = cursor.fetchone()[0]
        return team_key

    def update_team(self, team_key, team):
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = """UPDATE team SET full_name = %s, abbreviation = %s, nickname = %s, city = %s, state = %s, 
                year_founded = %s WHERE (id = %s)"""
                cursor.execute(query, (team.full_name, team.abbreviation, team.nickname, team.city, team.state,
                                       team.year_founded, team_key))

    def delete_team(self, team_key):
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "DELETE FROM team WHERE (id = %s)"
                cursor.execute(query, (team_key,))

    def get_teams_with_empty_attributes(self):
        teams_attributes = []
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = """SELECT team.id, team.full_name FROM team_attributes RIGHT JOIN team 
                ON team.id = team_attributes.team_id WHERE team_attributes.team_id IS NULL ORDER BY team.id;"""
                cursor.execute(query)
                if cursor.rowcount == 0:
                    return None
                for team_id, full_name in cursor:
                    teams_attributes.append((team_id, full_name))
        return teams_attributes
    
    def get_team_attributes(self, team_id):
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = """SELECT arena, arena_capacity, owner, general_manager, head_coach, d_league_affiliation, 
                facebook_website_link, instagram_website_link, twitter_website_link FROM team_attributes WHERE (team_id = %s);"""
                cursor.execute(query, (team_id,))
                if cursor.rowcount == 0:
                    return None
                (arena, arena_capacity, owner, general_manager, head_coach, d_league_affiliation, 
                facebook_website_link, instagram_website_link, twitter_website_link )= cursor.fetchone()
        team_attributes = TeamAttributes(team_id, arena, arena_capacity, owner, general_manager, 
                                        head_coach, d_league_affiliation, facebook_website_link, 
                                        instagram_website_link, twitter_website_link)
        return team_attributes

    def get_teams_attributes(self):
        teams_attributes = []
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = """SELECT team_id, arena, arena_capacity, owner, general_manager, head_coach,
                d_league_affiliation, facebook_website_link, instagram_website_link, twitter_website_link 
                FROM team_attributes ORDER BY team_id;"""
                cursor.execute(query)
                for (team_id, arena, arena_capacity, owner, general_manager, head_coach, d_league_affiliation,
                facebook_website_link, instagram_website_link, twitter_website_link) in cursor:
                    teams_attributes.append((team_id, TeamAttributes(team_id, arena, arena_capacity, 
                                                                     owner, general_manager, head_coach, 
                                                                     d_league_affiliation, facebook_website_link, 
                                                                     instagram_website_link, twitter_website_link)))
        return teams_attributes

    def get_teams_attributes_by_search(self, search_string):
        teams_attributes = []
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = """SELECT team_id, arena, arena_capacity, owner, general_manager, head_coach, d_league_affiliation, facebook_website_link, instagram_website_link, twitter_website_link FROM team_attributes
                        WHERE team_id::text LIKE %s OR arena LIKE %s OR arena_capacity::text LIKE %s OR owner LIKE %s OR general_manager LIKE %s OR head_coach LIKE %s OR d_league_affiliation LIKE %s 
                         ORDER BY team_id;"""
                search_string = "%" + search_string + "%"
                cursor.execute(query, (search_string, search_string, search_string, search_string, search_string, search_string, search_string,))
                if cursor.rowcount == 0:
                    return None
                for team_id, arena, arena_capacity, owner, general_manager, head_coach, d_league_affiliation, facebook_website_link, instagram_website_link, twitter_website_link in cursor:
                    teams_attributes.append((team_id, TeamAttributes(team_id, arena, arena_capacity, owner, general_manager, head_coach, d_league_affiliation, facebook_website_link, instagram_website_link, twitter_website_link)))
        return teams_attributes
    
    def add_team_attributes(self, team_attributes):
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "INSERT INTO team_attributes (team_id, arena, arena_capacity, owner, general_manager, head_coach, d_league_affiliation, facebook_website_link, instagram_website_link, twitter_website_link) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING team_id"
                cursor.execute(query, (team_attributes.team_id, team_attributes.arena, team_attributes.arena_capacity, team_attributes.owner, team_attributes.general_manager, team_attributes.head_coach, team_attributes.d_league_affiliation, team_attributes.facebook_website_link, team_attributes.instagram_website_link, team_attributes.twitter_website_link))
                team_attributes_key = cursor.fetchone()[0]
        return team_attributes_key

    def update_team_attributes(self, team_attributes_key, team_attributes):
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "UPDATE team_attributes SET team_id = %s, arena = %s, arena_capacity = %s, owner = %s, general_manager = %s, head_coach = %s, d_league_affiliation = %s, facebook_website_link = %s, instagram_website_link = %s, twitter_website_link = %s WHERE (team_id = %s)"
                cursor.execute(query, (team_attributes.team_id, team_attributes.arena, team_attributes.arena_capacity, team_attributes.owner, team_attributes.general_manager, team_attributes.head_coach, team_attributes.d_league_affiliation, team_attributes.facebook_website_link, team_attributes.instagram_website_link, team_attributes.twitter_website_link, team_attributes_key))

    def delete_team_attributes(self, team_attributes_key):
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "DELETE FROM team_attributes WHERE (team_id = %s)"
                cursor.execute(query, (team_attributes_key,))

    def get_players(self):
        players = []
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "SELECT id, full_name, first_name, last_name, is_active FROM Player ORDER BY id;"
                cursor.execute(query)
                for id, full_name, first_name, last_name, is_active in cursor:
                    players.append(( Player(id, full_name, first_name, last_name, is_active)))
        return players
    
    def get_player(self, player_id):
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "SELECT id, full_name, first_name, last_name, is_active FROM player WHERE (id = %s);"
                cursor.execute(query, (player_id,))
                id, full_name, first_name, last_name, is_active = cursor.fetchone()
        player = Player(id, full_name, first_name, last_name, is_active)
        return player
    
    def get_player_with_name(self, name):
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "SELECT id, full_name, first_name, last_name, is_active FROM player WHERE (id = %s);"
                cursor.execute(query, (name,))
                id, full_name, first_name, last_name, is_active = cursor.fetchone()
        player = Player(id, full_name, first_name, last_name, is_active)
        return player
    
    def get_players_for_player_attributes(self):
        players = []
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "SELECT id, full_name FROM Player ORDER BY id;"
                cursor.execute(query)
                for id, full_name in cursor:
                    players.append((id, full_name))
        return players
    
    def get_players_with_empty_attributes(self):
        players = []
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "SELECT Player.id, Player.full_name FROM Player_Attributes RIGHT JOIN Player ON Player.id = Player_Attributes.id WHERE Player_Attributes.id IS NULL ORDER BY Player.id;"
                cursor.execute(query)
                for id, full_name in cursor:
                    players.append((id, full_name))
        return players
    
    def add_player(self, player):
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "INSERT INTO Player (full_name, first_name, last_name, is_active) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (player.full_name, player.first_name, player.last_name, player.is_active))
                player_key = cursor.lastrowid
        return player_key

    def update_player(self, player_id, player):
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "UPDATE Player SET full_name = %s, first_name = %s, last_name = %s, is_active = %s WHERE (id = %s)"
                cursor.execute(query, (player.full_name, player.first_name, player.last_name, player.is_active, player_id))
                
    def delete_player(self, player_id):
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "DELETE FROM Player WHERE (id = %s)"
                cursor.execute(query, (player_id,))
    
    
    def get_player_attributes(self, player_id):
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "SELECT id, first_name, last_name, display_fi_last, player_slug, birthdate, country, last_affilation, height, weight, season_exp, jersey, position, rosterstatus, games_played_current_season_flag, team_id, team_name, playercode, from_year, to_year, dleague_flag, nba_flag, games_played_flag, draft_year, draft_round ,draft_number, pts, ast, reb, all_star_appearances, pie FROM Player_Attributes WHERE (id = %s);"
                cursor.execute(query, (player_id,))
                id, first_name, last_name, display_fi_last, player_slug, birthdate, country, last_affilation, height, weight, season_exp, jersey, position, rosterstatus, games_played_current_season_flag, team_id, team_name, playercode, from_year, to_year, dleague_flag, nba_flag, games_played_flag, draft_year, draft_round, draft_number, pts, ast, reb, all_star_appearances, pie = cursor.fetchone()
            player_attributes = PlayerAttributes(id, first_name, last_name, display_fi_last, player_slug, birthdate, country, last_affilation, height, weight, season_exp, jersey, position, rosterstatus, games_played_current_season_flag, team_id, team_name, playercode, from_year, to_year, dleague_flag, nba_flag, games_played_flag, draft_year, draft_round, draft_number, pts, ast, reb, all_star_appearances, pie)
        return player_attributes

    def get_players_attributes(self):
        player_attributes = []
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "SELECT id, first_name, last_name, display_fi_last, player_slug, birthdate, country, last_affilation, height, weight, season_exp, jersey, position, rosterstatus, games_played_current_season_flag, team_id, team_name, playercode, from_year, to_year, dleague_flag, nba_flag, games_played_flag, draft_year, draft_round ,draft_number, pts, ast, reb, all_star_appearances, pie FROM Player_Attributes;"
                cursor.execute(query)
                for id, first_name, last_name, display_fi_last, player_slug, birthdate, country, last_affilation, height, weight, season_exp, jersey, position, rosterstatus, games_played_current_season_flag, team_id, team_name, playercode, from_year, to_year, dleague_flag, nba_flag, games_played_flag, draft_year, draft_round, draft_number, pts, ast, reb, all_star_appearances, pie in cursor:
                    player_attributes.append(PlayerAttributes(id, first_name, last_name, display_fi_last, player_slug, birthdate, country, last_affilation, height, weight, season_exp, jersey, position, rosterstatus, games_played_current_season_flag, team_id, team_name, playercode, from_year, to_year, dleague_flag, nba_flag, games_played_flag, draft_year, draft_round, draft_number, pts, ast, reb, all_star_appearances, pie))
        return player_attributes
    
    def add_player_attributes(self, player_attributes):
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "INSERT INTO Player_Attributes (id, first_name, last_name, display_fi_last, player_slug, birthdate, country, last_affilation, height, weight, season_exp, jersey, position, rosterstatus, games_played_current_season_flag, team_id, team_name, playercode, from_year, to_year, dleague_flag, nba_flag, games_played_flag, draft_year, draft_round ,draft_number, pts, ast, reb, all_star_appearances, pie) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(query, (player_attributes.id, player_attributes.first_name, player_attributes.last_name, player_attributes.display_fi_last, player_attributes.player_slug, player_attributes.birthdate, player_attributes.country, player_attributes.last_affiliation, player_attributes.height, player_attributes.weight, player_attributes.season_exp, player_attributes.jersey, player_attributes.position, player_attributes.rosterStatus, player_attributes.games_played_current_season_flag, player_attributes.team_id, player_attributes.team_name, player_attributes.playerCode, player_attributes.from_year, player_attributes.to_year, player_attributes.dleague_flag, player_attributes.nba_flag, player_attributes.games_played_flag, player_attributes.draft_year, player_attributes.draft_round, player_attributes.draft_number, player_attributes.pts, player_attributes.ast, player_attributes.reb, player_attributes.all_star_appearances, player_attributes.pie))
                player_attributes_id = cursor.lastrowid
        return player_attributes_id
    
    def update_player_attributes(self, player_attributes_id, player_attributes):
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "UPDATE Player_Attributes SET first_name = %s, last_name = %s, display_fi_last = %s, player_slug = %s, birthdate = %s, country = %s, last_affilation = %s, height = %s, weight = %s, season_exp = %s, jersey = %s, position = %s, rosterstatus = %s, games_played_current_season_flag = %s, team_id = %s, team_name = %s, playercode = %s, from_year = %s, to_year = %s, dleague_flag = %s, nba_flag = %s, games_played_flag = %s, draft_year = %s, draft_round = %s,draft_number = %s, pts = %s, ast = %s, reb = %s, all_star_appearances = %s, pie = %s WHERE (id = %s)"
                cursor.execute(query, (player_attributes.first_name, player_attributes.last_name, player_attributes.display_fi_last, player_attributes.player_slug, player_attributes.birthdate, player_attributes.country, player_attributes.last_affiliation, player_attributes.height, player_attributes.weight, player_attributes.season_exp, player_attributes.jersey, player_attributes.position, player_attributes.rosterStatus, player_attributes.games_played_current_season_flag, player_attributes.team_id, player_attributes.team_name, player_attributes.playerCode, player_attributes.from_year, player_attributes.to_year, player_attributes.dleague_flag, player_attributes.nba_flag, player_attributes.games_played_flag, player_attributes.draft_year, player_attributes.draft_round, player_attributes.draft_number, player_attributes.pts, player_attributes.ast, player_attributes.reb, player_attributes.all_star_appearances, player_attributes.pie, player_attributes_id))
    
    def delete_player_attributes(self, player_attributes_id):
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "DELETE FROM Player_Attributes WHERE (id = %s)"
                cursor.execute(query, (player_attributes_id,))
                
    
    def get_players_photos(self):
        player_photos = []
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "SELECT namePlayer, idPlayer, idTeam, urlPlayerPhoto FROM Player_Photos;"
                cursor.execute(query)
                for namePlayer, idPlayer, idTeam, urlPlayerPhoto in cursor:
                    player_photos.append(PlayerPhoto(namePlayer, idPlayer, idTeam, urlPlayerPhoto))
        return player_photos
    
    def get_players_bios(self):
        player_bios = []
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "SELECT namePlayerBREF, urlPlayerBioBREF, nameTable, urlPlayerImageBREF, slugPlayerBREF, numberTransactionPlayer, dateTransaction, descriptionTransaction, slugSeason, nameTeam, slugLeague, amountSalary, detailsContract, namePosition, heightInches, weightLBS, dateBirth, locationBirthplace, cityBirthplace, stateBirthplace, nameCollege, nameHighSchool, dateNBADebut, career_length, yearsExperience FROM Player_Bios;"
                cursor.execute(query)
                for namePlayerBREF, urlPlayerBioBREF, nameTable, urlPlayerImageBREF, slugPlayerBREF, numberTransactionPlayer, dateTransaction, descriptionTransaction, slugSeason, nameTeam, slugLeague, amountSalary, detailsContract, namePosition, heightInches, weightLBS, dateBirth, locationBirthplace, cityBirthplace, stateBirthplace, nameCollege, nameHighSchool, dateNBADebut, career_length, yearsExperience in cursor:
                    player_bios.append(PlayerBio(namePlayerBREF, urlPlayerBioBREF, nameTable, urlPlayerImageBREF, slugPlayerBREF, numberTransactionPlayer, dateTransaction, descriptionTransaction, slugSeason, nameTeam, slugLeague, amountSalary, detailsContract, namePosition, heightInches, weightLBS, dateBirth, locationBirthplace, cityBirthplace, stateBirthplace, nameCollege, nameHighSchool, dateNBADebut, career_length, yearsExperience))
        return player_bios

    def get_games(self):
        games = []
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "SELECT gameID, teamIDHome, teamNameHome, gameDate, WLHome, pointsHome, teamIDAway, teamNameAway, WLAway, pointsAway FROM Game ORDER BY gameID;"
                cursor.execute(query)
                for gameID,teamIDHome,teamNameHome,gameDate ,WLHome,pointsHome,teamIDAway,teamNameAway,WLAway,pointsAway in cursor:
                    games.append((Game(gameID,teamIDHome,teamNameHome,gameDate ,WLHome,pointsHome,teamIDAway,teamNameAway,WLAway,pointsAway)))
        return games
    def get_game(self,gameID):
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "SELECT gameID, teamIDHome, teamNameHome, gameDate, WLHome, pointsHome, teamIDAway, teamNameAway, WLAway, pointsAway FROM Game WHERE (gameID::INTEGER = %s);"
                cursor.execute(query, (gameID,))
                gameID, teamIDHome, teamNameHome, gameDate, WLHome, pointsHome, teamIDAway, teamNameAway, WLAway, pointsAway = cursor.fetchone()
        game = Game(gameID, teamIDHome, teamNameHome, gameDate, WLHome, pointsHome, teamIDAway, teamNameAway, WLAway, pointsAway)
        return game

    def add_game(self, game):
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "INSERT INTO Game (gameID, teamIDHome, teamNameHome, gameDate, WLHome, pointsHome, teamIDAway, teamNameAway, WLAway, pointsAway) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING gameID"
                cursor.execute(query, (game.gameID, game.teamIDHome, game.teamNameHome, game.gameDate, game.WLHome, game.pointsHome, game.teamIDAway, game.teamNameAway, game.WLAway, game.pointsAway))
                gameKey = cursor.fetchone()[0]
        return gameKey

    def delete_game(self,gameNo):
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "DELETE FROM game WHERE (gameID::INTEGER = %s)"
                cursor.execute(query, (gameNo,))

    def update_game(self, gameID, game):
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "UPDATE Game SET teamIDHome = %s, teamNameHome = %s, gameDate = %s, WLHome = %s, pointsHome = %s, teamIDAway = %s, teamNameAway = %s, WLAway = %s, pointsAway = %s WHERE (gameID = %s);"
                cursor.execute(query, (game.teamIDHome, game.teamNameHome, game.gameDate, game.WLHome, game.pointsHome, game.teamIDAway, game.teamNameAway, game.WLAway, game.pointsAway, gameID ))
    def get_max_gameID(self):
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "SELECT max(gameID) FROM Game"
                cursor.execute(query)
                maxNum = cursor.fetchone()[0]
        return maxNum
    def get_min_gameID(self):
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "SELECT min(gameID) FROM Game"
                cursor.execute(query)
                minNum = cursor.fetchone()[0]
        return minNum

    def get_games_with_search(self,searched):
        games = []
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = """ SELECT gameID, teamIDHome, teamNameHome, gameDate, WLHome, pointsHome, teamIDAway, teamNameAway, WLAway, pointsAway FROM Game
                            WHERE gameID::text LIKE %s OR teamIDHome::text LIKE %s OR teamNameHome LIKE %s OR gameDate LIKE %s OR WLHome LIKE %s OR pointsHome::text LIKE %s OR teamIDAway::text LIKE %s OR teamNameAway LIKE %s OR WLAway LIKE %s OR pointsAway::text LIKE %s;"""
                searched = "%" + searched + "%"
                cursor.execute(query, (searched,searched,searched,searched,searched,searched,searched,searched,searched,searched))
                if cursor.rowcount == 0:
                    return None
                for gameID, teamIDHome, teamNameHome, gameDate, WLHome, pointsHome, teamIDAway, teamNameAway, WLAway, pointsAway in cursor:
                    games.append(Game(gameID, teamIDHome, teamNameHome, gameDate, WLHome, pointsHome, teamIDAway, teamNameAway, WLAway, pointsAway))
        return games

    def update_game2(self, gameID, game, game2):
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                teamIDHome = game2.teamIDHome
                teamIDAway = game2.teamIDAway
                query = "DELETE FROM Game WHERE (gameID = %s)"
                cursor.execute(query, (gameID,))
                query = "INSERT INTO Game (gameID, teamIDHome, teamNameHome, gameDate, WLHome, pointsHome, teamIDAway, teamNameAway, WLAway, pointsAway) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING gameID"
                cursor.execute(query, (gameID, teamIDHome, game.teamNameHome, game.gameDate, game.WLHome, game.pointsHome, teamIDAway, game.teamNameAway, game.WLAway, game.pointsAway))

    def get_drafts(self):
        drafts = []
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "SELECT id,yearDraft,numberPickOverAll,numberRound ,numberRoundPick,nameOrganizationFrom,typeOrganizationFrom,idPlayer,team_id,Player_Profile_Flag ,slugOrganizationTypeFrom,locationOrganizationFrom FROM Draft ORDER BY id;"
                cursor.execute(query)
                for id,yearDraft,numberPickOverAll,numberRound ,numberRoundPick,nameOrganizationFrom,typeOrganizationFrom,idPlayer,team_id,Player_Profile_Flag ,slugOrganizationTypeFrom,locationOrganizationFrom in cursor:
                    drafts.append((Draft(id,yearDraft,numberPickOverAll,numberRound ,numberRoundPick,nameOrganizationFrom,typeOrganizationFrom,idPlayer,team_id,Player_Profile_Flag ,slugOrganizationTypeFrom,locationOrganizationFrom)))
        return drafts
    def get_draft(self, id):
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "SELECT id,yearDraft,numberPickOverAll,numberRound ,numberRoundPick,nameOrganizationFrom,typeOrganizationFrom,idPlayer,team_id,Player_Profile_Flag ,slugOrganizationTypeFrom,locationOrganizationFrom FROM Draft WHERE (id = %s);"
                cursor.execute(query, (id,))
                id,yearDraft,numberPickOverAll,numberRound ,numberRoundPick,nameOrganizationFrom,typeOrganizationFrom,idPlayer,team_id,Player_Profile_Flag ,slugOrganizationTypeFrom,locationOrganizationFrom = cursor.fetchone()
        draft = Draft(id,yearDraft,numberPickOverAll,numberRound ,numberRoundPick,nameOrganizationFrom,typeOrganizationFrom,idPlayer,team_id,Player_Profile_Flag ,slugOrganizationTypeFrom,locationOrganizationFrom)
        return draft
    def add_draft(self, draft):
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "INSERT INTO Draft (yearDraft,numberPickOverAll,numberRound ,numberRoundPick,nameOrganizationFrom,typeOrganizationFrom,idPlayer,team_id,Player_Profile_Flag ,slugOrganizationTypeFrom,locationOrganizationFrom) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s)"
                cursor.execute(query,(draft.yearDraft, draft.numberPickOverAll, draft.numberRound, draft.numberRoundPick,draft.nameOrganizationFrom, draft.typeOrganizationFrom, draft.idPlayer, draft.team_id,draft.Player_Profile_Flag, draft.slugOrganizationTypeFrom, draft.locationOrganizationFrom))
                draft_key = cursor.lastrowid
        return draft_key
    def update_draft(self,id,draft):
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "UPDATE Draft SET yearDraft = %s, numberPickOverAll = %s, numberRound = %s, numberRoundPick = %s, nameOrganizationFrom = %s, typeOrganizationFrom = %s, idPlayer = %s, team_id = %s, Player_Profile_Flag = %s, slugOrganizationTypeFrom = %s, locationOrganizationFrom = %s WHERE (id = %s)"
                cursor.execute(query, (draft.yearDraft, draft.numberPickOverAll, draft.numberRound, draft.numberRoundPick, draft.nameOrganizationFrom, draft.typeOrganizationFrom, draft.idPlayer, draft.team_id, draft.Player_Profile_Flag, draft.slugOrganizationTypeFrom, draft.locationOrganizationFrom,id))
    def delete_draft(self,draft_key,draft):
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "DELETE FROM Draft WHERE (id = %s)"
                cursor.execute(query, (draft_key,))
    def get_draft_combines(self):
        draft_combines = []
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "SELECT id,yearCombine,idPlayer,slugPosition ,heightWOShoesInches,heightWOShoes,weightLBS,wingspanInches,wingspan,reachStandingInches ,reachStandingO,verticalLeapStandingInches,verticalLeapMaxInches,timeLaneAgility,timeThreeQuarterCourtSprint,repsBenchPress135 FROM Draft_Combine ORDER BY id;"
                cursor.execute(query)
                for id,yearCombine,idPlayer,slugPosition ,heightWOShoesInches,heightWOShoes,weightLBS,wingspanInches,wingspan,reachStandingInches ,reachStandingO,verticalLeapStandingInches,verticalLeapMaxInches,timeLaneAgility,timeThreeQuarterCourtSprint,repsBenchPress135 in cursor:
                    draft_combines.append((Draft_Combine(id,yearCombine,idPlayer,slugPosition ,heightWOShoesInches,heightWOShoes,weightLBS,wingspanInches,wingspan,reachStandingInches ,reachStandingO,verticalLeapStandingInches,verticalLeapMaxInches,timeLaneAgility,timeThreeQuarterCourtSprint,repsBenchPress135)))
        return draft_combines
    def get_draft_combine(self, id):
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "SELECT id,yearCombine,idPlayer,slugPosition ,heightWOShoesInches,heightWOShoes,weightLBS,wingspanInches,wingspan,reachStandingInches ,reachStandingO,verticalLeapStandingInches,verticalLeapMaxInches,timeLaneAgility,timeThreeQuarterCourtSprint,repsBenchPress135 FROM Draft_Combine WHERE (id = %s);"
                cursor.execute(query, (id,))
                id,yearCombine,idPlayer,slugPosition ,heightWOShoesInches,heightWOShoes,weightLBS,wingspanInches,wingspan,reachStandingInches ,reachStandingO,verticalLeapStandingInches,verticalLeapMaxInches,timeLaneAgility,timeThreeQuarterCourtSprint,repsBenchPress135 = cursor.fetchone()
        draft_combine = Draft_Combine(id,yearCombine,idPlayer,slugPosition ,heightWOShoesInches,heightWOShoes,weightLBS,wingspanInches,wingspan,reachStandingInches ,reachStandingO,verticalLeapStandingInches,verticalLeapMaxInches,timeLaneAgility,timeThreeQuarterCourtSprint,repsBenchPress135)
        return draft_combine
    def add_draft_combine(self, draft_combine):
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "INSERT INTO Draft_Combine (yearCombine,idPlayer,slugPosition ,heightWOShoesInches,heightWOShoes,weightLBS,wingspanInches,wingspan,reachStandingInches ,reachStandingO,verticalLeapStandingInches,verticalLeapMaxInches,timeLaneAgility,timeThreeQuarterCourtSprint,repsBenchPress135) VALUES (%s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s)"
                cursor.execute(query,(draft_combine.yearCombine,draft_combine.idPlayer,draft_combine.slugPosition ,draft_combine.heightWOShoesInches,draft_combine.heightWOShoes,draft_combine.weightLBS,draft_combine.wingspanInches,draft_combine.wingspan,draft_combine.reachStandingInches ,draft_combine.reachStandingO,draft_combine.verticalLeapStandingInches,draft_combine.verticalLeapMaxInches,draft_combine.timeLaneAgility,draft_combine.timeThreeQuarterCourtSprint,draft_combine.repsBenchPress135))
                draft_combine_key = cursor.lastrowid
        return draft_combine_key
    def update_draft_combine(self,id,draft_combine):
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "UPDATE Draft_Combine SET yearCombine = %s, idPlayer = %s, slugPosition = %s, heightWOShoesInches = %s, heightWOShoes = %s, weightLBS = %s, wingspanInches = %s, wingspan = %s, reachStandingInches = %s, reachStandingO = %s, verticalLeapStandingInches = %s, verticalLeapMaxInches = %s, timeLaneAgility = %s, timeThreeQuarterCourtSprint = %s, repsBenchPress135 = %s WHERE (id = %s)"
                cursor.execute(query, (draft_combine.yearCombine,draft_combine.idPlayer,draft_combine.slugPosition ,draft_combine.heightWOShoesInches,draft_combine.heightWOShoes,draft_combine.weightLBS,draft_combine.wingspanInches,draft_combine.wingspan,draft_combine.reachStandingInches ,draft_combine.reachStandingO,draft_combine.verticalLeapStandingInches,draft_combine.verticalLeapMaxInches,draft_combine.timeLaneAgility,draft_combine.timeThreeQuarterCourtSprint,draft_combine.repsBenchPress135,id))
    def delete_draft_combine(self,draft_combine_key,draft_combine):
        with dbapi2.connect(self.db_url) as connection:
            with connection.cursor() as cursor:
                query = "DELETE FROM Draft_Combine WHERE (id = %s)"
                cursor.execute(query, (draft_combine_key,))            