from google.cloud import bigquery
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

# Adapted from Google Cloud's tutorials/documentation on Python libraries
# related to BigQuery and sentiment analysis.

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
    numSubmissions = 0
    newest_time = 0
    for row in results:
        vec = [x for x in row[2:-1]]
        vec.append(row.NumSubmissions / row.NumAuthors)
        numSubmissions = row.NumSubmissions
        newest_time = row.newest_time
    print(vec)

    # get data from comments table
    # # comments, # unique comment authors
    # avg comments/author
    # avg comments/submission
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
        vec.append(row.NumComments / numSubmissions)
    print(vec)

    # get avg sentiment of comments (currently sampling 250 comments)
    # (weighted and unweighted by magnitude, along with avg magnitude)
    # note: sentiment queries on a sample of text give a score and a magnitude
    query_job = client.query(
    """
    SELECT Subreddit,
    subreddit_id,
    body
    FROM `pushshift.rt_reddit.comments`
    WHERE lower(subreddit)="{}"
    LIMIT 250
    ;
    """.format(curr_subreddit)
    )
    results = query_job.result()
    print('received results! got data for sentiment analysis')

    total = 0
    wt_total = 0
    total_mag = 0
    count = 0
    for row in results:
        try:
            text = row.body
            sentiment = analyze(text)
            total += sentiment.score
            total_mag += sentiment.magnitude
            wt_total += sentiment.score * sentiment.magnitude
            count += 1
        except Exception:
            continue
    if count > 0:
        vec.append(wt_total / count)
        vec.append(total / count)
        vec.append(total_mag / count)
    else:
        vec.extend([0,0])
    print(vec)

    return vec

def sentiment_test(curr_subreddit):
    query_job = client.query(
    """
    SELECT Subreddit,
    subreddit_id,
    body
    FROM `pushshift.rt_reddit.comments`
    WHERE lower(subreddit)="{}"
    LIMIT 10;
    """.format(curr_subreddit)
    )
    results = query_job.result()
    print('received results! got data')
    for row in results:
        text = row.body
        sentiment = analyze(text)
        print('Text: {}'.format(text))
        print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))

def analyze(input):
    # Run a sentiment analysis request on passed content.
    document = types.Document(
        content=input,
        type=enums.Document.Type.PLAIN_TEXT)
    annotations = lang_client.analyze_sentiment(document=document)
    sentiment = annotations.document_sentiment
    return sentiment

    # Print the results
    print_result(annotations)

if __name__ == '__main__':
    #sentiment_test('braincels')
    query_feature_vec('chess')
