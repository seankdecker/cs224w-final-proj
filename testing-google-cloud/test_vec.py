from google.cloud import bigquery
from google.cloud import language

client = bigquery.Client()

def query_feature_vec(curr_subreddit):
    # get unique authors on subreddit
    query_job = client.query(
"""
SELECT Subreddit,
    subreddit_id,
    max(subreddit_subscribers) as NumSubs,
    COUNT(*) AS NumSubmissions,
    COUNT ( DISTINCT author ) AS NumAuthors,
    AVG(CAST(CAST(over_18 AS int64) AS float64)) AS frac_over_18,
    MAX(created_utc) AS newest_time
FROM `pushshift.rt_reddit.submissions`
WHERE lower(subreddit)="{}"
GROUP BY SUBREDDIT, subreddit_id
LIMIT 1
;
""".format(curr_subreddit)
)
    results = query_job.result()  # Waits for job to complete.
    print('recieved results! got vector')

    vec = []
    for row in results:
        vec = [row.NumSubs, row.NumSubmissions, row.NumAuthors, row.frac_over_18, row.newest_time]
    print(vec)

if __name__ == '__main__':
    query_feature_vec('chess')
