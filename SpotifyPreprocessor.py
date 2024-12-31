import pandas as pd
import numpy as np
import os
import json
import pickle
import matplotlib.pyplot as plt
plt.style.use('bmh')
from tqdm import tqdm


def SpotifyPreprocessor(folder_path, pickle_path):
    """
    Combines JSON files in a folder into a single DataFrame and pickles it.

    Parameters:
        folder_path (str): Path to the folder containing JSON files.
        pickle_path (str): Path to the pickle file to save or load.

    Returns:
        pd.DataFrame: Combined DataFrame.
    """

    if os.path.exists(pickle_path):
        print('Pickled data already exists. Generating dataframe from existing pickle')
        with open(pickle_path, 'rb') as f:
            return pickle.load(f)

    base_template = {
        "ts": None,
        "username": None,
        "platform": None,
        "ms_played": None,
        "conn_country": None,
        "ip_addr_decrypted": None,
        "user_agent_decrypted": None,
        "master_metadata_track_name": None,
        "master_metadata_album_artist_name": None,
        "master_metadata_album_album_name": None,
        "spotify_track_uri": None,
        "episode_name": None,
        "episode_show_name": None,
        "spotify_episode_uri": None,
        "reason_start": None,
        "reason_end": None,
        "shuffle": None,
        "skipped": None,
        "offline": None,
        "offline_timestamp": None,
        "incognito_mode": None,
        "extras": None,
    }

    all_data = []

    for file_name in tqdm(os.listdir(folder_path), desc="Processing Files", unit="file"):
        file_path = os.path.join(folder_path, file_name)

        if file_name.endswith(".json"):
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)

                    for item in data:

                        record = base_template.copy() # start with the base template

                        extras = {} # prepare an additional feature for extra data


                        for key, value in item.items():
                            if key in record:
                                record[key] = value
                            else:
                                extras[key] = value

                        record["extras"] = json.dumps(extras) if extras else None # add up the extras

                        if record["offline"] is False:
                            record["offline_timestamp"] = False

                        all_data.append(record)

                except json.JSONDecodeError:
                    print(f"Error decoding JSON file: {file_path}")
        else:
            print(f"{file_name} not eligible: Not a JSON.")

    df = pd.DataFrame(all_data)

    # ISO 8601 compatible conversion
    df["ts"] = pd.to_datetime(df["ts"], format='%Y-%m-%dT%H:%M:%SZ', errors='coerce')
    df = df.sort_values(by="ts")
    df = df.reset_index(drop=True)

    with open(pickle_path, 'wb') as f:
        pickle.dump(df, f)

    return df
