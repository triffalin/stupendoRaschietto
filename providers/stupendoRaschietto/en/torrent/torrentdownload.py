# -*- coding: utf-8 -*-

from providerModules.stupendoRaschietto import core

class sources(core.DefaultSources):
    def __init__(self, *args, **kwargs):
        super(sources, self).__init__(__name__, *args, **kwargs)

    def _parse_magnet(self, row, row_tag=''):
        matches = core.safe_list_get(core.re.findall(r'<a href="\/([0-9A-Z]*?)\/(.*?)>', row), 0, [])
        if len(matches) == 2:
          return 'magnet:?xt=urn:btih:%s&dn=%s' % (matches[0], matches[1])
        return None

    def _parse_seeds(self, row):
        return core.safe_list_get(core.re.findall(r'<td class="tdseed">(.*?)</td>', row), 0)