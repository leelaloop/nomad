import logging
from flask_appbuilder.security.sqla.models import User, Role
from app import appbuilder, db
from app.models import Contact, Location, Tag, Share, Address
import random
from datetime import datetime

log = logging.getLogger(__name__)

################################################################## HELPER MATH
import math
LOGBASE = 2


############################################################## Read Names List
f = open('NAMES.DIC', "rb")
names_list = [x.strip() for x in f.readlines()]
f.close()
def get_random_name(names_list, size=1):
    name_lst = [names_list[random.randrange(0, len(names_list))].capitalize() for i in range(0, size)]
    return " ".join(name_lst)


######################################################## CREATE ADMIN ACCOUNTS
role_admin = appbuilder.sm.find_role(appbuilder.sm.auth_role_admin)

user_scouras = appbuilder.sm.add_user('scouras', 'Alex', 'Scouras', 'alexscouras@gmail.com', role_admin, 'password')
user_leela = appbuilder.sm.add_user('leela', 'Leela', 'Universe', 'leela.loop@gmail.com', role_admin, 'password')
admins = [user_scouras, user_leela]

db.session.merge(user_scouras)
db.session.merge(user_leela)
db.session.commit()


##################################################################### CONTACTS

contacts = []
NUM_USERS = 10

for i in range(NUM_USERS):
    c = Contact()
    c.name = get_random_name(names_list, 2)
    c.email = 'foo@bar.com'
    c.phone = random.randrange(1111111, 9999999)
    
    c.changed_on = datetime.now()
    c.created_on = datetime.now()
    c.created_by = admins[i%len(admins)]
    c.changed_by = admins[i%len(admins)]

    db.session.add(c)
    contacts.append(c)
    try:
        db.session.commit()
        print "Inserted Contact: ", c
    except Exception, e:
        log.error('Contact creation error: %s', e)
        db.session.rollback()
    

##### FRIENDSHIPS

for c in contacts:
    friends = random.sample(contacts, 3)
    for f in friends:
        if c == f:
            continue
        c.friends.append(f)
    print "Friending %-20s with %s" % (c.name, c.friends)
    try:
        db.session.commit()
    except Exception, e:
        log.error('Contact friendship error: %s', e)
        db.session.rollback()





######################################################################### TAGS

tag_names = ['cnc', '3D printer', 'shower', 'hot tub', 'kitchen', 'spare bed',
        'observatory', 'plasma cutter', 'microscope', 'garden', 'replicator']
tags = []

try:
    for tag_name in tag_names:
        tag = Tag(name=tag_name)
        db.session.add(tag)
        tags.append(tag)
        print "Inserted Tag: %s" % tag
        db.session.commit()
except Exception, e:
    log.error('Tag creation error: %s', e)
    db.session.rollback()
    exit(1)


#################################################################### LOCATIONS

NUM_LOCATIONS = 10
for i in range(NUM_LOCATIONS):
    l = Location()
    l.name = get_random_name(names_list, 1) + "'s House"
    l.owner = contacts[i%len(contacts)]
    l.description = "Filler Description"
    l.tags = random.sample(tags, int(random.triangular(0, len(tags), 1)))
    
    l.members = random.sample(contacts, int(random.triangular(0, len(contacts), 1)))
    
    l.changed_on = datetime.now()
    l.created_on = datetime.now()
    l.created_by = admins[i%len(admins)]
    l.changed_by = admins[i%len(admins)]

    db.session.add(l)
    
    try:
        db.session.commit()
        print "inserted location", l
    except Exception, e:
        log.error('Location creation error: %s', e)
        db.session.rollback()
    


