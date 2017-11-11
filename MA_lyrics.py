#api_key=b142c98c-6e4b-4580-8de1-ac34e5be8a30
#lyrics way - https://www.metal-archives.com/release/ajax-view-lyrics/id/72592
import sys
import collections
import requests
import json
from bs4 import BeautifulSoup
import re
import os
from mutagen.id3 import ID3, USLT

payload = {'api_key': 'b142c98c-6e4b-4580-8de1-ac34e5be8a30'}

class Album:
    def __init__(self,artist_tag,album_tag,tracklist):
        self.artist = artist_tag
        self.album = album_tag
        self.tracklist = tracklist
    def GetInfoMA(self):
        query='http://em.wemakesites.net/search/album_title/'+self.album
        r = requests.get(query,params=payload)
        print(self.album,self.artist)
        data=r.json()
        for item in data["data"]["search_results"]:
            if bandtag.lower()==item["band"]["name"].lower() and albumtag.lower()==item["album"]["title"].lower():
                self.album_id_MA = data["data"]["search_results"][0]["album"]['id']
                self.band_name_MA = data["data"]["search_results"][0]["band"]["name"].replace(" ", "_")
                self.album_name_MA = data["data"]["search_results"][0]["album"]["title"].replace(" ", "_")
        query='http://em.wemakesites.net/album/'+self.album_id_MA
        r = requests.get(query,params=payload)
        data = r.json()
        i=1
        self.tracklist_MA={}
        for item in data["data"]["album"]["songs"]:
            self.tracklist_MA[i]=item["title"]
            i=i+1
        print('MA album playlist')
        print(self.tracklist_MA)
    def GetLyricsMA(self):
        page = requests.get('https://www.metal-archives.com/albums/'+A.band_name_MA+'/'+A.album_name_MA+'/'+A.album_id_MA)
        soup = BeautifulSoup(page.text, 'html.parser')
    #print(soup.prettify())
        s=soup.find_all(id=re.compile('(?<=song)\d+'))
    #going to have list of songid
        songid=[]
        for item in s:
            songid.append(re.search('(?<=song)\d+',str(item)).group())
        self.lyrics_MA=dict.fromkeys(songid)
        for item in self.lyrics_MA.keys():
            page1 = requests.get('https://www.metal-archives.com/release/ajax-view-lyrics/id/'+item)
            self.lyrics_MA[item]=BeautifulSoup(page1.text,'html.parser').get_text()
    def UpdateLyrics(self, file_paths):
        i=0
        lyrics=list(self.lyrics_MA.values())
        for item in file_paths:
            song=ID3(item)
            song.add(USLT(text=lyrics[i]))
            song.save()
            i=i+1

def getAlbumFromTag(path):
    band_names=[]
    album_titles = []
    play_list={}
    file_paths=[]
    i=1
    for root, dirs, files in os.walk(os.path.abspath(path)):
        for file in files:
            print(os.path.join(root, file))
            if os.path.join(root, file).endswith(".mp3"):
                file_paths.append(os.path.join(root, file))
                song=ID3(os.path.join(root, file))
                if song["TPE1"].text[0] not in band_names:
                    band_names.append(song["TPE1"].text[0])
                if song["TALB"].text[0] not in album_titles:
                    album_titles.append(song["TALB"].text[0])
                play_list[i] = song["TIT2"].text[0]
                i=i+1
    print(band_names)
    print(album_titles)
    print(play_list)
    if len(band_names)==1 and len(album_titles)==1:
        return band_names[0], album_titles[0], play_list, file_paths

if __name__ == '__main__':
    while True:
        full_path=input('please enter full path to folder:')
        bandtag, albumtag, tracklist, file_paths = getAlbumFromTag(full_path)
        A=Album(bandtag,albumtag,tracklist)
        try:
            A.GetInfoMA()
            break
        except TypeError:
            print('Album %s of %s was not found, please try again' % (A.album, A.artist))
    A.GetLyricsMA()
    ans = input("do you want to update lyrics?")
    if ans=='y':
        A.UpdateLyrics(file_paths)
