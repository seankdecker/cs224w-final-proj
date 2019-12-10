from google.cloud import bigquery
import numpy as np
from test_vec import query_feature_vec

# Builds feature vectors for a sample of subreddits that are not banned.
SAMPLE_SIZE = 857 # 1000-143
SUBREDDIT_LIST_SIZE = 2000

# time constraints
# (maximally overlaping interval between the two)
MAX_TIME = "2018-06-26 19:57:21" #1530043041
MIN_TIME = "2018-05-23 12:19:21" #1527077961

# Gets the list of 143 banned subreddits.
def get_banlist():
    f = open("banned_pr.txt", "r")
    banlist = set()
    for line in f:
        name = line.strip()
        if name not in banlist:
            banlist.add(name)
    f.close()
    return banlist

# Gets a list of SUBREDDIT_LIST_SIZE randomly sampled unbanned subreddits,
#     out of the 118743 currently queryable.
# This excludes personal (user) subreddits, which begin with "u_".
# (118886 total subreddits - 143 banned)
def get_subreddits(banlist):
    client = bigquery.Client()
    o = open("sampled_subs.txt", "w")
    query_job = client.query(
    """
    SELECT subreddit, subreddit_id
    FROM `pushshift.rt_reddit.submissions`
    WHERE created_utc <= CAST("{}" AS TIMESTAMP)
    AND created_utc >= CAST("{}" AS TIMESTAMP)
    AND lower(subreddit) NOT LIKE "u_%"
    GROUP BY SUBREDDIT, subreddit_id
    ORDER BY RAND()
    LIMIT {}
    ;
    """.format(MAX_TIME, MIN_TIME, SUBREDDIT_LIST_SIZE)
    )
    results = query_job.result()  # Waits for job to complete.
    for row in results:
        sub = row.subreddit.lower()
        if sub not in banlist:
            o.write(sub)
            o.write("\n")
    o.close()

# Saves the feature vectors for a sample.
def get_vecs():
    f = open("sampled_subs.txt", "r")
    remainder = SAMPLE_SIZE % 100
    #parts = (SAMPLE_SIZE // 100) + 1
    N = np.zeros((100,12)) # output array of feature vecs
    i = 0 # counter
    for line in f:
        if i >= SAMPLE_SIZE:
            break
        sub = line.strip()
        N[i] = query_feature_vec(sub)
        i += 1
        if i % 5 == 0:
            print("===")
            print(i)
            print("===")
        if i % 100 == 0:
            np.save('normal_data_{}.npy'.format(i // 100), N)
            if SAMPLE_SIZE - i < 100:
                N = np.zeros((remainder,12))
            else:
                N = np.zeros((100,12))
    if i % 100 != 0:
        np.save('normal_data_{}.npy'.format((i//100)+1), N)

    f.close()
    #return N

if __name__ == '__main__':
    #get_subreddits(get_banlist())
    get_vecs()
