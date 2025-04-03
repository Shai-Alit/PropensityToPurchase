import os
import sasctl
from sasctl import pzmm
from sasctl import Session
from sasctl.services import model_repository as mr, model_management as mm
from pathlib import Path
import requests

WORKSPACE = os.environ['WORKSPACE']

with open(WORKSPACE + '/workspaces/myfolder/creds.json') as f:
    creds = json.load(f)

st = Session(creds['verde']['host'], token=creds['verde']['token'], verify_ssl=False)
st


repository = mr.get_repository('DMRepository')
repository.name

project_name = "Baseball Salary Prediction WB"
try:
    project = mr.create_project(project_name, repository)
except:
    project = mr.get_project(project_name)


model_params = {
    "name": "ViyaWorkbench_SASRF",
    "projectId": project.id,
    "type": "ASTORE",
}

astore = mr.post(
    "/models",
    files={"files": (f"/workspaces/myfolder/models/baseball/pipeline/model_export.astore",sasrf.export())},
    data=model_params,
)

path = '/workspaces/myfolder/models/baseball/pipeline/artefacts/'

# Save to same folder as pickle file
modelPklName = 'rf'
tool_version = str(sys.version_info.major)+'_'+str(sys.version_info.minor)+'_'+str(sys.version_info.micro)

pklFileName = modelPklName+'_V'+tool_version+'.pkl'

import pickle

with open(path+pklFileName, 'wb') as fp:
    pickle.dump(rf, fp)
fp.close()

model_name = "scikit-learn_RandomForest"

pzmm.JSONFiles.write_model_properties_json(model_name=model_name,
                            model_desc='Scikit-learn RandomForestRegressor for Baseball Salary',
                            target_variable='logSalary',
                            model_algorithm='scikit-learn.RandomForestRegressor',
                            json_path=path,
                            modeler='Sean T Ford')

import_model = pzmm.ImportModel.import_model(
    model_files=path,
    model_prefix=model_name,
    project=project_name, 
    input_data=x_num,
    predict_method='{}.predict({})',
    target_values=["0","100"],
    force=True
)

model = mr.get_model(import_model[0].id)

## On-demand Score code
scorefile = mr.add_model_content(
    model,
    open(path+'/score_rf.py', 'rb'),
    name='score_rf.py',
    role='score'
)

## Python Pickle file
python_pickle = mr.add_model_content(
    model,
    open(path+pklFileName, 'rb'),
    name=pklFileName,
    role='python pickle'
)