Owl is a simple python script which I created in a night (thus, the name) to find out which is the most viewed video of a YouTube channel.

Owl accesses the YouTube Data API, to find out which video has the most views
It currently fetches for my favorite channel, [CokeStudioPK](https://www.youtube.com/user/CokeStudioPk), paginates to get all the videos uploaded, ignores the channels or playlists, and considers only the videos which have a like count greater than 1000.

You'll need to change the API Key to your own, though. Get it from [console.developers.google.com](https://console.developers.google.com/)

Run Owl from command line, once you have the API Key, as long as you have the `json` and `urllib2` modules installed

`$python owl.py`

In the end it will tell you about the most watched video, while printing which video it is currently processing

![Sample result of the script, showing Tajdar-e-Haram to be the most viewed video of the channel](http://i.imgur.com/QOPciSG.png)

Note:
-----
 - Calls to YouTube Data API will cost against your Quota, read the developer documentation on Google APIs from Google
 - You'll need to know the channel ID (not the channel user name) of the channel you want this to work for
 
Any questions? Ask me on Twitter [@AmanAlam](https://www.twitter.com/AmanAlam)
