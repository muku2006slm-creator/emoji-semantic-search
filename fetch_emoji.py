import requests, json

URL = "https://raw.githubusercontent.com/milesj/emojibase/master/packages/data/en/data.raw.json"

data = requests.get(URL).json()

print("Total entries:", len(data))
print("Keys on first entry:", list(data[0].keys()))

print("\n--- entry 0 ---")
print(json.dumps(data[0], indent=2, ensure_ascii=False))

print("\n--- entry 900 ---")
print(json.dumps(data[900], indent=2, ensure_ascii=False))

with open("emoji_raw.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)

print("\nSaved. File is larger this time.")