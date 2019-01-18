import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MyProject.settings")
django.setup()

from hotshot.channel.lishipin.config import LISHIPIN_URL, headers, LISHIPIN_MORE_URL
from hotshot.models import LSPHotVideoModel
from hotshot.utils.fetch import fetch


class LiShiPin:
    def get_hot_video(self):
        response = fetch(LISHIPIN_URL, headers=headers)
        resultCode = response['resultCode']
        if resultCode == '1':
            dataListDict = response['dataList']
            for data in dataListDict:
                nodeType = data.get('nodeType')
                if nodeType == '1' or nodeType == '6':
                    contList = data.get('contList')
                    if contList != None:
                        for cont in reversed(contList):
                            contId = cont['contId']
                            self.get_more_from_id(contId)

    def get_more_from_id(self, id):
        response = fetch(LISHIPIN_MORE_URL + id, headers=headers)
        resultCode = response['resultCode']
        if resultCode == '1':
            data = {}
            content = response['content']
            data['title'] = content['name']
            data['des'] = content['summary']
            data['cover'] = content['pic']
            videos = content['videos']
            for video in videos:
                tag = video['tag']
                if tag == 'hd':
                    data['playUrl'] = video['url']
            self.inser_video_data(data, type='hot')

    def inser_video_data(self, data, type='hot'):
        if type == 'hot':
            LSPHotVideoModel.objects.update_or_create(title=data['title'], description=data['des'],
                                            cover=data['cover'], playUrl=data['playUrl'])


if __name__ == '__main__':
    lishipin = LiShiPin()
    lishipin.get_hot_video()
