from google.cloud import bigquery

edges = {};

client = bigquery.Client()

# get top n most popular subreddits by number of users
def get_top_n(n):
    query_job = client.query(
"""
-- get most popular 10 subreddits based on distinct author
SELECT COUNT ( DISTINCT author ) AS commenters, subreddit
FROM `pushshift.rt_reddit.comments`
GROUP BY SUBREDDIT
ORDER BY COUNT(DISTINCT author) DESC
LIMIT {};
""".format(n))
    tops = query_job.result();
    print('=====got tops subreddits!=======')
    res = []
    for top in tops:
        print('{0} has {1} distinct commenters'.format(top.subreddit, top.commenters))
        res.append(top.subreddit)
    return res

def get_similarity(sub0, sub1):
    # get unique authors on subreddit
    query_job = client.query(
"""
select
  count(*) as num_shared_redditors
from(
  select 
    distinct author
  from
    `pushshift.rt_reddit.comments` comments
  where
    comments.subreddit in ("{0}", "{1}")
  group by
    comments.author
  having 
    sum(case comments.subreddit when '{0}' then 1 else 0 end) > 1
    and
    sum(case comments.subreddit when '{1}' then 1 else 0 end) > 1
 );
 """.format(sub0, sub1))
    res = query_job.result()  # Waits for job to complete.
    num_shared = 0
    for r in res:
        num_shared = r.num_shared_redditors
    count = 0
    print('{0} and {1} have {2} shared commentors'.format(sub0, sub1, num_shared))
    edges[(sub0, sub1)] = num_shared

if __name__ == '__main__':
    # tops = get_top_n(10)
    subs = ['baduk', 'chess', 'warriors', 'nbastreams', 'todayilearned', 'physicsmemes', 'mathematics', 'holdmybread']
    for s0 in subs:
        for s1 in subs:
            get_similarity(s0, s1)
    print('---------JOB DONE -------')
    print(edges)
