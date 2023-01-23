CREATE TABLE IF NOT EXISTS Player (
	id SERIAL PRIMARY KEY NOT NULL,
  	full_name TEXT,
  	first_name TEXT,
  	last_name TEXT,
  	is_active INTEGER
);

CREATE TABLE IF NOT EXISTS team (
	id SERIAL PRIMARY KEY, 
	full_name TEXT UNIQUE, 
	abbreviation TEXT UNIQUE, 
	nickname TEXT UNIQUE, 
	city TEXT, 
	state TEXT, 
	year_founded NUMERIC(4)
);

CREATE TABLE IF NOT EXISTS team_attributes (
	team_id INTEGER PRIMARY KEY REFERENCES team(id) 
		ON DELETE CASCADE 
		ON UPDATE CASCADE,
	arena TEXT, 
	arena_capacity INTEGER, 
	owner TEXT, 
	general_manager TEXT, 
	head_coach TEXT, 
	d_league_affiliation TEXT, 
	facebook_website_link TEXT, 
	instagram_website_link TEXT, 
	twitter_website_link TEXT
);


CREATE TABLE IF NOT EXISTS Player_Attributes (
	id INTEGER PRIMARY KEY NOT NULL,
	first_name TEXT,
	last_name TEXT,
	display_fi_last TEXT,
	player_slug TEXT,
	birthdate TEXT,
	country TEXT,
	last_affilation TEXT,
	height REAL,
	weight REAL,
	season_exp INTEGER,
	jersey TEXT,
	position TEXT,
	rosterstatus TEXT,
	games_played_current_season_flag TEXT,
	team_id INTEGER NOT NULL REFERENCES team(id)		
		ON DELETE CASCADE 
		ON UPDATE CASCADE,
	team_name TEXT,
	team_abbreviation TEXT,
	team_city TEXT,
	playercode TEXT,
	from_year TEXT,
	to_year TEXT,
	dleague_flag TEXT,
	nba_flag TEXT,
	games_played_flag TEXT,
	draft_year TEXT,
	draft_round TEXT,
	draft_number TEXT,
	pts REAL,
	ast REAL,
	reb REAL,
	all_star_appearances REAL,
	pie REAL
);

CREATE TABLE IF NOT EXISTS Player_Salary (
	slugSeason TEXT,
	nameTeam TEXT,
	namePlayer TEXT,
	statusPlayer TEXT,
	isFinalSeason INTEGER,
	isWaived INTEGER,
	isOnRoster INTEGER,
	isNonGuaranteed INTEGER,
	isTeamOption INTEGER,
	isPlayerOption INTEGER,
	typeContractDetail TEXT,
	"value" REAL
);

CREATE TABLE IF NOT EXISTS Player_Photos (
	isActive INTEGER,
	isRookie INTEGER,
	namePlayer TEXT,
	idPlayer INTEGER NOT NULL REFERENCES Player(id)		
		ON DELETE CASCADE 
		ON UPDATE CASCADE,
	countSeasons REAL,
	yearSeasonFirst REAL,
	yearSeasonLast REAL,
	idTeam INTEGER,
	hasGamesPlayedFlag INTEGER,
	urlPlayerStats TEXT,
	urlPlayerThumbnail TEXT,
	urlPlayerHeadshot TEXT,
	urlPlayerActionPhoto TEXT,
	hasHeadShot INTEGER,
	hasThumbnail INTEGER,
	hasAction INTEGER,
	urlPlayerPhoto TEXT

);

CREATE TABLE IF NOT EXISTS Player_Bios (
	namePlayerBREF TEXT,
	urlPlayerBioBREF TEXT,
	nameTable TEXT,
	urlPlayerImageBREF TEXT,
	slugPlayerBREF TEXT,
	numberTransactionPlayer INTEGER,
	dateTransaction REAL,
	descriptionTransaction TEXT,
	isGLeagueMovement INTEGER,
	isDraft INTEGER,
	isSigned INTEGER,
	isWaived INTEGER,
	isTraded INTEGER,
	slugSeason TEXT,
	nameTeam TEXT,
	slugLeague TEXT,
	amountSalary REAL,
	detailsContract TEXT,
	namePronunciation TEXT,
	namePosition TEXT,
	heightInches REAL,
	weightLBS REAL,
	dateBirth REAL,
	locationBirthplace TEXT,
	cityBirthplace TEXT,
	stateBirthplace TEXT,
	nameCollege TEXT,
	nameHighSchool TEXT,
	dateNBADebut REAL,
	career_length TEXT,
	yearsExperience REAL,
	nameTwitter TEXT,
	yearHighSchool REAL,
	rankHighSchool REAL,
	dateDeath REAL,
	high_schools TEXT,
	descriptionRelatives TEXT,
	descriptionHOF TEXT,
	playerNicknames TEXT,
	colleges TEXT
); 

CREATE TABLE IF NOT EXISTS Draft (
	id SERIAL PRIMARY KEY,
	yearDraft INTEGER,
	numberPickOverAll INTEGER,
	numberRound INTEGER,
	numberRoundPick INTEGER,
	nameOrganizationFrom TEXT,
	typeOrganizationFrom TEXT,
	idPlayer INTEGER NOT NULL REFERENCES Player(id)		
		ON DELETE CASCADE 
		ON UPDATE CASCADE,
	team_id INTEGER NOT NULL REFERENCES team(id) 
		ON DELETE CASCADE 
		ON UPDATE CASCADE,
	Player_Profile_Flag INTEGER,
	slugOrganizationTypeFrom TEXT,
	locationOrganizationFrom TEXT	
);
CREATE TABLE IF NOT EXISTS Draft_Combine (
	id SERIAL PRIMARY KEY,
	yearCombine INTEGER,
	idPlayer INTEGER NOT NULL REFERENCES Player(id) 
		ON DELETE CASCADE 
		ON UPDATE CASCADE,
	slugPosition TEXT,
	heightWOShoesInches REAL,
	heightWOShoes TEXT,
	weightLBS REAL,
	wingspanInches REAL,
	wingspan TEXT,
	reachStandingInches REAL,
	reachStandingO TEXT,
	verticalLeapStandingInches REAL,
	verticalLeapMaxInches TEXT,
	timeLaneAgility REAL,
	timeThreeQuarterCourtSprint REAL,
	repsBenchPress135 REAL
);

CREATE TABLE IF NOT EXISTS Game (
	gameID SERIAL PRIMARY KEY NOT NULL,
	teamIDHome INTEGER NOT NULL REFERENCES team(id)		
		   ON DELETE CASCADE 
		   ON UPDATE CASCADE,
	teamNameHome TEXT,
	gameDate TEXT,
	WLHome TEXT,
	pointsHome INTEGER,
	teamIDAway INTEGER NOT NULL REFERENCES team(id)		
		   ON DELETE CASCADE 
		   ON UPDATE CASCADE,
	teamNameAway TEXT,
	WLAway TEXT,
	pointsAway INTEGER,
);