import re
import pandas as pd


def data_chunk_func(df, simul_dir, window_size, detect_period, attack_standard_idx, tx, rx):
    feature_cols = [
        # 'Time', 'Mote', 'Seq', 'Version',
        'Rank',
        'DIS-UR', 'DIS-MR', 'DIS-US', 'DIS-MS',
        'DIO-UR', 'DIO-MR', 'DIO-US', 'DIO-MS',
        'DAO-R', 'DAO-S', 'DAOA-R', 'DAOA-S', 'dio_intcurrent', 'dio_counter']
    # ['Time', 'Mote', 'Seq', 'Rank', 'Version', 'DIS-R', 'DIS-S', 'DIO-R', 'DIO-S', 'DAO-R', 'RPL-total-sent']
    meta_cols = ['tx', 'rx', 'Attack']
    all_data = []
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

    pd.concat(datas)

    all_data.append(pd.concat(datas))

    df_data = pd.concat(all_data)
    # csv_path = \
    #     f"{simul_dir}/../data-ws{window_size}-dp{detect_period}-asi{attack_standard_idx}{'-pm' if conopts.permote \
    # else''}.csv"
    csv_path = f"{simul_dir}/../data-ws{window_size}-dp{detect_period}-asi{attack_standard_idx}.csv"
    df_data.to_csv(csv_path)

    print("Data process fin")
    df_data = pd.read_csv(csv_path)

    return csv_path
