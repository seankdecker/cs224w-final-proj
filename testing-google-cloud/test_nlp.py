# Run this cell to authenticate yourself to BigQuery
# from google.colab import auth
project_id = "subtle-chimera-258301"
# auth.authenticate_user()

# Initialize BiqQuery client
from google.cloud import bigquery, language
nl_client = language.LanguageServiceClient()
client = bigquery.Client(project=project_id)
# Visualization Libraries
import altair as alt
import matplotlib.pyplot as plt
from vega_datasets import data

from google.cloud import storage, language
from tqdm import tqdm
import pandas as pd

df = pd.read_csv('test.csv')

dataset = df['body'].tolist()
subreddits = df['subreddit'].tolist()

def gc_sentiment(text,nl_client): 
    client = nl_client
    document = language.types.Document(
            content=text,
            type=language.enums.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_sentiment(document=document)
    score = annotations.document_sentiment.score
    magnitude = annotations.document_sentiment.magnitude
    return score, magnitude

gc_results = [gc_sentiment(row,nl_client) for row in tqdm(dataset, ncols = 100)]
gc_score, gc_magnitude = zip(*gc_results) # Unpacking the result into 2 lists
gc = list(zip(subreddits, dataset, gc_score, gc_magnitude))
columns = ['subreddit','text', 'score', 'magnitude']
gc_df = pd.DataFrame(gc, columns = columns)
import os # for the finding of curr path
gc_df.to_csv(path_or_buf=os.path.join(os.getcwd(),r'results.csv'), index=False)
