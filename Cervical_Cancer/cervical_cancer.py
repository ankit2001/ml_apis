import pandas as pd
import numpy as np
import math


cancer_df = pd.read_csv('./kag_risk_factors_cervical_cancer.csv', header=0, na_values='?')
cancer_df.drop(['STDs: Time since first diagnosis','STDs: Time since last diagnosis'],inplace=True,axis=1)
numerical_df = ['Age', 'Number of sexual partners', 'First sexual intercourse','Num of pregnancies', 'Smokes (years)',
                'Smokes (packs/year)','Hormonal Contraceptives (years)','IUD (years)','STDs (number)']
categorical_df = ['Smokes','Hormonal Contraceptives','IUD','STDs','STDs:condylomatosis','STDs:cervical condylomatosis',
                  'STDs:vaginal condylomatosis','STDs:vulvo-perineal condylomatosis', 'STDs:syphilis',
                  'STDs:pelvic inflammatory disease', 'STDs:genital herpes','STDs:molluscum contagiosum', 'STDs:AIDS', 
                  'STDs:HIV','STDs:Hepatitis B', 'STDs:HPV', 'STDs: Number of diagnosis','Dx:Cancer', 'Dx:CIN', 
                  'Dx:HPV', 'Dx', 'Hinselmann', 'Schiller','Citology', 'Biopsy']
cancer_df = cancer_df.replace('?', np.NaN)
### Filling the missing values of numeric data columns with mean of the column data.
for feature in numerical_df:
    feature_mean = round(pd.to_numeric(cancer_df[feature], errors='coerce').mean(),1)
    cancer_df[feature] = cancer_df[feature].fillna(feature_mean)
for feature in categorical_df:
    cancer_df[feature] = pd.to_numeric(cancer_df[feature], errors='coerce').fillna(1.0)
category_df = ['Hinselmann', 'Schiller','Citology', 'Biopsy']

cancer_df['Number of sexual partners'] = round(pd.to_numeric(cancer_df['Number of sexual partners']))
cancer_df['First sexual intercourse'] = pd.to_numeric(cancer_df['First sexual intercourse'])
cancer_df['Num of pregnancies']=round(pd.to_numeric(cancer_df['Num of pregnancies']))
cancer_df['Smokes'] = pd.to_numeric(cancer_df['Smokes'])
cancer_df['Smokes (years)'] = pd.to_numeric(cancer_df['Smokes (years)'])
cancer_df['Hormonal Contraceptives'] = pd.to_numeric(cancer_df['Hormonal Contraceptives'])
cancer_df['Hormonal Contraceptives (years)'] = pd.to_numeric(cancer_df['Hormonal Contraceptives (years)'])
cancer_df['IUD (years)'] = pd.to_numeric(cancer_df['IUD (years)'])

## removing the smokes column from the dataframe.
cancer_df.drop('Smokes',axis=1,inplace=True)
cancer_df.drop('Hormonal Contraceptives',axis=1,inplace=True)
### Dropping IUD column because IUD (years) has a non-zero value only if IUD is non-zero.
cancer_df.drop('IUD',axis=1,inplace=True)
cancer_df['STDs (number)'] = round(pd.to_numeric(cancer_df['STDs (number)']))
cancer_df.drop('Dx',axis=1,inplace=True)


cancer_df_features = cancer_df.drop(['Hinselmann', 'Schiller', 'Citology','Biopsy'],axis=1)
cancer_df_label = pd.DataFrame(data=cancer_df['Hinselmann'])
cancer_df_label['Schiller'] = cancer_df['Schiller']
cancer_df_label['Citology'] = cancer_df['Citology']
cancer_df_label['Biopsy'] = cancer_df['Biopsy']
def cervical_cancer(cancer_label):
    
    hil, sch, cit, bio = cancer_label
    
    return hil+sch+cit+bio

cancer_df_label['cervical_cancer'] = cancer_df_label[['Hinselmann', 'Schiller', 'Citology','Biopsy']].apply(cervical_cancer,axis=1)
cancer_df_label.drop(['Hinselmann', 'Schiller', 'Citology','Biopsy'],axis=1,inplace=True)
print('Value counts of each target variable:',cancer_df_label['cervical_cancer'].value_counts())
cancer_df_label = cancer_df_label.astype(int)
cancer_df_label = cancer_df_label.values.ravel()

print('Final feature vector shape:',cancer_df_features.shape)
print('Final target vector shape',cancer_df_label.shape)
### cross validation on 26 features model with oversampling and StratifiedKFold
from sklearn.model_selection import StratifiedKFold
from sklearn import model_selection
from sklearn.linear_model import LogisticRegressionCV
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.model_selection import cross_val_score
import pickle
import warnings 
warnings.filterwarnings("ignore")
#Tried out different
# models = []
# models.append(('LogisticRegMulti', LogisticRegressionCV(class_weight=None, multi_class='multinomial', solver='newton-cg', max_iter=1000,penalty='l2')))
# models.append(('LogisticRegOVR', LogisticRegressionCV(class_weight=None, multi_class='ovr', solver='newton-cg', max_iter=1000,penalty='l2')))
# models.append(('svm_linear', svm.LinearSVC(C=1.0,class_weight=None,multi_class='ovr',penalty='l2',max_iter=1000)))
# models.append(('svm_rbf', svm.SVC(gamma='auto', C=1.2,degree=4, probability=True,kernel='rbf',decision_function_shape='ovr')))
# models.append(('RandomForest',RandomForestClassifier(n_jobs=4, bootstrap=True, class_weight=None, criterion='gini',max_depth=None, max_features='auto', max_leaf_nodes=None,
#                          min_samples_leaf=1, min_samples_split=2,min_weight_fraction_leaf=0.0, n_estimators=10, 
#                          oob_score=False, random_state=None, verbose=0,warm_start=False)
# ))
scoring = 'recall_weighted'
## oversampling
from imblearn.over_sampling import SMOTE, ADASYN
cancer_df_features_ovr, cancer_df_label_ovr = SMOTE().fit_sample(cancer_df_features, cancer_df_label)

### Building a model for future predictions:

random_forest_model = RandomForestClassifier(n_jobs=16, bootstrap=True, class_weight=None, criterion='gini',max_depth=None, max_features='auto', max_leaf_nodes=None,
                         min_samples_leaf=1, min_samples_split=2,min_weight_fraction_leaf=0.0, n_estimators=10, 
                         oob_score=False, random_state=None, verbose=0,warm_start=False)
cv_results = model_selection.cross_val_score(random_forest_model, cancer_df_features_ovr, cancer_df_label_ovr, cv=None, scoring=scoring)
print("%0.2f accuracy with a standard deviation of %0.2f" %( cv_results.mean(),cv_results.std()))
model = random_forest_model.fit(cancer_df_features,cancer_df_label)
pkl_filename = "pickle_model.pkl"
with open(pkl_filename, 'wb') as file:
    pickle.dump(model, file)
