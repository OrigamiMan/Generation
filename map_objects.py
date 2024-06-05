import pygame
from pnoise import Noise
from typing import Sequence, List, Generator, Tuple
from pickle import load, dumps
import constants

n = Noise()
n.seed(567)

def save_map(map: List[List["Tile"]], filepath: str) -> None:
    file = open(filepath, "wb")
    binary_data = dumps(map)
    file.write(binary_data)
    file.close()

def load_map(filepath: str) -> List[List["Tile"]]:
    file = open(filepath, "r")
    return load(file)




class Tile:
    def __init__(self, biome: int) -> None:
        self.biome: int = biome

MapType = List[List[Tile]]

class Map:
    def __init__(self) -> None: 
        self.map_img = pygame.Surface((constants.MAP_WIDTH, constants.MAP_HEIGHT))
        #self.map = self.generate_map()
        #save_map(self.map, "./map.bin")
        #self.map = load_map("./map.bin")
        self.tile_imgs = self.load_tile_imgs()
        self.tile_mini_imgs = self.load_mini_tile_imgs()
        #self.draw_map()
        self.map_pos = pygame.Vector2(0, 0)
        self.offset_px = pygame.Vector2(0, 0)
        self.offset_tiles = pygame.Vector2(0, 0)
        self.is_loaded = False
        
    def load_tile_imgs(self) -> List:
        tile_images = []
        for i in range(6):
            filename = "./assets/tile" + str(i) + ".png"
            img = pygame.image.load(filename)
            tile_images.append(img)
            
        return tile_images
    
    def load_mini_tile_imgs(self) -> List:
        tile_images = []
        for i in range(6):
            filename = "./assets/mini_" + str(i) + ".png"
            img = pygame.image.load(filename)
            tile_images.append(img)
            
        return tile_images
        
    def handle_pressed(self, pressed: Sequence[bool]) -> None:
        step = pygame.Vector2(0, 0)
        
        step_v = pygame.Vector2(0, 5)
        step_h = pygame.Vector2(5, 0)
        if pressed[pygame.K_w]:
            step += + step_v
        if pressed[pygame.K_s]:
            step += - step_v
        if pressed[pygame.K_a]:
            step += + step_h
        if pressed[pygame.K_d]:
            step += - step_h

        next_offset = self.offset_px + step

        
        if next_offset.x > 0:
            reverse_offset_x = constants.WINDOW_WIDTH - constants.MAP_WIDTH
            self.offset_tiles.x += int(reverse_offset_x / 64)
            self.offset_px.x += int(reverse_offset_x / 2)
            self.draw_map()
            return
        
        if next_offset.y > 0:            
            reverse_offset_y = constants.WINDOW_HEIGHT - constants.MAP_HEIGHT
            self.offset_tiles.y += int(reverse_offset_y / 64)
            self.offset_px.y += int(reverse_offset_y / 2)
            self.draw_map()
            return
        
        if next_offset.x < constants.WINDOW_WIDTH - constants.MAP_WIDTH:
            
            next_offset_tiles_x = self.offset_tiles.x - int(self.offset_px.x / 64)
            
            self.offset_tiles.x = next_offset_tiles_x
            self.offset_px.x -= int(self.offset_px.x / 2)
            self.draw_map()
            return
        
        if next_offset.y < constants.WINDOW_HEIGHT - constants.MAP_HEIGHT:
            self.offset_tiles.y -= int(self.offset_px.y / 64)
            self.offset_px.y -= int(self.offset_px.y / 2)
            self.draw_map()
            return

        self.offset_px = next_offset
            
    def choose_biome(self, noise: float) -> int:
        intervals = (0, 0.3, 0.4, 0.5, 0.6, 0.7, 1)
        for i in range(len(intervals)):
            if noise >= intervals[i] and noise < intervals[i + 1]:
                return i

    
    def generate_map(self) -> Generator[MapType, None, Tuple[int, int]]:
        result = []
        tile_counter = 0
        tpf = 256
        width, height = constants.TOTAL_TILES_WIDTH, constants.TOTAL_TILES_HEIGHT
        total_tiles = width * height
        for i in range(height):
            row = []
            for j in range(width):
                scale = 0.08
                noise = n.perlin(i * scale, j * scale, 1)
                biome = self.choose_biome(noise)
                if biome > 5:
                    biome = 5
                if biome < 0:
                    biome = 0
                tile = Tile(biome)
                row.append(tile)
                tile_counter += 1
                if tile_counter % tpf == 0:
                    yield tile_counter, total_tiles
            result.append(row)
        self.map = result
    
    def draw_map(self) -> None:
        tiles_i = int(constants.MAP_HEIGHT / 32) + 1
        tiles_j = int(constants.MAP_WIDTH / 32) + 1
        for i in range(tiles_i):
            for j in range(tiles_j):
                di, dj = int(self.offset_tiles.y), int(self.offset_tiles.x)
                tile = self.map[i+di][j+dj]
                            
                tile_img = self.tile_imgs[tile.biome]
                self.map_img.blit(tile_img, (j* 32, i* 32))


    def draw_checker_board(self) -> None:
        for i in range(2000//50):
            for j in range(2000//50):
                colour = (100, 100, 100) if (i +  j) % 2 == 0 else (40, 40, 40)
                rect = pygame.Rect((i * 50, j * 50), (50, 50))
                pygame.draw.rect(self.map_img, colour, rect)
                
    def get_minimap(self, map: List[List[Tile]]) -> pygame.Surface:
        surface = pygame.Surface((constants.TOTAL_TILES_WIDTH, constants.TOTAL_TILES_HEIGHT))
        return_surface = pygame.Surface((150, 150))
        return_surface.set_alpha(200)
        rect = pygame.Rect((0, 0), (10, 10))
        pygame.draw.rect(surface, (255, 0, 0), rect)
        for row in range(len(map)):
            for col in range(len(map[row])):
                tile_img = self.tile_mini_imgs[map[row][col].biome]
                surface.blit(tile_img, (col, row))
        return_surface.blit(pygame.transform.scale(surface, (150, 150)), (0, 0))
        return return_surface       
