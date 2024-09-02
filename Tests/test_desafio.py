import pandas as pd
import pytest
from desafio import data_preprocessing
import numpy as np

@pytest.fixture(name = 'result')
def result():
    input_data = 'data/exercise_results_labelled.csv'
    data_preprocessing(input_data)
    result = pd.read_csv("data/result.csv").sort_values('session_group').reset_index(drop=True)
    return result

@pytest.fixture(name = 'benchmark')
def benchmark():
    result = pd.read_csv("data/session_results_labelled.csv").sort_values('session_group').reset_index(drop=True)
    return result

class TestDataPreprocessing:

    def test_if_columns_missing(self, result, benchmark):
        missing_columns = [col for col in benchmark.columns if col not in result.columns]
        assert not missing_columns, f"{', '.join(missing_columns)} missing from result"
        print("No columns are missing in result")

    def test_compare_common_columns(self, result, benchmark):
        diff_columns = []
        for col in result.columns:
            if not result[col].equals(benchmark[col]):
                diff_lines = np.sum(result[col] != benchmark[col])
                diff_columns.append((col, diff_lines))
        assert(not diff_columns), f"Columns with differences: {diff_columns}, {len(diff_columns)} columns out of a possible {len(result.columns)} columns"
        


