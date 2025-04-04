import os
import sasctl
from sasctl import pzmm
from sasctl import Session
from sasctl.services import model_repository as mr, model_management as mm
from pathlib import Path
import requests
import json
import pandas as pd

WORKSPACE = os.environ['WORKSPACE']
model_path = WORKSPACE + '/github/PropensityToPurchase/models/'
src_path = WORKSPACE + '/github/PropensityToPurchase/src/'

with open(WORKSPACE + '/creds.json') as f:
    creds = json.load(f)

st = Session(creds['verde']['host'], token=creds['verde']['token'], verify_ssl=False)
st


repository = mr.get_repository('DMRepository')
repository.name

project_name = "Propensity"
try:
    project = mr.create_project(project_name, repository)
except:
    project = mr.get_project(project_name)


# Save to same folder as pickle file
modelPklName = 'logreg'
pklFileName = modelPklName + '.pickle'
#tool_version = str(sys.version_info.major)+'_'+str(sys.version_info.minor)+'_'+str(sys.version_info.micro)

#pklFileName = modelPklName+'_V'+tool_version+'.pkl'

#import pickle

#with open(model_path +pklFileName, 'wb') as fp:
#    pickle.dump(rf, fp)
#fp.close()

target_df = pd.DataFrame(data=[["1",1.0,""]],columns=['EM_CLASSIFICATION','EM_PROBABILITY','_ERROR'])
input_df = pd.DataFrame(data=[[1,1,1]],columns=['RecencyScore','FrequencyScore','MonetaryScore'])

pzmm.JSONFiles.write_var_json(input_df, is_input=True, json_path=model_path)

pzmm.JSONFiles.write_var_json(target_df, is_input=False, json_path=model_path)

model_name = "scikit-learn_LogReg"

pzmm.JSONFiles.write_model_properties_json(model_name=model_name,
                            model_desc='Scikit-learn Logistic Regression for Propensity to Purchase',
                            target_variable='Ordered',
                            model_algorithm='scikit-learn.LogisticRegression',
                            target_values=["1","0"],
                            json_path=model_path,
                            modeler='Sean T Ford')

import_model = pzmm.ImportModel.import_model(
    model_files=model_path,
    model_prefix=model_name,
    project=project_name,
    input_data=input_df,
    predict_method='{}.predict_proba({})', 
    target_values=["1","0"],
    force=True
)

model = mr.get_model(import_model[0].id)

## On-demand Score code
scorefile = mr.add_model_content(
    model,
    open(src_path + '/scoreModel.py', 'rb'),
    name='scoreModel.py',
    role='score'
)

## Python Pickle file
python_pickle = mr.add_model_content(
    model,
    open(model_path + pklFileName, 'rb'),
    name=pklFileName,
    role='python pickle'
)