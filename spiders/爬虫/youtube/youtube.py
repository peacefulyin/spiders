#coding=utf-8
import requests
from collections import defaultdict
import json
import re
from urllib.parse import urlparse, parse_qs, unquote


QUALITY_PROFILES = {
    # flash
    5: ('flv', '240p', 'Sorenson H.263', 'N/A', '0.25', 'MP3', '64'),

    # 3gp
    17: ('3gp', '144p', 'MPEG-4 Visual', 'Simple', '0.05', 'AAC', '24'),
    36: ('3gp', '240p', 'MPEG-4 Visual', 'Simple', '0.17', 'AAC', '38'),

    # webm
    43: ('webm', '360p', 'VP8', 'N/A', '0.5', 'Vorbis', '128'),
    100: ('webm', '360p', 'VP8', '3D', 'N/A', 'Vorbis', '128'),

    # mpeg4
    18: ('mp4', '360p', 'H.264', 'Baseline', '0.5', 'AAC', '96'),
    22: ('mp4', '720p', 'H.264', 'High', '2-2.9', 'AAC', '192'),
    82: ('mp4', '360p', 'H.264', '3D', '0.5', 'AAC', '96'),
    83: ('mp4', '240p', 'H.264', '3D', '0.5', 'AAC', '96'),
    84: ('mp4', '720p', 'H.264', '3D', '2-2.9', 'AAC', '152'),
    85: ('mp4', '1080p', 'H.264', '3D', '2-2.9', 'AAC', '152'),

    160: ('mp4', '144p', 'H.264', 'Main', '0.1', '', ''),
    133: ('mp4', '240p', 'H.264', 'Main', '0.2-0.3', '', ''),
    134: ('mp4', '360p', 'H.264', 'Main', '0.3-0.4', '', ''),
    135: ('mp4', '480p', 'H.264', 'Main', '0.5-1', '', ''),
    136: ('mp4', '720p', 'H.264', 'Main', '1-1.5', '', ''),
    298: ('mp4', '720p HFR', 'H.264', 'Main', '3-3.5', '', ''),

    137: ('mp4', '1080p', 'H.264', 'High', '2.5-3', '', ''),
    299: ('mp4', '1080p HFR', 'H.264', 'High', '5.5', '', ''),
    264: ('mp4', '2160p-2304p', 'H.264', 'High', '12.5-16', '', ''),
    266: ('mp4', '2160p-4320p', 'H.264', 'High', '13.5-25', '', ''),

    242: ('webm', '240p', 'vp9', 'n/a', '0.1-0.2', '', ''),
    243: ('webm', '360p', 'vp9', 'n/a', '0.25', '', ''),
    244: ('webm', '480p', 'vp9', 'n/a', '0.5', '', ''),
    247: ('webm', '720p', 'vp9', 'n/a', '0.7-0.8', '', ''),
    248: ('webm', '1080p', 'vp9', 'n/a', '1.5', '', ''),
    271: ('webm', '1440p', 'vp9', 'n/a', '9', '', ''),
    278: ('webm', '144p 15 fps', 'vp9', 'n/a', '0.08', '', ''),
    302: ('webm', '720p HFR', 'vp9', 'n/a', '2.5', '', ''),
    303: ('webm', '1080p HFR', 'vp9', 'n/a', '5', '', ''),
    308: ('webm', '1440p HFR', 'vp9', 'n/a', '10', '', ''),
    313: ('webm', '2160p', 'vp9', 'n/a', '13-15', '', ''),
    315: ('webm', '2160p HFR', 'vp9', 'n/a', '20-25', '', '')
}

# The keys corresponding to the quality/codec map above.
QUALITY_PROFILE_KEYS = (
    'extension',
    'resolution',
    'video_codec',
    'profile',
    'video_bitrate',
    'audio_codec',
    'audio_bitrate'
)

