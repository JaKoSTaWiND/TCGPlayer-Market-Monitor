import requests

url = "https://infinite-api.tcgplayer.com/price/history/597065/detailed?range=quarter"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json",
    "Referer": "https://www.tcgplayer.com/",
    "Origin": "https://www.tcgplayer.com"
}

response = requests.get(url, headers=headers)

print(response.status_code)
print(response.text)
