from collections import deque

def ignite_pixel(image, coordinate, id):
    y, x = coordinate
    burn_queue = deque()

    if image[y, x] == 255:
        burn_queue.append((y, x))

    while len(burn_queue) > 0:
        current_coordinate = burn_queue.pop()
        y, x = current_coordinate
        if image[y, x] == 255:
            image[y, x] = id

            if x + 1 < image.shape[1] and image[y, x + 1] == 255:
                burn_queue.append((y, x + 1))
            if y + 1 < image.shape[0] and image[y + 1, x] == 255:
                burn_queue.append((y + 1, x))
            if x - 1 >= 0 and image[y, x - 1] == 255:
                burn_queue.append((y, x - 1))
            if y - 1 >= 0 and image[y - 1, x] == 255:
                burn_queue.append((y - 1, x))

        if len(burn_queue) == 0:
            return id + 50

    return id


def grassfire(image):
    next_id = 50
    for y, row in enumerate(image):
        for x, pixel in enumerate(row):
            next_id = ignite_pixel(image, (y, x), next_id)