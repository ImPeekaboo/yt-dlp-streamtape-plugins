import re

#from __future__ import unicode_literals

from yt_dlp.extractor.common import InfoExtractor
from yt_dlp.utils import js_to_json, urljoin


class StreamtapeIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?streamtape.[comt]+/[ev]/(?P<id>[^/?#]+)'
    _TESTS = [{
        'url': 'https://streamtape.to/v/7qDqGjlQe4UA9MR/Soul_Land_03_VOSTFR.mp4',
        'md5': '2bd8790b33d8e445575070774153c19f',
        'info_dict': {
            'id': '7qDqGjlQe4UA9MR',
            'ext': 'mp4',
            'title': 'Soul Land 03 VOSTFR.mp4',
            'age_limit': 18,
        },
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        PREFIX='https:/'

        html = self._download_webpage(url, video_id)
        token = re.match(r".*document.getElementById.*\('norobotlink'\).innerHTML =.*?token=(.*?)'.*?;", html, re.M|re.S).group(1)
        infix=re.match(r'.*<div id="ideoooolink" style="display:none;">(.*?token=).*?<[/]div>', html, re.M|re.S).group(1)
        final_URL=f'{PREFIX}{infix}{token}'
        orig_title=re.match(r'.*<meta name="og:title" content="(.*?)">', html, re.M|re.S).group(1)

        #video,title = get_curl_command(url,webpage)

        return {
            'id': video_id,
            'url': final_URL,
            'title': orig_title,
            'age_limit': 18,
            'ext': 'mp4',
        }
