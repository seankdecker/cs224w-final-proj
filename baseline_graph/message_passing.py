from load_datasets import load_banned
from load_datasets import load_graph
from load_datasets import get_banned_ids, banned_sub_in_G, get_random_subgraph, get_random_subgraph_connected
import random
import snap
DATASET = 'title' 

# lists of strings, which are the names of banned subreddits to train and test on
TESTING, TRAINING = [], []

if __name__ == '__main__':
  # load graph and maps that are used to map ids (int) to subreddit names (str)
  G, id_to_subreddit, subreddit_to_id = load_graph(DATASET)
  # load banned subreddits [str]
  banned = load_banned()
  # get banned subreddits that appear in G
  banned = banned_sub_in_G(G, id_to_subreddit, banned)
  # get list of random sample of banned subreddits to train on. 
  TRAINING = random.sample(banned, int(len(banned) * 3 / 4))
  # rest of subreddits are for testing.
  TESTING = list(set(banned) - set(TRAINING))
  # generate subgraph of G
  G_new = get_random_subgraph_connected(G, get_banned_ids(TRAINING, subreddit_to_id))
  print('number of nodes in random subgraph: ', G_new.GetNodes())

