from typing import Union
from bidict import bidict


class WeatherCondition:
    CLOUDNESS = 0
    PRECIPITATION = 1
    PRECIPITATION_TYPE = 2

    CLOUDNESS_VALUES = bidict(
        {
            0: "clear",
            1: "partly",
            2: "half",
            3: "broken",
            4: "overcast",
            5: "fog",
        }
    )

    PRECIPITATION_VALUES = bidict(
        {0: "no", 1: "slight", 2: "shower", 3: "precipitation", 4: "thunder"}
    )

    PRECIPITATION_TYPE_VALUES = bidict({0: "rain", 1: "sleet", 2: "snow"})

    def __init__(
        self,
        cloudness: Union[int, str],
        precipitation: Union[int, str],
        precipitation_type: Union[int, str],
    ):
        self._cloudness = self._transform_to_int(cloudness, self.CLOUDNESS)
        self._precipitation = self._transform_to_int(precipitation, self.PRECIPITATION)
        self._precipitation_type = self._transform_to_int(
            precipitation_type, self.PRECIPITATION_TYPE
        )

    @property
    def cloudness(self) -> int:
        return self._cloudness

    @property
    def precipitation(self) -> int:
        return self._precipitation

    @property
    def precipitation_type(self) -> int:
        return self._precipitation_type

    @staticmethod
    def _transform_to_int(value: Union[str, int], type: int) -> int:
        if type == WeatherCondition.CLOUDNESS:
            values = WeatherCondition.CLOUDNESS_VALUES
        elif type == WeatherCondition.PRECIPITATION:
            values = WeatherCondition.PRECIPITATION_VALUES
        elif type == WeatherCondition.PRECIPITATION_TYPE:
            values = WeatherCondition.PRECIPITATION_TYPE_VALUES
        else:
            raise ValueError("Invalid number")
        if isinstance(value, str):
            if value in values:
                return values[value]
            else:
                raise ValueError(f"Invalid cloudness value '{value}'")
        else:
            if not (0 <= value < len(values)):
                raise ValueError("Out of bounds value")
            return value

    def __int__(self):
        return self.CLOUDNESS * 100 + self.PRECIPITATION * 10 + self.PRECIPITATION_TYPE

    @classmethod
    def from_int(cls, integer: int) -> "WeatherCondition":
        cloudness = integer % 10
        integer //= 10
        precipitation = integer % 10
        integer //= 10
        precipitation_type = integer % 10
        return cls(cloudness, precipitation, precipitation_type)

    def __repr__(self):
        return "{},{},{}".format(
            self.transform(self.cloudness, self.CLOUDNESS),
            self.transform(self.precipitation, self.PRECIPITATION),
            self.transform(self.precipitation_type, self.PRECIPITATION_TYPE),
        )

    @staticmethod
    def transform(value: Union[str, int], type: int) -> Union[str, int]:
        if type == WeatherCondition.CLOUDNESS:
            return WeatherCondition.CLOUDNESS_VALUES.get(value, 0)
        elif type == WeatherCondition.PRECIPITATION:
            return WeatherCondition.PRECIPITATION_VALUES.get(value, 0)
        elif type == WeatherCondition.PRECIPITATION_TYPE:
            return WeatherCondition.PRECIPITATION_TYPE_VALUES.get(value, 0)
