import snap

data = {('baduk', 'baduk'): 242, ('baduk', 'chess'): 10, ('baduk', 'warriors'): 2, ('baduk', 'nbastreams'): 2, ('baduk', 'todayilearned'): 14, ('baduk', 'physicsmemes'): 0, ('baduk', 'mathematics'): 1, ('baduk', 'holdmybread'): 0, ('chess', 'baduk'): 10, ('chess', 'chess'): 1553, ('chess', 'warriors'): 11, ('chess', 'nbastreams'): 1,
('chess', 'todayilearned'): 106, ('chess', 'physicsmemes'): 0, ('chess', 'mathematics'): 3, ('chess', 'holdmybread'): 0, ('warriors', 'baduk'): 2, ('warriors', 'chess'): 11, ('warriors', 'warriors'): 3596, ('warriors', 'nbastreams'): 14, ('warriors', 'todayilearned'): 142,
('warriors', 'physicsmemes'): 1, ('warriors', 'mathematics'): 1, ('warriors', 'holdmybread'): 0, ('nbastreams', 'baduk'): 2, ('nbastreams', 'chess'): 1, ('nbastreams', 'warriors'): 14, ('nbastreams', 'nbastreams'): 218, ('nbastreams', 'todayilearned'): 15,
('nbastreams', 'physicsmemes'): 0, ('nbastreams', 'mathematics'): 0, ('nbastreams', 'holdmybread'): 0, ('todayilearned', 'baduk'): 14, ('todayilearned', 'chess'): 106, ('todayilearned', 'warriors'): 142, ('todayilearned', 'nbastreams'): 15, ('todayilearned', 'todayilearned'): 58248, ('todayilearned', 'physicsmemes'): 11, ('todayilearned', 'mathematics'): 5,
('todayilearned', 'holdmybread'): 0, ('physicsmemes', 'baduk'): 0, ('physicsmemes', 'chess'): 0, ('physicsmemes', 'warriors'): 1, ('physicsmemes', 'nbastreams'): 0, ('physicsmemes', 'todayilearned'): 11, ('physicsmemes', 'physicsmemes'): 105,
('physicsmemes', 'mathematics'): 0, ('physicsmemes', 'holdmybread'): 0, ('mathematics', 'baduk'): 1, ('mathematics', 'chess'): 3, ('mathematics', 'warriors'): 1, ('mathematics', 'nbastreams'): 0, ('mathematics', 'todayilearned'): 5, ('mathematics', 'physicsmemes'): 0,
('mathematics', 'mathematics'): 81, ('mathematics', 'holdmybread'): 0, ('holdmybread', 'baduk'): 0, ('holdmybread', 'chess'): 0, ('holdmybread', 'warriors'): 0, ('holdmybread', 'nbastreams'): 0, ('holdmybread', 'todayilearned'): 0, ('holdmybread', 'physicsmemes'): 0, ('holdmybread', 'mathematics'): 0, ('holdmybread', 'holdmybread'): 0}



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
            if val > 0:
                G.AddEdge(indicies[sub0], indicies[sub1])

    snap.DrawGViz(G, snap.gvlNeato, "output.png", " a sample subgraph ", labels)



