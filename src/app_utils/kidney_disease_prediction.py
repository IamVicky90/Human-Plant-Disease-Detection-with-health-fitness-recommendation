            
from flask import request
import pickle
import os
import pandas as pd
from src.loggings import add_logger
def kidney_disease_pred(age, bp, sg, al, su, bgr, bu, sc, sod, pot, hemo,pcv, wc, rc):
    log=add_logger()
    try:
        model_path=os.path.join('Model','kidney_disease_ab1_model.sav')    
        model = pickle.load(open(model_path, 'rb'))
        log.log(f'sucessfully read the model in path {str(model_path)}','kidney_disease_prediction.log',1)    
    except Exception as e:
        try:
            log.log(f'Could not read the model in path {str(model_path)} error {str(e)}','kidney_disease_prediction.log',3) 
        except Exception as NameError:
            log.log(f'{str(NameError)} occured while reading the model path error {str(e)}','kidney_disease_prediction.log',3) 
    try:     
        pc_=request.form['pc']
        if pc_=='normal':
            pc_normal=1
            pc_nan=0
        elif pc_=='nan':
            pc_normal=0
            pc_nan=1
        else:
            pc_normal=0
            pc_nan=0
        pcc_=request.form['pcc']
        if pcc_=='present':
            pcc_present=1
        else:
            pcc_present=0
        ba_=request.form['ba']
        if ba_=='present':
            ba_present=1
        else:
            ba_present=0    
        htn_=request.form['htn']
        if htn_=='yes':
            htn_yes=1
        else:
            htn_yes=0
        dm_=request.form['dm']
        if dm_=='yes':
            dm_no=0
            dm_yes=1
        else:
            dm_no=0
            dm_yes=0

        cad_=request.form['cad']
        if cad_=='yes':
            cad_yes=1
        else:
            cad_yes=0
        appet_=request.form['appet']
        if appet_=='poor':
            appet_poor=1
        else:
            appet_poor=0
        pe_=request.form['pe']
        if pe_=='yes':
            pe_yes=1
        else:
            pe_yes=0
        ane_=request.form['ane']
        if ane_=='yes':
            ane_yes=1
        else:
            ane_yes=0
        rbc_=request.form['rbc']
        if rbc_=='normal':
            rbc_normal=1
            rbc_nan=0
        elif rbc_=='nan':
            rbc_normal=0
            rbc_nan=1
        else:
            rbc_normal=0
            rbc_nan=0
        X=pd.DataFrame([[age, bp, sg, al, su, bgr, bu, sc, sod, pot, hemo,pcv, wc, rc, rbc_normal, rbc_nan, pc_normal, pc_nan,pcc_present, ba_present, htn_yes, dm_no, dm_yes, cad_yes,appet_poor, pe_yes, ane_yes]],columns=['age', 'bp', 'sg', 'al', 'su', 'bgr', 'bu', 'sc', 'sod', 'pot', 'hemo','pcv', 'wc', 'rc', 'rbc_normal', 'rbc_nan', 'pc_normal', 'pc_nan','pcc_present', 'ba_present', 'htn_yes', 'dm_no', 'dm_yes', 'cad_yes','appet_poor', 'pe_yes', 'ane_yes'])

        X_col=X.columns[[ True,  True, False,  True, False,  True,  True,  True,  True,True,  True,  True,True,  True,  True,  True,  True, False,False, False,  True, False,  True,  True, False, False,True]]
        output=model.predict(X[X_col])
        log.log(f'kidney_disease_pred funtion run sucessfully','kidney_disease_prediction.log',1)    
    except Exception as e:
        log.log(f'Could not run kidney_disease_pred funtion sucessfully error {str(e)}','kidney_disease_prediction.log',3)    
    return output