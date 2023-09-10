import numpy as np
import pandas as pd
from .pyttsx_test import *
from sentence_transformers import SentenceTransformer, util
import os


def encode_dataset(dataset,columns_to_encode):
    model = SentenceTransformer('distiluse-base-multilingual-cased')
    encoded = pd.DataFrame()
    for i in range(dataset.shape[1]):
        new_column = []
        if i in columns_to_encode:
            for j in range(dataset.shape[0]):
                try:
                    new_column.append(model.encode(dataset.iloc[j, i]))
                except:
                    new_column.append(model.encode("NaN"))
        else:
            new_column=dataset[dataset.columns[i]]
        encoded[dataset.columns[i]] = new_column
    return encoded


def cos_sim(initial,encoded,query,first_iterator,second_iterator,model):

    query_encoded = model.encode(query, convert_to_tensor=True)
    mx = float('-inf')
    ans=[]
    ansj=float('-inf')

    for i in first_iterator:
        for j in second_iterator:
            scores = util.pytorch_cos_sim(query_encoded, encoded.loc[i,j])
            if scores>mx:
                mx=scores
                ans.clear()
                ans.append(i)
                ansj=j
            elif scores == mx:
                 ans.append(i)
                 ansj=j
    if (ansj==initial.shape[1]-3):
        say_something(initial.iloc[ans[0],ansj+1])
        print(initial.iloc[ans[0],ansj])
        return ans[0],ansj+1
    else:
        print(*ans)
        return second_attempt(initial, encoded, query, ans, ansj+1)


def second_attempt(initial, encoded, query, first_iterator, column):
    wrong = []
    print(column)
    if column >= initial.shape[1]:
        text_to_speech('По вашему запросу ничего не найдено')
        return -1,-1
    for reason in first_iterator:
        if (initial.iloc[reason,column] not in wrong):
            text_to_speech('Правда ли, что ' + initial.iloc[reason,column]+'?')
            inp = input()
            if (inp == 'нет'):
                wrong.append(initial.iloc[reason,column])
            elif (inp == 'да'):
                if (column==len(initial.columns)-3):
                    return reason,column+1
                else:
                    new_indexes = []
                    for i in first_iterator:
                        if initial.iloc[reason,column]==initial.iloc[i,column]:
                            new_indexes.append(i)
                    return second_attempt(initial,encoded,query,new_indexes,column+1)
        else:
            continue

############################### to install #########################################
#pip install numpy
#pip install pandas
#pip install pyaudio
# #pip install openpyxl --upgrade
#pip install sentence_transformers
##########################example of parsing the data###############################


class AIWoman:
    def __init__(self, dataset_path: str):
        self.data = pd.read_excel(dataset_path, index_col=0)
        if os.path.exists('./core/backend/encoded.npy'):
            encoded = pd.DataFrame(np.load('encoded.npy', allow_pickle=True))
        else:
            encoded = encode_dataset(self.data, np.arange(1, 6))
            encoded = encoded.to_numpy(copy=True)
            np.save('encoded.npy', encoded)
        self.encoded = encoded
        self.model = SentenceTransformer('distiluse-base-multilingual-cased')

    def find_cos_sim(self, input_: str, train_model='говновоз'):
        return cos_sim(
            self.data,
            self.encoded,
            input_,
            np.arange(self.encoded.shape[0]),
            np.arange(2, self.encoded.shape[1]-1),
            self.model
        )
