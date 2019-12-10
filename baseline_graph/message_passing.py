from load_datasets import load_banned
from load_datasets import load_graph
from load_datasets import get_banned_ids, banned_sub_in_G
import random
DATASET = 'title' 

subgraph_size = 300

def get_random_subgraph(G, banned_ids):
  banned_ids = random.sample(banned_ids, 10)
  others_ids = random.sample()
  

TESTING, TRAINING = [], []

if __name__ == '__main__':
  G, id_to_subreddit, subreddit_to_id = load_graph(DATASET)
  banned = load_banned()
  banned = banned_sub_in_G(G, id_to_subreddit, banned)
  TRAINING = random.sample(banned, int(len(banned) * 3 / 4))
  TESTING = list(set(banned) - set(TRAINING))
  print(TRAINING, TESTING)

