import snap

data = {('AskReddit', 'AskReddit'): 0,
        ('AskReddit', 'funny'): 103421,
        ('AskReddit', 'pics'): 107353,
        ('AskReddit', 'gaming'): 88782,
        ('AskReddit', 'worldnews'): 82762,
        ('AskReddit', 'gifs'): 70026,
        ('AskReddit', 'todayilearned'): 77981,
        ('AskReddit', 'politics'): 53766,
        ('AskReddit', 'aww'): 62768, ('AskReddit', 'news'): 67337, ('funny', 'AskReddit'): 103421, ('funny', 'funny'): 0, ('funny', 'pics'): 71445,
        ('funny', 'gaming'): 57415, ('funny', 'worldnews'): 45490, ('funny', 'gifs'): 50804, ('funny', 'todayilearned'): 45106,
        ('funny', 'politics'): 27592, ('funny', 'aww'): 42811, ('funny', 'news'): 38013, ('pics', 'AskReddit'): 107353, ('pics', 'funny'): 71445,
        ('pics', 'pics'): 0, ('pics', 'gaming'): 52798, ('pics', 'worldnews'): 53619, ('pics', 'gifs'): 51102, ('pics', 'todayilearned'): 48277,
        ('pics', 'politics'): 34202, ('pics', 'aww'): 41743, ('pics', 'news'): 43798, ('gaming', 'AskReddit'): 88782, ('gaming', 'funny'): 57415,
        ('gaming', 'pics'): 52798, ('gaming', 'gaming'): 0, ('gaming', 'worldnews'): 39546, ('gaming', 'gifs'): 39011, ('gaming', 'todayilearned'): 36711,
        ('gaming', 'politics'): 22645, ('gaming', 'aww'): 30828, ('gaming', 'news'): 32175, ('worldnews', 'AskReddit'): 82762,
        ('worldnews', 'funny'): 45490, ('worldnews', 'pics'): 53619, ('worldnews', 'gaming'): 39546, ('worldnews', 'worldnews'): 0,
        ('worldnews', 'gifs'): 35006, ('worldnews', 'todayilearned'): 43697, ('worldnews', 'politics'): 43775, ('worldnews', 'aww'): 24592,
        ('worldnews', 'news'): 52035, ('gifs', 'AskReddit'): 70026, ('gifs', 'funny'): 50804, ('gifs', 'pics'): 51102, ('gifs', 'gaming'): 39011,
        ('gifs', 'worldnews'): 35006, ('gifs', 'gifs'): 0, ('gifs', 'todayilearned'): 33762, ('gifs', 'politics'): 19098, ('gifs', 'aww'): 31313, ('gifs', 'news'): 30334, ('todayilearned', 'AskReddit'): 77981, ('todayilearned', 'funny'): 45106,
        ('todayilearned', 'pics'): 48277, ('todayilearned', 'gaming'): 36711, ('todayilearned', 'worldnews'): 43697, ('todayilearned', 'gifs'): 33762, ('todayilearned', 'todayilearned'): 0,
        ('todayilearned', 'politics'): 26075, ('todayilearned', 'aww'): 25194, ('todayilearned', 'news'): 35783, ('politics', 'AskReddit'): 53766, ('politics', 'funny'): 27592, ('politics', 'pics'): 34202,
        ('politics', 'gaming'): 22645, ('politics', 'worldnews'): 43775, ('politics', 'gifs'): 19098, ('politics', 'todayilearned'): 26075,
        ('politics', 'politics'): 0, ('politics', 'aww'): 14420, ('politics', 'news'): 33827, ('aww', 'AskReddit'): 62768, ('aww', 'funny'): 42811, ('aww', 'pics'): 41743, ('aww', 'gaming'): 30828,
        ('aww', 'worldnews'): 24592, ('aww', 'gifs'): 31313, ('aww', 'todayilearned'): 25194, ('aww', 'politics'): 14420, ('aww', 'aww'): 0,
        ('aww', 'news'): 21564, ('news', 'AskReddit'): 67337, ('news', 'funny'): 38013, ('news', 'pics'): 43798, ('news', 'gaming'): 32175,
        ('news', 'worldnews'): 52035, ('news', 'gifs'): 30334, ('news', 'todayilearned'): 35783, ('news', 'politics'): 33827, ('news', 'aww'): 21564, ('news', 'news'): 0}



indicies = {}
labels = snap.TIntStrH()
counter = 0


if __name__=="__main__":
    G = snap.TUNGraph.New()
    for (sub0, sub1), val in data.items():
        if (sub0 not in indicies):
            G.AddNode(counter)
            labels[counter] = sub0
            indicies[sub0] = counter
            counter += 1
        if (sub1 not in indicies):
            G.AddNode(counter)
            labels[counter] = sub1
            indicies[sub1] = counter
            counter += 1
        if (not G.IsEdge(indicies[sub0], indicies[sub1])):
            G.AddEdge(indicies[sub0], indicies[sub1])

    snap.DrawGViz(G, snap.gvlNeato, "output.png", " top 10 subreddits ", labels)



