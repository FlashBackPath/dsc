import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, accuracy_score


df = pd.read_csv("C:/Users/roma5/OneDrive/Рабочий стол/ml_case/train.csv")
df.dropna(inplace = True)

df.head()
df.info()

df.drop(['bdate', 'has_photo', 'has_mobile', 'followers_count', 'langs', 'people_main', 'city',
        'last_seen', 'occupation_name', 'career_start', 'career_end'], axis = 1, inplace = True)

print(df.value_counts(["education_form"]))
print(df.value_counts(["education_status"]))
list(df.value_counts("education_status").index)
educ_status = list(df.value_counts("education_status").index)
def education(x):
    global educ_status
    return educ_status.index(x)
df["education_status"] = df["education_status"].apply(education)
df[(pd.get_dummies(df["education_form"]).columns)] = pd.get_dummies(df["education_form"])
df[(pd.get_dummies(df["occupation_type"]).columns)] = pd.get_dummies(df["occupation_type"])
df.head()

df.drop(["education_form", "occupation_type"], axis=1, inplace=True)
df.drop("life_main", axis=1, inplace=True)


X = df.drop('result', axis = 1)
y = df['result']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
classifier = KNeighborsClassifier(n_neighbors = 5)
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)
print('Процент правильно предсказанных исходов:', accuracy_score(y_test, y_pred) * 100)
print('Confusion matrix:')
print(confusion_matrix(y_test, y_pred))