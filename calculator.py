import math
from math import pi, sin, cos
from scipy import spatial
import numpy as np

def distanceCubed(*args):
    return sum(map(lambda n: n**2, args))

class location():
    def __init__(self, x, y, z=None):
        self.x, self.y, self.z = x, y, z


    def __getitem__(self, key):
        if key in ["x","y","z"]:
            return getattr(self, key)
        else:
            raise KeyError("non-coordinate key asked from location")

    def __len__ (self):
        return 2 + (self.z != None)

    def __iter__(self):
        if self.z != None:
            return iter([self.x, self.y, self.z])
        else:
            return iter([self.x, self.y])

    def to2D(self):
        self.z = None
        return self
    def to3D(self, z=0):
        self.z = z
        return self





def calculateOnPlane(pos: location):
    deviation = distanceCubed(*pos)
    if deviation <= 1:
        return cos(deviation**0.5 * pi * 0.5)
    return 0

def calculateOnGlobe(pos: location):
    # This code assumes a xy-plane perpendicular to the light source, with
    # the z-axis's positive side facing the light source (negative z is the
    # opposite side of the globe)
    return calculateOnPlane(pos.to2D())

def calculatePoint(timeOfDay = 0, timeOfYear = 0, inclination = 0, latitude = 0, longitude = 0):
    """Calculates the relative amount of light a point on a globe recieves
    on a time of day (0,1) at a time of the year (0,1) on a given latitude
    and longtude (-1,1), on a globe with a specific inclination (0,1)
    """
    # rotation vector:
    # x= cos(pi * timeOfYear * 2) * 0.5 * pi * inclination
    # y= sin(pi * timeOfYear *2) * 0.5* pi * inclination
    # z= 0
    localLongitudeAngle = pi * (longitude + timeOfDay * 2)
    a = cos(pi * latitude * 0.5)
    locVec = np.array([
        a * cos(localLongitudeAngle),
        sin(pi * latitude * 0.5),
        a * sin(localLongitudeAngle) ])
    rotAngle = 0.5 * pi * inclination
    yearPerpAngle = pi * (timeOfYear+0.5) * 2
    rotVec = np.array([cos(yearPerpAngle) * rotAngle, sin(yearPerpAngle) * rotAngle, 0])
    rotationVector = spatial.transform.Rotation.from_rotvec(rotVec)
    rotatedVector = rotationVector.apply(locVec)

    return calculateOnGlobe(location(*rotatedVector))


# globe = Globe()
# print(globe.calculatePointIncl0(0.25,0))
