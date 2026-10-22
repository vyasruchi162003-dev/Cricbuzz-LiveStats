from pathlib import Path
import sqlite3
from datetime import date, timedelta
ROOT=Path(__file__).resolve().parents[1]
DB_PATH=ROOT/'data'/'cricbuzz.db'
SCHEMA='''
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS teams(team_id INTEGER PRIMARY KEY,team_name TEXT UNIQUE NOT NULL,country TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS venues(venue_id INTEGER PRIMARY KEY,venue_name TEXT NOT NULL,city TEXT NOT NULL,country TEXT NOT NULL,capacity INTEGER CHECK(capacity IS NULL OR capacity>=0));
CREATE TABLE IF NOT EXISTS players(player_id INTEGER PRIMARY KEY,full_name TEXT NOT NULL,team_id INTEGER,role TEXT NOT NULL CHECK(role IN ('Batsman','Bowler','All-rounder','Wicket-keeper')),batting_style TEXT,bowling_style TEXT,matches INTEGER DEFAULT 0 CHECK(matches>=0),runs INTEGER DEFAULT 0 CHECK(runs>=0),wickets INTEGER DEFAULT 0 CHECK(wickets>=0),batting_average REAL DEFAULT 0,strike_rate REAL DEFAULT 0,FOREIGN KEY(team_id) REFERENCES teams(team_id) ON DELETE SET NULL);
CREATE TABLE IF NOT EXISTS matches(match_id INTEGER PRIMARY KEY,description TEXT NOT NULL,format TEXT NOT NULL,team1_id INTEGER NOT NULL,team2_id INTEGER NOT NULL,venue_id INTEGER,match_date TEXT NOT NULL,status TEXT NOT NULL DEFAULT 'Completed',winner_team_id INTEGER,win_margin INTEGER,win_type TEXT,FOREIGN KEY(team1_id) REFERENCES teams(team_id),FOREIGN KEY(team2_id) REFERENCES teams(team_id),FOREIGN KEY(venue_id) REFERENCES venues(venue_id) ON DELETE SET NULL,FOREIGN KEY(winner_team_id) REFERENCES teams(team_id) ON DELETE SET NULL);
CREATE TABLE IF NOT EXISTS innings(innings_id INTEGER PRIMARY KEY,match_id INTEGER NOT NULL,batting_team_id INTEGER NOT NULL,innings_number INTEGER NOT NULL,total_runs INTEGER DEFAULT 0,wickets_lost INTEGER DEFAULT 0,FOREIGN KEY(match_id) REFERENCES matches(match_id) ON DELETE CASCADE,FOREIGN KEY(batting_team_id) REFERENCES teams(team_id));
CREATE TABLE IF NOT EXISTS batting_scores(score_id INTEGER PRIMARY KEY,innings_id INTEGER NOT NULL,player_id INTEGER NOT NULL,batting_position INTEGER NOT NULL,runs INTEGER DEFAULT 0,balls INTEGER DEFAULT 0,fours INTEGER DEFAULT 0,sixes INTEGER DEFAULT 0,not_out INTEGER DEFAULT 0,FOREIGN KEY(innings_id) REFERENCES innings(innings_id) ON DELETE CASCADE,FOREIGN KEY(player_id) REFERENCES players(player_id) ON DELETE CASCADE);
CREATE TABLE IF NOT EXISTS bowling_figures(bowling_id INTEGER PRIMARY KEY,innings_id INTEGER NOT NULL,player_id INTEGER NOT NULL,overs REAL DEFAULT 0,runs_conceded INTEGER DEFAULT 0,wickets INTEGER DEFAULT 0,FOREIGN KEY(innings_id) REFERENCES innings(innings_id) ON DELETE CASCADE,FOREIGN KEY(player_id) REFERENCES players(player_id) ON DELETE CASCADE);
CREATE INDEX IF NOT EXISTS idx_matches_date ON matches(match_date);CREATE INDEX IF NOT EXISTS idx_matches_format ON matches(format);CREATE INDEX IF NOT EXISTS idx_players_team ON players(team_id);CREATE INDEX IF NOT EXISTS idx_scores_player ON batting_scores(player_id);
'''
def get_connection():
    DB_PATH.parent.mkdir(parents=True,exist_ok=True)
    c=sqlite3.connect(DB_PATH,check_same_thread=False); c.row_factory=sqlite3.Row; c.execute('PRAGMA foreign_keys=ON'); return c
