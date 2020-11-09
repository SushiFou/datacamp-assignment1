# noqa: D100
import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.validation import check_X_y, check_is_fitted
from sklearn.utils.validation import check_array
from sklearn.metrics.pairwise import euclidean_distances


class OneNearestNeighbor(BaseEstimator, ClassifierMixin):
    """One Nearest Neighbor Classifier  - Scikit Learn API.

    Author :  Yann KERVELLA
    """

    def __init__(self):  # noqa: D107
        pass

    def nearest_neighbor_index(self, data):
        """Utility function to find the nearest datapoint in the training
        predictors.

        Parameters
        ----------
        self : OneNearestNeihbor() Model
        data : ndarray of shape (n_features) - a sample of data

        Returns
        -------
        index : Index of the nearest data point
        """
        dist = euclidean_distances(self.X_, [data])
        return np.argmin(dist)

    def fit(self, X, y):
        """Fit function of our One nearest neighbor model.

        Parameters
        ----------
        X : ndarray of training predictors (n_samples, n_features)
        y : ndarray of training target values (n_samples)

        Returns
        -------
        self : OneNearestNeighbor() class

        Raises
        ------
        ValueError
            Maximum number of classes has been reached,
             are you sure it is not regression problem?
        """
        X, y = check_X_y(X, y)
        self.classes_ = np.unique(y)
        if len(self.classes_) > 50:
            raise ValueError("Maximum number of classes has been reached,"
                             " are you sure it is not regression problem ?")
        else:
            # Model fitting
            self.X_ = X
            self.y_ = y

        return self

    def predict(self, X):
        """Predict function of our One nearest neighbor model.

        Parameters
        ----------
        X : ndarray of test predictors (n_samples, n_features)

        Returns
        -------
        y_pred = ndarray the predicted values (n_samples)
        """
        check_is_fitted(self)
        X = check_array(X)
        y_pred = np.full(shape=len(X), fill_value=self.classes_[0])
        if y_pred.dtype == '<U3':
            y_pred = y_pred.astype('<U5')
        for i in range(0, len(X)):
            y_pred[i] = self.y_[self.nearest_neighbor_index(X[i])]

        return y_pred

    def score(self, X, y):
        """Score function of our One nearest neighbor model.

        Parameters
        ----------
        X : ndarray of test predictors (n_samples, n_features)
        y : ndarray of test target values (n_samples)

        Returns
        -------
        The accuracy of the predictions using a mean function.
        """
        X, y = check_X_y(X, y)
        y_pred = self.predict(X)
        return np.mean(y_pred == y)
