# point.py


class Point:
    def __init__(self, frac_x: float, frac_y: float):
        """
        Initializing Point python file
        :param frac_x: Fraction x compared to the canvas
        :param frac_y: Fraction y compared to canvas
        """
        self._frac_x = frac_x
        self._frac_y = frac_y

    def frac(self) -> (float, float):
        """
        Return a tuple of fractional coordinates x and y
        :return: A tuple of fractional coordinates x and y
        """
        return self._frac_x, self._frac_y

    def pixel(self, width: int, height: int) -> (int, int):
        """
        Using pixels of the canvas, compute where point is from the fractional coordinates
        :param width: Width of Canvas
        :param height: Height of Canvas
        :return: Tuple of the coordinates of the point of the following canvas
        """
        return int(self._frac_x * width), int(self._frac_y * height)


def from_frac(frac_x: float, frac_y: float) -> Point:
    """
    Return the Point object using fractional x and y coordinates
    :param frac_x: Fractional X coordinates
    :param frac_y: Fractional Y coordinates
    :return: Point object
    """
    return Point(frac_x, frac_y)


def from_pixel(pixel_x: int, pixel_y: int, width: int, height: int) -> Point:
    """
    Using the pixels of the point and the canvas, figure out the fractional coordinates for the Point objects
    :param pixel_x: X pixel coordinates
    :param pixel_y: Y pixel coordinates
    :param width: Width of canvas
    :param height: Height of canvas
    :return: Point object
    """
    return Point(float(pixel_x) / float(width), float(pixel_y) / float(height))
