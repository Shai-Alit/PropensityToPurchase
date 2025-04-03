options set=SSLREQCERT="allow";

/*create a partition to separate training and validation data*/
proc partition data=SNOWLIB.baseball samppct=30 seed=919 partind;
    by logSalary;
    output out=work.baseball;
run;

*fit the model;
proc gradboost data=work.baseball(where=(_PartInd_ = 0));
    /* Specify the target variable */
    target logSalary / level=interval;
    
    /* Specify the predictor variables */
    input nAtBat nHits nHome nRuns nRBI nBB YrMajor CrAtBat CrHits CrHome CrRuns CrRbi CrBB nOuts nAssts nError;
   
    code file="/workspaces/myfolder/models/baseball/sas/gboost_bball_score_code.sas";
    saveState rstore = work.gradboost_baseball;
run;

*score the fitted model against training and validation data sets;
data work.gradboost_scored;
    set work.baseball;
    %include '/workspaces/myfolder/models/baseball/sas/gboost_bball_score_code.sas';
run;

*assess model performance against validation data;
proc assess data=work.gradboost_scored LIFTout=gradboost_lift;
    var P_logSalary;
    target logSalary / level=interval;
    by _PartInd_;
run;

*download score code;
proc astore;
   download rstore = work.gradboost_baseball
            store = "/workspaces/myfolder/models/baseball/sas/gradboostbballAstore.sasast";

run;

*register the model in Viya model manager;
proc registermodel
      name = "WB Gradboost BBall Astore"
      description = "Gradboost BBall Astore Model"
      data = sashelp.baseball
      algorithm = GRADBOOST
      function = PREDICTION
      server = "https://verde-viya.mtes-tt.unx.sas.com"
      oauthtoken = "myTokenName"
      replace;
   project id="82f0eb9a-bc9c-4050-8dd3-385834b01df1";
   astoremodel store = "/workspaces/myfolder/models/baseball/sas/gradboostbballAstore.sasast";
   target logSalary / level=interval;
   assessment;
run;


