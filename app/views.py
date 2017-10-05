from flask import g
from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.models.filters import BaseFilter
from flask_appbuilder.models.sqla.filters import get_field_setup_query
from app import db, appbuilder
from .models import Location, Tag, assoc_location_tag
from .models import Contact, Share, Address


class FilterInManyFunction(BaseFilter):
    name = "Filter view where field is in a list returned by a function"

    def apply(self, query, func):
        query, field = get_field_setup_query(query, self.model, self.column_name)
        return query.filter(field.any(Company.id.in_(func())))



class TagModelView(ModelView):
    datamodel = SQLAInterface(Tag)
    list_columns = ['name']
    add_columns = ['name']
    edit_columns = ['name']
    base_order = ('name', 'asc')
    #related_views = [LocationModelView]

class LocationModelView(ModelView):
    datamodel = SQLAInterface(Location)
    list_columns = ['name', 'owner.name', 'address', 'description', 'members', 'tags']
    add_columns = ['name', 'owner', 'address', 'description', 'members', 'tags']
    edit_columns = ['name', 'owner', 'address', 'description', 'members', 'tags']
    base_order = ('name', 'asc')
    related_views = [TagModelView]

class ContactModelView(ModelView):
    datamodel = SQLAInterface(Contact)
    list_columns = ['name', 'phone', 'email', 'friends', 'followers', 'created_by.username']
    add_columns  = ['name', 'phone','email', 'friends', 'followers']
    edit_columns = ['name', 'phone','email', 'friends', 'followers']
    base_order = ('name', 'asc')
    #base_filters = [['created_by.companies', FilterInManyFunction, get_user_companies]]



class AddressModelView(ModelView):
    datamodel = SQLAInterface(Address)
    list_columns = ['street', 'city', 'state', 'zip']
    add_columns = ['street', 'city', 'state', 'zip']
    edit_columns = ['street', 'city', 'state', 'zip']

class ShareModelView(ModelView):
    datamodel = SQLAInterface(Share)
    list_columns = ['follower.name', 'friend.name', 'location.name']
    add_columns = ['follower', 'friend', 'location']
    edit_columns = ['follower', 'friend', 'location']
    #base_order = ('follower.name', 'asc')

    #base_filters = [['friend', FilterEqualFunction, 



db.create_all()
appbuilder.add_view(TagModelView, "List Tags", icon="fa-folder-open-o", category="Locations")
appbuilder.add_view(LocationModelView, "List Locations", icon="fa-folder-open-o", category="Locations")
appbuilder.add_view(AddressModelView, "List Addresses", icon="fa-envelope", category="Locations")
appbuilder.add_separator("Locations")

appbuilder.add_view(ContactModelView, "List Contacts", icon="fa-envelope", category="Contacts")
appbuilder.add_view(ShareModelView, "Shared Locations", icon="fa-envelope", category="Contacts")
appbuilder.add_separator("Contacts")

