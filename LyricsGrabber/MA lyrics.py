#api_key=b142c98c-6e4b-4580-8de1-ac34e5be8a30
#lyrics way - https://www.metal-archives.com/release/ajax-view-lyrics/id/72592
import requests
import json
from bs4 import BeautifulSoup

payload = {'api_key': 'b142c98c-6e4b-4580-8de1-ac34e5be8a30'}

def getAlbumID(album):
    query='http://em.wemakesites.net/search/album_title/'+album
    r = requests.get(query,params=payload)
    data=r.json()
    return (data["data"]["search_results"][0]["album"]['id'])

if __name__ == '__main__':
    album = input()
    albumID = getAlbumID(album)
    print(albumID)
    import requests
    page = requests.get('https://www.metal-archives.com/albums/Antaeus/Cut_Your_Flesh_and_Worship_Satan/8228')
    print(page.text)
