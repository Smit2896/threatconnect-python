""" standard """
import types

""" custom """
from threatconnect import FilterMethods
from threatconnect.Config.ResourceProperties import ResourceProperties
from threatconnect.Config.ResourceType import ResourceType
from threatconnect.Config.VictimAssetType import VictimAssetType
from threatconnect.Properties.VictimAssetsProperties import VictimAssetsProperties
from threatconnect.Resource import Resource
from threatconnect.FilterObject import FilterObject

""" Note: PEP 8 intentionally ignored for variable/methods to match API standard. """


class VictimAssets(Resource):
    """ """

    def __init__(self, tc_obj):
        """ """
        super(VictimAssets, self).__init__(tc_obj)
        self._filter_class = VictimAssetFilterObject

        # set properties
        properties = VictimAssetsProperties()
        self._http_method = properties.http_method
        self._owner_allowed = properties.base_owner_allowed
        self._resource_pagination = properties.resource_pagination
        self._request_uri = properties.base_path
        self._resource_type = properties.resource_type


class VictimAssetFilterObject(FilterObject):
    """ """

    def __init__(self, victim_asset_type_enum=None):
        """ """
        super(VictimAssetFilterObject, self).__init__()
        self._owners = []

        # get resource type from indicator type
        if isinstance(victim_asset_type_enum, VictimAssetType):
            # get resource type from indicator type number
            resource_type = ResourceType(victim_asset_type_enum.value)

            # get resource properties from resource type name
            self._properties = ResourceProperties[resource_type.name].value()
        else:
            self._properties = ResourceProperties['VICTIM_ASSETS'].value()

        # define properties for resource type
        self._owner_allowed = self._properties.base_owner_allowed
        self._resource_pagination = self._properties.resource_pagination
        self._request_uri = self._properties.base_path
        self._resource_type = self._properties.resource_type

        #
        # add_obj filter methods
        #
        for method_name in self._properties.filters:
            method = getattr(FilterMethods, method_name)
            setattr(self, method_name, types.MethodType(method, self))