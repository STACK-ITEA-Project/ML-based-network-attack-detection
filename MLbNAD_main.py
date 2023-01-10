import argparse
import glob
import os
import pandas as pd

import ML
import to_arff
import analysis
import sys

pd.set_option('mode.chained_assignment',  None)
#input : path is to convert CSV_FILES folder (collected rpl-statistics.csv)
parser = argparse.ArgumentParser()
parser.add_argument('input', type=str, nargs="+")
parser.add_argument('--permote', action="store_true")

conopts = parser.parse_args()

if len(conopts.input) == 1 and isinstance(conopts.input, list):
    conopts.input = conopts.input[0]
if sys.platform.startswith("win") and "*" in conopts.input:
    conopts.input = glob.glob(conopts.input)

# Read data
# if not isinstance(conopts.input, list) and conopts.input.endswith(".csv"):
#     assert (os.path.exists(conopts.input))
#     df_data = pd.read_csv(conopts.input)
#     print("Read preprocessed data fin")
# else:
#     if not isinstance(conopts.input, list):
#         conopts.input = [conopts.input]
#     conopts.input = [i for i in conopts.input if os.path.isdir(i)]
#     simul_dirs = conopts.input
#     data_path = data_chunk.datachunk(simul_dirs)

simul_dirs = conopts.input  
csv_dir = to_arff.to_arff_main(simul_dirs)

X, Y = analysis.analysis_data(csv_dir)

ML.run_model(X, Y)
