import time
start = time.clock()

from pkg import preprocess
from pkg import vectorizer
from sklearn.model_selection import KFold
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import f1_score

data = preprocess.readplz()
x,y=preprocess.get(data)

def cv_loop(model, name):
    model.fit(x,y)
    predict_y = model.predict(x)
    print('f1-score:')
    print(f1_score(y,predict_y, average='weighted'))

    print('k-fold--',end='')

    SPLITS = 10
    kf = KFold(n_splits=SPLITS)
    avg_train_f1score=0
    avg_test_f1score=0
    print('begin!')
    for train,test in kf.split(x):

        x_train,x_test,y_train,y_test = x[train],x[test],y[train],y[test]
        print('fit--->', end='')
        model.fit(x_train,y_train)
        
        print('test predit',end='')
        predict_y = model.predict(x_test)
        t_score = f1_score(y_test,predict_y, average='weighted')
        avg_test_f1score += t_score
        print('test t1 score',end='')
        print(t_score, end='')

        print('train predit',end='')
        predict_y = model.predict(x_train)
        t_score = f1_score(y_train,predict_y, average='weighted')
        avg_train_f1score += t_score
        print('train t1 score',end='')
        print(t_score)


    print(name)
    print('avg_test_f1score = ',end='')
    print(avg_test_f1score/SPLITS)
    print('avg_train_f1score = ',end='')
    print(avg_train_f1score/SPLITS)

if __name__ == '__main__':
    

    models = [RandomForestClassifier(), ExtraTreesClassifier(), GaussianNB(), KNeighborsClassifier(), 
        DecisionTreeClassifier(), LogisticRegression(), SVC()]
    model_names = ['RandomForestClassifier()', 'ExtraTreesClassifier()', 'GaussianNB()', 'KNeighborsClassifier()', 
        'DecisionTreeClassifier()', 'LogisticRegression()', 'SVC()']

    for i in range(len(models)):
        cv_loop(models[i], model_names[i])

    elapsed = (time.clock() - start)
    print("Time used:", elapsed)