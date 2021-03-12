import pandas as pd
import numpy as np
df=pd.read_csv("PCOS ANALYSIS FINAL.csv")

df.columns=['time','diagnosed','result','age','overweight','weightgain','periods','conceiving','chinHair','cheeksHair','upperLipHair','betweenBreastHair','armsHair','innerThighHair','acneOrskinTag','hairThinning','darkPatch','tiredness','moodSwings','exercise','eatOutside','cannedFood','city']
df.dtypes

new=pd.DataFrame(df[df.diagnosed=='Yes'])
new.reset_index(drop=True,inplace=True)
new
new.drop('time',axis=1,inplace=True)
new
new.weightgain.fillna('abc',inplace=True)
y=pd.DataFrame(new.result)
new.drop('result',axis=1,inplace=True)
new
def g(s):
    if(s=="YES"):
        return 1
    if(s=="NO"):
        return 0
    if s=="Yes":
        return 1
    if s=="No":
        return 0
    if s=="abc":
        return 2
    return 0

new["Diagnose"]=new.diagnosed.apply(g)
new["Overweight"]=new.overweight.apply(g)
new["Weightgain"]=new.weightgain.apply(g)
new["Periods"]=new.periods.apply(g)
new["Conceiving"]=new.conceiving.apply(g)
new["AcneOrskinTag"]=new.acneOrskinTag.apply(g)
new["HairThinning"]=new.hairThinning.apply(g)
new["DarkPatch"]=new.darkPatch.apply(g)
new["Tiredness"]=new.tiredness.apply(g)
new["MoodSwings"]=new.moodSwings.apply(g)
new["CannedFood"]=new.cannedFood.apply(g)
new["City"]=new.city.apply(g)
del new["diagnosed"]
del new["overweight"]
del new["weightgain"]
del new["periods"]
del new["conceiving"]
del new["acneOrskinTag"]
del new["hairThinning"]
del new["darkPatch"]
del new["tiredness"]
del new["moodSwings"]
del new["cannedFood"]
del new["city"]
new.head()

def f(s):
    if(s=="Yes"):
        return True
    if(s=="No"):
        return False
    if(s=="Yes(Detected Positive)"):
        return True
    if(s=="No(Detected Negative)"):
        return False
y=y.result.apply(f)

y.head()
#converting dataframe to array
xnew=new.values
ynew=y.values

from sklearn.preprocessing import MinMaxScaler
scaler=MinMaxScaler(copy=True)
scaler.fit(xnew)
x_scaled=scaler.transform(xnew)

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(xnew,ynew,random_state=3)
############SVC ALGORITHM########################################
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.svm import SVC
clf=SVC(kernel='poly',degree=2,C=0.01)
clf.fit(x_train,y_train)
ypredsvm=clf.predict(x_test)
clf.score(x_train,y_train),clf.score(x_test,y_test)
############Decision Tree ALGORITHM########################################
from sklearn.tree import DecisionTreeClassifier
clf1=DecisionTreeClassifier()
clf1.fit(x_train,y_train)
ypredDT=clf1.predict(x_test)
clf1.score(x_train,y_train),clf1.score(x_test,y_test)
new.columns
clf1.feature_importances_
############Naive Bayse ALGORITHM########################################
from sklearn.naive_bayes import GaussianNB
clf2=GaussianNB()
clf2.fit(x_train,y_train)
ypredNB=clf2.predict(x_test)
clf2.score(x_train,y_train),clf2.score(x_test,y_test)
############Linear Regression ALGORITHM########################################
from sklearn.linear_model import LinearRegression
clf5=LinearRegression()
clf5.fit(x_train,y_train)
ypredLR=clf5.predict(x_test)
clf5.score(x_train,y_train),clf5.score(x_test,y_test)
############Logistic Regression ALGORITHM########################################
from sklearn.linear_model import LogisticRegression
clf3 = LogisticRegression(C=0.01)
clf3.fit(x_train,y_train)
ypredLR=clf3.predict(x_test)
clf3.score(x_train,y_train),clf3.score(x_test,y_test)
############KNN ALGORITHM########################################
from sklearn.neighbors import KNeighborsClassifier
clf6=KNeighborsClassifier(n_neighbors=3)
clf6.fit(x_train,y_train)
ypredKNN=clf6.predict(x_test)
clf6.score(x_train,y_train),clf6.score(x_test,y_test)
############Random Forest ALGORITHM########################################
from sklearn.ensemble import RandomForestClassifier
clf7 = RandomForestClassifier(criterion="entropy")
clf7.fit(x_train, y_train)
ypredRF=clf7.predict(x_test)
clf7.score(x_train,y_train),clf7.score(x_test,y_test)
from sklearn.model_selection import StratifiedKFold
def Stacking(model,train,y,test,n_fold):
    folds=StratifiedKFold(n_splits=n_fold,random_state=None)
    test_pred=np.empty((test.shape[0],1),float)
    train_pred=np.empty((0,1),float)
    for train_indices,val_indices in folds.split(train,y.values):
        x_train,x_val=train.iloc[train_indices],train.iloc[val_indices]
        y_train,y_val=y.iloc[train_indices],y.iloc[val_indices]
        model.fit(X=x_train,y=y_train)
        train_pred=np.append(train_pred,model.predict(x_val))
        test_pred=np.append(test_pred,model.predict(test))
    return test_pred.reshape(-1,1),train_pred

xtrain=pd.DataFrame(x_train)
ytrain=pd.DataFrame(y_train)
xtest=pd.DataFrame(x_test)
##########K Fold Validation ####################################
test_pred1 ,train_pred1=Stacking(model=clf6,n_fold=5, train=xtrain,test=xtest,y=ytrain)
test_pred2 ,train_pred2=Stacking(model=clf1,n_fold=5, train=xtrain,test=xtest,y=ytrain)
test_pred3 ,train_pred3=Stacking(model=clf,n_fold=5, train=xtrain,test=xtest,y=ytrain)

train_pred1=pd.DataFrame(train_pred1)
test_pred1=pd.DataFrame(test_pred1)

train_pred2=pd.DataFrame(train_pred2)
test_pred2=pd.DataFrame(test_pred2)

train_pred3=pd.DataFrame(train_pred3)
test_pred3=pd.DataFrame(test_pred3)

test_pred1=test_pred1.iloc[:41]
test_pred2=test_pred2.iloc[:41]
test_pred3=test_pred3.iloc[:41]

df_train = pd.concat([train_pred1, train_pred2, train_pred3], axis=1)
df_test = pd.concat([test_pred1, test_pred2,test_pred3], axis=1)

ytest=pd.DataFrame(y_test)
model = RandomForestClassifier(random_state=1,criterion="entropy")
model.fit(df_train,y_train)
model.score(df_test,y_test)



#Bagging 
from sklearn.ensemble import BaggingClassifier, AdaBoostClassifier, VotingClassifier
bg = BaggingClassifier(clf3, max_samples= 0.5, max_features = 1.0, n_estimators = 20)
bg.fit(x_train,y_train)
bg.score(x_test,y_test)

#Boosting - Ada Boost
adb = AdaBoostClassifier(LogisticRegression(),n_estimators = 5, learning_rate = 1)
adb.fit(x_train,y_train)
adb.score(x_test,y_test)

evc = VotingClassifier( estimators= [('svm',clf),('dt',clf1),('nb',clf2),('lr',clf3),('knn',clf6)], voting = 'hard')
evc.fit(x_train,y_train)
evc.score(x_test, y_test)
x_train[0]

###working directory
import joblib  # Save to filepip 
joblib_file = "model.pkl"   
joblib.dump(evc, joblib_file)

