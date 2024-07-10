import pygame
from pnoise import Noise
from typing import Sequence, List
from random import randint
from map_objects import Map
from player import Player
import constants
from inventory import InventoryItem, PlayerInv


pygame.init()
window = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 20)

map = Map()
player = Player()
map_generator = map.generate_map()

game_surface = pygame.Surface(map.map_img.get_size())


minimap = None

def bar(done, total) -> None:
    pygame.draw.rect(window, (255, 255, 255), pygame.Rect(105, 325, 500, 50))
    pygame.draw.rect(window, (0, 0, 0), pygame.Rect(107, 327, 498*done/total, 46))
    
    
robe_hood = InventoryItem("assets\character\walkcycle\HEAD_robe_hood.png")
robe_hood2 = InventoryItem("assets\character\walkcycle\HEAD_robe_hood.png")
inventory = PlayerInv()
inventory.common_slots[2][2] = robe_hood
inventory.common_slots[2][4] = robe_hood2
    
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if inventory.shown:
            inventory.handle_event_drag_drop(event)
        if event.type == pygame.MOUSEBUTTONDOWN and map.is_loaded and not inventory.shown:
            if event.button == pygame.BUTTON_LEFT:
                map_col = round((-map.offset_px.x + event.pos[0])//32 + map.offset_tiles.x)
                map_row = round((-map.offset_px.y + event.pos[1])//32 + map.offset_tiles.y)
                player.set_target(pygame.Vector2(map_col, map_row), map.map)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                inventory.shown = not inventory.shown
    
    pressed = pygame.key.get_pressed()
    if not inventory.shown:
        map.handle_pressed(pressed)
        
    
    window.fill((0, 0, 0))
    
    if not map.is_loaded:
        try:
            done, total = next(map_generator)
            bar(done, total)
        except StopIteration:
            map.is_loaded = True
            map.draw_map()
    else:       
        game_surface.blit(map.map_img, (0, 0))
        player.draw(game_surface, map.offset_tiles) 
        player.update_pos()
        if minimap == None:
            minimap = map.get_minimap(map.map)
        window.blit(game_surface, map.offset_px)
        
        window.blit(minimap, (0, 0))
        inventory.display(window)

            
    pygame.display.update()
    clock.tick(60)      