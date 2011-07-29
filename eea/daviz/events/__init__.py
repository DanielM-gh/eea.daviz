# -*- coding: utf-8 -*-

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alec Ghica, Alin Voinea"""

from zope.interface import implements
from interfaces import IDavizEnabledEvent, IDavizFacetDeletedEvent

class DavizEnabledEvent(object):
    """ Sent if a document was converted to exhibit json
    """
    implements(IDavizEnabledEvent)

    def __init__(self, context, **kwargs):
        self.object = context
        self.columns = kwargs.get('columns', [])

class DavizFacetDeletedEvent(object):
    """ Sent if a daviz facet was deleted
    """
    implements(IDavizFacetDeletedEvent)

    def __init__(self, context, **kwargs):
        self.object = context
        self.facet = kwargs.get('facet', '')
