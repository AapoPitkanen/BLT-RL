from utils import distance
import time

scent_tiles = {
    (15, 16): 10,
    (15, 15): 11,
    (12, 14): 8,
    (15, 17): 20,
    (14, 16): 15,
    (13, 14): 19
}

#print(scent_tiles)

player_x, player_y = (15, 15)

for coord in scent_tiles.keys():
    x = coord[0]
    y = coord[1]
    print(x, y)

    distance_to_player = distance(x, y, player_x, player_y)

    if not distance_to_player:
        print("distance is zero")
        continue
    elif 0 < distance_to_player < 2:
        print(
            f"distance is {distance_to_player}, distance is above zero but less than 2"
        )
        print("decrementing by one")
        scent_tiles[coord] -= 1
    elif 2 <= distance_to_player < 3:
        print(
            f"distance is {distance_to_player}, distance is greater than or equal than 2 and less than 3"
        )
        print("decrementing by two")
        scent_tiles[coord] -= 2
    elif distance_to_player >= 3:
        print(
            f"distance is {distance_to_player}, distance is greater than or equal 3"
        )
        print("decrementing by three")
        scent_tiles[coord] -= 3

#print(scent_tiles)

#print(f"distance to (57, 35) is {distance(57, 35, 0, 0)}")