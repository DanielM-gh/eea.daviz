""" Daviz content schema
"""
import logging
from zope.event import notify
from Products.Archetypes.atapi import Schema
from plone.app.folder.folder import ATFolder
from eea.daviz.config import EEAMessageFactory as _
from eea.daviz.events import DavizRelationsChanged, DavizSpreadSheetChanged
from Products.Archetypes.public import StringField, ReferenceField
from Products.Archetypes.public import TextAreaWidget, StringWidget, LabelWidget
from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
from eea.forms.widgets.QuickUploadWidget import QuickUploadWidget
logger = logging.getLogger('eea.daviz')
#
# eea.relations
#
EEAReferenceField = ReferenceField
EEAReferenceBrowserWidget = ReferenceBrowserWidget
try:
    from eea.relations.field.referencefield import EEAReferenceField
    from eea.relations.widget.referencewidget import EEAReferenceBrowserWidget
except ImportError:
    logger.warn('eea.relations is not installed')
#
# eea.dataservice
#
OrganisationsWidget = StringWidget
OrganisationsVocabulary = None
try:
    from eea.dataservice.widgets import OrganisationsWidget
    OrganisationsVocabulary = u'Organisations'
except ImportError:
    logger.warn('eea.dataservice is not installed')


class DavizReferenceField(EEAReferenceField):
    """ Notify on set
    """
    def set(self, instance, value, **kwargs):
        """ Notify custom event on set
        """
        old = self.getRaw(instance, aslist=True)
        super(DavizReferenceField, self).set(instance, value, **kwargs)

        if set(old) != set(value):
            relatedItems = self.get(instance, aslist=True)
            notify(DavizRelationsChanged(instance, relatedItems=relatedItems))

class DavizStringField(StringField):
    """ Notify on set
    """
    def set(self, instance, value, **kwargs):
        """ Custom set
        """
        super(DavizStringField, self).set(instance, value, **kwargs)
        notify(DavizSpreadSheetChanged(instance, spreadsheet=value))

class DavizDataField(StringField):
    """ Custom data field
    """

SCHEMA = Schema((
    DavizReferenceField(
        'relatedItems',
        schemata="data input",
        relationship='relatesTo',
        multiValued=True,
        widget=EEAReferenceBrowserWidget(
            label=_("daviz_label_related_items",
                    default="Find and reuse existing data"),
            description=_("daviz_help_related_items",
              default=(
                "Look for compatible datasets in catalogue"
                " (e.g. visualization data, .tsv, .csv, SPARQL, etc)"
              )
            ),
            i18n_domain="eea",
            visible={'edit': 'visible', 'view': 'invisible' }
        )),
    StringField(
        'quickUpload',
        schemata='data input',
        widget=QuickUploadWidget(
            label=_('daviz_label_quick_upload',
                    default='Upload CSV/TSV data files from your computer'),
            description=_('daviz_help_quick_upload',
              default=(
                "Drag and drop '.tsv, .csv files' in the area below, see "
                '<a target="_blank" href="http://www.eea.europa.eu/'
                'data-and-maps/daviz/learn-more/examples">data examples</a> '
                'or read '
                '<a target="_blank" href="http://www.eea.europa.eu/'
                'data-and-maps/daviz/learn-more/prepare-data">'
                'how to prepare data</a>'
              )
            ),
            i18n_domain="eea",
            visible={'edit': 'visible', 'view': 'invisible' }
        )
    ),
    DavizStringField(
        'spreadsheet',
        schemata='data input',
        validators=('csvfile',),
        widget=TextAreaWidget(
            label=_('daviz_label_spreadsheet',
                    default='Copy and paste a data table from a file/webpage'),
            description=_('daviz_help_spreadsheet',
              default=(
                "Check these "
                '<a target="_blank" href="http://www.eea.europa.eu/'
                'data-and-maps/daviz/learn-more/examples">data examples</a> '
                'or read '
                '<a target="_blank" href="http://www.eea.europa.eu/'
                'data-and-maps/daviz/learn-more/prepare-data">'
                'how to prepare data</a>'
              )
            ),
        i18n_domain="eea",
        helper_js=('++resource++eea.daviz.spreadsheet.js',),
        helper_css=('++resource++eea.daviz.spreadsheet.css',),
        visible={'edit': 'visible', 'view': 'invisible'}
        )
    ),
    StringField(
        'dataWarning',
        schemata='data input',
        widget=LabelWidget(
            label=_('daviz_label_dataWarning',
                default='Warning'),
            description=_('daviz_help_dataWarning',
                default=(
                    "Changing data sources may break existing "
                    "visualizations for this context. You should consider "
                    "creating a new Visualization rather than changing this "
                    "one if the new data is different than the existing one. "
                    "Are you sure you want to continue?"
                )
            ),
            i18n_domain="eea",
            helper_js=('++resource++eea.daviz.warnings.js',),
            helper_css=('++resource++eea.daviz.edit.css',),
            visible={'edit': 'visible', 'view': 'invisible'}
        )
    ),
    DavizDataField(
        'dataTitle',
        schemata='default',
        widget=StringWidget(
            label=_('daviz_label_dataTitle', default="Data source title"),
            description=_('daviz_help_dataTitle',
                          default="Specify data source"),
            i18n_domain="eea",
        ),
    ),
    DavizDataField(
        'dataLink',
        schemata='default',
        widget=StringWidget(
            label=_('daviz_label_dataLink', default="Data source link"),
            description=_('daviz_help_dataLink',
                          default="Specify data source link"),
            i18n_domain="eea",
            helper_js=('++resource++eea.daviz.datasource.js',),
            helper_css=('++resource++eea.daviz.datasource.css',)
        )
    ),
    DavizDataField(
        'dataOwner',
        schemata='default',
        vocabulary_factory=OrganisationsVocabulary,
        widget=OrganisationsWidget(
            label=_('daviz_label_dataOwner',
                    default="Data source Organisation"),
            description=_('daviz_help_dataOwner',
                          default="Specify data source Organisation"),
            i18n_domain="eea",
        )
    ),
))

DAVIZ_SCHEMA = ATFolder.schema.copy() + SCHEMA.copy()

def finalizeSchema(schema=DAVIZ_SCHEMA):
    """ Reorder and update schemata
    """
    # Move all fields to Metadata schemata
    for field in schema.fields():
        # Leave this fields in their original schemata
        if field.schemata == 'data input':
            continue

        # We use schema extender for this fields, so leave them in
        # categorization tab
        if field.getName() in ('subject', 'location', 'themes'):
            field.schemata = 'categorization'
            continue

        # Group all the other fields in a new schemata. Don't try to use
        # 'metadata' as it seems to be a reserved keyword in Plone (or EEA)
        field.schemata = 'other metadata'

    # Add a default value for title
    schema['title'].default = u'Data Visualization'

    # Reorder data input fields
    schema.moveField('spreadsheet', pos=0)
    schema.moveField('quickUpload', after="spreadsheet")
    schema.moveField('relatedItems', after="quickUpload")

    # Reorder data source fields
    schema.moveField('dataTitle', after='description')
    schema.moveField('dataLink', after='dataTitle')
    schema.moveField('dataOwner', after='dataLink')


finalizeSchema(DAVIZ_SCHEMA)