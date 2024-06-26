import pygame
from typing import List, Sequence, Optional
import constants

def empty_slot() -> pygame.Surface:
    item_surface = pygame.Surface((64, 64))
    item_surface.fill((200, 200, 200))
    pygame.draw.rect(item_surface, (190, 190, 190), (4, 4, 56, 56), 64, 6)
    pygame.draw.rect(item_surface, (170, 170, 170), (4, 4, 56, 56), 2, 6)
    
    return item_surface

class InventoryItem:
    def __init__(self, filename: str) -> None:
        self.img = pygame.image.load(filename)
        self.icon = self.img.subsurface((0, 128, 64, 64))

    
    def display_icon(self, surface: pygame.Surface, coords: Sequence[float]):
        surface.blit(self.icon, (0, 0))
        
        
class PlayerInv:
    def __init__(self) -> None:
        self.common_slots: List[List[InventoryItem | None]] = [[None]*9 for _ in range(3)]
        self.hotbar: List[List[InventoryItem | None]] = [[None] * 9]
        self.clothes: List[List[InventoryItem | None]] = [[None] for _ in range(4)]
        self.offhand: List[List[InventoryItem | None]] = [[None]]
        self.shown = False
        
        self.moving_item: Optional[InventoryItem] = None
        
        self.common_slots_rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)
        self.hotbar_rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)
        self.clothes_rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)
        self.offhand_rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)
    
    def handle_event(self, event: pygame.event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.common_slots_rect.collidepoint(event.pos):
                i = (event.pos.y - self.common_slots_rect.top) // 64
                j = (event.pos.x - self.common_slots_rect.left) // 64
                print(i, j)
        if event.type == pygame.MOUSEBUTTONUP:
            pass
        if event.type == pygame.MOUSEMOTION:
            pass
        
    def render_slots(self, surface: pygame.Surface, slots: List[List[InventoryItem | None]], offset: pygame.Vector2) -> pygame.Rect:
        for i in range(len(slots)):
            for j in range(len(slots[i])):
                item = slots[i][j]
                item_surface = empty_slot()
                if item is not None:
                    item.display_icon(item_surface, (0, 0))
                #return surface.blit(item_surface, (j * 64, i * 64) + offset)
                surface.blit(item_surface, (j * 64, i * 64) + offset)
    
    def display(self, surface: pygame.Surface) -> None:
        if not self.shown:
            return
        
        inv_surface = pygame.Surface((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT), pygame.SRCALPHA, 32)
        pygame.draw.rect(inv_surface, (200, 200, 200), (0, 0, 800, 800))

        # self.common_slots_rect = self.render_slots(inv_surface, self.common_slots, pygame.Vector2(96, 384))
        # self.clothes_rect = self.render_slots(inv_surface, self.clothes, pygame.Vector2(96, 96))
        # self.hotbar_rect = self.render_slots(inv_surface, self.hotbar, pygame.Vector2(96, 594))
        # self.offhand_rect = self.render_slots(inv_surface, self.offhand, pygame.Vector2(288, 288))
        self.render_slots(inv_surface, self.common_slots, pygame.Vector2(96, 384))
        self.render_slots(inv_surface, self.clothes, pygame.Vector2(96, 96))
        self.render_slots(inv_surface, self.hotbar, pygame.Vector2(96, 594))
        self.render_slots(inv_surface, self.offhand, pygame.Vector2(288, 288))

        
        surface.blit(inv_surface, (0, 0))