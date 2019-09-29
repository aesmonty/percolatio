from conduit.apps.core.renderers import ConduitJSONRenderer


class FoundationJSONRenderer(ConduitJSONRenderer):
    object_label = 'foundation'
    pagination_object_label = 'foundations'
    pagination_count_label = 'foundationsCount'

