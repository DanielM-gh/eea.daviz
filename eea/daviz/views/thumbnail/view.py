# -*- coding: utf-8 -*-

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from zope.interface import implements
from Products.Five.browser import BrowserView
from interfaces import IExhibitThumbnailView

class View(BrowserView):
    """ Thumbnail view
    """
    label = 'Thumbnail View'
    implements(IExhibitThumbnailView)
