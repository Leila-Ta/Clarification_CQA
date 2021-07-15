import re
from sklearn.datasets import load_files
import pickle
from nltk.stem import WordNetLemmatizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import model_selection, preprocessing
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import pandas as pandas
import xlrd
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.metrics import f1_score


typelabels, patternlabels, texts ,ptl, ptl_temp= [], [], [],[], []

# load the dataset
loc = ("./Train.xlsx")
#loc = ("/Users/leila/PycharmProjects/StackExchange/Result/Business/quant.stackexchange.com/Analyse/no answer67_labelled.xlsx")

wb = xlrd.open_workbook(loc)
#sheet = wb.sheet_by_name('Pattern')
sheet = wb.sheet_by_name('Sheet2')
for i in range(sheet.nrows):
    #patternlabels.clear()
    ptl.clear()
    texts.append((sheet.cell_value(i,0)).lower())
    # ptl=[sheet.cell_value(i, 5).lower()]
    # ptl=ptl+[sheet.cell_value(i, 6).lower()]

    # ptl_temp.clear()
    # if(patternlabels):
    #     for z in patternlabels:
    #         ptl_temp=(ptl_temp+[z]).copy()
    #         #print([z])
    #     patternlabels=(ptl_temp+[ptl.copy()])
    # else:
    #     patternlabels = [(ptl).copy()]

    #patternlabels.append((sheet.cell_value(i, 1)).lower()+" "+(sheet.cell_value(i, 2)).lower())
    patternlabels.append((sheet.cell_value(i, 1)).lower())
    #patternlabels.append((sheet.cell_value(i, 1)+" "+sheet.cell_value(i, 2)).lower())
print("patternlabel")
print(patternlabels)
# print(ptl)
#print(texts)
ClarQ = []
Y =[]
pt=list()
ClarQ_temp=list()

stemmer = WordNetLemmatizer()

for sen in range(0, len(texts)):

    # Substituting multiple spaces with single space
    Y = re.sub(r'\s+', ' ', texts[sen], flags=re.I)

    # # Lemmatization
    # Y = Y.split()

    # Y = [stemmer.lemmatize(word) for word in Y]
    # Y = ' '.join(Y)

    ClarQ.append(Y)

# create a dataframe using texts and lables

trainDF = pandas.DataFrame()
trainDF['text'] = ClarQ
# print("0000")
# print(trainDF['text'][0])
print("trainDF['text']")
print(trainDF['text'])
# print(len(trainDF['text']))
#print(ClarQ)
trainDF['label'] = patternlabels
print("trainDF['label']")
print(trainDF['label'])
#trainDF['type'] = typelabels
#print(trainDF['type'])
#ClarQ_temp=trainDF['label']
#ClarQ_temp.append(trainDF['type'])
#print(ClarQ_temp)

# split the dataset into training and validation datasets

tfidf_vect_ngram = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}', ngram_range=(1,6), max_features=None, min_df=1, max_df=0.9)
# for x in range(len(trainDF['text'])):
#     ClarQ_temp.clear()
#     ClarQ_temp = trainDF['text'][x]
#     print(ClarQ_temp)
XCLARQ= tfidf_vect_ngram.fit_transform(trainDF['text'])
print("XCLARQ")
print(XCLARQ)
YCLARQ= tfidf_vect_ngram.transform(trainDF['label'])

train_x, test_x, train_y, test_y = train_test_split(XCLARQ,trainDF['label'], test_size=0.2, random_state=0)

classifier = RandomForestClassifier(n_estimators=1000, random_state=1,n_jobs=-1)
classifier.fit(train_x,train_y)
y_pred = classifier.predict(test_x)
print("train_x")
print(train_x)
print("train_y")
print(train_y)
print("test_X")
print(test_x)
print("test_y")
print(test_y)

print("y_pred")
print(y_pred)
print("confusion_matrix(test_y,y_pred)")
print(confusion_matrix(test_y,y_pred))
print("classification_report(test_y,y_pred)")
print(classification_report(test_y,y_pred))
print("accuracy_score(test_y, y_pred)")
print(accuracy_score(test_y, y_pred))




