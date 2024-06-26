import pygame
from typing import List, Sequence

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
        self.hotbar: List[InventoryItem | None] = [None] * 9
        self.clothes: List[InventoryItem | None] = [None] * 4
        self.offhand: None
        self.shown = False
        
        self.moving_item = None
    
    def handle_event(self, event: pygame.event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
        if event.type == pygame.MOUSEBUTTONUP:
            pass
        if event.type == pygame.MOUSEMOTION:
            pass
        print(event)
    
    def display(self, surface: pygame.Surface) -> None:
        if not self.shown:
            return
        pygame.draw.rect(surface, (200, 200, 200), (0, 0, 800, 800))
        
        for i in range(len(self.common_slots)):
            for j in range(len(self.common_slots[i])):
                item = self.common_slots[i][j]
                item_surface = empty_slot()
                if item is not None:
                    item.display_icon(item_surface, (0, 0))
                surface.blit(item_surface, (j * 64, i * 64) + pygame.Vector2(96, 384))
                
        
        for i in range(len(self.clothes)):
            item = self.clothes[i]
            item_surface = empty_slot()
            if item is not None:
                item.display_icon(item_surface, (0, 0))
            surface.blit(item_surface, (0, i * 64) + pygame.Vector2(96, 96))
            
        for i in range(len(self.hotbar)):
            item = self.hotbar[i]
            item_surface = empty_slot()
            if item is not None:
                item.display_icon(item_surface, (0, 0))
            surface.blit(item_surface, (i * 64, 0) + pygame.Vector2(96, 594))
            
        item = self.offhand
        item_surface = empty_slot()
        if item is not None:
            item.display_icon(item_surface, (0, 0))
        surface.blit(item_surface, (64, 0) + pygame.Vector2(224, 288))