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


dataset = ["Yep. And companies complain about how millennials have no loyalty.It's like someone who beats their partners bemoaning their lack of long-term relationship stability. _People today_, they whine, _just don't know how to make a relationship work_.",
           "Lorithia from Xenoblade Chronicles. I got so mad, I beat Dark Souls then I came back and fought this boss. She's incredibly unfair.",
           "pineapples on pizza tastes good",
           "eventually you'll find someone into it, as inexperienced as you, patient or not. might want you to be eager to learn, that eagerness might work in your favor",
           "Nice try James, keeping it in the family I see ...", 
           "Thanks for this, I look forward to reading.",
           "That's a better answer than mine. I'd pay off my the debts of my family.",
           "8.75 / 10 because I think the perfect length is 8 inches and mine is 7. 7 / 8 * 10 = 8.75. I'm perfectly happy with my girth so no adjustment there"
           "My aunt peed in the fridge as a young girl while asleep",
           "Same thing as what we were before we were born. Nothing."
           ]


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
gc = list(zip(dataset, gc_score, gc_magnitude))
columns = ['text', 'score', 'magnitude']
gc_df = pd.DataFrame(gc, columns = columns)
import os # for the finding of curr path
gc_df.to_csv(path_or_buf=os.path.join(os.getcwd(),r'results.csv'), index=False)
