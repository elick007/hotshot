import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MyProject.settings")
django.setup()
from rest_framework.authtoken.models import Token
from hotshot.models import DYHotVideoModel, HotShotUser
from hotshot.channel.douyin.config import douyin_hot_video_url, header, douyin_positive_video_url
from hotshot.utils.fetch import fetch


class Douyin:
    def get_hot_video(self):
        response = fetch(douyin_hot_video_url, headers=header)
        if response == None:
            pass
        response_json = response
        status_code = response_json['status_code']
        if status_code == 0:
            data = response_json['data']
            aweme_list = data['aweme_list']
            for aweme in reversed(aweme_list):
                aweme_info = aweme['aweme_info']
                status = aweme_info['status']
                is_delete = status['is_delete']
                if not is_delete:
                    statistics = aweme_info['statistics']
                    author = aweme_info['author']
                    video = aweme_info['video']
                    play_addr = video['play_addr']
                    video_url_list = play_addr['url_list']
                    cover = video['cover']
                    cover_url_list = cover['url_list']
                    duration = aweme_info['music']['duration']
                    data = {}
                    data['author'] = author['nickname']
                    data['view'] = statistics['play_count']
                    data['description'] = aweme_info['desc']
                    data['title'] = aweme_info['desc']
                    data['cover'] = cover_url_list[0]
                    data['playUrl'] = video_url_list[0].replace('https://', 'http://')
                    data['type'] = 'dy'
                    data['date'] = aweme_info['create_time']
                    data['duration'] = duration
                    self.insert_video(data)

    def insert_video(self, data=None):
        DYHotVideoModel.objects.update_or_create(playUrl=data['playUrl'],
                                                 defaults={'author': data['author'], 'view': data['view'],
                                                           'description': data['description'],
                                                           'cover': data['cover'], 'type': data['type'],
                                                           'date': data['date'], 'title': data['title'],
                                                           'duration': data['duration']})

    def get_positive_video(self):
        response = fetch(douyin_positive_video_url, headers=header)
        if response == None:
            pass
        response_json = response
        status_code = response_json['status_code']
        if status_code == 0:
            data = response_json['data']
            aweme_list = data['aweme_list']
            for aweme in aweme_list:
                aweme_info = aweme['aweme_info']
                status = aweme_info['status']
                is_delete = status['is_delete']
                if not is_delete:
                    statistics = aweme_info['statistics']
                    play_count = statistics['play_count']
                    author = aweme_info['author']
                    nickname = author['nickname']
                    video = aweme_info['video']
                    play_addr = video['play_addr']
                    video_url_list = play_addr['url_list']
                    video_url = video_url_list[0]
                    cover = video['cover']
                    cover_url_list = cover['url_list']
                    cover_url = cover_url_list[0]
                    desc = aweme_info['desc']
                    print(nickname + " " + play_count)
                    print(desc)
                    print(cover_url)
                    print(video_url)


if __name__ == '__main__':
    douyin = Douyin()
    douyin.get_hot_video()
