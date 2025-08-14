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
