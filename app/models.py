import datetime
from flask import g
from flask_appbuilder.security.sqla.models import User
from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Table
from sqlalchemy.orm import relationship, relation
from sqlalchemy.ext.declarative import declared_attr
from flask_appbuilder.models.mixins import AuditMixin
from flask_appbuilder import Model

mindate = datetime.date(datetime.MINYEAR, 1, 1)




assoc_location_tag = Table('ab_location_tag', Model.metadata,
        Column('id', Integer, primary_key=True),
        Column('location_id', Integer, ForeignKey('location.id')),
        Column('tag_id', Integer, ForeignKey('tag.id'))
)

memberships = Table('location_membership', Model.metadata,
        Column('id', Integer, primary_key=True),
        Column('location_id', Integer, ForeignKey('location.id'), nullable=False),
        Column('contact_id', Integer, ForeignKey('contact.id'), nullable=False)
)

class Tag(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)

    def __repr__(self):
        return self.name

class Address(Model):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    street = Column(String)
    city = Column(String)
    state = Column(String)
    zip = Column(String)

    def __repr__(self):
        return "%s\n%s, %s  %s" % (self.street, self.city, self.state, self.zip)


class Location(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=False, nullable=False)
    owner_id = Column(Integer, ForeignKey('contact.id'), nullable=False)
    owner = relationship("Contact")
    description = Column(String(255))
    #address = Column(String(255))

    address_id = Column(Integer, ForeignKey("address.id"))
    address = relationship("Address")

    members = relationship('Contact', secondary=memberships)
    tags = relationship('Tag', secondary=assoc_location_tag, backref='Location')

    def __repr__(self):
        return self.name





def get_user_id(cls):
        try:
            return g.user.id
        except Exception as e:
            # log.warning("AuditMixin Get User ID {0}".format(str(e)))
            return None




friendships = Table('friendships', Model.metadata,
        Column("friend_id", Integer, ForeignKey("contact.id", primary_key=True), nullable=False),
        Column("follower_id", Integer, ForeignKey("contact.id", primary_key=True), nullable=False)
)

class Contact(Model):
    id = Column(Integer, primary_key=True)
    name  = Column(String(150), unique = True, nullable=False)
    email = Column(String(255))
    phone = Column(String(20))

    friends = relationship(
                "Contact",
                secondary='friendships',
                primaryjoin='Contact.id == friendships.c.follower_id',
                secondaryjoin='Contact.id == friendships.c.friend_id',
                backref='followers',
                cascade="all, delete-orphan",
                single_parent=True,
                order_by="Contact.name",
    )
    
    
    created_on = Column(DateTime, default=datetime.datetime.now, nullable=False)


    @declared_attr
    def created_by_fk(cls):
        #return Column(Integer, ForeignKey('ab_user.id'),
        return Column(Integer, ForeignKey('ab_user.id'),
                      default=cls.get_user_id, nullable=False)

    @declared_attr
    def created_by(cls):
        return relationship("User", primaryjoin='%s.created_by_fk == User.id' % cls.__name__, enable_typechecks=False)

    def __repr__(self):
        return self.name

    @classmethod
    def get_user_id(cls):
        try:
            return g.user.id
        except Exception as e:
            # log.warning("AuditMixin Get User ID {0}".format(str(e)))
            return None 



class Share(Model):
    __tablename__ = 'shared_locations'

    follower_id = Column(Integer, ForeignKey("contact.id"), primary_key=True, nullable=False)
    friend_id = Column(Integer, ForeignKey("contact.id"), primary_key=True, nullable=False)
    location_id = Column(Integer, ForeignKey("location.id"), primary_key=True, nullable=False)

    follower = relationship( "Contact", foreign_keys=[follower_id])
    friend = relationship( "Contact", foreign_keys=[friend_id])
    location = relationship("Location")


    def __repr__(self):
        return "%s => %s @ %s" % (follower.name, friend.name, location.name)

    '''
    def __init__(self, follower, friend, location):

        if friend == follower:
            log.warning("Share Warning: %s shared %s with themself"
                    % (follower.name, location.name))
            return

        if friend in location.members:
            log.warning("Share Warning: %s already a member of %s"
                    % (friend.name, location.name))
            return

        if follower not in location.members:
            raise Exception("Share Exception: %s is not a member of location %s"
                    % (follower.name, location.name))

        self.follower = follower
        self.friend = friend
        self.location = location
    '''

#class Nomad(User):
#    contact_id = Column(Integer, ForeignKey('contact.id'))
#    contact = relationship("Contact", foreign_keys="Contact.id")
    #emp_number = Column(Integer)
    #companies = relationship('Company', secondary=assoc_user_company, backref='MyUser')


