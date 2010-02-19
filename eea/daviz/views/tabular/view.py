# -*- coding: utf-8 -*-

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from zope.interface import implements
from zope.component import queryAdapter
from Products.Five.browser import BrowserView
from eea.daviz.interfaces import IDavizConfig
from interfaces import IExhibitTabularView

class View(BrowserView):
    """ Tabular view
    """
    label = 'Tabular View'
    implements(IExhibitTabularView)

    @property
    def columns(self):
        adapter = queryAdapter(self.context, IDavizConfig)
        res = [facet.get('name') for facet in adapter.facets]
        res = ['.%s' % item for item in res]
        return ', '.join(res)
