import snap
import numpy as np
import csv # for reading in banned_labels, node_labels
import matplotlib.pyplot as plt
import random

"""
UTILITY FUNCTIONS
"""

DATASET = 'title'
####### PATHS ############
folder = '{}-data'
raw_hyperlinks = 'soc-redditHyperlinks-{}.csv' # csv of all subreddits, without ids. Use snap_hyperlinks for load of graph, since it has ids(int) instead of subreddit names(strings)
snap_subreddit_ids = 'snap-subreddit-ids-{}.csv' # csv mapping subreddits to their ids
snap_hyperlinks ='snap-redditHyperlinks-{}.csv' # csv with hyperlinks formatted in style for LoadEdgeList

banned_labels = 'banned_subreddits.csv'

# load the map from id to subreddits given name of dataset we are interested in
def load_labels(name):
    id_to_subreddit, subreddit_to_id = {}, {}
    with open('./{}/{}'.format(folder.format(name), snap_subreddit_ids.format(name)),'r') as f:
        cr = csv.reader(f, delimiter=',')
        for row in cr:
            sub_name, sub_id = row[0], row[1]
            id_to_subreddit[int(sub_id)] = sub_name
            subreddit_to_id[sub_name] = int(sub_id)
    return id_to_subreddit, subreddit_to_id

# load the graph for the subreddit that we are interested in
# ret:
#   G - snap PNGraph
#   node_labels - maps node ids to their subreddit name
def load_graph(name):
    '''
    Helper function to load graphs.
    Make sure to convert from tsv to csv if you haven't already
    '''
    if name == 'body':
        G = snap.LoadEdgeList(snap.PNGraph, './{}/{}'.format(folder.format(name), snap_hyperlinks.format(name)), 0, 1, ',')
        id_to_subreddit, subreddit_to_id = load_labels(name)
    elif name == 'title':
        G = snap.LoadEdgeList(snap.PNGraph, './{}/{}'.format(folder.format(name), snap_hyperlinks.format(name)), 0, 1, ',')
        id_to_subreddit, subreddit_to_id = load_labels(name)
    else: 
        raise ValueError('Invalid graph: please use "body" or "title".')
    if G.GetNodes() == 0:
        raise ValueError('Graph G loaded without any nodes being added. Something went wrong')
    return G, id_to_subreddit, subreddit_to_id

# load list of banned subreddits
def load_banned():
    banned = set()
    with open(banned_labels,'r') as fin:
        cr = csv.reader(fin, delimiter=',')
        for row in cr:
            banned.add(row[0][2:].lower()) # get rid of leading 'r/' and make case insensitive
    return banned

# returns list of banned subreddits ids
def get_banned_ids(banned, subreddit_to_id):
    res = []
    for ban in banned:
        res.append(subreddit_to_id[ban])
    return res

# returns a list of all banned subreddits that appear in G
def banned_sub_in_G(G, node_labels, banned):
    res = []
    for n in G.Nodes():
        if (node_labels[n.GetId()] in banned):
            res.append(node_labels[n.GetId()])
    return res

# prints out all banned subreddits in G
def check_for_banned(G, node_labels, banned):
    count = 0
    for n in G.Nodes():
        if (node_labels[n.GetId()] in banned):
            print('BANNED: ', node_labels[n.GetId()], ' - ', n.GetId())
            count += 1
    print(count, len(banned), G.GetNodes())

# generate a random subgraph from G of no more than size subgraph_size with num_banned banned 
def get_random_subgraph(G, banned_ids, subgraph_size = 300, num_banned=10):
  banned_ids = random.sample(banned_ids, num_banned)
  # Graph contains nodes with ids that increase sequentially, so 
  # just take a random random from a list from 0 to G.GetNodes()
  others_ids = random.sample([i for i in range(G.GetNodes())], subgraph_size - num_banned)
  ids_to_include = list(set(banned_ids + others_ids))
  Vector_to_include = snap.TIntV()
  for id_included in ids_to_include:
    Vector_to_include.Add(id_included)
  return snap.GetSubGraph(G, Vector_to_include)

# generate a random subgraph from G of no more than size subgraph_size
def get_random_subgraph_connected(G, banned_ids, subgraph_size = 300):
  root = random.choice(banned_ids)
  # do bfs from root, which is a banned subreddit
  Vector_to_include.Add()
  subgraph = set()
  curr_elems = [root]
  while(len(curr_elems) > 0 and len(subgraph) < subgraph_size):
    pass

  ids_to_include = list(set(banned_ids + others_ids))
  Vector_to_include = snap.TIntV()
  for id_included in ids_to_include:
    
  return snap.GetSubGraph(G, Vector_to_include)

# load dataset of banned subreddits
# load SNAP graph which corresponds to DATASET
# filter out
def main():
    banned = load_banned()
    G, id_to_subreddit, subreddit_to_id = load_graph(DATASET)
    check_for_banned(G, id_to_subreddit, banned)

if __name__ == '__main__':
    main()