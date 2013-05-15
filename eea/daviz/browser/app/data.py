""" Data controllers
"""
from urllib2 import urlparse
from zope.component import queryMultiAdapter
from Products.Five.browser import BrowserView

class Info(BrowserView):
    """ Data source info
    """
    def __init__(self, context, request):
        super(Info, self).__init__(context, request)
        self._info = {}

    @property
    def info(self):
        """ Info
        """
        if not self._info:
            self._info = {
                'source': {
                    'title': '',
                    'url': '',
                    },
                'owner': {
                    'title': '',
                    'url': ''
                },
                'provenances': []
            }
        return self._info

    def fallback(self):
        """ Try to get data info from relatedItems
        """
        relatedItems = self.context.getRelatedItems()
        for item in relatedItems:
            info = queryMultiAdapter((item, self.request),
                                     name=u'data.info')
            if not info:
                continue

            self.info.update(info())
            break
        return self.info

    def __call__(self, **kwargs):
        field = self.context.getField('dataTitle')
        if field:
            self.info['source']['title'] = field.getAccessor(self.context)()


        field = self.context.getField('dataLink')
        if field:
            self.info['source']['url'] = field.getAccessor(self.context)()

        field = self.context.getField('dataOwner')
        if field:
            vocab = field.Vocabulary(self.context)
            url = field.getAccessor(self.context)()
            title = self.context.displayValue(vocab, url)
            self.info['owner']['title'] = title

            parser = urlparse.urlparse(url)
            if all((parser.scheme, parser.netloc)):
                self.info['owner']['url'] = url
            else:
                self.info['owner']['url'] = self.info['source']['url']

        field = self.context.getField('provenances')
        provenances = field.getAccessor(self.context)()
        formatted_provenances = []
        for provenance in provenances:
            title = provenance.get('title', '')
            link = provenance.get('link', '')
            owner = provenance.get('owner', '')
            if title != '' or owner != '' or link != '':
                formatted_provenance = {'source':{}, 'owner':{}}
                formatted_provenance['source']['title'] = title
                formatted_provenance['source']['url'] = link

                if owner != '':
                    vocab = field.Vocabulary(self.context)
                    owner_title = self.context.displayValue(vocab, owner)
                    formatted_provenance['owner']['title'] = owner_title
                    parser = urlparse.urlparse(owner)
                    if all((parser.scheme, parser.netloc)):
                        formatted_provenance['owner']['url'] = owner
                    else:
                        formatted_provenance['owner']['url'] = link
                formatted_provenances.append(formatted_provenance)

        self.info['provenances'] = formatted_provenances
        return self.info
#        return self.fallback()
