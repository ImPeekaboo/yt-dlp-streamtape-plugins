from __future__ import unicode_literals

from .common import InfoExtractor
from ..utils import js_to_json, urljoin

# strings are obfuscated by concatenating substrings
split_string_part = r'(?:%s|%s)' % (r'"(?:[^"\\]|\\.)*"',
                                    r"'(?:[^'\\]|\\.)*'")
split_string = r'(?:' + split_string_part + r'(?:\s*\+\s*' + split_string_part + r')*)'
videolink = r"(?:'\+')?".join('videolink')
videolink = r"document\.getElementById\('" + videolink + r"'\)\.innerHTML\s*=\s*(?P<data>" + split_string + r")"


class StreamtapeIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?streamtape.to/[ev]/(?P<id>[^/?#]+)'
    _TESTS = [{
        'url': 'https://streamtape.to/v/7qDqGjlQe4UA9MR/Soul_Land_03_VOSTFR.mp4',
        'md5': '2bd8790b33d8e445575070774153c19f',
        'info_dict': {
            'id': '7qDqGjlQe4UA9MR',
            'ext': 'mp4',
            'title': 'Soul Land 03 VOSTFR.mp4',
            'thumbnail': r're:^https?://.*\.jpg$',
            'age_limit': 18,
        },
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)

        webpage = self._download_webpage(url, video_id)

        video = self._html_search_regex(videolink, webpage, 'video', group='data')
        video = video.split('+')
        video = [self._parse_json(v, video_id, js_to_json) for v in video]
        video = urljoin(url, ''.join(video))

        try:
            poster = self._html_search_regex(r' id="mainvideo"[^>]* poster="(?P<data>.*?)"',
                                             webpage, 'poster', group='data')
            poster = urljoin(url, poster)
        except ValueError:
            poster = None

        title = self._og_search_title(webpage)

        return {
            'id': video_id,
            'url': video,
            'title': title,
            'thumbnail': poster,
            'age_limit': 18,
            'ext': 'mp4',
        }
