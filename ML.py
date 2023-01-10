
from sklearn import model_selection
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree


# -- run model
def run_model(X_data, Y_data):

    # clf = svm.SVC(kernel='rbf', C=1, verbose=True, shrinking=0)
    # scores_res = model_selection.cross_val_score(clf, X_data, Y_data,cv=5)

    # print(scores_res)
    # print(scores_res.mean())
    print("RandomForest Start")
    model = RandomForestClassifier(n_estimators=1000, random_state=0 )
    scores_res = model_selection.cross_val_score(model, X_data, Y_data, cv=5)

    print(scores_res)
    print(scores_res.mean())
