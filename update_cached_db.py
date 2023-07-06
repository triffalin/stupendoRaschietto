# -*- coding: utf-8 -*-

import os
import sys
import importlib
import time
import requests

STUPENDORASCHIETTO_ENV = os.getenv('STUPENDORASCHIETTO_ENV')
if STUPENDORASCHIETTO:
  for env_var in STUPENDORASCHIETTO.split('|==|'):
    if env_var == '':
      continue
    env_var_sep_index = env_var.index('=')
    env_var_name = env_var[:env_var_sep_index]
    env_var_value = env_var[env_var_sep_index+1:]
    os.environ[env_var_name] = env_var_value

dir_name = os.path.dirname(__file__)
providers = os.path.join(dir_name, 'providers')
stupendoRaschietto = os.path.join(providers, 'stupendoRaschietto')
en = os.path.join(stupendoRaschietto, 'en')
torrent = os.path.join(en, 'torrent')

providerModules = os.path.join(dir_name, 'providerModules')
stupendoRaschietto2 = os.path.join(providerModules, 'stupendoRaschietto')
third_party = os.path.join(stupendoRaschietto2, 'third_party')

sys.path.append(dir_name)
sys.path.append(providers)
sys.path.append(stupendoRaschietto)
sys.path.append(en)
sys.path.append(torrent)

sys.path.append(providerModules)
sys.path.append(stupendoRaschietto2)
sys.path.append(third_party)

from providerModules.stupendoRaschietto import core, cache
from providers.stupendoRaschietto.en import torrent as torrent_module

torrent_scrapers = {}
for scraper in torrent_module.__all__:
    if scraper in ['bitlord', 'bitsearch', 'glo', 'kickass', 'lime', 'magnetdl', 'nyaa', 'piratebay', 'torrentapi', 'torrentio', 'torrentdownload', 'torrentgalaxy' 'torrentz2', 'yts']:
        torrent_scrapers[scraper] = importlib.import_module('providers.stupendoRaschietto.en.torrent.%s' % scraper)

url = os.getenv('STUPENDORASCHIETTO_TRAKT_API_URL')

headers_array = os.getenv('STUPENDORASCHIETTO_TRAKT_HEADERS').split(';')
headers = { 'Content-Type': 'application/json' }
for header in headers_array:
  key, value = header.split('=')
  headers[key] = value

movies = requests.get(url, headers=headers).json()
sources_dict = {}

for movie_result in movies:
    full_query = ''
    scraper_results = {}

    movie = movie_result['movie']
    for scraper in torrent_scrapers:
        sources = sources_dict.setdefault(scraper, torrent_scrapers[scraper].sources())
        results = sources.movie(movie['title'], str(movie['year']), movie['ids']['imdb'])

        if not isinstance(sources.scraper, core.NoResultsScraper):
            full_query = sources.scraper.full_query
            scraper_results[scraper] = results

    cache.set_cache(full_query, scraper_results)