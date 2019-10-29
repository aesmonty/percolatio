from conduit.apps.core.renderers import ConduitJSONRenderer


class GrantJSONRenderer(ConduitJSONRenderer):
    object_label = 'grant'
    pagination_object_label = 'grants'
    pagination_count_label = 'grantsCount'
