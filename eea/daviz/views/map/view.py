# -*- coding: utf-8 -*-

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from zope.interface import implements
from interfaces import IExhibitMapView
from eea.daviz.views.view import ViewForm

class View(ViewForm):
    """ Thumbnail view
    """
    label = 'Map View'
    implements(IExhibitMapView)

    @property
    def latlng(self):
        """ Return latitude longitude column
        """
        return self.data.get('latlng', '')
