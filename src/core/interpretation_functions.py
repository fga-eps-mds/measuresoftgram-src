from .exceptions import InvalidMetricValue, InvalidInterpretationFunctionArguments
import pandas as pd
import numpy as np


def check_arguments(data_frame):
    if not isinstance(data_frame, pd.DataFrame):
        raise InvalidInterpretationFunctionArguments(
            "Expected data_frame to be a pandas.DataFrame"
        )


def check_number_of_files(number_of_files):
    if number_of_files <= 0:
        raise InvalidMetricValue("The number of files is lesser or equal than 0")


def interpolate_series(series, x, y):
    """
    Interpolates a series using the given x and y values.

    This function interpolates a series using the given x and y values.
    """

    return [np.interp(item / 100, x, y) for item in series]


def create_coordinate_pair(min_threshhold, max_threshold):
    """
    Creates a pair of values.

    This function creates a pair of coordinates (x, y).
    """

    return np.array([min_threshhold, max_threshold]), np.array([1, 0])


def non_complex_files_density(data_frame):
    """
    Calculates non-complex files density (m1).

    This function calculates non-complex files density measure (m1)
    used to assess the changeability quality subcharacteristic.
    """

    check_arguments(data_frame)

    # files_complexity = m1 metric
    files_complexity = data_frame["complexity"].astype(float)
    # files_functions = m2 metric
    files_functions = data_frame["functions"].astype(float)
    # number_of_files = m3 metric
    number_of_files = len(data_frame)

    check_number_of_files(number_of_files)

    if files_complexity.sum() <= 0:
        raise InvalidMetricValue(
            "The cyclomatic complexity of all files is lesser or equal than 0"
        )

    if files_functions.sum() <= 0:
        raise InvalidMetricValue(
            "The number of functions of all files is lesser or equal than 0"
        )

    # m0 =
    m0 = np.median(files_complexity / files_functions)

    x, y = create_coordinate_pair(0, m0)

    files_in_thresholds_df = (files_complexity / files_functions) <= m0

    IF1 = np.interp(list(files_in_thresholds_df[(files_functions > 0)]), x, y)

    return sum(IF1) / number_of_files


def commented_files_density(data_frame):
    """
    Calculates commented files density (m2).

    This function calculates commented files density measure (m2)
    used to assess the changeability quality subcharacteristic.
    """

    MINIMUM_COMMENT_DENSITY_THRESHOLD = 10
    MAXIMUM_COMMENT_DENSITY_THRESHOLD = 30

    check_arguments(data_frame)

    # number_of_files = m3 metric
    number_of_files = len(data_frame)
    # files_comment_lines_density = m4 metric
    files_comment_lines_density = data_frame["comment_lines_density"].astype(
        float
    )  # m4

    check_number_of_files(number_of_files)

    if files_comment_lines_density.sum() < 0:
        raise InvalidMetricValue(
            "The number of files comment lines density is lesser than 0"
        )

    x, y = create_coordinate_pair(
        MINIMUM_COMMENT_DENSITY_THRESHOLD / 100, MAXIMUM_COMMENT_DENSITY_THRESHOLD / 100
    )

    files_between_thresholds = files_comment_lines_density[
        files_comment_lines_density.between(
            MINIMUM_COMMENT_DENSITY_THRESHOLD,
            MAXIMUM_COMMENT_DENSITY_THRESHOLD,
            inclusive="both",
        )
    ]

    em2i = interpolate_series(files_between_thresholds, x, y)

    return np.sum(em2i) / number_of_files


def absence_of_duplications(data_frame):
    """
    Calculates duplicated files absence (m3).

    This function calculates the duplicated files absence measure (m3)
    used to assess the changeability quality subcharacteristic.
    """

    DUPLICATED_LINES_THRESHOLD = 5.0

    check_arguments(data_frame)

    # files_duplicated_lines_density = m5 metric
    files_duplicated_lines_density = data_frame["duplicated_lines_density"].astype(
        float
    )
    # number_of_files = m3 metric
    number_of_files = len(data_frame)

    check_number_of_files(number_of_files)

    if files_duplicated_lines_density.sum() < 0:
        raise InvalidMetricValue(
            "The number of files duplicated lines density is lesser than 0"
        )

    x, y = create_coordinate_pair(0, DUPLICATED_LINES_THRESHOLD / 100)

    files_below_threshold = files_duplicated_lines_density[
        files_duplicated_lines_density < DUPLICATED_LINES_THRESHOLD
    ]

    em2i = interpolate_series(files_below_threshold, x, y)

    return np.sum(em2i) / number_of_files
