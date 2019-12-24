from PIL import Image
import calculator, os
from multiprocessing import pool

def calculatexyt(globe, x, y, w, h, t, a):
    fraction = globe.calculatePoint(timeOfDay = x/w - 0.25, latitude = 2 * y/h - 1, inclination=4/9, timeOfYear=t/a)
    return t, x, y , int((fraction)*255),0,0,int(fraction*128)+127


if __name__ == "__main__":
    P = pool.Pool(processes=12)
    width, height = 320, 320
    globe = calculator.Globe(False)
    points = [(globe, x, y, width, height, t, 8) for t in range(8) for x in range(width) for y in range(height)]
    data = P.starmap(calculatexyt, points)
    P.terminate()
    print("c")
    im, px = {}, {}
    for t in range(8):
        im[t] = Image.new("RGBA",(width, height))
        px[t] = im[t].load()
    for item in data:
        t, x, y, *color = item
        color = tuple(color)
        px[t][x,y] = color
    for t in range(8):
        im[t].save(f"year/result{t}.png")
    print("d")
    exit()
