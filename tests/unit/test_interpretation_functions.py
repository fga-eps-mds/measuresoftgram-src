from src.core.interpretation_functions import non_complex_files_density, commented_files_density, absence_duplications
from src.core.exceptions import InvalidMetricValue, InvalidInterpretationFunctionArguments
from tests.test_helpers import create_file_df
import pandas as pd
from glob import glob
import pytest


INVALID_METRICS_TEST_DATA = [
    (non_complex_files_density, 'tests/unit/data/zero_number_of_files.json', 'The number of files is lesser or equal than 0'),
    (non_complex_files_density, 'tests/unit/data/zero_number_of_functions.json',
     'The number of functions of all files is lesser or equal than 0'),
    (non_complex_files_density, 'tests/unit/data/zero_cyclomatic_complexity.json',
     'The cyclomatic complexity of all files is lesser or equal than 0'),
    (commented_files_density, 'tests/unit/data/zero_number_of_files.json',
     'The number of files is lesser or equal than 0'),
    (absence_duplications, 'tests/unit/data/zero_number_of_files.json',
     'The number of files is lesser or equal than 0'),
]


SUCCESS_TEST_DATA = [
    (non_complex_files_density, 'tests/unit/data/fga-eps-mds_2021-2-SiGeD-Frontend-03-15-2022-23_57_08.json', 0.688622754491018),
    (non_complex_files_density, 'tests/unit/data/fga-eps-mds-2020_2-Projeto-Kokama-Usuario-17-04-2021.json', 1.0),
    (non_complex_files_density, 'tests/unit/data/fga-eps-mds-2020_2-Lend.it-Raleway-user-13-04-2021.json', 0.6428571428571429),
    (commented_files_density, 'tests/unit/data/fga-eps-mds-2020_2-Projeto-Kokama-Usuario-17-04-2021.json', 0.0),
    (commented_files_density, 'tests/unit/data/fga-eps-mds_2021-2-SiGeD-Frontend-03-15-2022-23_57_08.json', 0.005988023952095809),
    (commented_files_density, 'tests/unit/data/fga-eps-mds-2020_2-Lend.it-Raleway-user-13-04-2021.json', 0.0),
    (absence_duplications, 'tests/unit/data/fga-eps-mds_2021-2-SiGeD-Frontend-03-15-2022-23_57_08.json', 0.9101796407185628),
    (absence_duplications, 'tests/unit/data/fga-eps-mds-2020_2-Projeto-Kokama-Usuario-17-04-2021.json', 1.0),
    (absence_duplications, 'tests/unit/data/fga-eps-mds-2020_2-Lend.it-Raleway-user-13-04-2021.json', 1.0)
]


INVALID_ARGUMENTS_TEST_DATA = [
    (non_complex_files_density, None),
    (non_complex_files_density, False),
    (non_complex_files_density, pd.Series(data={'a': 1, 'b': 2, 'c': 3}, index=['a', 'b', 'c'])),
    (commented_files_density, None),
    (commented_files_density, False),
    (commented_files_density, pd.Series(data={'a': 1, 'b': 2, 'c': 3}, index=['a', 'b', 'c'])),
    (absence_duplications, None),
    (absence_duplications, False),
    (absence_duplications, pd.Series(data={'a': 1, 'b': 2, 'c': 3}, index=['a', 'b', 'c']))
]


@pytest.mark.parametrize("interpretation_func,file_path,error_msg", INVALID_METRICS_TEST_DATA)
def test_interpretation_functions_invalid_metrics(interpretation_func, file_path, error_msg):
    json = glob(file_path)

    with pytest.raises(InvalidMetricValue) as error:
        interpretation_func(create_file_df(json))

    assert str(
        error.value) == error_msg, f"Expected: {interpretation_func.__name__}(create_file_df('{file_path.split('/')[-1]}')) to raise an InvalidMetricValue('{error_msg}')"


@pytest.mark.parametrize("interpretation_func,file_path,expected_result", SUCCESS_TEST_DATA)
def test_interpretation_functions_success(interpretation_func, file_path, expected_result):
    json = glob(file_path)

    result = interpretation_func(create_file_df(json))

    assert result == expected_result, f"Expected: {interpretation_func.__name__}(create_file_df('{file_path.split('/')[-1]}')) == {expected_result}"
    assert 0 <= result <= 1.0, f"Expected: 0 <= {interpretation_func.__name__}(create_file_df('{file_path.split('/')[-1]}')) <= 1.0"


@pytest.mark.parametrize("interpretation_func,data_frame", INVALID_ARGUMENTS_TEST_DATA)
def test_non_complex_files_density_error_arguments(interpretation_func, data_frame):

    with pytest.raises(InvalidInterpretationFunctionArguments) as error:
        interpretation_func(data_frame)

    str_value = 'pd.Series()' if isinstance(data_frame, pd.Series) else data_frame

    assert str(error.value) == 'Expected data_frame to be a pandas.DataFrame', f"Expected: {interpretation_func.__name__}({str_value}) to raise an InvalidInterpretationFunctionArguments"
