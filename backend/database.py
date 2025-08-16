import os
import pickle

def build_database(fingerprint_dir="fingerprints"):
    """Load all fingerprint files and create a combined database."""
    database = {}
    for file in os.listdir(fingerprint_dir):
        if file.endswith(".pk1"):
            song_id = file.replace(".pk1", "")
            with open(os.path.join(fingerprint_dir, file), "rb") as f:
                fingerprints = pickle.load(f)
                for hash_val, time in fingerprints:
                    if hash_val not in database:
                        database[hash_val] = []
                    database[hash_val].append((song_id, time))
    return database

def save_database(database, output_file="fingerprint_database.pk1"):
    with open(output_file, "wb") as f:
        pickle.dump(database, f)
        print(f"Saved database with {len(database)} hash entries to {output_file}")

def add_fingerprints_to_db(fingerprints, track_url):
    db_file = "fingerprint_database.pk1"
    if os.path.exists(db_file):
        with open(db_file, "rb") as f:
            database = pickle.load(f)
    else:
        database = {}

    for hash_val, time in fingerprints:
        if hash_val not in database:
            database[hash_val] = []
        database[hash_val].append((track_url, time))

    with open(db_file, "wb") as f:
        pickle.dump(database, f)
    print(f"Added {len(fingerprints)} fingerprints for {track_url}")