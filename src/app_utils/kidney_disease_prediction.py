            
from flask import request
import pickle
import os
import pandas as pd
def kidney_disease_pred(age, bp, sg, al, su, bgr, bu, sc, sod, pot, hemo,pcv, wc, rc):    
    model = pickle.load(open(os.path.join('Model','kidney_disease_ab1_model.sav'), 'rb'))        
    pc_=request.form['pc']
    print(pc_,'.....................')
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
    return output