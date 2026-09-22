from __future__ import annotations  # 1. MUST BE LINE 1 OF THE FILE
from typing import TYPE_CHECKING
import pygame

if TYPE_CHECKING:   #This is a step that comes after python evaluates all imports but right before it type checks, so it'll import the class JUST in time for use!
    from PygameEX import PygameEX


class ScreenObject():
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def get_x(self):
        return self.rect.left
    def get_y(self):
        return self.rect.top
    def get_width(self):
        return self.rect.width
    def get_height(self):
        return self.rect.height
    def get_text(self):
        return self.text
    def get_text_size(self):
        return self.text_size
    def get_font(self):
        return self.font.name

    def update_pos(self, new_x: int, new_y: int):
        self.rect = pygame.Rect(new_x, new_y, self.get_width(), self.get_height())
    def update_wh(self, new_w: int, new_h: int):
            self.rect = pygame.Rect(self.rect.left, self.rect.top, new_w, new_h)

    
    def was_clicked(self, x: int, y: int, window: PygameEX):
        return  self.rect.collidepoint((x, y)) and window.element_on_screen(self)


class ScreenText(ScreenObject):
    def __init__(self, text: str, x: int, y: int, text_font: str = "Arial", text_size: int = 20, color: tuple[int, int, int] = (0, 0, 0)):

        self.font = pygame.font.SysFont(text_font, text_size)
        self.color = color
        self.text_size = text_size

        (width, height) = self.font.size(text)

        super().__init__(x, y, width, height)
        self.text = text


    def update_text(self, text: str):
        self.text = text
        (width, height) = self.font.size(text)
        self.rect = pygame.Rect(self.rect.left, self.rect.top, width, height)

    def update_font(self, font: str):
        self.font = pygame.font.SysFont(font, self.text_size)
        (width, height) = self.font.size(self.text)
        self.update_wh(width, height)

    def update_text_size(self, size: int):
            self.text_size = size
            self.font = pygame.font.SysFont(self.font.name, self.text_size)
            (width, height) = self.font.size(self.text)
            self.update_wh(width, height)
    

    def draw(self, screen: PygameEX):
        text_surf = self.font.render(self.text, True, self.color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

class ScreenImage(ScreenObject):
    def __init__(self, image_path: str, x: int, y: int):
        self.image = pygame.image.load(image_path)
        (width, height) = self.image.get_size()

        super().__init__(x, y, width, height)

    def resize_image(self, width: int, height: int):
        self.image = pygame.transform.scale(self.image, (width, height))
        (width, height) = self.image.get_size()
        self.update_wh(width, height)

    def scale_image(self, scale_factor: float):
            self.image = pygame.transform.scale(self.image, (int(self.get_width() * scale_factor), int(self.get_height() * scale_factor)))
            (width, height) = self.image.get_size()
            self.update_wh(width, height)

    def draw(self, screen: PygameEX):
        screen.blit(self.image, (self.get_x(), self.get_y()))



class ScreenButton(ScreenObject):

    #Initializes a button with the desired parameretrs & flags
    def __init__(self, x: int, y: int, width: int, height: int, text: str, text_size: int = 20, 
                 text_font: str = "Arial", text_color: tuple[int, int, int] = (0, 0, 0), color: tuple[int, int, int] = (255, 255, 255), click_callback = None):
        #This is all basic object init stuff
        super().__init__(x, y, width, height)
        self.text = text
        self.text_color = text_color
        self.color = color

        self.click_callback = click_callback

        #The pygame way to create a font renderer.
        #Please note that this has a lot of boiler plate for a python function,
        #BUT IT STILL HAS LESS THAN SYSTEM.OUT.PRINTLN
        self.font = pygame.font.SysFont(text_font, text_size)

    #Draws the button on the given surface
    def draw(self, screen: PygameEX):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
