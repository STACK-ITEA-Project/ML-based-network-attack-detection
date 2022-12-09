import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as pl
from itertools import cycle
import numpy as np


def analysis_data(data_path):

    df_data = pd.read_csv(data_path)

    # print(df_data)
    # -- filter cols
    feature_cols = [
        # 'Time',
        'DIS-UR', 'DIS-MR', 'DIS-US', 'DIS-MS',
        'DIO-UR', 'DIO-MR', 'DIO-US', 'DIO-MS',
        # 'DAO-R', 'DAO-S', 'DAOA-R', 'DAOA-S',
        'dio_intcurrent',
        # 'dio_counter',
                    ]

    # [
    #     # 'Time',
    #     'Mote',
    #     # 'Seq', 'Rank',
    #     'DIS-R', 'DIS-S', 'DIO-R', 'DIO-S', 'DAO-R',
    #     # 'RPL-total-sent'
    #     ]
    cols = []
    for c in df_data.columns:
        for fc in feature_cols:
            if fc in c:
                cols.append(c)

    # -- filter rows
    trxrs = [0.7, 0.8, 0.9, 1.0]
    df_data = df_data[np.isin(df_data['Trxr'], trxrs)]
    # df_data = df_data[np.isin(df_data['Attack'], ['No', "dio-drop"])]

    # -- get data
    X = df_data[cols]
    Y = df_data['Attack']

    # -- PCA
    pca_n_comp = 2  # pca dimension (2 or 3)
    pca = PCA(n_components=pca_n_comp, whiten=True).fit(X)
    X_pca = pca.transform(X)
    print('explained variance ratio:', pca.explained_variance_ratio_)
    print('Preserved Variance:', sum(pca.explained_variance_ratio_))
    # pcacol = [[f'pca {i+1}' for i in range(pca_n_comp)]]
    # principalDf = pd.DataFrame(data = X_pca, columns = pcacol)

    colors = cycle('rgb')
    target_names = np.unique(Y)
    if True:
        fg = pl.figure(figsize=(16, 9))
        for fi, trxr in enumerate(trxrs):
            print(fi, trxr)
            ax = fg.add_subplot(2, 2, fi + 1)

            tix = df_data['Trxr'] == trxr
            target_list = np.array(Y[tix]).flatten()
            _X_pca = X_pca[tix]
            for t_name, c in zip(target_names, colors):
                ax.scatter(_X_pca[target_list == t_name, 0], _X_pca[target_list == t_name, 1],
                           c=c, label=t_name, s=2)
            ax.legend(target_names)
            ax.set_xlabel('pca 1')
            ax.set_ylabel('pca 2')
            ax.set_title(trxr)

    else:
        fg = pl.figure()
        ax = fg.add_subplot(projection='3d') if pca_n_comp == 3 else fg.add_subplot()

        target_list = np.array(Y).flatten()
        for t_name, c in zip(target_names, colors):
            if pca_n_comp == 2:
                ax.scatter(X_pca[target_list == t_name, 0], X_pca[target_list == t_name, 1],
                           c=c, label=t_name, s=2)
            elif pca_n_comp == 3:
                ax.scatter(X_pca[target_list == t_name, 0], X_pca[target_list == t_name, 1],
                           X_pca[target_list == t_name, 2], c=c, label=t_name)
        ax.legend(target_names)
        ax.set_xlabel('pca 1')
        ax.set_ylabel('pca 2')
        if pca_n_comp == 3:
            ax.set_zlabel('pca 3')

    # pl.show()
    pl.suptitle(data_path.replace(".csv", ""))
    pl.tight_layout()
    pl.savefig(data_path.replace(".csv", ".png"))

    return X, Y
