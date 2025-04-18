import sys


class Radii:
    xs: int = 2
    sm: int = 4
    md: int = 6
    lg: int = 8
    xl: int = 12
    xxl: int = 16
    none: int = 0
    full: int = sys.maxsize

    @staticmethod
    def get_radii_x_xl(size: int) -> int:
        return Radii.xl * size
