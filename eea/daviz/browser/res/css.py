# -*- coding: utf-8 -*-

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from App.Common import rfc1123_date
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.ResourceRegistries.tools.packer import CSSPacker

class CSS(object):
    """ Handle criteria
    """
    def __init__(self, context, request, resources=()):
        self.context = context
        self.request = request
        self._resources = resources
        self.duration = 3600*24*365

        self.csstool = getToolByName(context, 'portal_css', None)
        if self.csstool:
            self.debug = self.csstool.getDebugMode()

    @property
    def resources(self):
        """ Return resources
        """
        return self._resources

    def get_resource(self, resource):
        """ Get resource content
        """
        obj = self.context.restrictedTraverse(resource, None)
        if not obj:
            return '/* ERROR */'
        try:
            content = obj.GET()
        except AttributeError, err:
            return str(obj)
        except Exception, err:
            return '/* ERROR: %s */' % err
        else:
            return content

    def get_content(self, **kwargs):
        """ Get content
        """
        output = []
        for resource in self.resources:
            content = self.get_resource(resource)
            header = '\n/* - %s - */\n' % resource
            if not self.debug:
                content = CSSPacker('safe').pack(content)
            output.append(header + content)
        return '\n'.join(output)

    @property
    def helper_css(self):
        """ Helper css
        """
        return []

class ViewCSS(CSS):
    """ CSS libs used in view mode
    """
    @property
    def css_libs(self):
        """ CSS libs
        """
        res = []
        res.extend(('++resource++eea.daviz.view.css',))
        return res

    @property
    def resources(self):
        """ Return view resources
        """
        res = self.helper_css
        res.extend(self.css_libs)
        return res

    def __call__(self, *args, **kwargs):
        """ view.css
        """
        self.request.RESPONSE.setHeader('content-type', 'text/css')
        expires = rfc1123_date((DateTime() + 365).timeTime())
        self.request.RESPONSE.setHeader('Expires', expires)
        self.request.RESPONSE.setHeader('Cache-Control', 'max-age=%d' % self.duration)
        return self.get_content()

class EditCSS(CSS):
    """ CSS libs used in edit form
    """
    @property
    def css_libs(self):
        res = []
        jquery_ui = False
        for css in self.csstool.getResources():
            if not css.getEnabled():
                continue
            css_id = css.getId()
            if 'jquery-ui-1.7.custom.css' in css_id:
                jquery_ui = True
            if jquery_ui:
                break

        if not jquery_ui:
            res.append('++resource++jquery.ui.theme/jquery-ui-1.7.custom.css')

        res.append('++resource++eea.daviz.edit.css')
        return res

    @property
    def resources(self):
        """ Return edit resources
        """
        res = self.helper_css
        res.extend(self.css_libs)
        return res

    def __call__(self, *args, **kwargs):
        """ edit.css
        """
        self.request.RESPONSE.setHeader('content-type', 'text/css')
        expires = rfc1123_date((DateTime() + 365).timeTime())
        self.request.RESPONSE.setHeader('Expires', expires)
        self.request.RESPONSE.setHeader('Cache-Control', 'max-age=%d' % self.duration)
        return self.get_content()
