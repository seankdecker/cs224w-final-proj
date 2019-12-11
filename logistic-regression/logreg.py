from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn import preprocessing
import numpy as np

TRAIN_FRAC = 0.7
BANNED_SUBS = 143
NORMAL_SUBS = 500

# Runs basic logistic regression on feature vectors.
def run_logreg():
    # get data
    N0 = np.load('banned_data.npy')
    np.random.shuffle(N0) # shuffle order of banned feature vectors
    N1 = np.load('normal_data_1.npy')
    N2 = np.load('normal_data_2.npy')
    N3 = np.load('normal_data_3.npy')
    N4 = np.load('normal_data_4.npy')
    N5 = np.load('normal_data_5.npy')
    Nn = np.concatenate((N1, N2, N3, N4, N5), axis=0)
    np.random.shuffle(Nn) # shuffle order of normal feature vectors
    print('got data')

    # aggregate data
    X = np.concatenate((N0, Nn), axis=0)
    X = preprocessing.scale(X, axis=0) # scale feature vectors to 0 mean, 1 var for preprocessing
    y = np.concatenate((np.ones(BANNED_SUBS), np.zeros(NORMAL_SUBS)))
    train_begin = int(BANNED_SUBS * (1-TRAIN_FRAC))
    train_end = int(BANNED_SUBS + (NORMAL_SUBS * TRAIN_FRAC))
    print(train_begin)
    print(train_end)
    print(X.shape)
    print(y.shape)

    # process data
    X_train = X[train_begin:train_end,:]
    X_test = np.concatenate((X[0:train_begin,:], X[train_end:,:]))
    y_train = y[train_begin:train_end]
    y_test = np.concatenate((y[0:train_begin], y[train_end:]))
    print('processed data')

    # run logistic regression
    logreg = LogisticRegression(max_iter=250) # default options otherwise
    clf = logreg.fit(X_train,y_train)
    print('finished logreg')

    # get results
    y_pred = clf.predict(X_test)
    print(y_pred)
    np.save('logreg_results.npy', y_pred)
    print(classification_report(y_test, y_pred))
    print(confusion_matrix(y_test, y_pred))
    # confusion matrix: C_ij = number of obs in i predicted to be in j

if __name__ == '__main__':
    run_logreg()
