from enum import Enum


class Direction(Enum):
    N = 1
    S = 2
    W = 3
    E = 4
    NW = 5
    NE = 6
    SW = 7
    SE = 8

    @staticmethod
    def from_degrees(degrees):
        for direction in DIRECTIONS:
            for degrees_range in DIRECTIONS[direction]:
                if degrees_range[0] <= degrees <= degrees_range[1]:
                    return direction


DIRECTIONS = {
    Direction.N: [[345, 375], [-15, 15]],
    Direction.S: [[165, 195]],
    Direction.E: [[75, 105]],
    Direction.W: [[255, 285]],
    Direction.NW: [[286, 344]],
    Direction.SW: [[196, 254]],
    Direction.NE: [[16, 74]],
    Direction.SE: [[106, 164]],
}
