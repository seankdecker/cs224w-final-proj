import snap
import numpy as np
import csv # for reading in banned_labels, node_labels
import matplotlib.pyplot as plt

DATASET = 'body'
####### PATHS ############
folder = '{}-data'
raw_hyperlinks = 'soc-redditHyperlinks-{}.csv' # csv of all subreddits, without ids. Use snap_hyperlinks for load of graph, since it has ids(int) instead of subreddit names(strings)
snap_subreddit_ids = 'snap-subreddit-ids-{}.csv' # csv mapping subreddits to their ids
snap_hyperlinks ='snap-redditHyperlinks-{}.csv' # csv with hyperlinks formatted in style for LoadEdgeList

banned_labels = 'banned_subreddits.csv'

# load the map from id to subreddits given name of dataset we are interested in
def load_labels(name):
    id_to_subreddit = {}
    with open('./{}/{}'.format(folder.format(name), snap_subreddit_ids.format(name)),'r') as f:
        cr = csv.reader(f, delimiter=',')
        for row in cr:
            sub_name, sub_id = row[0], row[1]
            id_to_subreddit[int(sub_id)] = sub_name
    return id_to_subreddit

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
        node_labels = load_labels(name)
    elif name == 'title':
        G = snap.LoadEdgeList(snap.PNGraph, './{}/{}'.format(folder.format(name), snap_hyperlinks.format(name)), 0, 1, ',')
        node_labels = load_labels(name)
    else: 
        raise ValueError('Invalid graph: please use "body" or "title".')
    if G.GetNodes() == 0:
        raise ValueError('Graph G loaded without any nodes being added. Something went wrong')
    return G, node_labels

# load list of banned subreddits
def load_banned():
    banned = set()
    with open(banned_labels,'r') as fin:
        cr = csv.reader(fin, delimiter=',')
        for row in cr:
            banned.add(row[0][2:].lower()) # get rid of leading 'r/' and make case insensitive
    return banned

# prints out all banned subreddits in G
def check_for_banned(G, node_labels, banned):
    count = 0
    for n in G.Nodes():
        if (node_labels[n.GetId()] in banned):
            print('BANNED: ', node_labels[n.GetId()], ' - ', n.GetId())
            count += 1
    print(count, len(banned))

# load dataset of banned subreddits
# load SNAP graph which corresponds to DATASET
# filter out
def main():
    banned = load_banned()
    G, node_labels = load_graph(DATASET)
    check_for_banned(G, node_labels, banned)

if __name__ == '__main__':
    main()