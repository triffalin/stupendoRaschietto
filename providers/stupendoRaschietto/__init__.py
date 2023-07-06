import json

from providers.stupendoRaschietto.en import get_torrent, get_hosters
from providerModules.stupendoRaschietto.source_utils import tools

def optimize_requests(cancel=lambda: False, results=[]):
    def optimize(scrapers, type, ctor_fn):
        for scraper in scrapers:
            if cancel():
                return

            scraper_module = __import__('providers.stupendoRaschietto.en.%s.%s' % (type, scraper), fromlist=[''])
            scraper_results = ctor_fn(scraper_module).optimize_requests()
            results.append(scraper_results)

            tools.log('stupendoRaschietto.optimize.%s:\n%s' % (scraper, json.dumps(scraper_results, sort_keys=True, indent=4)), 'notice')

    optimize(get_torrent(), 'torrent', lambda mod: mod.sources())
    optimize(get_hosters(), 'hosters', lambda mod: mod.source())