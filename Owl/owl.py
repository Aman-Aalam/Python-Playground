import urllib2
import json

# Copyright 2016, Aman Alam
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This script accesses the YouTube Data API, to find out which video
# from a YouTube channel was the most viewed video
# It currently fetches for CokeStudioPK channel, paginates to get all the videos uploaded,
# ignores the channels or playlists, and considers only the videos which have a like count
# greater than 1000.

# You'll need to change the API Key to your own, though. Read the README on the repo to know how

apiKey = "<put-your-own-API-Key-Here>"  # Put your API Key here
channelCokeStudioId = "UCM1VesJtJ9vTXcMLLr_FfdQ"
getListUrl = "https://www.googleapis.com/youtube/v3/search?order=date&part=snippet" \
             "&channelId={}&maxResults=50&safeSearch=none&&type=video&key={}"
getVideoStatsUrl = "https://www.googleapis.com/youtube/v3/videos?part=contentDetails,statistics" \
                   "&id={}&key={}"
paramPageToken = "&pageToken="
largestViewCount = 0

viewCountThreshold = 10000  # ignore any video below this view count.


def getjsonfromurl(url):
    response_body = urllib2.urlopen(url).read()
    return response_body


def getallvideos(channelid):
    jsonStr = getjsonfromurl(getListUrl.format(channelid, apiKey))
    videoListJsonDict = json.loads(jsonStr)
    print "Will get list of ~{} videos..".format(videoListJsonDict['pageInfo']['totalResults'])
    items = videoListJsonDict['items']
    while ('nextPageToken' in videoListJsonDict):
        jsonStr = getjsonfromurl(getListUrl.format(channelid, apiKey)+paramPageToken+videoListJsonDict['nextPageToken'])
        videoListJsonDict = json.loads(jsonStr)
        items = items+videoListJsonDict['items']
    print "Total videos fetched : ", len(items)
    return items

print "Querying the API.."
items = getallvideos(channelCokeStudioId)

for idx, val in enumerate(items):
    if val['id']['kind'] == "youtube#video":
        print 'Getting info for : '+val['snippet']['title']
        statsJsonStr = getjsonfromurl(getVideoStatsUrl.format(val['id']['videoId'], apiKey))
        videoStatsJsonDict = json.loads(statsJsonStr)
        viewCount = int(videoStatsJsonDict['items'][0]['statistics']['viewCount'])
        if viewCount > viewCountThreshold:
            if largestViewCount < viewCount:
                largestViewCount = viewCount
                mostViewedVideo = [
                    # Video Name
                    val['snippet']['title'],
                    # View Count
                    viewCount,
                    # Like Count
                    videoStatsJsonDict['items'][0]['statistics']['likeCount'],
                    # Youtube Url
                    "https://www.youtube.com/watch?v=" + val['id']['videoId']
                ]
        else:
            print "- Skipping short video "+val['snippet']['title']

print "Most viewed Video: "+mostViewedVideo[0]\
      + ",\nView count: "+str(mostViewedVideo[1])\
      + ",\nLike Count: "+mostViewedVideo[2]\
      + ",\nWatch here : "+mostViewedVideo[3]
