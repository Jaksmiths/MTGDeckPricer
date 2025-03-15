import pandas as pd
import urllib.request
from io import BytesIO
from zipfile import ZipFile

class Fetcher:
    """Fetch json.zip files online
    """
    def urlRequester(self, url):
        """Builds a URL request with a given URL link

        Args:
            url: string of a url link

        Returns:
            urllib request
        """
        return urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'} )

    def fetchRequester(self, request, filename):
        """given a urllib request of a zipped json file, fetches the data and returns it

        Args:
            request: urllib request
            filename: string of the json file's name

        Returns:
            pandas dataframe of json file
        """
        with urllib.request.urlopen(request) as url:
            zipf = ZipFile(BytesIO(url.read()))
            req_list = pd.read_json(zipf.open(filename))
            return req_list