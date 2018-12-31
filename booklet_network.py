from network2tikz import plot
import igraph

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

tricks_ref = db.collection(u'tricksSR')
docs = tricks_ref.get()

nodes = []
edges = []
type = []
colors = {'manipulation': 'yellow',
         'basic': 'green',
         'multiple': 'blue',
         'power': 'red',
         'release': 'orange',
         'impossible': 'pink'}

for doc in docs:
    trick = doc.to_dict()
    trick_name = trick[u'name'].replace('(', '').replace(')','')
    nodes.append(trick_name)
    type.append(trick[u'type'])
    try:
        for prereq_ref in trick[u'prerequisites']:
            prereq = prereq_ref[u'ref'].get().to_dict()
            prereq_name = prereq[u'name'].replace('(', '').replace(')','')
            edges.append((trick_name, prereq_name))
    except KeyError as e:
        # No prereqs found
        pass
    #print(u'{} => {}'.format(doc.id, doc.to_dict()))

print(nodes)
print(edges)

net = igraph.Graph([])
net.add_vertices(len(nodes))
for edge in edges:
    source = nodes.index(edge[0])
    target = nodes.index(edge[1])
    net.add_edges([(source, target)])

layout = net.layout('fr')

print(layout.coords)


style = {}
style['node_size'] = 0.3
style['node_label'] = nodes
style['node_color'] = [colors[g] for g in type]
style['node_opacity'] = .5
style['node_label_position'] = 'below'
style['edge_curved'] = .1
style['edge_width'] = .3
style['edge_opacity'] = .5
style['edge_directed'] = [True for _ in nodes]

# visual options
style['canvas'] = (25, 25)
style['layout'] = layout.coords


plot(net, 'network.tex', **style)
