import numpy as np
import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

df = pd.read_csv('https://raw.githubusercontent.com/aLeadPencil/SimpleFlaskDashIntegration/master/Iris.csv?token=AKXMDUQVY5XI7KHWI2ZGS3K62P6HY')
X_train, X_test, y_train, y_test = train_test_split(
    df[['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm']], 
    df['Species'],
    random_state = 1,
    test_size = 0.5
)

clf = LogisticRegression()
clf.fit(X_train, y_train)

pickle.dump(clf, open('logistic_regression_model.pkl', 'wb'))