from datetime import datetime
from enum import IntEnum
from functools import cached_property
from typing import Annotated, Literal

import pandas as pd
from dateutil.relativedelta import relativedelta
from pandas.api import types as ptypes
from pydantic import BaseModel, Field, PositiveInt

from apps.analysis.core import BaseStep, Params, ParamsForm, StepContext, StepError


class DurationUnit(IntEnum):
    minutes = 0
    hours = 1
    days = 2
    weeks = 3
    months = 4
    years = 5

    def delta(self, quantity: int):
        return relativedelta(**{self.name: quantity})


class TimeseriesFilterParams(Params):
    duration_unit: DurationUnit = DurationUnit.months
    duration_value: PositiveInt = 1
    anchor_type: Literal["this", "last"] = "this"
    anchor_point: Annotated[datetime, Field(default_factory=datetime.utcnow)]

    @cached_property
    def range_tuple(self) -> tuple[datetime, datetime]:
        anchor = self.anchor_point
        start = anchor + self.anchor_adjustment()
        if self.anchor_type == "last":
            start -= self.delta()
        return start, start + self.delta()

    @property
    def start(self):
        return self.range_tuple[0]

    @property
    def end(self):
        return self.range_tuple[1]

    def filter(self, date: datetime) -> bool:
        start, end = self.range_tuple
        return start <= date < end

    def delta(self) -> relativedelta:
        return self.duration_unit.delta(self.duration_value)

    def anchor_adjustment(self) -> relativedelta:
        delta = relativedelta(second=0, microsecond=0)
        if self.duration_unit >= DurationUnit.hours:
            delta += relativedelta(minute=0)
        if self.duration_unit >= DurationUnit.days:
            delta += relativedelta(hour=0)

        if self.duration_unit == DurationUnit.weeks:
            return relativedelta(weeks=-1, weekday=0)

        if self.duration_unit >= DurationUnit.months:
            delta += relativedelta(day=1)
        if self.duration_unit >= DurationUnit.years:
            delta += relativedelta(month=1)
        return delta

    def get_form_class(self) -> type[ParamsForm] | None:
        from apps.analysis.steps.forms import TimeseriesFilterForm

        return TimeseriesFilterForm


class TimeseriesStep(BaseStep[pd.DataFrame, pd.DataFrame]):
    input_type = pd.DataFrame
    output_type = pd.DataFrame

    def preflight_check(self, context: StepContext):
        if not ptypes.is_datetime64_any_dtype(context.data.index):
            raise StepError("Dataframe must have a datetime index")


class TimeseriesFilter(TimeseriesStep):
    param_schema = TimeseriesFilterParams
    input_type = pd.DataFrame
    output_type = pd.DataFrame

    def run(self, params: TimeseriesFilterParams, data: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
        self.log.info(f"Initial timeseries data from {data.index.min()} to {data.index.max()} ({len(data)} rows)")
        result = data.loc[params.start : params.end]
        self.log.info(f"Filtered timeseries data from {params.start} to {params.end} ({len(result)} rows)")
        return result, {}
