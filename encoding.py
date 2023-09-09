import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer, util
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

def cos_sim(encoded,query,first_iterator,second_iterator):
    mx = float('-inf')
    ans=[]
    ansj=float('-inf')
    for i in first_iterator:
        for j in second_iterator:
            scores = util.pytorch_cos_sim(query, encoded.loc[i,j])
            if scores>mx:
                mx=scores
                ans.clear()
                ans.append(i)
                ansj=j
            elif scores == mx:
                ans.append(i)
                ansj=j
    return ans,ansj
############################### to install #########################################
#pip install numpy
#pip install pandas
#pip install pyaudio
# #pip install openpyxl --upgrade
#pip install sentence_transformers
##########################example of parsing the data###############################
#data = pd.read_excel("parsed_dataV2.xlsx",index_col=0)
#encoded = encode_dataset(data,np.arange(1,6))
#encoded_np=encoded.to_numpy(copy=True)
#np.save('encoded.npy', encoded_np)
####################################################################################
