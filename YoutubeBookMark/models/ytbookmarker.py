from pytube import YouTube


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
        return (f"'url': '{self.url}', 'video name': '{self.title}', 'channel name': '{self.channel_name}'")

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
            vid_title = self.get_url().title
        else:
            vid_title = 'No video found.'
        return(vid_title)
    

    def get_channel_name(self) -> str:
        if self.get_url():
            # Get the author of the video
            c_name = self.get_url().author
        else:
            c_name  = 'No Channel Name found'
        return (c_name )




# url = "https://www.youtube.com/watch?v=z18nw4adsx4"
# details = YouTubeBookMarker(url)
# print(f"Video Name: {details.get_title()}, Channel Name: {details.get_channel_name()}")