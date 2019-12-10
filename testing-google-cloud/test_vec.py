from google.cloud import bigquery
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

client = bigquery.Client()
lang_client = language.LanguageServiceClient()

def query_feature_vec(curr_subreddit):
    # get data from submissions table
    # # subscribers, # submissions, # unique authors, % posts marked NSFW, latest submission time
    # avg submissions/author
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
    print('received results! got submission data')

    vec = []
    for row in results:
        vec = [x for x in row[2:]]
        vec.append(row.NumSubmissions / row.NumAuthors)
    print(vec)

    # get data from comments table
    # # comments, # unique comment authors
    # avg comments/author
    query_job = client.query(
    """
    SELECT Subreddit,
    subreddit_id,
    COUNT(*) AS NumComments,
    COUNT ( DISTINCT author ) AS NumCommentAuthors
    FROM `pushshift.rt_reddit.comments`
    WHERE lower(subreddit)="{}"
    GROUP BY SUBREDDIT, subreddit_id
    LIMIT 1;
    """.format(curr_subreddit)
    )
    results = query_job.result()
    print('received results! got comment data')
    for row in results:
        vec.extend([x for x in row[2:]])
        vec.append(row.NumComments / row.NumCommentAuthors)
    print(vec)


def analyze(input):
    """Run a sentiment analysis request on passed content."""
    document = types.Document(
        content=input,
        type=enums.Document.Type.PLAIN_TEXT)
    annotations = lang_client.analyze_sentiment(document=document)

    # Print the results
    print_result(annotations)

if __name__ == '__main__':
    query_feature_vec('chess')
