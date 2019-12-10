'''
Before you can use the functions inside of this folder,
do the following:
  1 - create two directories, body-data and title-data in this folder
  2 - download the snap datasets from https://snap.stanford.edu/data/soc-RedditHyperlinks.html
  3 - unpack the body one in body-date
  4 - unpack the title one in title-data
  5 - make sure that you have the file banned_subreddits.csv
  6 - run run_me_to_init_datasets.py
'''
import csv
from tsv_to_csv import tsv_to_csv
from make_snap_graph import build_snap_graph

DATASETS = ['body', 'title']
####### PATHS ############
folder = '{}-data'
raw_hyperlinks_tsv = './soc-redditHyperlinks-{}.tsv'
raw_hyperlinks_csv = 'soc-redditHyperlinks-{}.csv' # csv of all subreddits, without ids. Use snap_hyperlinks for load of graph, since it has ids(int) instead of subreddit names(strings)
snap_subreddit_ids = 'snap-subreddit-ids-{}.csv' # csv mapping subreddits to their ids
snap_hyperlinks ='snap-redditHyperlinks-{}.csv' # csv with hyperlinks formatted in style for LoadEdgeList
banned_labels = 'banned_subreddits.csv'

def build_snap_graph(dataset_name):
  # read tab-delimited file
  with open('{}-data/soc-redditHyperlinks-{}.csv'.format(dataset_name, dataset_name),'r') as fin:
    cr = csv.reader(fin, delimiter=',')
    # remove the last element in each line because we don't need it
    # and it has commas in it
    filecontents = [line for line in cr]

  del filecontents[0] # get rid of headers
  subreddit_to_id = {}
  counter = 0
  snapgraph = []
  # build graph-like structures using file contents
  for f in filecontents:
    src, dst = f[0], f[1]
    if src not in subreddit_to_id:
      subreddit_to_id[src], counter = counter, counter + 1
    if dst not in subreddit_to_id:
      subreddit_to_id[dst], counter = counter, counter + 1
    snapgraph.append([subreddit_to_id[src], subreddit_to_id[dst]])

  # write comma-delimited file (comma is the default delimiter)
  with open('./{}-data/snap-redditHyperlinks-{}.csv'.format(dataset_name, dataset_name),'w') as fou1:
    cw = csv.writer(fou1, quotechar='', quoting=csv.QUOTE_NONE)
    cw.writerows(snapgraph)

  # write comma-delimited file (comma is the default delimiter)
  with open('./{}-data/snap-subreddit-ids-{}.csv'.format(dataset_name, dataset_name),'w') as fou2:
    cw = csv.writer(fou2, quotechar='', quoting=csv.QUOTE_NONE)
    for sub, id in subreddit_to_id.items():
      cw.writerow([sub, id])

def build_snap_graph(dataset_name):
  # read tab-delimited file
  with open('{}-data/soc-redditHyperlinks-{}.csv'.format(dataset_name, dataset_name),'r') as fin:
    cr = csv.reader(fin, delimiter=',')
    # remove the last element in each line because we don't need it
    # and it has commas in it
    filecontents = [line for line in cr]

  del filecontents[0] # get rid of headers
  subreddit_to_id = {}
  counter = 0
  snapgraph = []
  # build graph-like structures using file contents
  for f in filecontents:
    src, dst = f[0], f[1]
    if src not in subreddit_to_id:
      subreddit_to_id[src], counter = counter, counter + 1
    if dst not in subreddit_to_id:
      subreddit_to_id[dst], counter = counter, counter + 1
    snapgraph.append([subreddit_to_id[src], subreddit_to_id[dst]])

  # write comma-delimited file (comma is the default delimiter)
  with open('./{}-data/snap-redditHyperlinks-{}.csv'.format(dataset_name, dataset_name),'w') as fou1:
    cw = csv.writer(fou1, quotechar='', quoting=csv.QUOTE_NONE)
    cw.writerows(snapgraph)

  # write comma-delimited file (comma is the default delimiter)
  with open('./{}-data/snap-subreddit-ids-{}.csv'.format(dataset_name, dataset_name),'w') as fou2:
    cw = csv.writer(fou2, quotechar='', quoting=csv.QUOTE_NONE)
    for sub, id in subreddit_to_id.items():
      cw.writerow([sub, id])

if __name__ == '__main__':
  for dataset in DATASETS:
    tsv_to_csv(
      './{}/{}'.format(folder.format(dataset), raw_hyperlinks_tsv.format(dataset)),
      './{}/{}'.format(folder.format(dataset), raw_hyperlinks_csv.format(dataset))
      )
    build_snap_graph(dataset)