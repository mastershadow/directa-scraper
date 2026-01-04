import requests
import time
from pathlib import Path
import json
import slugify
import pandas as pd

#
# CONFIGURATION NEEDED
# Set these to True before launching
# Please do not abuse of this tool
#
UPDATE = False
PROCESS = True

FEEZERO_BASEURL = "https://www.directa.it/api/v1/tabelle/feezero"
PAC_BASEURL = "https://www.directa.it/api/v1/tabelle/pac"
DATA_DIR = Path(__file__).parent / "data"
OUT_DIR = Path(__file__).parent / "out"
ETF_LIST = DATA_DIR / "etf_list.json"

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
    global DATA_DIR, ETF_LIST

    etfs = {}
    if ETF_LIST.exists():
        with open(ETF_LIST, "r") as f:
            etf_list_data = json.load(f)
            for entry in etf_list_data:
                etfs[entry['isin']] = entry

    # process feezero
    feezero_entries = []
    with open(DATA_DIR / f"{FEEZERO_BASENAME}.json", "r") as f:
        data = json.load(f)
        for entry in data:
            emitter_name = entry['EMIT']
            emitter = slugify.slugify(emitter_name)
            with open(DATA_DIR / f"{FEEZERO_BASENAME}-{emitter}.json", "r") as data_file:
                data_file_content = json.load(data_file)
            for entry in data_file_content:
                entry['Emittente'] = emitter_name
                if entry['Isin'] in etfs:
                    entry['Categoria'] = etfs[entry['Isin']]['category']
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
                for entry in data_file_content:
                    if entry['Isin'] in etfs:
                        entry['Categoria'] = etfs[entry['Isin']]['category']
            pac_entries = pac_entries + data_file_content
    with open(OUT_DIR / f"{PAC_BASENAME}.json", "w") as f:
        json.dump(pac_entries, f)

    # convert to csv
    with open(OUT_DIR / f"{FEEZERO_BASENAME}.json", "r") as f:
        df = pd.read_json(f)
        df.to_csv(OUT_DIR / f"{FEEZERO_BASENAME}.csv", index=False)
    with open(OUT_DIR / f"{PAC_BASENAME}.json", "r") as f:
        df = pd.read_json(f)
        df.to_csv(OUT_DIR / f"{PAC_BASENAME}.csv", index=False)

if __name__ == "__main__":
    if not UPDATE and not PROCESS:
        print("Please update variables at the top of main.py.\nThis is a safety check to avoid abuses. Cheers️ ❤️")
    if UPDATE:
        print("Updating...")
        update()
    if PROCESS:
        print("Processing...")
        process()