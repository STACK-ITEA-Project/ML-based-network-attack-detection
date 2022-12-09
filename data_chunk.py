import argparse
import glob
import os
import re
import pandas as pd
import numpy as np

def data_chunk_func(simul_dirs):

    window_size = 10 # feature input chunk size
    detect_period = 5 # period to run detection
    attack_standard_idx = 2 # attack이라고 판단할 frame 번호. 숫자 클수록 빠르게 반응

    feature_cols = ['Time', 'Mote', 
                        'Seq', 'Rank', 'Version', 
                        'DIS-UR', 'DIS-MR', 'DIS-US', 'DIS-MS', 
                        'DIO-UR', 'DIO-MR', 'DIO-US', 'DIO-MS', 
                        'DAO-R', 'DAO-S', 'DAOA-R', 'DAOA-S', 'dio_intcurrent','dio_counter']
    #['Time', 'Mote', 'Seq', 'Rank', 'Version', 'DIS-R', 'DIS-S', 'DIO-R', 'DIO-S', 'DAO-R', 'RPL-total-sent']
    meta_cols = ['Attack', 'Trxr']


    # Feature engineering and data chunking
    all_data, all_metadata = [], []
    for si, simul_dir in enumerate(simul_dirs):
        print(si+1, len(simul_dirs))
        df = pd.read_csv(f'{simul_dir}/rpl-statistics.csv')
        
        # Get configs from simul name
        m = re.search(r'trxr.*?(-|$)', simul_dir)
        cfg_trxr = m.group().split("_")[1][:-1]
        
        # Permote processing
        # if conopts.permote:
        #     permote_col = ['Time',
        #                 'DIS-UR', 'DIS-MR', 'DIS-US', 'DIS-MS', 
        #                 'DIO-UR', 'DIO-MR', 'DIO-US', 'DIO-MS', 
        #                 'DAO-R', 'DAO-S', 'DAOA-R', 'DAOA-S', 'dio_intcurrent','dio_counter']
        #     # ['Time', 'DIS-R', 'DIS-S', 'DIO-R', 'DIO-S', 'DAO-R', 'RPL-total-sent']
        #     for moteIdx in np.unique(df['Mote']):
        #         _df_mote = df[df['Mote'] == moteIdx]
        #         df_mote = _df_mote.copy()
        #         for rowIdx in range(len(df_mote.index)):
        #             if rowIdx != 0:
        #                 for col in permote_col:
        #                     df_mote[col].iloc[rowIdx] = _df_mote[col].iloc[rowIdx] - _df_mote[col].iloc[rowIdx -1]
                
        #         df[df['Mote'] == moteIdx] = df_mote
            
        df_split = [None] * len(df.index)
        datas = []
        for row_idx in range(0, len(df.index)-window_size, detect_period):
            df_perrow = []
            time_base = 0
            for d in range(window_size):
                i = row_idx + d
                if df_split[i] is None:
                    df_split[i] = df.iloc[i:i+1, :]
                
                df_el = df_split[i][feature_cols]
                
                df_el.columns = [idx+str(d) for idx in df_el.columns]
                df_el = df_el.reset_index(drop=True)
                df_perrow.append(df_el)
                
                # if d == 0:
                #     time_base = df_el['Time0'].iloc[0]
                # df_el['Time'+str(d)] -= time_base
                
            
            df_metadata = pd.DataFrame([[df_split[row_idx + attack_standard_idx]['Attack'].item(), cfg_trxr]], columns=meta_cols)
            df_perrow = pd.concat(df_perrow + [df_metadata], axis=1)
            datas.append(df_perrow)
        
        all_data.append(pd.concat(datas))

    df_data = pd.concat(all_data)
    # csv_path = f"{simul_dir}/../data-ws{window_size}-dp{detect_period}-asi{attack_standard_idx}{'-pm' if conopts.permote else ''}.csv"
    csv_path = f"{simul_dir}/../data-ws{window_size}-dp{detect_period}-asi{attack_standard_idx}.csv"
    df_data.to_csv(csv_path)

    print("Data process fin")
    df_data = pd.read_csv(csv_path)

    return csv_path
    
