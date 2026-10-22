"""Cricket Data (CricAPI) client for live and match-list data.

Configure CRICKETDATA_API_KEY in Streamlit Secrets or a local .env file.
Never commit the real API key to GitHub.
"""
import os
from typing import Any

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
BASE_URL = "https://api.cricapi.com/v1"


class CricbuzzAPIError(RuntimeError):
    """Raised when a Cricket Data API request fails."""


def _get_api_key() -> str:
    """Read the API key from environment variables or Streamlit Cloud secrets."""
    key = os.getenv("CRICKETDATA_API_KEY", "").strip()
    if not key:
        try:
            key = str(st.secrets.get("CRICKETDATA_API_KEY", "")).strip()
        except Exception:
            key = ""
    if not key or key.lower() in {"replace_me", "your_api_key_here"}:
        raise CricbuzzAPIError(
            "Cricket Data API key is not configured. Add CRICKETDATA_API_KEY "
            "to Streamlit app Secrets (deployed app) or your local .env file."
        )
    return key


def fetch_json(endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    """Call a Cricket Data endpoint and return its JSON response."""
    query = {"apikey": _get_api_key(), "offset": 0}
    if params:
        query.update(params)
    url = f"{BASE_URL}/{endpoint.lstrip('/')}"
    try:
        response = requests.get(url, params=query, timeout=20)
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        raise CricbuzzAPIError(f"Cricket Data request failed: {exc}") from exc
    except ValueError as exc:
        raise CricbuzzAPIError("Cricket Data returned an invalid JSON response.") from exc

    if not isinstance(payload, dict):
        raise CricbuzzAPIError("Cricket Data returned an unexpected response format.")
    if payload.get("status") == "failure" or payload.get("error"):
        message = payload.get("reason") or payload.get("message") or payload.get("error")
        raise CricbuzzAPIError(
            f"Cricket Data API error: {message or 'request was not successful.'}"
        )
    return payload


def get_live_matches() -> dict[str, Any]:
    """Return current matches and scores from Cricket Data."""
    return fetch_json("currentMatches")


def get_recent_matches() -> dict[str, Any]:
    """Return the provider's match-list response (may include scheduled matches)."""
    return fetch_json("matches")