def initialize_database():
    with get_connection() as c:
        c.executescript(SCHEMA)
        if c.execute('SELECT COUNT(*) FROM teams').fetchone()[0]==0: seed_demo_data(c)
def seed_demo_data(c):
    teams=[(1,'India','India'),(2,'Australia','Australia'),(3,'England','England'),(4,'South Africa','South Africa')]
    c.executemany('INSERT INTO teams VALUES(?,?,?)',teams)
    venues=[(1,'Wankhede Stadium','Mumbai','India',33108),(2,'Melbourne Cricket Ground','Melbourne','Australia',100024),(3,"Lord's",'London','England',30000),(4,'Eden Gardens','Kolkata','India',68000)]
    c.executemany('INSERT INTO venues VALUES(?,?,?,?,?)',venues)
    players=[(1,'Virat Kohli',1,'Batsman','Right-hand','Right-arm medium',292,13848,4,58.2,93.5),(2,'Rohit Sharma',1,'Batsman','Right-hand','Right-arm offbreak',265,10866,9,49.1,92.8),(3,'Jasprit Bumrah',1,'Bowler','Right-hand','Right-arm fast',89,80,149,8.2,60),(4,'Ravindra Jadeja',1,'All-rounder','Left-hand','Slow left-arm orthodox',197,2756,220,32.8,85.1),(5,'Pat Cummins',2,'Bowler','Right-hand','Right-arm fast',88,550,141,16.3,78.2),(6,'Steve Smith',2,'Batsman','Right-hand','Right-arm legbreak',155,5350,28,43.9,87.1),(7,'Mitchell Marsh',2,'All-rounder','Right-hand','Right-arm medium',88,2700,54,35.4,91.2),(8,'Jos Buttler',3,'Wicket-keeper','Right-hand','Right-arm medium',181,4900,0,39.4,117.8),(9,'Ben Stokes',3,'All-rounder','Left-hand','Right-arm fast-medium',114,3460,74,36.2,95),(10,'Kagiso Rabada',4,'Bowler','Left-hand','Right-arm fast',101,230,157,9.4,65)]
    c.executemany('INSERT INTO players VALUES(?,?,?,?,?,?,?,?,?,?,?)',players)
    today=date.today(); matches=[(1,'India vs Australia, ODI','ODI',1,2,1,3,1,6,'wickets'),(2,'Australia vs England, Test','Test',2,3,2,10,2,120,'runs'),(3,'India vs England, T20I','T20I',1,3,4,18,3,4,'wickets'),(4,'South Africa vs India, ODI','ODI',4,1,3,35,1,22,'runs'),(5,'India vs Australia, T20I','T20I',1,2,1,50,2,3,'wickets'),(6,'England vs South Africa, ODI','ODI',3,4,3,65,3,18,'runs'),(7,'Australia vs India, Test','Test',2,1,2,90,1,2,'wickets'),(8,'India vs South Africa, T20I','T20I',1,4,4,120,1,7,'runs')]
    for mid,desc,fmt,t1,t2,venue,days,winner,margin,wtype in matches:
        c.execute('INSERT INTO matches VALUES(?,?,?,?,?,?,?,?,?,?,?)',(mid,desc,fmt,t1,t2,venue,(today-timedelta(days=days)).isoformat(),'Completed',winner,margin,wtype))
    iid=sid=bid=1
    for mid,desc,fmt,t1,t2,venue,days,winner,margin,wtype in matches:
        for num,team in [(1,t1),(2,t2)]:
            c.execute('INSERT INTO innings VALUES(?,?,?,?,?,?)',(iid,mid,team,num,200+mid*9+num*12,4+num))
            team_players=[p for p in players if p[2]==team][:2] or players[:2]
            for pos,p in enumerate(team_players,1):
                runs=(mid*13+pos*17+team*5)%110
                c.execute('INSERT INTO batting_scores VALUES(?,?,?,?,?,?,?,?,?)',(sid,iid,p[0],pos,runs,max(1,int(runs*.75)),runs//10,runs//25,0)); sid+=1
                c.execute('INSERT INTO bowling_figures VALUES(?,?,?,?,?,?)',(bid,iid,p[0],4.0,25+mid,1 if mid%2 else 2)); bid+=1
            iid+=1
