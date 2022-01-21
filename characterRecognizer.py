import math
from dataclasses import dataclass

@dataclass
class CharacterRecognizer:
    filepath: str

    def trace():
        points = []
        # sample points
        length = 10
        for i in range( 720 ):
            x = length * math.cos( math.radians( 360.0/720 * i ) )
            y = length * math.sin( math.radians( 360.0/720 * i ) )
            points.append( [x,y] )

        return points


if __name__ == '__main__':
    cr = CharacterRecognizer
    result = cr.trace()
    print(result)