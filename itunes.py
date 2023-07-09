import requests

# Instead of hard coding
# res = requests.get('https://itunes.apple.com/search?term=jack+johnson&limit=25')

term = "Madona"

res = requests.get("https://itunes.apple.com/search", params={"term": term, "limit": 5})


data = res.json()

for result in data["results"]:
    print(result["trackName"])
    # print(result['collectionName'])
