import numpy  as np
import pandas as pd

from xmlot.data.scale import *
from xmlot.data.describe    import Entry, Descriptor
from xmlot.data.dataframes    import build_survival_accessor

_ = build_survival_accessor(event="c", duration="t", accessor_code="test_surv")

DF = pd.DataFrame({
    "x1": [4., 2.],
    "x2": [50., 100.],
    "c" : [1, 0],
    "t" : [10., 20.]
})

DESCRIPTOR = Descriptor({
    Entry(
        "x1",
        is_categorical=False
    ),
    Entry(
        "x2",
        is_categorical=False
    ),
    Entry(
        "c",
        is_categorical=True
    ),
    Entry(
        "t",
        is_categorical=False
    )
})

class FakeOHE:
    def __init__(self, descriptor):
        self.descriptor = descriptor
        self.separator  = "#"


OHE = FakeOHE(DESCRIPTOR)


def test_nothing():
    scaler = Scaler(
        DF,
        accessor_code="test_surv",
        ohe=OHE
    )
    untransformed_df = scaler(DF)

    assert untransformed_df.equals(DF)

def test_standardisation():
    s = np.sqrt(1 / 2)
    df_ = pd.DataFrame(
        {
            "x1": [s  , -s ],
            "x2": [-s , s  ],
            "c" : [1  , 0  ],
            "t" : [10., 20.]
        }
    )

    standardiser = Scaler(
        DF,
        "test_surv",
        OHE,
        **get_standardisation(DF)
    )
    standardised_df = standardiser(DF)

    decimals = 15  # floats are badly handled, so we can't use `equals`.

    assert standardised_df.round(decimals).equals(df_.round(decimals))                                        \
           and getattr(standardised_df, "test_surv").event    == getattr(df_, "test_surv").event    \
           and getattr(standardised_df, "test_surv").duration == getattr(df_, "test_surv").duration


def test_normalisation():
    df_ = pd.DataFrame(
        {
            "x1": [1. , 0. ],
            "x2": [0. , 1. ],
            "c" : [1  , 0  ],
            "t" : [10., 20.]
        }
    )

    normaliser = Scaler(
        DF,
        "test_surv",
        OHE,
        **get_normalisation(DF)
    )
    normalised_df = normaliser(DF)

    assert normalised_df.equals(df_)
