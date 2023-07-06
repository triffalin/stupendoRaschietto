# -*- coding: utf-8 -*-

import os
import unittest
import importlib

os.environ['STUPENDORASCHIETTO_TEST'] = '1'
#os.environ['STUPENDORASCHIETTO_TEST_ALL'] = '1' # verifica tutti gli URL per tracker
#os.environ['STUPENDORASCHIETTO_TEST_TOTAL'] = '1'
os.environ['STUPENDORASCHIETTO_CACHE_LOG'] = '1'

from providerModules.stupendoRaschietto import core
from providers.stupendoRaschietto import en as scrapers

torrent_scrapers = {}
for scraper in scrapers.get_torrent():
    torrent_scrapers[scraper] = importlib.import_module('providers.stupendoRaschietto.en.torrent.%s' % scraper)

hoster_scrapers = {}
for scraper in scrapers.get_hosters():
    hoster_scrapers[scraper] = importlib.import_module('providers.stupendoRaschietto.en.hosters.%s' % scraper)

from providerModules.stupendoRaschietto.test_utils import test_torrent, test_hoster, total_results

class TestTorrentScraping(unittest.TestCase):
    pass

class TestHosterScraping(unittest.TestCase):
    pass

for scraper in scrapers.get_torrent():
    method = lambda scraper: lambda self: test_torrent(self, torrent_scrapers[scraper], scraper)
    setattr(TestTorrentScraping, 'test_%s' % scraper, method(scraper))

for scraper in scrapers.get_hosters():
    method = lambda scraper: lambda self: test_hoster(self, hoster_scrapers[scraper], scraper)
    setattr(TestHosterScraping, 'test_%s' % scraper, method(scraper))

if os.getenv('STUPENDORASCHIETTO_TEST_TOTAL') == '1':
    def log_results(self):
        for title in total_results.keys():
            print(title.encode('utf8'))
        print('Total results: %s' % len(total_results.keys()))

    setattr(TestTorrentScraping, 'test_zzz', log_results)

if __name__ == '__main__':
    unittest.main()