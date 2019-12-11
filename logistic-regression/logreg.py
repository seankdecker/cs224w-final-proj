from sklearn.linear_model import LogisticRegression
import numpy as np

TRAIN_FRAC = 0.7
BANNED_SUBS = 143
NORMAL_SUBS = 300

def run_logreg():
    N0 = np.load('banned_data.npy')
    N1 = np.load('normal_data_1.npy')
    N2 = np.load('normal_data_2.npy')
    N3 = np.load('normal_data_3.npy')

    X = np.concatenate((N0, N1, N2, N3), axis=0)
    y = np.concatenate((np.ones(BANNED_SUBS), np.zeros(NORMAL_SUBS)))


    X_train = X[int(BANNED_SUBS * (1-TRAIN_FRAC)): int(BANNED_SUBS + (NORMAL_SUBS * TRAIN_FRAC))]
    X_test = np.concatenate(X[0:int(BANNED_SUBS * (1-TRAIN_FRAC))], X[int(BANNED_SUBS + (NORMAL_SUBS * TRAIN_FRAC)):])
    y_train = y[int(BANNED_SUBS * (1-TRAIN_FRAC)): int(BANNED_SUBS + (NORMAL_SUBS * TRAIN_FRAC))]
    y_test = np.concatenate(y[0:int(BANNED_SUBS * (1-TRAIN_FRAC))], y[int(BANNED_SUBS + (NORMAL_SUBS * TRAIN_FRAC)):])

    logreg = LogisticRegression()
    clf = logreg.fit(X_train,y_train)
    y_logreg = clf.predict(X)
    np.save('logreg_results.npy', y_logreg)
    print(y_logreg)
    num_correct = 0
    for i in range(y_test.size):
        if y_logreg[i] == y_test[i]:
            num_correct += 1
    print("Correct: {} out of {}".format(num_correct, y_test.size))
    frac_correct = num_correct / y_test.size
    print("Fraction: {}".format(frac_correct))

if __name__ == '__main__':
    run_logreg()
