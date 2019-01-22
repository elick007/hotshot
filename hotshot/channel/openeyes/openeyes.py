import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MyProject.settings")
django.setup()
from hotshot.models import OpenEyesDailyVideo, OpenEyesHotVideo
import json
from hotshot.channel.openeyes import config
from hotshot.utils.fetch import fetch


# Video.objects.create(title='123', cover='456')
# Video.objects.create(title='000',cover='111')
class OpenEyes:

    def get_daily_video(self):
        response = fetch(config.OPENEYES_DAILY_URL, headers=config.header)
        if response == None:
            pass
        # resJson=response.json()
        responseJson = json.loads(response.content)
        issueList = responseJson['issueList']
        itemList = issueList[0]['itemList']
        for item in itemList:
            if item['type'] == 'video':
                data = item['data']
                cover = data['cover']
                srcData = {}
                srcData['title'] = data['title']
                srcData['description'] = data['description']
                srcData['detail'] = cover['detail']
                srcData['playUrl'] = data['playUrl']
                self.insert_video(srcData)

    def get_hot_video(self):
        response = fetch(config.OPENEYES_HOT_URL, headers=config.header)
        if response == None:
            pass
        # responseJson = json.loads(response)
        responseJson = response
        itemList = responseJson['itemList']
        for item in reversed(itemList):
            if item['type'] == 'video':
                data = item['data']
                cover = data['cover']
                srcData = {}
                srcData['title'] = data['title']
                srcData['description'] = data['description']
                srcData['detail'] = cover['detail']
                srcData['playUrl'] = data['playUrl']
                self.insert_video(srcData, 'hot')

    def insert_video(self, data=None, type='daily'):
        if type == 'daily':
            OpenEyesDailyVideo.objects.create(title=data['title'], description=data['description'],
                                              cover=data['detail'],
                                              playUrl=data['playUrl'])
        elif type == 'hot':
            # HotVideo.objects.update_or_create(playUrl=data['playUrl'])
            OpenEyesHotVideo.objects.update_or_create(playUrl=data['playUrl'], defaults={'title': data['title'],
                                                                                         'description': data[
                                                                                             'description'],
                                                                                         'cover': data['detail'],
                                                                                         })

    def deleteVideo(self):
        OpenEyesDailyVideo.objects.filter().delete()


if __name__ == '__main__':
    openeyes = OpenEyes()
    openeyes.get_hot_video()
