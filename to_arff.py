import os
import pandas as pd
import numpy as np
import re


def data_chunk_func(df, window_size, detect_period, attack_standard_idx, tx, rx):
    feature_cols = [
        # 'Time', 'Mote', 'Seq', 'Version',
        'Rank',
        'DIS-UR', 'DIS-MR', 'DIS-US', 'DIS-MS',
        'DIO-UR', 'DIO-MR', 'DIO-US', 'DIO-MS',
        'DAO-R', 'DAO-S', 'DAOA-R', 'DAOA-S', 'dio_intcurrent', 'dio_counter']
    # ['Time', 'Mote', 'Seq', 'Rank', 'Version', 'DIS-R', 'DIS-S', 'DIO-R', 'DIO-S', 'DAO-R', 'RPL-total-sent']
    meta_cols = ['tx', 'rx', 'Attack']

    # Feature engineering and data chunking

    df_split = [None] * len(df.index)
    datas = []
    for row_idx in range(0, len(df.index)-window_size, detect_period):
        df_perrow = []
        for d in range(window_size):
            i = row_idx + d
            if df_split[i] is None:
                df_split[i] = df.iloc[i:i+1, :]

            df_el = df_split[i][feature_cols]

            df_el.columns = [idx+str(d) for idx in df_el.columns]
            df_el = df_el.reset_index(drop=True)
            df_perrow.append(df_el)

        df_metadata = pd.DataFrame([[tx, rx, df_split[row_idx + attack_standard_idx]['Attack'].item(),]],
                                   columns=meta_cols)
        df_perrow = pd.concat(df_perrow + [df_metadata], axis=1)
        datas.append(df_perrow)

    return pd.concat(datas)


def to_arff(relation_name, df):
    df = df.astype(str)
    arff_str = f"@relation {relation_name}\n"

    for attribute in df.columns:
        value = f"{{{','.join(np.unique(df[attribute]))}}}" \
            if attribute in ['Mote', 'Attack'] else "numeric"

        arff_str += f"@attribute {attribute} {value}\n"
    arff_str += "\n@data\n"

    for i, row in df.iterrows():
        arff_str += ','.join(row.values) + "\n"
    return arff_str


if __name__ == "__main__":
    csv_dir = "D:/multi-trace/feature_data/flooding/"
    dfs = []
    # attack_types = ["diodrop", "none"]
    attack_types = ["all"]
    window_size = 10  # feature input chunk size
    detect_period = 5  # period to run detection
    attack_standard_idx = 2  # Frame number to define as attack. More sensitive at bigger number.

    csv_files = os.listdir(csv_dir)
    files = []
    if attack_types[0] != "all":
        for csv_file in csv_files:
            for attack_type in attack_types:
                if attack_type in csv_file:
                    files.append(csv_file)
    else:
        files = csv_files

    for file in files:
        file_name = os.path.join(csv_dir, file)
        # file_name = "D:/multi-trace/feature_data/flooding/"\
        #     "diodrop-tx0.80-rx0.90-00001-dt-1670587999643.csv"
        # relation_name = os.path.split(os.path.splitext(file_name)[0])[1]

        df = pd.read_csv(file_name)
        df = df.drop(columns=['Time', 'Mote', 'Seq', 'Version'])

        tx = re.search(r'tx.*?(-|$)', file).group()[2:-1]
        rx = re.search(r'rx.*?(-|$)', file).group()[2:-1]
        df = data_chunk_func(df, window_size, detect_period, attack_standard_idx, tx, rx)
        print(file)
        dfs.append(df)

    relation_name = attack_types[0] + "_" + "-".join(map(str, [window_size, detect_period, attack_standard_idx]))
    arff_str = to_arff(relation_name, pd.concat(dfs))
    with open(relation_name+".arff", "w") as f:
        f.write(arff_str)
