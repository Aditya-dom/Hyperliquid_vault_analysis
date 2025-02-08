import json
import os
import re
from datetime import datetime, timedelta

import requests
import streamlit as st

# URL for the vaults
VAULTS_URL = "https://stats-data.hyperliquid.xyz/Mainnet/vaults"
INFO_URL = "https://api-ui.hyperliquid.xyz/info"

CACHE_DIR = "./cache/"

CACHE_FILE = CACHE_DIR + "vaults_cache.json"
DETAILS_CACHE_FILE = CACHE_DIR + "/vault_detail/#KEY#/vault_details_cache.json"


CACHE_DAYS_VALIDITY = 7


def update_all_cache_data(show_progress=True):
    """Updates both vault list and individual vault details cache."""
    progress_bar = st.progress(0) if show_progress else None
    status_text = st.empty() if show_progress else None

    if show_progress:
        status_text.text("Downloading vault list...")

    # First get vault list
    response = requests.get(VAULTS_URL)
    data = response.json()

    vaults = [
        {
            "Name": vault["summary"]["name"],
            "APR %": int(vault["apr"] * 100),
            "Vault": vault["summary"]["vaultAddress"],
            "Leader": vault["summary"]["leader"],
            "Total Value Locked": float(vault["summary"]["tvl"]),
            "Days Since": (datetime.now() - datetime.fromtimestamp(vault["summary"]["createTimeMillis"] / 1000)).days,
        }
        for vault in data
        if not vault["summary"]["isClosed"]
    ]

    # Save vault list cache
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump({"last_update": datetime.now().isoformat(), "data": vaults}, f)

    # Now get details for each vault
    if show_progress:
        status_text.text("Downloading vault details...")

    total_steps = len(vaults)
    for i, vault in enumerate(vaults):
        if show_progress:
            progress_bar.progress(i / total_steps)
            status_text.text(f"Downloading vault details ({i+1}/{total_steps})...")

        fetch_vault_details(vault["Leader"], vault["Vault"])

    if show_progress:
        progress_bar.empty()
        status_text.empty()
        st.toast("All vault data updated!", icon="✅")

    return vaults


def fetch_vaults_data():
    """Fetches vault data (with cache)."""
    try:
        with open(CACHE_FILE, "r") as f:
            cache = json.load(f)
            last_update = datetime.fromisoformat(cache["last_update"])
            if datetime.now() - last_update < timedelta(hours=24):
                return cache["data"]
            print("Cache is older than 24 hours, refreshing...")
    except (FileNotFoundError, KeyError, ValueError):
        pass

    return update_all_cache_data()


def fetch_vault_details(leader, vault_address):
    """Fetches vault details with a caching system."""

    cache_key = re.sub(r"[^a-zA-Z0-9_]", "", leader + "_" + vault_address)
    local_DETAILS_CACHE_FILE = DETAILS_CACHE_FILE.replace("#KEY#", cache_key)

    # Extract the directory path without the file
    directory_path = os.path.dirname(local_DETAILS_CACHE_FILE)

    # Create directories if needed
    os.makedirs(directory_path, exist_ok=True)

    try:
        with open(local_DETAILS_CACHE_FILE, "r") as f:
            # print("Vault DETAIL: cache used", cache_key)
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Vault DETAIL: No cache found")

    print("Vault DETAIL: Download used", cache_key)

    # Otherwise, make the request
    payload = {"type": "vaultDetails", "user": leader, "vaultAddress": vault_address}
    response = requests.post(INFO_URL, json=payload)
    if response.status_code == 200:
        details = response.json()
        with open(local_DETAILS_CACHE_FILE, "w") as f:
            json.dump(details, f)
        return details
    else:
        return None