class youtube(object):
    def __init__(self, url=None):

        self._filename = None
        self._video_url = None
        self._js_cache = None
        self._videos = []
        if url:
            self.from_url(url)

    def from_url(self, url):
        self._video_url = url
        self._filename = None
        self._videos = []

        video_data = self.get_video_data()

        self.title = video_data.get('args', {}).get('title')

        js_partial_url = video_data.get('assets', {}).get('js')
        if js_partial_url.startswith('//'):
            js_url = 'http:' + js_partial_url
        elif js_partial_url.startswith('/'):
            js_url = 'https://youtube.com' + js_partial_url

        stream_map = video_data.get('args', {}).get('stream_map')
        video_urls = stream_map.get('url')

        for i, url in enumerate(video_urls):
            try:
                itag, quality_profile = self._get_quality_profile_from_url(url)
                if not quality_profile:
                    print('unable to identify profile for itag=%s', itag)
                    continue
            except (TypeError, KeyError) as e:
                print('passing on exception %s', e)
                continue

        self._js_cache = None

    @property
    def url(self):
        return self._video_url

    @url.setter
    def url(self, url):

        print('url setter deprecated, use `from_url()` ''instead.')
        self.from_url(url)

    def get_videos(self):
        return self._videos

    @property
    def filename(self):
        if not self._filename:
            self._filename = safe_filename(self.title)
        return self._filename

    @filename.setter
    def filename(self, filename):

        self.set_filename(filename)

    def truncate(text, max_length=200):
        return text[:max_length].rsplit(' ', 0)[0]

    def safe_filename(text, max_length=200):
        text = text.replace('_', ' ')
        text = text.replace(':', ' -')

        # NTFS forbids filenames containing characters in range 0-31 (0x00-0x1F)
        ntfs = [chr(i) for i in range(0, 31)]

        # Removing these SHOULD make most filename safe for a wide range of
        # operating systems.
        paranoid = ['\"', '\#', '\$', '\%', '\'', '\*', '\,', '\.', '\/', '\:',
                    '\;', '\<', '\>', '\?', '\\', '\^', '\|', '\~', '\\\\']

        blacklist = re.compile('|'.join(ntfs + paranoid), re.UNICODE)
        filename = blacklist.sub('', text)
        return truncate(filename)

    def set_filename(self, filename):

        self._filename = filename
        if self.get_videos():
            for video in self.get_videos():
                video.filename = filename
        return True

    def get(self, extension=None, resolution=None, profile=None):

        result = []
        for v in self.get_videos():
            if extension and v.extension != extension:
                continue
            elif resolution and v.resolution != resolution:
                continue
            elif profile and v.profile != profile:
                continue
            else:
                result.append(v)
        matches = len(result)
        if matches <= 0:
            print('No videos met this criteria.')
        elif matches == 1:
            return result[0]
        else:
            print('Multiple videos met this criteria.')

    def get_video_data(self):
        self.title = None
        response = requests.get(self.url)
        if not response:
            print('Unable to open url: {0}'.format(self.url))

        html = response.text
        if isinstance(html, str):
            restriction_pattern = 'og:restrictions:age'
        else:
            restriction_pattern = bytes('og:restrictions:age', 'utf-8')

        if restriction_pattern in html:
            print('Age restricted video. Unable to download ''without being signed in.')

        json_object = self._get_json_data(html)

        encoded_stream_map = json_object.get('args', {}).get(
            'url_encoded_fmt_stream_map')
        json_object['args']['stream_map'] = self._parse_stream_map(
            encoded_stream_map)
        return json_object

    def _get_json_data(self, html):
        if isinstance(html, str):
            json_start_pattern = 'ytplayer.config = '
        else:
            json_start_pattern = bytes('ytplayer.config = ', 'utf-8')
        pattern_idx = html.find(json_start_pattern)
        # In case video is unable to play
        if(pattern_idx == -1):
            print('Unable to find start pattern.')
        start = pattern_idx + 18
        html = html[start:]

        offset = self._get_json_offset(html)
        if not offset:
            print('Unable to extract json.')
        if isinstance(html, str):
            json_content = json.loads(html[:offset])
        else:
            json_content = json.loads(html[:offset].decode('utf-8'))

        return json_content

    def _get_json_offset(self, html):
        unmatched_brackets_num = 0
        index = 1
        for i, ch in enumerate(html):
            if isinstance(ch, int):
                ch = chr(ch)
            if ch == '{':
                unmatched_brackets_num += 1
            elif ch == '}':
                unmatched_brackets_num -= 1
                if unmatched_brackets_num == 0:
                    break
        else:
            print('json offset处理失败')
        return index + i

    def _parse_stream_map(self, blob):
        """A modified version of `urlparse.parse_qs` that's able to decode
        YouTube's stream map.

        :param str blob:
            An encoded blob of text containing the stream map data.
        """
        dct = defaultdict(list)

        # Split the comma separated videos.
        videos = blob.split(',')

        # Unquote the characters and split to parameters.
        videos = [video.split('&') for video in videos]

        # Split at the equals sign so we can break this key value pairs and
        # toss it into a dictionary.
        for video in videos:
            for kv in video:
                key, value = kv.split('=')
                dct[key].append(unquote(value))
        return dct

    def _get_quality_profile_from_url(self, video_url):

        reg_exp = re.compile('itag=(\d+)')
        itag = reg_exp.findall(video_url)
        if itag and len(itag) == 1:
            itag = int(itag[0])
            quality_profile = QUALITY_PROFILES.get(itag)
            if not quality_profile:
                return itag, None

            return itag, dict(list(zip(QUALITY_PROFILE_KEYS, quality_profile)))
        if not itag:
            print('Unable to get encoding profile, no itag found.')
        elif len(itag) > 1:
            print('Multiple itags found: %s', itag)
            print('Unable to get encoding profile, multiple itags '
                              'found.')
        return False

you = youtube('https://www.youtube.com/watch?v=Ol58Mo98AOE')
you.get('mp4')