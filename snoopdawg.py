#!/usr/bin/env python3
#
# SNOOPDAWG
# K0RNH0LI0 2021
#
# Searches the GitHub event stream for "interesting" commits.
# See README.txt for more information.
#
# This program is Free Software, licensed under the terms of
# GNU GPLv2. See LICENSE.txt for details.
#

import os
import re
import sys
import time
import json
import requests

# URL of GitHub's event API
EVT_URL = "https://api.github.com/events"

# GitHub Username
USERNAME=""
# GitHub OAuth token
TOKEN=""

# number of pages to check per scan
PAGES = 1

# whether or not to save files/diffs to downloads/
DOWNLOAD = True
# if True, the script will continue scanning until
# it is interrupted
# if False, the script will scan once
LOOP = False

# re patterns to search commits for
PATTERNS = []
# blacklist of file extensions to not examine
BLACKLIST = []

# dictionary for storing results
# will be written to results.json
RESULTS = {}

# first ID of the previous scan
# current scan will stop if this is reached
PREV_START = ""
# temporary start tracker for each scan
T_START = ""

def api_get(url, PARAMS=None):
    resp = requests.get(
        url,
        params=PARAMS,
        auth=(USERNAME, TOKEN)
    )

    if resp.status_code != 200:
        print(resp.text)
        return None
    else:
        return resp.json()

def get_events(page):
    REQ_PARAMS = {
        "Accept": "application/vnd.github.v3+json",
        "per_page": 100,
        "page": page
    }
    return api_get(EVT_URL, REQ_PARAMS)

def check_file(f):
    """
    Search the JSON object representing a file in
    a commit for the regex we're interested in.
    """
    if f["raw_url"] is None or f["sha"] is None:
        return False
    # check blacklisted extensions
    for ext in BLACKLIST:
        if f["raw_url"].endswith(ext):
            return False

    scantext = ""
    if "patch" in f:
        scantext = f["patch"]
    else:
        if os.path.exists("downloads/" + f["sha"]):
            print(f["sha"] + " exists, skipping")
            return True
        scantext = requests.get(f["raw_url"]).text

    for ptn in PATTERNS:
        if re.search(ptn, scantext) is not None:
            print(f"MATCH {f['sha']} {ptn}")
            RESULTS[f["sha"]] = {
                "raw_url": f["raw_url"],
                "match": ptn
            }

            #\TODO "stream" to results file instead of
            # rewriting the whole dict every time
            with open("results.json", "w") as of:
                of.write(json.dumps(RESULTS))

            if DOWNLOAD:
                # create downloads directory if necessary
                if not os.path.exists("downloads/"):
                    os.mkdir("downloads")
                # save file/diff to downloads folder with
                # SHA hash for name
                with open("downloads/" + f["sha"], "w") as of:
                    of.write(scantext)
            return True
    return False

def check_commit(commit_url):
    """
    Check all files in a commit based on commit URL.
    """
    commit = api_get(commit_url)

    if commit is None:
        return
    elif not "files" in commit:
        return

    for f in commit["files"]:
        check_file(f)

def check_push_event(evt):
    """
    Check all commits in a push event based on
    a PushEvent JSON object.
    """
    if not "payload" in evt:
       return
    elif not "commits" in evt["payload"]:
        return

    for commit in evt["payload"]["commits"]:
        check_commit(commit["url"])

def scanpage(page, pagenum):
    """
    Scan all events in an event page for PushEvents, then
    pass them to check_push_event().
    page: JSON object representing a page
    pagenum: index of this page (1-indexed)
    """
    global PREV_START
    global T_START

    evt = [x for x in page if x["type"] == "PushEvent"]
    if len(evt) == 0:
        return 0
    if pagenum == 1:
        T_START = evt[0]["id"]

    for x in evt:
        if x["id"] == PREV_START:
            print("reached prev start")
            return None
        check_push_event(x)
    return 1

def scan_pages(numpages):
    """
    Scan the number of pages from the event
    stream specified by numpages.
    """
    global PREV_START
    global T_START
    pages = []
    # pre-load pages
    for i in range(1, numpages + 1):
        evt = get_events(i)
        if evt is not None:
            pages.append(evt)
    # scan loaded pages
    for i in range(len(pages)):
        if scanpage(pages[i], i + 1) is None:
            break
    PREV_START = T_START

def load_list(filename, dest):
    """
    Load a wordlist from a text file into a list.
    Lines starting with # are comments.
    filename: list to load
    dest: list object to append to
    """
    with open(filename, "r") as f:
        for line in f.readlines():
            if line[0] != "#": # comment lines
                dest.append(line.replace("\n", ""))

if __name__ == "__main__":
    # load OAuth token
    if not os.path.exists("auth.priv"):
        print("auth.priv file not found.")
        print("See README.txt")
        exit()
    with open("auth.priv", "r") as f:
        USERNAME = f.readline().replace("\n", "")
        TOKEN = f.readline().replace("\n", "")

    # check flags
    if "--no-dl" in sys.argv:
        DOWNLOAD = False
    if "--loop" in sys.argv:
        LOOP = True

    # load re patterns
    load_list("lists/patterns.txt", PATTERNS)
    # load file extension blacklist
    load_list("lists/blacklist.txt", BLACKLIST)

    # load results.json if it exists
    if os.path.exists("results.json"):
        with open("results.json", "r") as f:
            RESULTS = json.loads(f.read())

    while True:
        scan_pages(PAGES)
        if not LOOP:
            break