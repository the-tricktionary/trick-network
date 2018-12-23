import os
import json
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
from trick import Trick

types = ['basics', 'manipulation', 'power', 'releases', 'multiples', 'impossible']

cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://project-5641153190345267944.firebaseio.com/'
})

root = db.reference()
# Add a new user under /users.
tricktionary = []
tricknames = []
id = 0
for i in range(5):
    tricks = root.child('tricks').child(str(i)).child('subs').get()
    for trick in tricks:
        if True:#trick['type'] == 'Multiples':
            t = Trick(id, i, trick['name'], types.index(str(trick['type']).lower()))
            prereqs = []
            for prereq in trick['prerequisites']:
                if prereq['name'] != 'None':
                    prereqs.append(prereq['name'])
            t.prereqs = prereqs
            id += 1
            tricktionary.append(t)
            tricknames.append(t.name)
            print(t.name)

nodes = [] ; links = []

for trick in tricktionary:
    nodes.append({'group': trick.type, 'name': trick.name})
    if trick.prereqs:
        for prereq in trick.prereqs:
            try:
                    print(trick.prereqs)
                    links.append({'source': trick.id, 'target': tricknames.index(str(prereq)), 'value': 1})
            except Exception as e:
                print(str(prereq), 'not in list')

graph = {'nodes': nodes, 'links': links}

os.remove('static/graph.json')
with open('static/graph.json','w') as f: json.dump(graph,f)
