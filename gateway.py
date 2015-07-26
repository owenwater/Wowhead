#!/usr/bin/python
# encoding: utf-8

from workflow import web
import json
import os.path
import urllib
search_url_tem = 'http://www.wowhead.com/search'
list_json = 'data/list.json'
faction_icon = 'icon/'
image_url_tem = 'http://wow.zamimg.com/images/wow/icons/large/%s.jpg'
image_suffix = ".jpg"

class WowheadGateway(object):
    
    result_list = 1
    metadata_list = -1

    def __init__(self, wf):
        with open(list_json) as fp:
            self.metadata_list = json.load(fp)
        self.cachedir = wf.cachedir

    def get_image_cache(self, image_name, default_image=None):
        if not image_name:
            return default_image

        if image_name.endswith("-icon.png"):
            return faction_icon + image_name
        image_cache_path = os.path.join(self.cachedir, image_name + image_suffix)

        if not os.path.isfile(image_cache_path):
            image_url = image_url_tem %(image_name)
            urllib.urlretrieve(image_url, image_cache_path)
        return image_cache_path


    def search(self, word):
        url, params = self.generate_search_url(word)
        response = self._send_request(url, params).json()
        ret = self._parse_json(response)
        return ret

    def generate_search_url(self, word, json=True):
        if json:
            return search_url_tem, {'q': word, 'opensearch': ''}
        else:
            return search_url_tem, {'q': word}



    def _parse_json(self, response):
        return [self._parse_data(name, metadata) for name,metadata in zip(response[1], response[-1])]

    def _parse_data(self, name, data):

        name,_,type_desc = name.rpartition('(')
        type_desc, _, _ = type_desc.rpartition(')')

        # data: (type, id, [image | faction] [quality])
        obj_type, obj_id, obj_quality, obj_image = None, None, None, None
        obj_type_id = None
        try:
            obj_type_id = data[0]
            obj_type = self.metadata_list['type'][obj_type_id]
            obj_id = data[1]
        except IndexError:
            pass

        if len(data) >= 3:
            if isinstance(data[2], unicode):
                obj_image = data[2]
            elif obj_type == 'quest' or obj_type == 'title':
                obj_image = self.metadata_list['faction'][data[2]-1]
            elif isinstance(data[2], int):
                obj_quality = self.metadata_list['quality'][data[2]]

        if len(data) >= 4:
            obj_quality = self.metadata_list['quality'][data[3]]
        
        return {
            'name': name,
            'type_desc': type_desc,
            'type_id': obj_type_id,
            'type': obj_type,
            'id': obj_id,
            'image': obj_image, 
            'quality': obj_quality,

        }

    
    def _send_request(self, url, params):
        response = web.get(url, params=params)
        response.raise_for_status()
        return response
    
    
if __name__ == "__main__":
    import sys
    import json
    from workflow import Workflow
    gateway = WowheadGateway(Workflow())
    ret = gateway.search(' '.join(sys.argv[1:]))
    print json.dumps(ret, indent = 2)
