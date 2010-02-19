# -*- coding: utf-8 -*-

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from zope.interface import implements
from interfaces import IDavizConfig
try:
    from zope.annotation.interfaces import IAnnotations
except ImportError:
    #BBB Plone 2.5
    from zope.app.annotation.interfaces import IAnnotations

from persistent.dict import PersistentDict
from persistent.list import PersistentList
from eea.daviz.config import ANNO_VIEWS, ANNO_FACETS, ANNO_JSON

class Configure(object):
    """ Get daviz configuration
    """
    implements(IDavizConfig)

    def __init__(self, context):
        self.context = context

    def _views(self):
        anno = IAnnotations(self.context)
        views = anno.get(ANNO_VIEWS, None)
        if views is None:
            views = anno[ANNO_VIEWS] = PersistentList()
        return views

    def _facets(self):
        anno = IAnnotations(self.context)
        facets = anno.get(ANNO_FACETS, None)
        if facets is None:
            facets = anno[ANNO_FACETS] = PersistentList()
        return facets

    def _json(self):
        anno = IAnnotations(self.context)
        json = anno.get(ANNO_JSON, None)
        if json is None:
            json = anno[ANNO_JSON] = PersistentDict()
        return json
    #
    # Accessors
    #
    @property
    def views(self):
        """ Return daviz enabled views
        """
        anno = IAnnotations(self.context)
        return anno.get(ANNO_VIEWS, [])

    @property
    def facets(self):
        """ Return daviz enabled facets
        """
        anno = IAnnotations(self.context)
        return anno.get(ANNO_FACETS, [])

    def set_json(self, value):
        """ Set json dict
        """
        anno = IAnnotations(self.context)
        anno[ANNO_JSON] = PersistentDict(value)

    def get_json(self):
        """ Return json from annotations
        """
        anno = IAnnotations(self.context)
        json = anno.get(ANNO_JSON, {})
        return json
    json = property(get_json, set_json)

    def view(self, key, default=None):
        """ Return view by given key
        """
        for view in self.views:
            if view.get('name', None) == key:
                return view
            return default

    def facet(self, key, default=None):
        """ Return facet by given key
        """
        for facet in self.facets:
            if facet.get('name') != key:
                continue
            return facet
        return default
    #
    # Mutators
    #
    def add_view(self, name, **kwargs):
        """ Add view
        """
        config = self._views()
        view = PersistentDict({
            'name': name
        })
        config.append(view)
        return view.get('name', '')

    def delete_view(self, key):
        """ Delete view by given key
        """
        config = self._views()
        for index, view in enumerate(config):
            if view.get('name', '') == key:
                config.pop(index)
                return
        raise KeyError, key

    def delete_views(self):
        """ Reset views
        """
        anno = IAnnotations(self.context)
        anno[ANNO_VIEWS] = PersistentList()

    def add_facet(self, name, **kwargs):
        """ Add facet
        """
        config = self._facets()
        facet_type = kwargs.get('type', u'daviz.list.facet')
        facet = PersistentDict({
            'name': name,
            'type': facet_type,
        })
        config.append(facet)
        return facet.get('name', '')

    def delete_facet(self, key):
        """ Delete facet by given key
        """
        config = self._facets()
        for index, facet in enumerate(config):
            if facet.get('name', '') == key:
                config.pop(index)
                return
        raise KeyError, key

    def delete_facets(self):
        """ Remove all facets
        """
        anno = IAnnotations(self.context)
        anno[ANNO_FACETS] = PersistentList()
