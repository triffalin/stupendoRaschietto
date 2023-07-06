# -*- coding: utf-8 -*-

from providerModules.stupendoRaschietto import core

class sources(core.DefaultSources):
    def __init__(self, *args, **kwargs):
        super(sources, self).__init__(__name__, *args, **kwargs)