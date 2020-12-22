import enum
import math

MONSTER_PATTERN = [x for x in """
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
""".split("\n")][1:4]


def rotateMatrix(pixels):
    width = len(pixels)
    new_pixels = []
    for i in range(0, width):
        new_pixels.append([None] * width)

    for y in range(0, width):
        for x in range(0, width):
            new_pixels[x][width - 1 - y] = pixels[y][x]
    return new_pixels


class Flip(enum.Enum):
    VERTICAL = 0
    HORIZONTAL = 1


class Image:
    def __init__(self, image_id, pixels, orientation):
        self.image_id = image_id
        self.pixels = pixels
        self.orientation = orientation
        self.flips = [None, None]
        self.edges_cache = {}
        self.edges = self.get_edges()
        return

    def rotate(self, i=1):
        self.orientation = (self.orientation + i) % 4

    def flip(self, direction):
        if direction == Flip.VERTICAL:
            self.flips[0] = None if self.flips[0] else True
            self.pixels.reverse()
        elif direction == Flip.HORIZONTAL:
            self.flips[1] = None if self.flips[1] else True
            pixels = self.pixels
            for i, pixel_row in enumerate(self.pixels):
                pixels[i] = pixel_row[::-1]
            return

    def get_edges(self):
        edge_key = ','.join(
            [str(self.orientation), str(self.flips[0]), str(self.flips[1])])
        if edge_key in self.edges_cache:
            return self.edges_cache[edge_key]

        pixels = self.pixels
        edges = []
        for i in range(0, 4):
            if self.orientation > 0:
                i = (4 + (i - self.orientation)) % 4
            if i == 0:
                edge = pixels[0]
            elif i == 1:
                edge = ''.join([x[9] for x in pixels])
            elif i == 2:
                edge = pixels[9][::-1]
            else:
                edge = ''.join([x[0] for x in pixels])[::-1]
            edges.append(edge)

        self.edges_cache[edge_key] = edges
        return edges

    def get_pixels_by_rotated(self):
        pixels = self.pixels
        for i in range(self.orientation):
            pixels = rotateMatrix(pixels)
        return pixels

    def does_align(self, other):
        edges = self.get_edges()
        other_edges = other.get_edges()
        for i, edge in enumerate(edges):
            comparable_edge = other_edges[(i + 2) % 4][::-1]
            if edge == comparable_edge:
                # other edge is mirror of this edge
                return i
        return False

    @staticmethod
    def parse(string):
        parts = string.split("\n")
        image_id = int(parts[0][5:9])
        pixels = parts[1:]
        orientation = 0
        return Image(image_id, pixels, orientation)


class ImageArrangement:
    def __init__(self, images):
        self.images = images
        self.locked = set()

    def __can_rotate_image_to_match(self, image, target):
        for vertical in [None, Flip.VERTICAL]:
            image.flip(vertical)
            for horizontal in [None, Flip.HORIZONTAL]:
                image.flip(horizontal)
                for orientation in range(0, 4):
                    image.rotate()
                    if target.does_align(image) is not False:
                        return True
        return False

    def __match(self):
        images = self.images
        image_matches = {}
        for image in images:
            if image.image_id not in image_matches:
                image_matches[image.image_id] = [None, None, None, None]
            for other_image in images:
                if image.image_id != other_image.image_id:
                    matched = image.does_align(other_image)
                    if matched is not False:
                        image_matches[image.image_id][matched] = other_image.image_id

        return image_matches

    def __get_matches(self):
        images = self.images
        locked = set()

        images_to_lock = [images[0]]
        while len(images_to_lock) > 0:
            image = images_to_lock.pop()
            image_id = image.image_id
            locked.add(image)
            for other_image in images:
                other_image_id = other_image.image_id
                if other_image_id != image_id and other_image not in locked and image.does_align(other_image):
                    images_to_lock.append(other_image)

        while len(locked) < len(images):
            for image in images:
                if image not in locked:
                    for locked_image in locked:
                        if self.__can_rotate_image_to_match(image, locked_image):
                            locked.add(image)
                            break
        return self.__match()

    def get_composite_arrangement(self):
        image_matches = self.__get_matches()
        width = int(math.sqrt(len(self.images)))

        corners = [None, None, None, None]
        total = 1
        found = 0
        for image_id in image_matches.keys():
            matches = image_matches[image_id]
            if matches[0] == None and matches[3] == None:
                # top left
                total *= image_id
                corners[0] = image_id
                found += 1
            if matches[0] == None and matches[1] == None:
                # top right
                total *= image_id
                corners[1] = image_id
                found += 1
            if matches[2] == None and matches[1] == None:
                # bottom right
                total *= image_id
                corners[2] = image_id
                found += 1
            if matches[2] == None and matches[3] == None:
                # bottom left
                total *= image_id
                corners[3] = image_id
                found += 1

        composite = []
        for i in range(0, width):
            composite.append([None] * width)

        grids_to_add = [corners[0]]
        y = 0
        x = 0
        while len(grids_to_add) > 0:
            image_id = grids_to_add.pop()
            composite[y][x] = image_id
            neighbor_grids = image_matches[image_id]
            if y % 2 == 0:
                if x == width - 1:
                    grids_to_add.append(neighbor_grids[2])
                    y += 1
                else:
                    grids_to_add.append(neighbor_grids[1])
                    x += 1
            else:
                if x == 0:
                    grids_to_add.append(neighbor_grids[2])
                    y += 1
                else:
                    x -= 1
                    grids_to_add.append(neighbor_grids[3])
            if y >= width:
                break

        return composite


