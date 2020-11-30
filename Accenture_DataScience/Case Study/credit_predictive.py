# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 16:30:03 2020

@author: Armando Alvarez Rolins

Description: A Diretoria de Risco de Crédito de grande banco brasileiro contratou a Accenture para desenvolver um modelo preditivo que os ajude a identificar os clientes com maior probabilidade de default, seja negando o empréstimo, ou concendo-o sob uma maior taxa de juros, o que permitirá um aumento na lucratividade dessa determinada carteira de clientes.

Sua tarefa será prever a probabilidade de default - que está identificado na variável default do dataset.  O resultado de seu estudo será encaminhado para as áreas jurídica e de negócios para a elaboração de novos contratos e produtos, portanto os resultados precisam ser acompanhados de uma explicação do funcionamento do seu modelo, em diferentes cenários.
"""
import pandas as pd
import numpy as np
import sklearn as sk
import matplotlib
import matplotlib.pyplot as plt
# Feature Engineering tools
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
# Oversampling e undersampling
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
# Modelagem
from sklearn.model_selection import (train_test_split, GridSearchCV)
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
# Métricas
from sklearn.metrics import accuracy_score, recall_score
from sklearn.metrics import roc_curve, auc
#Random
import random
# Seed
random_Seed = random.seed(42)

matplotlib.pyplot.close('all')

# Leitura do arquivo e extração de dados para um panda dataframe
df_credit = pd.read_csv("../Case Study/credit risk.csv")

"""
# Plotar a proporção de clientes que entram em default contra os que não entram
plt.figure(num=1, clear=True)
default_countplot = sns.countplot(data=df_test, x="default")
default_countplot.set_title("Proporção de Default")

# Plotar a correlação de variáveis numericas
plt.figure(num=2, figsize=(14,12), clear=True)
corr_heatmap = df_credit.select_dtypes(exclude = 'object').corr()
corr_heatmap.index = df_credit.select_dtypes(exclude = 'object').columns
sns.heatmap(corr_heatmap, annot = True, vmin=-1, vmax=1)
plt.title("Correlação de variáveis numericas")
plt.show()
"""
# %% Feature Engineering - Handling Outliers (Capping)
# Tratação das variáveis categóricas
count_score_1 = df_credit['score_1'].value_counts() [df_credit['score_1'].value_counts() < 10000]
count_score_2 = df_credit['score_2'].value_counts() [df_credit['score_2'].value_counts() < 1000]
#count_reason = df_credit['reason'].value_counts()[df_credit['reason'].value_counts() < 1000]
count_state = df_credit['state'].value_counts()[df_credit['state'].value_counts() < 500]
count_zip = df_credit['zip'].value_counts()[df_credit['zip'].value_counts() < 500]
#count_channel = df_credit['channel'].value_counts()#[df_credit['channel'].value_counts() < 1000]
#count_job_name = df_credit['job_name'].value_counts()[df_credit['job_name'].value_counts() < 100]
count_real_state = df_credit['real_state'].value_counts()
[df_credit['real_state'].value_counts() < 1000]

# Removendo excesso de categorias
df_credit.loc[df_credit['score_1'].isin((count_score_1).index), 'score_1'] = 'other'
df_credit.loc[df_credit['score_2'].isin((count_score_2).index), 'score_2'] = 'other'
#df_credit.loc[df_credit['reason'].isin((count_reason).index), 'reason'] = 'other'
df_credit.loc[df_credit['state'].isin((count_state).index), 'state'] = 'other'
df_credit.loc[df_credit['zip'].isin((count_zip).index), 'zip'] = 'other'
#df_credit.loc[df_credit['job_name'].isin((count_job_name).index), 'job_name'] = 'other'
df_credit.loc[df_credit['real_state'].isin((count_real_state).index), 'real_state'] = 'other'

# Removendo features para diminuir complexidade do modelo
df_credit.drop(labels='channel', axis=1, inplace=True)
df_credit.drop(labels='reason', axis=1, inplace=True)
df_credit.drop(labels='sign', axis=1, inplace=True)
df_credit.drop(labels='facebook_profile', axis=1, inplace=True)
#df_credit.drop(labels='gender', axis=1, inplace=True)
df_credit.drop(labels='zip', axis=1, inplace=True)
df_credit.drop(labels='state', axis=1, inplace=True)
df_credit.drop(labels='job_name', axis=1, inplace=True)

# %% Feature Engineering - Creating
# Features numéricas
df_credit['d2i_ratio'] = df_credit['amount_borrowed'] / df_credit['income']
df_credit['l2i_ratio'] = df_credit['credit_limit'] / df_credit['income']

# Separando objetos
object_columns = df_credit.select_dtypes(include='object').columns.tolist()
object_columns = [i for i in object_columns if i not in ('ids', 'default')]

# Preenchendo espaços vazios com NaN
df_credit[object_columns] = df_credit[object_columns].fillna('nan')
df_credit[object_columns] = df_credit[object_columns].astype(str)

# Definindo atributos de categoria e numéricos
atrib_cat = df_credit.select_dtypes(include=['object']).columns.tolist()
atrib_cat = [elem for elem in atrib_cat if elem not in ('ids', 'default')]
atrib_num = df_credit.select_dtypes(exclude=['object']).columns.tolist()

# Definindo variaveis categoricas e numericas
df_credit_cat = df_credit[atrib_cat]
df_credit_num = df_credit[atrib_num]
df_credit['default'] = df_credit['default'].replace(True, 1)
df_credit['default'] = df_credit['default'].replace(False, 0)

# Separando os dados de teste e de treinamento
df_pred = df_credit[df_credit['default'].isna()]
X_pred = df_pred.drop(columns=['ids','default'], axis=1)
y_pred = df_pred['default']
df_model = df_credit.dropna(subset=['default'])
X_model = df_model.drop(columns=['ids','default'], axis=1)
y_model = df_model['default']

# %% Feature Engineering - Imputing
encoder = OneHotEncoder(sparse=False) #sparse=False handle_unknown='ignore'
imputer = SimpleImputer(missing_values=np.nan)

# Encoding dados categóricos
encoder.fit(X_pred[atrib_cat])
out = encoder.transform(X_pred[atrib_cat])
X_pred_cat_enc = pd.DataFrame(out)
encoder.fit(X_model[atrib_cat])
out = encoder.transform(X_model[atrib_cat])
X_model_cat_enc = pd.DataFrame(out)

# Imputing dados numéricos com a estratégia padrão de média
imputer.fit(X_pred[atrib_num])
X_pred_num_imp = pd.DataFrame(imputer.transform(X_pred[atrib_num]))
X_pred_num_imp.columns = X_pred[atrib_num].columns.tolist()
imputer.fit(X_model[atrib_num])
X_model_num_imp = pd.DataFrame(imputer.transform(X_model[atrib_num]))
X_model_num_imp.columns = X_model[atrib_num].columns.tolist()

X_pred = pd.concat([X_pred_num_imp, X_pred_cat_enc], axis=1)
X_model = pd.concat([X_model_num_imp, X_model_cat_enc], axis=1)

# %% Test-Train Split
X_train, X_test, y_train, y_test = train_test_split(X_model, y_model)

X_pred, X_train = X_pred.align(X_train, join='inner', axis=1)

# %% Feature Engineering - Sampling
# Aplicando Random unersampling para equilibrar as classes de default
ros = RandomUnderSampler(random_state=0)
ros.fit(X_train, y_train)
X_train, y_train = ros.fit_resample(X_train, y_train)

# %% Classificação - Regressão Logística

# Usando Grid Search para buscar os melhores parametros do Random Forest
"""
lr_grid = {
		   'penalty': ['l1', 'l2'],
		   'C': np.logspace(-4, 4, 20),
		   'solver': ['liblinear', 'saga']
		   }

