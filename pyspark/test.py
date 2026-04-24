import json, random, datetime, os

os.makedirs("data", exist_ok=True)  # won't fail if it already exists

events = []
types = ["click", "purchase", "signup", "view"]

for i in range(1000):
    events.append({
        "event_id": i + 1,
        "event_type": random.choice(types),
        "ts": (datetime.datetime(2024, 1, 1) + datetime.timedelta(seconds=random.randint(0, 31536000))).isoformat(),
        "amount": round(random.uniform(1.0, 500.0), 2)
    })

with open("data/events.json", "w") as f:
    for e in events:
        f.write(json.dumps(e) + "\n")

print("Done:", os.path.abspath("data/events.json"))