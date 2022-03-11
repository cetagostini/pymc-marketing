import numpy as np
import pytest
from aesara.tensor.var import TensorVariable

from pymmmc.transformers import geometric_adstock, logistic_saturation


def test_geometric_adsstock_output_type():
    x = np.ones(shape=(100))
    y = geometric_adstock(x=x, alpha=1.0)
    assert isinstance(y, TensorVariable)
    assert isinstance(y.eval(), np.ndarray)


def test_geometric_adsstock_alpha_zero():
    x = np.ones(shape=(100))
    y = geometric_adstock(x=x, alpha=0.0)
    np.testing.assert_array_equal(x, y.eval())


def test_geometric_adsstock_x_zero():
    x = np.zeros(shape=(100))
    y = geometric_adstock(x=x, alpha=0.2)
    np.testing.assert_array_equal(x=x, y=y.eval())


@pytest.mark.parametrize(
    "x, alpha, l_max",
    [
        (np.ones(shape=(100)), 0.0, 10),
        (np.ones(shape=(100)), 0.0, 100),
        (np.zeros(shape=(100)), 0.2, 5),
        (np.ones(shape=(100)), 0.5, 7),
        (np.linspace(start=0.0, stop=1.0, num=50), 0.8, 3),
        (np.linspace(start=0.0, stop=1.0, num=50), 0.8, 50),
    ],
)
def test_geometric_adsstock_alpha_non_zero(x, alpha, l_max):
    y = geometric_adstock(x=x, alpha=alpha, l_max=l_max)
    y_np = y.eval()
    assert y_np[0] == x[0]
    assert y_np[1] == x[1] + alpha * x[0]
    assert y_np[2] == x[2] + alpha * x[1] + (alpha**2) * x[0]


def test_logistic_saturation_output_type():
    x = np.ones(shape=(100))
    y = logistic_saturation(x=x, lam=1.0)
    assert isinstance(y, TensorVariable)
    assert isinstance(y.eval(), np.ndarray)


def test_logistic_saturation_lam_zero():
    x = np.ones(shape=(100))
    y = logistic_saturation(x=x, lam=0.0)
    np.testing.assert_array_equal(x=np.zeros(shape=(100)), y=y.eval())


def test_logistic_saturation_lam_one():
    x = np.ones(shape=(100))
    y = logistic_saturation(x=x, lam=1.0)
    np.testing.assert_array_equal(
        x=((1 - np.e ** (-1)) / (1 + np.e ** (-1))) * x, y=y.eval()
    )


@pytest.mark.parametrize(
    "x",
    [
        np.ones(shape=(100)),
        np.linspace(start=0.0, stop=1.0, num=50),
        np.linspace(start=200, stop=1000, num=50),
    ],
)
def test_logistic_saturation_lam_large(x):
    y = logistic_saturation(x=x, lam=1e6)
    assert abs(y.eval()).mean() == pytest.approx(1.0, 1e-1)


@pytest.mark.parametrize(
    "x, lam",
    [
        (np.ones(shape=(100)), 30),
        (np.linspace(start=0.0, stop=1.0, num=50), 90),
        (np.linspace(start=200, stop=1000, num=50), 17),
        (np.zeros(shape=(100)), 200),
    ],
)
def test_logistic_saturation_min_max_value(x, lam):
    y = logistic_saturation(x=x, lam=lam)
    assert y.eval().max() <= 1
    assert y.eval().min() >= 0