lr_gridcv = GridSearchCV(estimator=LogisticRegression(random_state=random_Seed),
						  scoring='roc_auc',
						  param_grid=lr_grid,
						  cv=3,
						  n_jobs=-1,
						  verbose=10)
lr_gridcv.fit(X_train, y_train)
"""

# Modelo Regressão Logística
lr_params = {
	'penalty': 'l1',
	'C': 0.615848211066026,
	'solver': 'liblinear'
}
lr = LogisticRegression(**lr_params, verbose=1)
lr.fit(X_train, y_train)
lr_prob_test = lr.predict(X_test)
lr_accuracy = accuracy_score(y_test, lr_prob_test)
lr_recall = recall_score(y_test, lr_prob_test, average='binary')
df_lr_test = pd.DataFrame({'reference': y_test, 'model': lr_prob_test})

lr_prob = lr.predict_proba(X_pred)
df_lr = pd.DataFrame({'ids': df_pred['ids'], 'prob_de_default': lr_prob[:, 1]})

# %% Classificação - Random Forest

# Usando Grid Search para buscar os melhores parametros do Random Forest
"""
rf_grid = {
		   'n_estimators': [250, 300, 350],
		   'max_features': [12, 14, 16],
		   'max_depth': [12, 14, 16],
		   'min_samples_leaf': [6, 8, 10],
	}

rf_gridcv = GridSearchCV(estimator=RandomForestClassifier(random_state=random_Seed),
			  scoring='roc_auc',
			  param_grid=rf_grid,
			  cv=3,
			  n_jobs=-1,
			  verbose=10)
rf_gridcv.fit(X_train, y_train)
"""
## Modelo Random Forest
rf_params = {'max_depth': 14,
			 'max_features': 12,
			 'min_samples_leaf': 8,
			 'n_estimators': 300,
			 'random_state': random_Seed
			 }
rf = RandomForestClassifier(**rf_params, verbose=1)
rf.fit(X_train, y_train)
rf_prob_test = rf.predict(X_test)
rf_accuracy = accuracy_score(y_test, rf_prob_test)
rf_recall = recall_score(y_test, rf_prob_test, average='binary')
df_rf_test = pd.DataFrame({'reference': y_test, 'model': rf_prob_test})

rf_prob = rf.predict_proba(X_pred)
df_rf = pd.DataFrame({'ids': df_pred['ids'], 'prob_de_default': rf_prob[:,1]})

# %% Plots

# Importância de cada feature
feature = pd.DataFrame(X_train.columns.tolist())
#lr_importance = pd.DataFrame(lr.feature_importances_)
rf_importance = pd.DataFrame(rf.feature_importances_)

#df_lr_importances = pd.concat([feature, lr_importance], axis=1)
df_rf_importance = pd.concat([feature, rf_importance], axis=1)
df_rf_importance.columns = ['feature', 'importance']
df_rf_importance = df_rf_importance.sort_values(by='importance', ascending=False, axis=0)

# Plotar
plt.figure(num=3, clear=True)
plt.scatter(X_pred['income'], rf_prob[:,1])
plt.title('[RF] Prob. de Default vs. Renda')
plt.xlabel('Renda')
plt.ylabel('Prob. de Default')
plt.show()
