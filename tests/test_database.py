from utils.db_connection import initialize_database,get_connection

def test_database_seeded():
 initialize_database()
 with get_connection() as c:
  assert c.execute('SELECT COUNT(*) FROM teams').fetchone()[0]>=4
  assert c.execute('SELECT COUNT(*) FROM players').fetchone()[0]>=10
  assert c.execute('SELECT COUNT(*) FROM matches').fetchone()[0]>=8

def test_invalid_role_rejected():
 initialize_database()
 with get_connection() as c:
  try: c.execute("INSERT INTO players(full_name,role) VALUES('Bad Role','Coach')")
  except Exception: pass
  else: raise AssertionError('Invalid role should be rejected')
