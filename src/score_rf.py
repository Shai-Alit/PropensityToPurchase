import numpy as np
import pickle
import pandas as pd
import settings

def score_rf_model(nAtBat, nHits, nHome, nRuns, nRBI, nBB, YrMajor,
       CrAtBat, CrHits, CrHome, CrRuns, CrRbi, CrBB, nOuts,
       nAssts, nError):
    "Output: P_LogSalary"
    
    ## Load pickled model
    try:
        dm_model
    except NameError:
        model = open(settings.pickle_path+'/rf_V3_11_9.pkl', 'rb')
        dm_model = pickle.load(model)
        model.close()

    ## Define input dataframe to score
    input_list=[nAtBat, nHits, nHome, nRuns, nRBI, nBB, YrMajor,
       CrAtBat, CrHits, CrHome, CrRuns, CrRbi, CrBB, nOuts,
       nAssts, nError]
    X = pd.DataFrame(input_list).T
    X.columns=(['nAtBat', 'nHits', 'nHome', 'nRuns', 'nRBI', 'nBB', 'YrMajor',
       'CrAtBat', 'CrHits', 'CrHome', 'CrRuns', 'CrRbi', 'CrBB', 'nOuts',
       'nAssts', 'nError'])
    
    ## predict
    P_LogSalary = dm_model.predict(X)

    return float(P_LogSalary)