import requests
import time
import pandas as pd

headers = {
    "Host": "mpapi.tcgplayer.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Content-Type": "application/json",
    "Origin": "https://www.tcgplayer.com",
    "Connection": "keep-alive",
    "Referer": "https://www.tcgplayer.com/",
    "Cookie": "tracking-preferences={%22version%22:1%2C%22destinations%22:{%22Actions%20Amplitude%22:true%2C%22AdWords%22:true%2C%22Google%20AdWords%20New%22:true%2C%22Google%20Enhanced%20Conversions%22:true%2C%22Google%20Tag%20Manager%22:true%2C%22Impact%20Partnership%20Cloud%22:true%2C%22Optimizely%22:true}%2C%22custom%22:{%22advertising%22:true%2C%22functional%22:true%2C%22marketingAndAnalytics%22:true}}; analytics_session_id=1760802558192; analytics_session_id.last_access=1760802679989; _gcl_au=1.1.1429207886.1755364466.2091947295.1760802568.1760802667; _ga_VS9BE2Z3GY=GS2.1.s1760802568$o35$g1$t1760802677$j30$l0$h407694816; _ga=GA1.1.1542919150.1755364468; valid=set=true; __ssid=a225eb449b24d7602f3dfa01ca4bc4b; _ga_KK8XBGNYRB=GS2.1.s1760802572$o41$g1$t1760802677$j60$l0$h0; _ga_0T2XGBC5QN=GS2.1.s1760802572$o34$g1$t1760802677$j60$l0$h0; _ga_JEQYTNS2WQ=GS2.1.s1760802572$o34$g1$t1760802677$j60$l0$h0; product-display-settings=sort=price+shipping&size=10; TCG_Data=M=1&SearchGameNameID=magic; ajs_anonymous_id=572d8c50-b316-4de6-92db-88edda4dfbd9; ajs_user_id=9c762180-cd0b-44c2-84b7-3a4ed31530be; setting=CD%3DKZ%26M%3D1; tcg-segment-session=1760802557586%257C1760802679467; TCGAuthTicket_Production=06051580AB4D74238D74734756A08B26699B63FEDA0FCC044EE91A4503BBFF7CB5A02D27C83FFA912BCE193DBE4751A1E46E44AF3185E82373E48D82E8B474FFC6242856ABDF2055E17F66B8CB9D00A1607EF2AAE933B35D836E0ED2BD6A67CCBE9A8BC0070E1025BAA20A53E7A95044B8227375; BuyerRevalidationKey=Revalidated; StoreSaveForLater_PRODUCTION=SFLK=f1e85eb0e75646c083c55781f680f4e2&Ignore=false; TCG_VisitorKey=efc79948-1968-4cf6-89e2-50d8a19a41f0; TCG_VisitorKey=5a8b7c9e-4702-403b-8d4e-91455875a01d; SearchSortSettings=M=1&ProductSortOption=BestMatch&ProductSortDesc=False&PriceSortOption=Shipping&ProductResultDisplay=grid; SellerProximity=ZipCode=&MaxSellerDistance=1000&IsActive=false",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site"
}


api_request = {
	"conditions": [],
	"languages": [
		1
	],
	"limit": 25,
    "offset": 0,
	"listingType": "All",
	"variants": []
}


url = "https://mpapi.tcgplayer.com/v2/product/221309/latestsales"

response = requests.post(url, headers=headers, json=api_request)

df = pd.DataFrame.from_dict(response.json())
df.to_csv("output.csv", index=False)


print(f"🔁 Status: {response.status_code}")
print(f"📄 Response:\n{response.text}")
