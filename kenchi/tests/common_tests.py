import unittest

import numpy as np
from matplotlib.axes import Axes
from kenchi.datasets import make_blobs
from sklearn.base import BaseEstimator
from sklearn.exceptions import NotFittedError
from sklearn.utils.estimator_checks import check_estimator


class ModelTestMixin:
    def test_score(self):
        self.sut.fit(self.X_train)

        score = self.sut.score(self.X_test)

        self.assertIsInstance(score, float)

    def test_score_notfitted(self):
        self.assertRaises(NotFittedError, self.sut.score, self.X_test)


class OutlierDetectorTestMixin:
    def prepare_data(self):
        n_features        = 2
        centers           = np.zeros((1, n_features))

        X_train, y_train  = make_blobs(
            centers       = centers,
            contamination = 0.01,
            n_features    = n_features,
            n_samples     = 100,
            random_state  = 0
        )

        X_test, y_test    = make_blobs(
            centers       = centers,
            contamination = 0.1,
            n_features    = n_features,
            n_samples     = 100,
            random_state  = 1
        )

        return X_train, X_test, y_train, y_test

    @unittest.skip('this test fail in scikit-larn 0.19.1')
    def test_check_estimator(self):
        self.assertIsNone(check_estimator(self.sut))

    def test_fit_predict(self):
        y_pred = self.sut.fit_predict(self.X_train)

        self.assertEqual(self.y_train.shape, y_pred.shape)

    def test_fit(self):
        self.assertIsInstance(self.sut.fit(self.X_train), BaseEstimator)

    def test_predict(self):
        if hasattr(self.sut, 'novelty'):
            self.sut.set_params(novelty=True)

        self.sut.fit(self.X_train)

        y_pred = self.sut.predict(self.X_test)

        self.assertEqual(self.y_test.shape, y_pred.shape)

    def test_decision_function(self):
        if hasattr(self.sut, 'novelty'):
            self.sut.set_params(novelty=True)

        self.sut.fit(self.X_train)

        y_score = self.sut.decision_function(self.X_test)

        self.assertEqual(self.y_test.shape, y_score.shape)

    def test_score_samples(self):
        if hasattr(self.sut, 'novelty'):
            self.sut.set_params(novelty=True)

        self.sut.fit(self.X_train)

        score_samples = self.sut.score_samples(self.X_test)

        self.assertEqual(self.y_test.shape, score_samples.shape)

    def test_anomaly_score(self):
        if hasattr(self.sut, 'novelty'):
            self.sut.set_params(novelty=True)

        self.sut.fit(self.X_train)

        anomaly_score = self.sut.anomaly_score(self.X_test)

        self.assertEqual(self.y_test.shape, anomaly_score.shape)

    def test_plot_anomaly_score(self):
        if hasattr(self.sut, 'novelty'):
            self.sut.set_params(novelty=True)

        self.sut.fit(self.X_train)

        ax = self.sut.plot_anomaly_score(self.X_test)

        self.assertIsInstance(ax, Axes)

    def test_plot_roc_curve(self):
        if hasattr(self.sut, 'novelty'):
            self.sut.set_params(novelty=True)

        self.sut.fit(self.X_train)

        ax = self.sut.plot_roc_curve(self.X_test, self.y_test)

        self.assertIsInstance(ax, Axes)

    def test_predict_notffied(self):
        self.assertRaises(NotFittedError, self.sut.predict, self.X_test)

    def test_decision_function_notffied(self):
        self.assertRaises(
            NotFittedError, self.sut.decision_function, self.X_test
        )

    def test_score_samples_notfitted(self):
        self.assertRaises(NotFittedError, self.sut.score_samples, self.X_test)

    def test_anomaly_score_notfitted(self):
        self.assertRaises(NotFittedError, self.sut.anomaly_score, self.X_test)

    def test_plot_anomaly_score_notfitted(self):
        self.assertRaises(
            NotFittedError, self.sut.plot_anomaly_score, self.X_test
        )

    def test_plot_roc_curve_notfitted(self):
        self.assertRaises(
            NotFittedError, self.sut.plot_roc_curve, self.X_test, self.y_test
        )