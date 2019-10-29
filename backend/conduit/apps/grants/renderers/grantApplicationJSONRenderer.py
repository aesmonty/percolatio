from conduit.apps.core.renderers import ConduitJSONRenderer


class GrantApplicationJSONRenderer(ConduitJSONRenderer):
    object_label = 'grantApplication'
    pagination_object_label = 'grantApplications'
    pagination_count_label = 'grantApplicationsCount'
