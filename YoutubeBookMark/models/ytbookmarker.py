import requests
from pytube import YouTube, Channel, Playlist
from pytube.exceptions import VideoUnavailable
from PIL import Image

class YouTubeBookMarker:
    """
    System that bookmarks youtube video url and saves in a website
    """
    def __init__(self, url: str, title: str, channel_name: str, thumbnail):
        """Initialize the YouTubeBookMarker class

        Args:
            url (str): this is the video link(url) to bookmark
            user (_type_): user details - fetched by a method that collects
            user login detials
        """
        self.url = url
        self.title = self.get_title
        self.thumbnail = self.get_thumbnail
        self.channel_name = self.get_channel_name


    def get_url(self, url) -> str:
        """get url link of the vidoe. Includes playlist link
        """
        try:
            url = str(input("Copy and Paste the YouTube link here!"))
        except VideoUnavailable:
            print(f'No video with the link, cannot bookmark.')
        else:
            return(url)

    # get the video detials like title and thumbnail
    # author
    def get_title(self, url) -> str:
        return (self.get_url.title)
    
    def get_thumbnail(self, url):
        resized_image = self.get_url.thumbnail.resize((100, 100))
        return (resized_image)
    
    def get_channel_name(self, url) -> str:
        return(self.get_url.author)
    
    def check_if_playlist(self) -> bool:
        if "list=" in self.get_url:
            return True

    def get_playlist_url(self):
        if self.check_if_playlist():
            playlist = Playlist(self.get_url)
            for video_url in playlist.video_urls:
                self.url = video_url
                self.tile = self.get_tile(self.get_url(video_url))
                self.channel_name = self.get_channel_name(self.get_url(video_url))
                self.thumbnail = self.get_thumbnail(self.get_url(video_url))
                return


