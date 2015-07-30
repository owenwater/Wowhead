#!/usr/bin/python
# encoding: utf-8

from base import Base
from gateway import WowheadGateway
from urllib import urlencode
from urlparse import urlunsplit
from util import show

scheme = 'http'
netloc = 'www.wowhead.com'
fragment = ''

arg_separator = '#'

default_icon = 'icon/blank.png'

class Main(Base):
    def main(self,wf):
        self.gateway = WowheadGateway(wf)
        
        search_result = self.gateway.search(self.args)

        sorted_result = sorted(search_result, key = lambda x: (x['type_id'], x['name']))
        
        self._show_result(sorted_result)

    @show
    def _show_result(self, result):
        if not result:
            self.wf.add_item(
                'search ' + self.args + ' in wowhead.com',
                arg=self._generate_arg({
                    'name':self.args,
                    'type':None,
                    'id':None,
                }),
                valid=True)

        for item in result:
            if item['type'] == 'title':
                item['name'] = item['name'].replace('%s', '<name>')
            
            self.wf.add_item(
                item['name'],
                subtitle=self._generate_subtitle(item),
                modifier_subtitles={
                    'cmd':'Search ' + item['name'],
                    'shift':'Search ' + self.args},
                arg=self._generate_arg(item),
                autocomplete=item['name'],
                valid=True,
                icon=self.gateway.get_image_cache(item['image'], default_icon)
            )
    
    def _generate_subtitle(self, item):
        subtitle = ''
        if item['quality']:
            subtitle = item['quality'].capitalize() + " "
        subtitle += item['type_desc']
        return subtitle

    def _generate_arg(self, item):
        return self._generate_item_url(item) \
            + arg_separator + self._generate_search_url(item['name']) \
            + arg_separator + self._generate_search_url(self.args)
    def _generate_item_url(self, item):
        if item['type'] and item['id']:
            path = '%s=%s' %(item['type'], item['id'])
            query = ''
            return urlunsplit((scheme, netloc, path, query, fragment))
        else:
            return ''

    def _generate_search_url(self, query):
        _, param = self.gateway.generate_search_url(query, json=False)
        path = 'search'
        query = urlencode(param, doseq=True)
        return urlunsplit((scheme, netloc, path, query, fragment))





if __name__ == "__main__":
    import sys
    main = Main(' '.join(sys.argv[1:]))
    main.execute()
