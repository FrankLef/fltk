import pandas as pd
from collections import Counter
from sklearn.preprocessing import MinMaxScaler
from typing import Final



class FeatureCleaner:
    def __init__(
        self,
        data: pd.DataFrame,
        null_cut: float = 0.8,
        near_zero_cut: float = 0.01,
        freq_cut: float = 90 / 10,
        uniq_cut: float = 0.1,
    ):
        self._data = data
        self._null_cut = self._check_rate(rate=null_cut, name="null_cut")
        self._near_zero_cut = self._check_rate(rate=near_zero_cut, name="near_zero_cut")
        self._freq_cut = self._check_freq_cut(freq_cut)
        self._uniq_cut = self._check_rate(rate=uniq_cut, name="uniq_cut")
        self._features_with_many_null: list[str] = []
        self._features_with_near_zero_cv: list[str] = []
        self._features_with_few_values: list[str] = []

    def _check_rate(self, rate: float, name: str) -> float:
        MIN_RATE: Final[float] = 0
        MAX_RATE: Final[float] = 1
        if (rate < MIN_RATE) or (rate > MAX_RATE):
            msg: str = f"The {name} must be between {MIN_RATE} and {MAX_RATE}. It is {rate}."
            raise ValueError(msg)
        return rate

    def _check_freq_cut(self, ratio: float) -> float:
        MIN_RATIO: Final[float] = 1
        if ratio < MIN_RATIO:
            msg: str = f"""
            The frequency cutoff must be >= {MIN_RATIO}. Is is {ratio}.
            For example, you could use freq_cut = 95 / 5.
            """
            raise ValueError(msg)
        return ratio

    @property
    def data(self):
        return self._data

    @property
    def cleaned_data(self):
        return self._cleaned_data

    @property
    def features_with_many_null(self):
        return self._features_with_many_null

    @property
    def features_with_near_zero_cv(self):
        return self._features_with_near_zero_cv

    @property
    def features_with_few_values(self):
        return self._features_with_few_values

    def fit_transform(self, verbose: bool = False) -> None:
        self.fit(verbose=verbose)
        self.transform()

    def fit(self, verbose: bool = False) -> None:
        # self._data_to_clean = self._data
        self._features_with_many_null = self.find_with_many_null()
        self._features_with_near_zero_cv = self.find_near_zero_cv()
        self._features_with_few_values = self.find_with_few_values()
        if verbose:
            cols = {
                "features_with_many_null": self.features_with_many_null,
                "features_with_few_values": self.features_with_few_values,
                "features_with_near_zero_cv": self.features_with_near_zero_cv,
            }
            for key, val in cols.items():
                print(f"{len(val)} {key}:\n", val)

    def transform(self) -> None:
        cols = self._features_with_many_null
        cleaned_data = self._data.drop(columns=cols, errors="ignore")
        cols = self._features_with_near_zero_cv
        cleaned_data.drop(columns=cols, errors="ignore", inplace=True)
        cols = self._features_with_few_values
        cleaned_data.drop(columns=cols, errors="ignore", inplace=True)
        self._cleaned_data = cleaned_data

    def find_with_many_null(self) -> list[str]:
        data = self._data
        selected_features: list[str] = [
            col
            for col in data.columns
            if sum(data[col].isnull()) / len(data[col]) >= self._null_cut
        ]
        return selected_features

    def find_near_zero_cv(self) -> list[str]:
        data = self._data
        data_to_clean = data.select_dtypes(include=["int64", "float64"])

        # NOTE: scale the values to ensure the mean is not zero. Unless
        # all values are the same.
        scaler = MinMaxScaler()

        selected_features: list[str] = []
        for col in data_to_clean.columns:
            is_selected: bool = False
            values = data_to_clean[col]

            scaled_values = scaler.fit_transform(values.to_numpy().reshape(-1, 1))
            mn = scaled_values.mean()
            sd = values.std()
            if mn != 0:
                cv = sd / mn
            else:
                # The cv = 0 because all values are the same when scaled data
                # has a mean of zero.
                cv = 0
            is_selected = cv < self._near_zero_cut

            if is_selected:
                selected_features.append(col)

        return selected_features

    def find_with_few_values(self) -> list[str]:
        """Inspired by nearZeroVar from R package caret by Max Khun."""
        data = self._data

        data_to_clean = data.select_dtypes(include=["object"])

        selected_features: list[str] = []
        for col in data_to_clean.columns:
            is_selected: bool = False
            values = data_to_clean[col]
            # values = data[col].dropna(inplace=True)
            values.dropna(inplace=True)
            counts = Counter(values)
            # print(f"{col}:", len(counts))
            if len(counts) >= 2:
                most_common = counts.most_common(2)
                first_frequency = most_common[0][1]
                second_frequency = most_common[1][1]
                if second_frequency > 0:
                    freq_ratio = first_frequency / second_frequency
                    uniq_pct = len(counts) / len(values)
                    # check = {"sfreq_ratio": freq_ratio, "uniq_pct": uniq_pct}
                    # print(f"{col}:", check)
                    is_selected = (freq_ratio > self._freq_cut) and (
                        uniq_pct < self._uniq_cut
                    )
                    # is_selected = (freq_ratio > freq_cut)
                else:
                    msg = f"The second largest frequency is {second_frequency} <= zero!"
                    raise AssertionError(msg)
            else:
                # Select if there is only 1 value or if it is empty.
                is_selected = True
            if is_selected:
                selected_features.append(col)
        return selected_features
