libname mylib '/workspaces/myfolder/models/baseball';


/* Gradient Boosting Model */
proc gradboost data=SASHELP.BASEBALL;
    /* Specify the target variable */
    target logSalary;
    
    /* Specify the predictor variables */
    input nAtBat nHits nHome nRuns nRBI nBB YrMajor CrAtBat CrHits CrHome CrRuns CrRbi CrBB Position nOuts nAssts nError Div;
    
    /* Output the results */
    output out=mylib.model_results;
run;