import requests
from pytube import YouTube, Channel, Playlist
from pytube.exceptions import VideoUnavailable, RegexMatchError
from PIL import Image

class YouTubeBookMarker:
    """
    System that bookmarks youtube video url and saves in a website
    """
    def __init__(self, url):
        """Initialize the YouTubeBookMarker class

        Args:
            url (str): this is the video link(url) to bookmark
            user (_type_): user details - fetched by a method that collects
            user login detials
        """
        self.url = url
        self.video = self.get_url()
        self.title = self.get_title()
        self.channel_name = self.get_channel_name()
    
    def __repr__(self):
        return(f"'url': '{self.url}', 'video name': '{self.title}', 'channel name': '{self.channel_name}'")

    # bookmarks = {}

    def get_url(self) -> str:
        """get url link of the vidoe. does not includes playlist link for now
        """
        if '.com/watch?' in self.url:
            self.video = YouTube(self.url)
            return(self.video)
        else:
            return None

    # get the video detials like title and thumbnail
    # author

    def get_title(self) -> str:
        # Get the video name
        if self.get_url():
            author = self.get_url().title
        else:
            author = 'No video found.'
        return(author)
    

    def get_channel_name(self) -> str:
        if self.get_url():
            # Get the author of the video
            author = self.get_url().author
        else:
            author = 'No Channel Name found'
        return (author)
    

    # For future updates
    """
    def get_thumbnail(self, url):
        # Get the video thumbnail
        resized_image = self.get_url.thumbnail.resize((100, 100))
        return (resized_image)
    

    def get_playlist(self, url):
        if "list=" in self.get_url(url):
            playlist = Playlist(self.get_url)
            for video_url in playlist.video_urls:
                self.video = YouTube(video_url)
                self.title = self.get_tile(video_url)
                self.channel_name = self.get_channel_name(video_url)
        else:
            self.video = YouTube(self.video_url)
            self.title = self.get_tile(video_url)
            self.channel_name = self.get_channel_name(video_url)

"""




# url = "https://www.youtube.com/watch?v=cYWiDiIUxQc"
# details = YouTubeBookMarker(url)
# print(f"Video Name: {details.get_title()}, Channel Name: {details.get_channel_name()}")