def solve(puzzle_input):

    images = [Image.parse(x) for x in puzzle_input.strip().split("\n\n")]
    images_by_id = {i.image_id: i for i in images}
    width = int(math.sqrt(len(images)))
    image_arrangement = ImageArrangement(images)

    composite = image_arrangement.get_composite_arrangement()

    # part 1
    print(composite[0][0] * composite[0][width - 1] *
          composite[width - 1][0] * composite[width - 1][width - 1])

    # part 2

    # build the composite image
    for y in range(0, width):
        for x in range(0, width):
            image_id = composite[y][x]
            image = images_by_id[image_id]
            composite[y][x] = image.get_pixels_by_rotated()

    # flatten to a single 2-d pixel array
    full_image = []
    width_per_image = len(images[0].pixels) - 2
    dpi = width * (len(images[0].pixels) - 2)
    for i in range(0, dpi):
        full_image.append([None] * dpi)

    for y in range(0, width):
        for x in range(0, width):
            for y2 in range(0, width_per_image):
                for x2 in range(0, width_per_image):
                    full_image[y2 + (width_per_image * y)][x2 +
                                                           (width_per_image * x)] = composite[y][x][y2 + 1][x2 + 1]

    full_image = Image(1, full_image, 0)

    def find_sea_monster(image, y, x):
        for my_rel_start in range(0, len(MONSTER_PATTERN)):
            for mx_rel_start in range(0, len(MONSTER_PATTERN[my_rel_start])):
                if MONSTER_PATTERN[my_rel_start][mx_rel_start] == "#":
                    dy = y + my_rel_start
                    dx = x + mx_rel_start
                    if dy < len(image) and dx < len(image[dy]):
                        if image[dy][dx] != "#":
                            return False
                    else:
                        return False
        return True

    def find_sea_monster_in_image(image):
        total = 0
        width = len(image)
        for y in range(0, width):
            for x in range(0, width):
                if find_sea_monster(image, y, x):
                    total += 1
        return total

    # search for sea monsters
    for vertical in [None, Flip.VERTICAL]:
        full_image.flip(vertical)
        for horizontal in [None, Flip.HORIZONTAL]:
            full_image.flip(horizontal)
            for orientation in range(0, 4):
                full_image.rotate()
                found = find_sea_monster_in_image(full_image.pixels)
                if found:
                    total = 0
                    for y in range(0, dpi):
                        for x in range(0, dpi):
                            if full_image.pixels[y][x] == "#":
                                total += 1
                    print(total - (found * 15))
                    return

    print("Failed to find any sea monsters")
    return


