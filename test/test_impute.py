import unittest
import pandas as pd
import numpy as np
from nose.tools import raises

from test.util import assert_frame_equal
from blight_risk_prediction import util


class TestImputationSeries(unittest.TestCase):

    def make_input(self, index, values):
        return pd.Series(values, index=index, name="original")

    def make_expected(self, index, values_expected, imputed_expected):
        values_expected = pd.Series(values_expected, index=index, name="original")
        impute_expected = pd.Series(imputed_expected, index=index, name="imputation_original")
        expected = pd.concat([values_expected, impute_expected], axis=1)
        return expected

    def test_no_impute(self):
        index = ["bla", "blue", "blo"]
        values = [0.2, 0.4, 0.4]

        values_expected = [0.2, 0.4, 0.4]
        impute_expected = [0, 0, 0]
        expected = self.make_expected(index, values_expected, impute_expected)

        actual = util.mean_impute_series(self.make_input(index, values))
        assert_frame_equal(expected, actual)
        
    def test_impute_one(self):
        index = ["bla", "blue", "blo"]
        values = [0.2, np.nan, 0.4]

        values_expected = [0.2, 0.3, 0.4]
        impute_expected = [0, 1, 0]
        expected = self.make_expected(index, values_expected, impute_expected)

        actual = util.mean_impute_series(self.make_input(index, values))
        assert_frame_equal(expected, actual)

    def test_impute_two(self):
        index = ["bla", "blue", "blo"]
        values = [np.nan, np.nan, 0.4]

        values_expected = [0.4, 0.4, 0.4]
        impute_expected = [1, 1, 0]
        expected = self.make_expected(index, values_expected, impute_expected)

        actual = util.mean_impute_series(self.make_input(index, values))
        assert_frame_equal(expected, actual)

    @raises(Exception)
    def test_all_missing(self):
        index = ["bla", "blue", "blo"]
        values = [np.nan, np.nan, np.nan]

        util.mean_impute_series(self.make_input(index, values))


class TestImputationFrame(unittest.TestCase):

    def make_input(self, index, values_list):
        all_series = []
        for i, values in enumerate(values_list):
            all_series.append(pd.Series(values, index=index, name="original{}".format(i)))
        return pd.concat(all_series, axis=1)

    def make_expected(self, index, expected):
        all_series = []
        for i, (values_expected, imputed_expected) in enumerate(expected):
            all_series.append(pd.Series(values_expected, index=index, name="original{}".format(i)))
            if imputed_expected is not None:
                all_series.append(pd.Series(imputed_expected, index=index, name="imputation_original{}".format(i)))
        expected = pd.concat(all_series, axis=1)
        return expected

    def test_no_impute(self):
        index = ["bla", "blue", "blo"]
        values0 = [0.2, 0.4, 0.4]
        values1 = [0.4, 0.8, 0.8]
        values2 = [0.3, 0.0, 0.8]

        expected0 = values0, [0, 0, 0]
        expected1 = values1, [0, 0, 0]
        expected2 = values2, [0, 0, 0]
        expected = self.make_expected(index, [expected0, expected1, expected2])

        actual = util.mean_impute_frame(self.make_input(index, [values0, values1, values2]))
        assert_frame_equal(expected, actual)

    def test_impute_one_series(self):
        index = ["bla", "blue", "blo"]
        values0 = [0.2, 0.4, 0.4]
        values1 = [0.4, np.nan, 0.8]
        values2 = [0.3, 0.0, 0.8]

        expected0 = values0, [0, 0, 0]
        expected1 = [0.4, 0.6, 0.8], [0, 1, 0]
        expected2 = values2, [0, 0, 0]
        expected = self.make_expected(index, [expected0, expected1, expected2])

        actual = util.mean_impute_frame(self.make_input(index, [values0, values1, values2]))
        assert_frame_equal(expected, actual)

    def test_impute_two_series(self):
        index = ["bla", "blue", "blo"]
        values0 = [np.nan, 0.4, np.nan]
        values1 = [0.4, np.nan, 0.8]
        values2 = [0.3, 0.0, 0.8]

        expected0 = [0.4, 0.4, 0.4], [1, 0, 1]
        expected1 = [0.4, 0.6, 0.8], [0, 1, 0]
        expected2 = values2, [0, 0, 0]
        expected = self.make_expected(index, [expected0, expected1, expected2])

        actual = util.mean_impute_frame(self.make_input(index, [values0, values1, values2]))
        assert_frame_equal(expected, actual)

    def test_impute_three_series(self):
        index = ["bla", "blue", "blo"]
        values0 = [np.nan, 0.4, np.nan]
        values1 = [0.4, np.nan, 0.8]
        values2 = [0.3, 0.0, np.nan]

        expected0 = [0.4, 0.4, 0.4], [1, 0, 1]
        expected1 = [0.4, 0.6, 0.8], [0, 1, 0]
        expected2 = [0.3, 0.0, 0.15], [0, 0, 1]
        expected = self.make_expected(index, [expected0, expected1, expected2])

        actual = util.mean_impute_frame(self.make_input(index, [values0, values1, values2]))
        assert_frame_equal(expected, actual)

    @raises(Exception)
    def test_all_missing(self):
        index = ["bla", "blue", "blo"]
        values0 = [np.nan, np.nan, np.nan]
        values1 = [0.4, np.nan, 0.8]
        values2 = [0.3, 0.0, np.nan]

        util.mean_impute_frame(self.make_input(index, [values0, values1, values2]))

    def test_impute_subset(self):
        index = ["bla", "blue", "blo"]
        values0 = [np.nan, 0.4, np.nan]
        values1 = [0.4, np.nan, 0.8]
        values2 = [0.3, 0.0, np.nan]
        subset = ["original2"]

        expected0 = values0, None
        expected1 = values1, None
        expected2 = [0.3, 0.0, 0.15], [0, 0, 1]
        expected = self.make_expected(index, [expected0, expected1, expected2])

        actual = util.mean_impute_frame(self.make_input(index, [values0, values1, values2]), subset=subset)
        assert_frame_equal(expected, actual)

    def test_impute_empty_subset(self):
        index = ["bla", "blue", "blo"]
        values0 = [np.nan, 0.4, np.nan]
        values1 = [0.4, np.nan, 0.8]
        values2 = [0.3, 0.0, np.nan]
        subset = []

        expected0 = values0, None
        expected1 = values1, None
        expected2 = values2, None
        expected = self.make_expected(index, [expected0, expected1, expected2])

        actual = util.mean_impute_frame(self.make_input(index, [values0, values1, values2]), subset=subset)
        assert_frame_equal(expected, actual)

    def test_all_missing_not_in_subset(self):
        index = ["bla", "blue", "blo"]
        values0 = [np.nan, np.nan, np.nan]
        values1 = [0.4, np.nan, 0.8]
        values2 = [0.3, 0.0, np.nan]
        subset = ["original2"]

        expected0 = values0, None
        expected1 = values1, None
        expected2 = [0.3, 0.0, 0.15], [0, 0, 1]
        expected = self.make_expected(index, [expected0, expected1, expected2])

        actual = util.mean_impute_frame(self.make_input(index, [values0, values1, values2]), subset=subset)
        assert_frame_equal(expected, actual)
