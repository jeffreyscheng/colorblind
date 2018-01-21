import itertools
from colorsys import rgb_to_hls, hls_to_rgb
from math import sin, cos, atan2, pi


def average_colors(rgb1, rgb2, ratio):
    h1, l1, s1 = rgb_to_hls(rgb1[0] / 255., rgb1[1] / 255., rgb1[2] / 255.)
    h2, l2, s2 = rgb_to_hls(rgb2[0] / 255., rgb2[1] / 255., rgb2[2] / 255.)
    s = 0.5 * (s1 + s2)
    l = 0.5 * (l1 + l2)
    x = ratio * cos(2 * pi * h1) + (1 - ratio) * cos(2 * pi * h2)
    y = ratio * sin(2 * pi * h1) + (1 - ratio) * sin(2 * pi * h2)
    if x != 0.0 or y != 0.0:
        h = atan2(y, x) / (2 * pi)
    else:
        h = 0.0
        s = 0.0
    r, g, b = hls_to_rgb(h, l, s)
    return int(r * 255.), int(g * 255.), int(b * 255.)


class Paint:
    def __init__(self, r, g, b, name=''):
        self.name = name
        self.r = r
        self.g = g
        self.b = b

    def __repr__(self):
        return 'Color ' + self.name + ': ' + str(self.r) + ', ' + str(self.g) + ', ' + str(self.b)

    @staticmethod
    def mix(p1, p2, ratio):
        # power = 1.2
        #
        # def combine(a, b):
        #     return 255 - (((255 - a) ** power * ratio + (255 - b) ** power * (1 - ratio)) / 2) ** (1 / power)
        #     # return a * b / 255
        #
        # return Paint(combine(p1.r, p2.r), combine(p1.g, p2.g), combine(p1.b, p2.b))
        new_rgb = average_colors((p1.r, p1.g, p1.b), (p2.r, p2.g, p2.b), ratio)
        return Paint(*new_rgb)

    @staticmethod
    def __mul__(p1, p2):
        return p1.r * p2.r + p1.g * p2.g + p1.b * p2.b

    @staticmethod
    def __sub__(self, other):
        return ((self.r - other.r) ** 2 + (self.g - other.g) ** 2 + (self.b - other.b) ** 2) ** 0.5


class Palette:
    def __init__(self, paints):
        self.paints = paints
        self.mixes = self.initialize_mixes()

    def make_color(self, color):
        distances = {key: (color - self.mixes[key]) for key in self.mixes}
        return max(distances, key=distances.get)

    def initialize_mixes(self):
        # initialize nd-array of all colors.
        potential_colors = itertools.combinations(self.paints, 5)
        mixes = {}
        for colors in potential_colors:
            print("new set")
            values = itertools.product(range(1, 6), repeat=5)
            for value in values:
                print(value)
                idx = []
                num_seen = 0
                palette = []
                for paint in self.paints:
                    if paint in colors:
                        idx.append(value[num_seen])
                        palette.append((paint, value[num_seen]))
                        num_seen += 1
                    else:
                        idx.append(0)
                palette = sorted(palette, key=lambda tup: tup[1])
                current_color = Paint(255, 255, 255)
                total_units = 0
                palette_key = tuple(palette)
                while palette:
                    latest_color, units = palette.pop()
                    total_units += units
                    current_color = Paint.mix(latest_color, current_color, units / total_units)
                mixes[palette_key] = current_color
        # print(len(mixes))
        # print(mixes)
        return mixes


red = Paint(255, 1, 1)
blue = Paint(1, 1, 255)
green = Paint(1, 255, 1)
black = Paint(0, 0, 0)
white = Paint(255, 255, 255)
yellow = Paint(255, 255, 0)
# yellow test
test_green = Paint.mix(blue, yellow, 0.5)
print(test_green)

# primary_paints = [red, blue, green, black, white]
# Palette(primary_paints).initialize_mixes()
