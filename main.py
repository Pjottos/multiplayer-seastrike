import socket

import classes
from exceptions import *

boatNames = ['Mothership', '4hitthingy', 'Submarine', '3hitthingy', 'Minesweeper']

playfield = classes.Grid(0, 10, 10)
enemyfield = classes.Grid(1, 10, 10)

def placeBoats(start=0):
    for i, item in enumerate(boatNames):
        if i < start:
            continue
        print(item+' where?')
        x, y = int(input('x:')), int(input('y:'))
        print(item+' rotate?')
        rot = int(input('id:'))
        try:
            curBoat = classes.Boat(i, x, y, rot)
            playfield.putBoat(curBoat)
        except (SpaceOccupied, NextToBoat, InvalidPosition):
            print('wrong placement')
            playfield.removeBoat(curBoat)
            placeBoats(start=i)
        except InvalidTurnID:
            print('turnid from 0 to 3')
            placeBoats(start=i)

placeBoats()

for i in playfield.cells:
    line = []
    for j in i:
        if j is None:
            line.append(None)
        else:
            line.append('B'+str(j.kind))
    print(line)