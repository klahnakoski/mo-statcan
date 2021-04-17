"""

curl 'https://dv-vd.shinyapps.io/71-607-x2020017_en/_w_3ce303be/session/e5e32cc98acfc0c8eca8f0b053dddc12/dataobj/mortalityTable?w=3ce303be&nonce=fd37ba164387acac'
-H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'
-H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Accept-Language: en-CA,en-US;q=0.7,en;q=0.3' --compressed
-H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8'
-H 'X-Requested-With: XMLHttpRequest'
-H 'Origin: https://dv-vd.shinyapps.io'
-H 'Connection: keep-alive'
-H 'Referer: https://dv-vd.shinyapps.io/71-607-x2020017_en/'
-H 'Cookie: session=bHVjaWQtcHJvZHVjdGlvbi1sZWdhY3ktYXBwczMxLmxwMDE6NDI0NDU%3d'
-H 'TE: Trailers'
--data-raw 'draw=1&columns%5B0%5D%5Bdata%5D=0&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=1&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=2&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=3&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=4&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&start=0&length=25&search%5Bvalue%5D=&search%5Bregex%5D=false&search%5BcaseInsensitive%5D=true&search%5Bsmart%5D=true&escape=true'
"""
from mo_dots import to_data
from mo_files import File, URL, mimetype
from mo_http import http

from mo_logs import Log

http.DEBUG = True
http.default_headers = to_data({
    "From": "kyle@lahnakoski.com",
    "Referer": "kyle@lahnakoski.com",
})

DEATH_RATES = 13100392

# result = http.get_json("https://www150.statcan.gc.ca/t1/wds/rest/getAllCubesList")

# ALL CAUSES DEATH RATES
result = http.post(
    "https://www150.statcan.gc.ca/t1/wds/rest/getCubeMetadata",
    json=[{"productId": DEATH_RATES}],
    headers={"User-Agent":"mo-statscan", "Content-Type": mimetype.JSON, "Accept": mimetype.ANY}
)


# EXAMPLE CUBE
# result = http.post_json(
#     "https://www150.statcan.gc.ca/t1/wds/rest/getCubeMetadata",
#     data=[{"productId":35100003}],
# )

# GET CSV OF CUBE
# result = http.get_json(URL("https://www150.statcan.gc.ca/t1/wds/rest/getFullTableDownloadCSV") /DEATH_RATES / "en")
# data = http.get(result.object)


Log.note("{{data}}", data=result)
