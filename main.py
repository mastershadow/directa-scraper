import requests
import time
from pathlib import Path
import json
import slugify

UPDATE = False
PROCESS = True

FEEZERO_BASEURL = "https://www.directa.it/api/v1/tabelle/feezero"
PAC_BASEURL = "https://www.directa.it/api/v1/tabelle/pac"
DATA_DIR = Path(__file__).parent / "data"
OUT_DIR = Path(__file__).parent / "out"

SLEEP_TIME = 1
FEEZERO_BASENAME = "feezero"
PAC_BASENAME = "pac"

def update():
    global FEEZERO_BASEURL, PAC_BASEURL, DATA_DIR

    # collect feezero data
    req = requests.get(FEEZERO_BASEURL)
    with open(DATA_DIR / f"{FEEZERO_BASENAME}.json", "w") as f:
        json.dump(req.json(), f)

    for entry in req.json():
        time.sleep(SLEEP_TIME)
        emitter = entry['EMIT']
        url = f"{FEEZERO_BASEURL}?EMIT={emitter}"
        datareq = requests.get(url)
        with open(DATA_DIR / f"{FEEZERO_BASENAME}-{slugify.slugify(emitter)}.json", "w") as f:
            json.dump(datareq.json(), f)

    # collect pac data
    req = requests.get(PAC_BASEURL)
    with open(DATA_DIR / f"{PAC_BASENAME}.json", "w") as f:
        json.dump(req.json(), f)

    for entry in req.json():
        time.sleep(SLEEP_TIME)
        emitter = entry['EMIT']
        url = f"{PAC_BASEURL}?EMIT={emitter}"
        datareq = requests.get(url)
        with open(DATA_DIR / f"{PAC_BASENAME}-{slugify.slugify(emitter)}.json", "w") as f:
            json.dump(datareq.json(), f)

def process():
    global DATA_DIR
    # process feezero
    feezero_entries = []
    with open(DATA_DIR / f"{FEEZERO_BASENAME}.json", "r") as f:
        data = json.load(f)
        for entry in data:
            emitter = slugify.slugify(entry['EMIT'])
            with open(DATA_DIR / f"{FEEZERO_BASENAME}-{emitter}.json", "r") as data_file:
                data_file_content = json.load(data_file)
            feezero_entries = feezero_entries + data_file_content
    with open(OUT_DIR / f"{FEEZERO_BASENAME}.json", "w") as f:
        json.dump(feezero_entries, f)

    # process pac
    pac_entries = []
    with open(DATA_DIR / f"{PAC_BASENAME}.json", "r") as f:
        data = json.load(f)
        for entry in data:
            emitter = slugify.slugify(entry['EMIT'])
            with open(DATA_DIR / f"{PAC_BASENAME}-{emitter}.json", "r") as data_file:
                data_file_content = json.load(data_file)
            pac_entries = pac_entries + data_file_content
    with open(OUT_DIR / f"{PAC_BASENAME}.json", "w") as f:
        json.dump(pac_entries, f)

if __name__ == "__main__":
    if UPDATE:
        print("Updating...")
        update()
    if PROCESS:
        print("Processing...")
        process()