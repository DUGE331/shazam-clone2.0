import pickle

def match_fingerprints(recorded_fingerprints, database_path="fingerprint_database.pk1"):
    """Matches recorded fingerprints against the database."""
    with open(database_path, "rb") as f:
        database = pickle.load(f)

    tally = {}
    for hash_val, recorded_time in recorded_fingerprints:
        if hash_val in database:
            for song_id, song_time in database[hash_val]:
                offset_diff = song_time - recorded_time
                key = (song_id, offset_diff)
                tally[key] = tally.get(key, 0) + 1

    if not tally:
        print("No match found.")
        return None

    best_match = max(tally.items(), key=lambda item: item[1])
    (best_song, best_offset), best_count = best_match
    print(f"Best Match: {best_song} with {best_count} aligned fingerprints (offset_diff: {best_offset})")
    return best_song, best_count
