from google.cloud import bigquery


counter = 0;
edges = {};

client = bigquery.Client()

def query_stackoverflow(curr_subreddit):
    # get unique authors on subreddit
    query_job = client.query(
"""
select 
  distinct author
from
  `pushshift.rt_reddit.comments` comments
where
  comments.subreddit = "{}";
""".format(curr_subreddit)
)
    results = query_job.result()  # Waits for job to complete.
    print('recieved results! got redditors')
    if (curr_subreddit not in edges):
        edges[curr_subreddit] = set()

    for redditor in results:
        print('querying for redditor: {}'.format(redditor.author))
        query_job = client.query(
"""
select 
  distinct subreddit
from
  `pushshift.rt_reddit.comments` comments
where
  comments.author = "{}";
""".format(redditor.author)
        )
        linked_subreddits = query_job.result()  # Waits for job to complete.
        print('got subreddits: ')
        for sub in linked_subreddits:
            print(' {},'.format(sub.subreddit))
            edges[curr_subreddit].add(sub.subreddit)
        print(' fin ')

if __name__ == '__main__':
    query_stackoverflow('chess')
