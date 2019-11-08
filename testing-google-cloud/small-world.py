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
  distinct author,
  sum(case comments.subreddit when "{0}" then 1 else 0 end) as num_comments_{0},
  sum(case comments.subreddit when "{1}" then 1 else 0 end) as num_commenets_{1}
from
  `pushshift.rt_reddit.comments` comments
where
  comments.subreddit in ("{0}", "{1}")
group by
  comments.author
having 
  count(distinct comments.subreddit) > 1;
""".format(sub0, sub1))
    shared_commentors = query_job.result()  # Waits for job to complete.
    count = 0
    for s in shared_commentors:
        count += 1
    print('{0} and {1} have {2} shared commentors'.format(sub0, sub1, count))
    edges[(sub0, sub1)] = count

if __name__ == '__main__':
    tops = get_top_n(10)
    for t0 in tops:
        for t1 in tops:
            get_similarity(t0, t1)
    print('---------JOB DONE -------')
    print(edges)
