from google.cloud import bigquery
import numpy as np
from test_vec import query_feature_vec

MAX_TIME = "2018-06-26 19:57:21" #1530043041
MIN_TIME = "2018-05-23 12:19:21" #1527077961

def makelist():
    f = open("banned_src.txt", "r")
    o = open("banned.txt", "w")
    for line in f:
        if line.startswith("r/"):
            o.write(line[2:].lower())
    f.close()
    o.close()

def check():
    client = bigquery.Client()
    f = open("banned.txt", "r")
    o = open("banned_ps.txt", "w")
    count = 0
    for line in f:
        count += 1
        query_job = client.query(
        """
        SELECT *
        FROM `pushshift.rt_reddit.submissions`
        WHERE lower(subreddit)="{}"
        AND created_utc <= CAST("{}" AS TIMESTAMP)
        AND created_utc >= CAST("{}" AS TIMESTAMP)
        ---GROUP BY SUBREDDIT, subreddit_id
        LIMIT 1
        ;
        """.format(line[:-1], MAX_TIME, MIN_TIME)
        )
        results = query_job.result()  # Waits for job to complete.
        isIn = False
        for row in results:
            isIn = True
        if isIn:
            o.write(line)
        if count % 10 == 0:
            print(count)
    f.close()
    o.close()

def prune():
    f = open("banned_ps.txt", "r")
    o = open("banned_pr.txt", "w")
    for line in f:
        banList = set()
        name = line.strip()
        if name not in banList:
            banList.add(name)
            o.write(line)
    f.close()
    o.close()

def get_vecs():
    f = open("banned_pr.txt", "r")
    N = np.zeros((143,12)) # output array of feature vecs
    i = 0 # counter
    for line in f:
        sub = line.strip()
        N[i] = query_feature_vec(sub)
        i += 1
        if i % 5 == 0:
            print("===")
            print(i)
            print("===")

    f.close()
    np.save('banned_data.npy', N)
    return N

def test_load():
    N = np.load('banned_data.npy')
    print(N[40])

if __name__ == '__main__':
    #makelist()
    #check()
    #prune()
    #get_vecs()
    test_load()
