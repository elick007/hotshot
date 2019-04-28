import os
import time

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MyProject.settings")
django.setup()

from hotshot.channel.lishipin.config import LISHIPIN_URL, LISHIPIN_MORE_URL, LISHIPIN_HOT_URL, HEADERS
from hotshot.models import LSPHotVideoModel
from hotshot.utils.fetch import fetch


class LiShiPin:
    def get_hot_video(self, url, isSecond):
        if url is None:
            url = LISHIPIN_HOT_URL
        response = fetch(url=url, headers=HEADERS)
        print(response)
        resultCode = response['resultCode']
        if resultCode == '1':
            contList = response['contList']
            for cont in contList:
                contId = cont['contId']
                self.get_more_from_id(contId)
        nextUrl = response['nextUrl']
        if isSecond:
            return
        self.get_hot_video(nextUrl, isSecond=True)

    def get_more_from_id(self, id):
        response = fetch(LISHIPIN_MORE_URL + id, headers=HEADERS)
        print(response)
        resultCode = response['resultCode']
        if resultCode == '1':
            data = {}
            content = response['content']
            data['title'] = content['name']
            data['des'] = content['summary']
            data['cover'] = content['pic']
            date = content['pubTime']
            timeArray = time.strptime(date, "%Y-%m-%d %H:%M")
            data['date'] = str(int(time.mktime(timeArray)) * 1000)
            data['type'] = 'lsp'
            userInfo = content['userInfo']
            data['author'] = userInfo['nickname']
            videos = content['videos']
            for video in videos:
                tag = video['tag']
                if tag == 'hd':
                    data['playUrl'] = video['url']
                    data['duration'] = video['duration']
            if data.get('playUrl') is None:
                return
            self.inser_video_data(data)

    def inser_video_data(self, data):
        LSPHotVideoModel.objects.update_or_create(playUrl=data['playUrl'],
                                                  defaults={'title': data['title'], 'description': data['des'],
                                                            'cover': data['cover'], 'date': data['date'],
                                                            'duration': data['duration'], 'type': data['type'],
                                                            'author': data['author']})


if __name__ == '__main__':
    lishipin = LiShiPin()
    lishipin.get_hot_video(None,False)