solve("""
Tile 2953:
.###.###..
.#....#..#
#.#......#
.###.#..##
#..##..#..
....#....#
.##.#..#.#
#......#..
#.........
..##..#.#.

Tile 2053:
##.##...#.
......#.#.
..###.#...
..#..#.###
##.......#
###...#.##
.#.##.##..
##...#...#
##.##..###
.#...####.

Tile 1213:
.......#..
#...##...#
....#..#..
..#..###..
#..##..#..
#.#.#.....
...#.#..##
#.#.#.#...
....#.....
..##....##

Tile 2801:
.#.##.#...
#.#....###
.....##..#
.....#....
#....##...
#.#...#..#
..#..#..##
#........#
#..#...#..
..###.....

Tile 1109:
#######...
..........
##..#....#
#........#
.#.#...#..
####.....#
...#.##...
.##....#.#
#..##...#.
#.#..##...

Tile 2833:
#.#.#.#..#
#.#...#..#
.....#.#.#
#.##....##
#.##..##.#
#.#..##.#.
..#......#
#....#....
..#.#.#...
#..##..##.

Tile 2099:
##.#..#..#
.....#..#.
.........#
.....###..
#.........
####.#..#.
######...#
##.##.#...
.....###..
.....##..#

Tile 1867:
#..####.#.
#....#..##
#..##.#..#
..#..#...#
#...#....#
...##.....
..........
....##.###
##..#.#.##
##..#.####

Tile 2551:
#.#.#...#.
#....#...#
.#.#.....#
#.#.#...#.
#.#...#.##
...#.##..#
...#.....#
#.........
#..#.#....
##..#.##.#

Tile 2239:
#.#...###.
#.#.....##
##....#...
##.......#
.#.#..#..#
###......#
#.........
...#....##
#..#.##..#
...###....

Tile 3049:
..##....#.
...##...##
....###..#
.#.##.....
.##...#.#.
..#...#..#
#......#..
.####...##
#..##.....
.##.##.###

Tile 1913:
###....#..
.....##...
#.#.....#.
....#....#
#...#...#.
.......###
..#....#..
##........
..#...#..#
##....#.#.

Tile 3469:
.##.##...#
#...####..
.###.##...
##.#...#..
#...#...##
#.##.#..##
##......##
..........
#.....#..#
#.##..##..

Tile 2467:
##.#.###..
..#####..#
#....##...
#.....#.##
#.#...#...
.....##.#.
#..#..#..#
#....##..#
#..###.#..
.##.......

Tile 3467:
##..##....
##......#.
##....#...
.#...##...
#.#....#..
##....#.##
#..#..#.#.
#.....####
#.#..####.
.#.#.#..#.

Tile 2683:
#..##...#.
.####....#
#.......##
#.....#.##
...##.#..#
##.#......
##....#...
.##.....#.
..#......#
##.....##.

Tile 2927:
.#..#.####
#..##....#
..##.###.#
..###..##.
##.....##.
#.........
.#..#..#.#
.###....#.
#..#..#...
##..##....

Tile 3037:
..###...#.
#..#.....#
.####....#
#....###.#
..#....#.#
#.##...#..
......#..#
.##..##...
..#..#..#.
.##....###

Tile 1019:
.##..#...#
...#..#.##
###.##..#.
.##..#....
#.#...#...
....##...#
..##.#.#.#
#.....####
......####
..###....#

Tile 3089:
#..##..##.
..##......
.#....#...
..#..#....
.......#.#
...##.....
#.#...#...
#.......#.
#........#
.##...#..#

Tile 2011:
...#.###.#
#.#..#.#.#
#.#..###..
.......##.
...#.....#
.#.......#
##..#..#..
...#..#...
###....##.
...#.#...#

Tile 1801:
..####...#
#..#..#..#
#...#...#.
....#....#
..##.....#
....#.....
#..##.....
#.###.....
....##....
..#.#.#...

Tile 1217:
#.#.#.##..
##.#...#.#
.....#....
..#.....#.
#...##...#
..#.#..###
#..#..#..#
.#........
#......#.#
#...#.##.#

Tile 1789:
.#.#####..
..#.#....#
.##..#..#.
..#.###.##
..##......
.#.#..#...
#...#.#...
..........
#.##......
#.#..#..##

Tile 3719:
..####.##.
###.......
...#..#.#.
.......#..
#.###....#
........##
#.....#...
...##..#.#
#.#....##.
#.#..##.#.

Tile 3637:
#....#..#.
##..#..#..
#.....#..#
#.........
##........
#.###....#
#..##....#
..#.#...#.
......###.
..#.#..##.

Tile 1471:
.##.#..#..
.##....#.#
###...##.#
..##.##.##
..........
#......###
#.#.#.#..#
.....#.###
#.#..#...#
...#####..

Tile 1933:
##.###....
#..#....#.
#..#..##.#
.#..#..###
.....##...
.##..#...#
....#.#..#
#..#......
#.##.#.##.
....###.#.

Tile 1381:
.##..##.#.
.#..###..#
##.#.##.##
.#..#.....
#...##...#
.#.......#
#........#
####.....#
#.#...####
.#..#..###

Tile 2423:
#.#.######
#.........
##....##.#
#....#.#..
..#..#....
......#..#
##..#..#..
....###...
#....#....
..#.##....

Tile 3373:
.#.#..####
#.#.#....#
#..#.....#
....#....#
#..#..#.##
.....##...
#...##..##
..#.....#.
.#.#....##
##..##.#.#

Tile 1163:
###.....##
#...#....#
##.......#
.........#
...###.#.#
..#.......
...##.#..#
.#.#...##.
..#.##....
######.###

Tile 2543:
#...#.##.#
#.#......#
....#.#..#
##......##
##..#...##
..........
#.....##.#
###..#.###
.####.#..#
##...##...

Tile 1427:
#.#....##.
#.......##
...#.###.#
...#......
..#..#....
.#.....#..
..##.....#
#.#.#...#.
..#.#.#.##
.#...##.##

Tile 3371:
.##...#..#
#...#..#..
.#........
..#...####
..###.#..#
##.#....#.
.##.#.#.##
#..####...
....#..###
###.#...#.

Tile 3529:
.#.#..#..#
##..#..#..
..........
#..#..##..
###....#.#
.#....##.#
#.#......#
...#.#.#.#
#.........
.#.#..#.##

Tile 3539:
###.#..##.
##.#...###
#..#...###
#..#......
...##..#.#
#...#.#...
#.#.##....
#.#..#..##
#..#.##.##
##.#.#....

Tile 1511:
#..#####..
.##..#..#.
#.....#..#
#.#..##..#
..#......#
.#........
#.#.#.#..#
##.#.#..#.
##........
....#.....

Tile 2521:
.###....#.
#........#
.......#..
.#....#..#
##....#..#
......#...
...#.#..##
#......###
#...#....#
....###..#

Tile 1637:
.#..#.....
#.......#.
...#..#.##
#......#..
#.###.#..#
.#...##...
..###.#...
##...#.###
..#..##.#.
.##.#..#.#

Tile 2351:
####.###..
##...###..
#....#..#.
#........#
#.#.......
##..##...#
####..#...
##...##.#.
##...#.#..
..#####.#.

Tile 3929:
.#..##...#
.#.#..#...
##..##.#.#
..#...#...
.##.#...#.
#.....#..#
...#..#..#
##...#....
##......#.
.##..##...

Tile 1223:
....#.....
..#..#....
..#...#...
...#....##
..#......#
#.....#...
..#..##...
....#.....
#.....##.#
..##.#....

Tile 1009:
#....###.#
#.#......#
....##..#.
#.........
#..##....#
.##.......
.....#...#
.......##.
.....#.#.#
.#.....##.

Tile 1289:
.##..#.#.#
.......##.
.#...#...#
....#.....
........##
#...#..#..
#....#...#
#....###.#
#..#....#.
###..#....

Tile 3943:
.#.#.#....
#.....#.#.
#....#...#
....#.#.#.
....#..#..
##.#.#.#..
##...#.#..
#.........
.#....##.#
#.#.#####.

Tile 2633:
.####..##.
....#.....
....###...
......#..#
....#.....
#..#.#...#
#.##...#.#
##..#.##.#
..#.....##
#.#.####..

Tile 2797:
.###..#.#.
#...#.##.#
#.....#..#
....#...#.
...#....#.
.##.#.....
......##..
....#....#
#.........
..#...###.

Tile 1973:
....#.##.#
##.....#.#
..#..#.#.#
#.#.#..#..
.....##.##
.##.#.#...
..###.#...
........##
##...#...#
..#...#..#

Tile 2621:
#.##.##.##
.#..#.#.##
........#.
#...##....
.####..#.#
....#....#
.#........
...#....##
..##.#.#.#
###.##....

Tile 1303:
..########
.#.#......
#.#..#..#.
.#.#.....#
...##..#..
..##......
.#.#...#..
#.....##..
#........#
#.##.#.#..

Tile 1483:
.##.......
.#.#.##.#.
.##...#...
##...#..##
.#.#..#.##
#...#.##..
.##...#...
.......#.#
.#........
.#..#.##..

Tile 1229:
#.#.##..##
..#.##.##.
#####.###.
.#.#.....#
....##..#.
...#.##.#.
#.....#..#
#.##......
.........#
#.###....#

Tile 1319:
#..#..##.#
##..#....#
..#....##.
#.#...#..#
...#.....#
#.#..#.#..
##....#..#
###.....#.
..#.#..#.#
.#..##....

Tile 2837:
#.##.#.##.
.##.#.....
##..#.....
#...##..#.
.#.#...#.#
..#...#..#
..#..#...#
..##..#...
...##....#
.#.#..##.#

Tile 2503:
##...#####
##...#....
....#....#
..#####...
##.#.##.#.
#....#.#.#
#.#....#..
........##
.#..#.....
#..####.##

Tile 2711:
.##.#.##..
.#.....#.#
......#..#
##..#...##
..#....###
.##.#.###.
....#..#.#
......#...
#....#...#
#..####.#.

Tile 2137:
#.......##
#.#.......
#.#.#.....
#.....#..#
#...##.#.#
#..#...#.#
#..#.#....
..#.#.#...
#.##......
#.####.#.#

Tile 1543:
#.....#.##
..##.....#
#..#......
####....#.
#.#.#..#.#
..#..#....
....#..#..
###..##..#
..##.#.###
##.#....##

Tile 2161:
..#...##..
##...####.
#.##.#.##.
##........
#.....##.#
..#.#.##..
#...#.....
#.#..#..##
...##..###
.#..###.#.

Tile 2377:
...######.
#.....#..#
#...##....
#.....##..
.#......#.
.#.#..##..
......#..#
.......#..
..#.....#.
..###.#.#.

Tile 1429:
.#.##.#..#
.#....##..
.#...##..#
.#...#...#
...##.###.
.......###
##......##
#..#..##.#
#....##..#
#..###..##

Tile 2113:
#.######..
..#...##..
#.####.#.#
..........
..##......
....#.###.
#....#...#
#...##....
......##..
.######...

Tile 2677:
#..#.#####
......#..#
....##...#
....#.....
.##.##....
#......##.
...###.#.#
####.#..#.
..#...#...
##.#####..

Tile 2591:
.#.##..##.
##.#......
.#..#.#.##
.##..##..#
.........#
#..#.#.##.
........#.
...#..#...
.....#..#.
.#.####...

Tile 2287:
..##...##.
##.###....
#....#..##
#.#.....##
#.......#.
#...#....#
...#..#.##
.#..##...#
#....#.##.
.####..#..

Tile 1279:
#..##.#..#
##........
...##.....
##...#...#
#..#.....#
.......#.#
..#..#...#
...#.#.##.
#..#....#.
#.#...##..

Tile 3769:
##.....##.
....#....#
...#.#....
....#....#
#....#...#
#..#..##.#
#......#.#
..........
.....#...#
##.#.##..#

Tile 1931:
.##.#.##.#
..###..#.#
#.##..#...
..#..#.#..
..#...####
#.....#.#.
..........
..####..##
..#....###
....#.##.#

Tile 3847:
.#.####...
.......#.#
##...#...#
#...##...#
....#....#
..#..#....
#.#.#..#..
..#..#....
##...#....
##..##.#..

Tile 2549:
..##....#.
#.........
#....#....
#.....#...
#.##...#..
##...#.#.#
.####..#..
......####
...####.##
..#####..#

Tile 3067:
..####..##
#....#....
##.....#.#
....#...##
........#.
...#...###
.......#.#
#..##..##.
..##...#.#
...#...##.

Tile 2083:
.####..#..
##.#..#..#
.......#..
##..##.#.#
.......##.
##....###.
#....#...#
#...##...#
...#......
.####.#..#

Tile 2819:
...##..###
#.##.....#
##.##.#..#
.....#..##
#......#.#
#........#
##....####
#.....#.#.
#....#...#
....#...#.

Tile 2089:
#####.#.#.
###..#..#.
#.....#...
.####..#..
..####..#.
#....#..#.
....#.#...
....#.#.##
#.#.......
..####.#..

Tile 1459:
..##..#..#
.##..#..#.
...#......
.....##.#.
.#.#.#....
.....#...#
.....##...
.#.#..####
#...##...#
.#.#.#.#..

Tile 3761:
..#.#...#.
...#.#####
.#...#..##
#..#.#....
..........
..#..#..##
#.####..#.
....####..
##.#..#...
#.##.#####

Tile 2707:
######.###
##..#.##.#
.#.......#
...#...#..
#.....#...
...#......
........#.
#...#.....
.###..#..#
.....#.##.

Tile 2371:
.###..####
###......#
......#...
...##..#.#
...#.....#
##......#.
...#..##.#
#.....##..
##..##.#..
##...#.#..

Tile 1907:
.#.#.####.
#..#.....#
#..##.....
##..#.###.
#...#.#.#.
..#.#.....
#.##......
###......#
#........#
#.#.#....#

Tile 1499:
####...#..
...#......
.....#....
##..#....#
#...##...#
#.#....#..
.....#.###
#......#.#
###...#.##
##..##...#

Tile 2267:
.#..##...#
#...#.#..#
##.....#.#
..........
###.##....
.####..#.#
#........#
......#.#.
#.#..#.#.#
..#.#...##

Tile 1283:
######..##
##.#.....#
#.......##
#...##...#
##........
#.....#..#
#....#...#
#..###.#..
#.........
...##.....

Tile 3499:
##..#..##.
#........#
#....#....
#.####....
#.#......#
....##...#
#..#....#.
#...#....#
#.#....##.
.#.#.#.#..

Tile 3881:
#..#....##
#..#.....#
..#...#..#
#...##...#
#.......##
..#..#####
....#...#.
##..##....
#.#..#....
..##.###.#

Tile 2341:
...##.#.##
...#.##.##
.##..###.#
#..#######
##..#..#.#
......##.#
....#.##.#
####.#..##
##....###.
.##.#..#.#

Tile 2399:
......####
#...#.....
..#...#.##
.#.#....##
##........
##.....##.
.....#...#
#....#.##.
#...#..#..
..#.#.###.

Tile 3697:
..#..##..#
#.###..#.#
.#.#.#...#
#.#.#....#
#.###.#..#
......##.#
##.#....##
.#......#.
####.#...#
#.#..#.###

Tile 3331:
#.#.##....
##.....###
####......
.#.##.#..#
.##.......
#.#..#...#
.....#.#..
#.##.#.##.
###......#
.#.#...##.

Tile 1979:
...###..##
..#..#..##
...##....#
###...#.#.
#.....#..#
..##..#...
.....#.#..
#..#......
##........
#####.....

Tile 3041:
#...##.#.#
#..###.#.#
...#...###
#...#..#.#
.#..##...#
#.....###.
......#...
.#.#.#...#
..#.##..##
...#..#.##

Tile 1307:
.#.#.#...#
.##...##.#
...#.....#
#.....#...
#........#
##.###.#.#
##....#..#
#........#
.###....##
##..#.###.

Tile 1523:
..#.....##
.....##...
#........#
#.#.#...#.
#..#..#.##
#.......##
..#..#.#.#
....#....#
###......#
...#.#..#.

Tile 3491:
####..#...
.#....#.##
.#..#..#.#
#...#..###
#.......#.
#.....#..#
.....#.#..
#.#..##...
.#...#...#
##.#..#.#.

Tile 3989:
####....##
##..###..#
#..#....##
...#####.#
###..#..##
#.####..#.
##..#....#
..#......#
...##...##
.##.#..###

Tile 3727:
#.#..#.#..
#.#......#
......#..#
..#....###
#..##.#...
...#..#...
#..##.####
#..#.....#
.......#..
...###..##

Tile 1583:
..##....##
#....##...
##..#...#.
....##.#..
#...###..#
.##.#.....
....#..#..
...#.#....
....##..##
#..##...#.

Tile 3581:
##..#.....
....#..##.
##..#....#
..#.......
#.....#...
#.....#...
#...#....#
.........#
.....##..#
##..#.####

Tile 3559:
.#........
....##....
....#..#.#
##..#.##..
#..#.#....
..##.#...#
.#..##..##
....#..#..
##.#.....#
#....#####

Tile 2131:
..########
#.........
..#.##..#.
.#.#.#....
####....##
#####.....
#.........
#.#.....#.
..##....##
...###.##.

Tile 1061:
###...##..
.#...##...
.#.#..#...
..##......
#......##.
#.....#...
#.......##
#........#
#.##.##...
##.#.##.#.

Tile 3947:
.#####.##.
..#.#.#...
#.......##
#.#....#.#
..#....##.
.##.#...##
#....#.##.
....####..
###....#.#
########.#

Tile 2213:
.###......
....#...##
#..##.....
#..##.#...
...#....#.
.........#
#####....#
#......#.#
###.......
..##.##.#.

Tile 3319:
..##.###..
.#...##...
..#.#..#..
..#.##....
...###....
##.#......
#.#...####
.....#.#.#
.#........
#.....#.##

Tile 1423:
#....#..#.
..#...#..#
.#.#.#.##.
#.##..##..
#.##......
#.#...##.#
..#......#
#.##...###
###.#.#.##
.###.....#

Tile 1607:
#.#...#..#
.##....#..
.#...#.#.#
##.#.....#
...###..##
#...#..#..
..........
#..#.....#
#..#......
.#.##..#.#

Tile 3301:
...#.#...#
.#.#....##
.#.####...
#..##.#...
##..###..#
#...#.#.##
......#..#
#........#
#..####.##
####..#.##

Tile 2917:
.##..####.
#......#.#
##.......#
.##..#....
......#..#
.##..##...
#.####.#.#
##......##
#......##.
.....#.##.

Tile 3851:
#.##.#.#.#
###..#...#
#.##.....#
..##..#...
#.##.....#
.##...#.#.
#..#.##...
#...#.....
...#.#...#
...#..####

Tile 1439:
..##.##.##
.....#...#
#..###...#
....##....
##.#..#...
.....#...#
##.#.#....
...#.#...#
..#..###..
..#...###.

Tile 1493:
.#.###....
.#.#.#....
#.#....#.#
#...#..#..
#....#..#.
..#...#...
...#......
..........
...#.##..#
##....#.#.

Tile 1889:
..###.###.
..##.#....
#....#...#
..#...#..#
#.......#.
#...#..#.#
..#..##...
..#......#
#....####.
##.#.##...

Tile 3407:
#..#.....#
........#.
..#.......
...#......
...#.##.##
#..##.....
##.##..##.
#...#.....
#....##...
##.##..##.

Tile 2699:
....##..#.
#.........
#.#...###.
...#..#..#
.##..#...#
##..#..##.
####....##
#.#...#..#
........##
.####.....

Tile 2861:
.....##...
.....#..##
...###....
..##..#..#
..#.#.....
#.#.......
.....#....
.##..#.#..
##.#..##..
#.####...#

Tile 1619:
##....#.##
#.#...#..#
#.#....#..
.......###
#.#.......
......##.#
.#....#.#.
#....###..
#....##.##
#.#####...

Tile 1531:
...#.##...
#..#.#....
#..#...##.
.....#....
#........#
#.#.......
##.##....#
......#..#
#.#.......
..#####...

Tile 3169:
##.####..#
..........
#...#..#.#
#........#
.#...#....
#...##....
.........#
#....#..#.
......###.
..#.####..

Tile 1249:
###.#..#.#
#..#.###.#
#.#.#.....
#...#.....
###.#.#...
.....#.##.
#.......##
#....#.#..
....#..##.
..#..##.##

Tile 2293:
..#...#..#
#....#...#
#....#..#.
..........
.......#.#
####......
.##....#.#
####.....#
#..#.....#
#.#.##....

Tile 1723:
.#.#..#..#
#...#..#.#
#.....#...
.##..#..#.
.........#
#.#..####.
###..###..
###..##.##
#.......#.
#..#.#.#.#

Tile 3191:
.#..#####.
........#.
.#..#...##
#..#...#.#
.##.##....
.......#.#
...#...#.#
..#.......
##.......#
...####..#

Tile 1663:
.####.##..
....#...##
##..##...#
#..#......
....##....
##.#..##..
##..##..#.
...#.#.#.#
#......#..
.##..###.#

Tile 2281:
####.#..#.
#......###
.#....###.
..........
..#.....##
.........#
..#.#.#.##
#...#.....
###.#..#..
##...#..#.

Tile 3677:
..####.##.
###......#
.##....#..
#....#...#
....#.#.#.
#.##.#..#.
...##.#...
....#.#..#
..#.......
##..##..#.

Tile 1361:
.#..###.##
.........#
#....##...
..##...#..
#.#.....##
#.#####...
##.#...#..
#..#...###
#..#.#...#
#####.#.#.

Tile 1051:
######.##.
####..#..#
###.##....
#.#......#
#####..###
#.#.#..#.#
...#.#...#
##.#.....#
..#...####
....#..###

Tile 1831:
##.#..####
####...##.
##...##..#
#...#...#.
....#.....
#...#....#
#.....#...
#####.....
......#...
.###.###.#

Tile 1861:
....###..#
.####...#.
#..#...###
#..#.#....
#.##.#....
....#.##..
.#..#...##
.....#....
#...#.##.#
##.##.#...

Tile 1873:
.#.###..#.
##.......#
.####...##
##......#.
#.........
.#........
.##.#....#
...###.##.
..#..##..#
.#.###...#

Tile 2129:
#####..###
##..##..#.
.#.#......
##....#..#
#.####....
....#....#
###..##.##
.##.#..#..
#.#..##.##
...#.##.#.

Tile 2333:
..#.#...#.
#.........
#...#....#
....######
..##...###
##....###.
...#......
##.####..#
#####.....
.#....#.#.

Tile 2851:
.###..##..
...#..##..
#......##.
......#.##
..........
.###....#.
#....#.#..
#.....#.##
..........
.#######..

Tile 2689:
.#######.#
.....#....
........##
###..#.##.
#.........
#......###
.#.###.#..
....###...
#..#..#...
..#...#.#.

Tile 1193:
.##...#...
####......
...#.###.#
..#..#..#.
#.#...##.#
.....##.#.
#...##.##.
#....#..##
...##...##
#..##.#..#

Tile 2663:
......#.##
##......##
.#.....##.
.##.##...#
#.##..##.#
...##..#.#
#.........
#.#..#...#
.......#..
.#...#####

Tile 1481:
.#.#...#.#
#..#......
.#.......#
#.##..#.#.
..#..#....
##........
.#...#####
#....#.#.#
#....##..#
.###.####.

Tile 2417:
###..####.
....#..#.#
...#....##
#........#
#.##...#.#
#.#.......
.......#.#
#......###
#..#.##.##
#.##.....#

Tile 3671:
..#####.##
....#.....
.....#.#..
....#...#.
..........
#.#..##.#.
..##.#...#
#..#.....#
.#......#.
...#.###.#

Tile 1181:
###..#.#.#
........#.
#........#
#..#..#.##
#.#..##...
..#....#.#
..........
.####.#.##
...#.#....
...#....##

Tile 1999:
#..#..##..
...#......
##.#.#.#.#
#.....#..#
...#....#.
##..##..##
####.#...#
....#....#
.....#...#
#.#.####.#

Tile 2207:
...##.##..
......#.#.
###.#.#..#
.....##...
..##.#.#..
#.....##.#
.#.#......
#...#..#..
..#.#####.
..###..#..

Tile 3359:
#.#..#...#
#.........
####..#.#.
#........#
....#.#...
.#..###...
.#....#..#
....####.#
#.....###.
#...##.#.#

Tile 1847:
##..#.#.##
#........#
#.#####...
..##.##...
##..#...##
##...#..##
.#...#....
#.#......#
##..##...#
..#.#####.
""")