"""Optional API client; confirm endpoint availability with your provider."""
import os, requests
from dotenv import load_dotenv
load_dotenv()
class CricbuzzAPIError(RuntimeError): pass
def fetch_json(endpoint,params=None):
 key=os.getenv('CRICBUZZ_API_KEY'); host=os.getenv('CRICBUZZ_API_HOST','cricbuzz-cricket.p.rapidapi.com')
 if not key or key=='replace_me': raise CricbuzzAPIError('API key not configured. Add CRICBUZZ_API_KEY to .env.')
 try:
  r=requests.get(f'https://{host}/{endpoint.lstrip("/")}',headers={'X-RapidAPI-Key':key,'X-RapidAPI-Host':host},params=params,timeout=15); r.raise_for_status(); return r.json()
 except requests.RequestException as e: raise CricbuzzAPIError(f'API request failed: {e}') from e
 except ValueError as e: raise CricbuzzAPIError('API returned invalid JSON.') from e
def get_live_matches(): return fetch_json('matches/v1/live')
def get_recent_matches(): return fetch_json('matches/v1/recent')
