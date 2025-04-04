import numpy as np
import pickle
import pandas as pd
import settings
from sklearn.linear_model import LogisticRegression

def scoreModel(RecencyScore,FrequencyScore,MonetaryScore):
    "Output: EM_CLASSIFICATION,EM_PROBABILITY,_ERROR"
    _ERROR="No Errors or Warnings."
    EM_CLASSIFICATION = str(0)
    EM_PROBABILITY = -1
    ## Load pickled model
    try:
        dm_model
    except NameError:
        model = open(settings.pickle_path+'/logreg.pickle', 'rb')
        dm_model = pickle.load(model)
        model.close()

    try:
        x = pd.DataFrame([[RecencyScore,FrequencyScore,MonetaryScore]],columns = ["RecencyScore","FrequencyScore","MonetaryScore"])
        preds = dm_model.predict(x)
        probs = dm_model.predict_proba(x)
        EM_CLASSIFICATION = str(preds[0])
        EM_PROBABILITY = float(probs[0,preds[0]])
    except Exception as error:
        _ERROR = str(error)
        print(error)


    return EM_CLASSIFICATION,EM_PROBABILITY,_ERROR
