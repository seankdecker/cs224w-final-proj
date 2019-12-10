import load_banned, load_graph, get_banned_ids from load_datasets
import random
DATASET = 'title' 

def get_random_subgraph(G, banned, subreddit_to_id):
  banned_ids = get_banned_ids(banned, subreddit_to_id)
  

TESTING, TRAINING = [], []

if __name__ == '__main__':
  G, id_to_subreddit, subreddit_to_id = load_graph(DATASET)
  banned = load_banned()
  banned = banned_sub_in_G(G, id_to_subreddit, banned)
  TRAINING = random.sample(banned, len(banned) * 3 / 4)

