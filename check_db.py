# check_db.py
import pickle

with open("fingerprint_database.pk1", "rb") as f:
    db = pickle.load(f)

print("Number of entries in DB:", len(db))

# Show a few sample entries
for i, (k, v) in enumerate(db.items()):
    print(k, v)
    if i >= 5:
        break
