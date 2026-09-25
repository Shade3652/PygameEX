from __future__ import annotations  # 1. MUST BE LINE 1 OF THE FILE
from typing import TYPE_CHECKING
import pygame

if TYPE_CHECKING:   #This is a step that comes after python evaluates all imports but right before it type checks, so it'll import the class JUST in time for use!
    from PygameEX import PygameEX
    from PygameEX import Screen


class ScreenObject():
    def __init__(self, x, y, width, height):
        """Initializes a ScreenObject class. Not recommended to be called directly, as this should be used exclusivley by classes that inherit ScreenObject."""
        self.rect = pygame.Rect(x, y, width, height)

    def get_x(self):
        """Returns the x coordinate of the top-left corner of a ScreenObject"""
        return self.rect.left
    def get_y(self):
        """Returns the y coordinate of the top-left corner of a ScreenObject"""
        return self.rect.top
    def get_width(self):
        """Returns width of a ScreenObject"""
        return self.rect.width
    def get_height(self):
        """Returns height of a ScreenObject"""
        return self.rect.height
    def get_text(self):
        """Returns the text of any ScreenObject that has a text field"""
        return self.text

    def update_pos(self, new_x: int, new_y: int):
        """Updates the x & y of a ScreenObject"""
        self.rect = pygame.Rect(new_x, new_y, self.get_width(), self.get_height())
    def update_wh(self, new_w: int, new_h: int):
        """Updates the width & height of a ScreenObject. Not recommended for usage unless you know what you're doing."""
        self.rect = pygame.Rect(self.rect.left, self.rect.top, new_w, new_h)


    def was_clicked(self, x: int, y: int, window: PygameEX):
        """Returns True if the ScreenObject was clicked"""
        return  self.rect.collidepoint((x, y)) and window.element_on_window(self)

    def draw(self, window: pygame.surface.Surface):
        """Draws the ScreenObject onto the canvas. do NOT call this unless you REALLY, REALLY know what you're doing"""
        self.draw_spec(window)


class ScreenText(ScreenObject):
    def __init__(self, text: str, x: int, y: int, text_font: str = "Arial", text_size: int = 20, color: tuple[int, int, int] = (0, 0, 0)):
        """Initiaizes a ScreenText Object"""

        self.font = pygame.font.SysFont(text_font, text_size)
        self.color = color
        self.text_size = text_size

        self.text = text

        max_width = 0
        for line in self.text.splitlines():
            if self.font.size(line)[0] > max_width:
                max_width = self.font.size(line)[0]

        height = 0
        for line in self.text.splitlines():
            height = height + self.font.size(line)[1]

        super().__init__(x, y, max_width, height)

    def add_text(self, char: str):
        """Appends the given text to the """
        if char == "\b":
            if len(self.text) != 0:
                self.text = self.text[:len(self.text) - 1]
        else:
            self.text = self.text + char
            lines = self.text.splitlines()
            max_width = 0
            for line in lines:
                if self.font.size(line)[0] > max_width:
                    max_width = self.font.size(line)[0]

        height = 0
        for line in self.text.splitlines():
            height = height + self.font.size(line)[1]

        self.update_wh(max_width, height)

    def update_text(self, text: str):
        """Sets the ScreenText's text to the given text"""
        self.text = text
        max_width = 0
        for line in self.text.splitlines():
            if self.font.size(line)[0] > max_width:
                max_width = self.font.size(line)[0]

        height = 0
        for line in self.text.splitlines():
            height = height + self.font.size(line)[1]

        self.update_wh(max_width, height)


    def update_font(self, font: str):
        """Updates the font to the supplied one. Look in the system fonts folder to see what options are availible."""
        self.font = pygame.font.SysFont(font, self.text_size)
        max_width = 0
        for line in self.text.splitlines():
            if self.font.size(line)[0] > max_width:
                max_width = self.font.size(line)[0]

        height = 0
        for line in self.text.splitlines():
            height = height + self.font.size(line)[1]

        self.update_wh(max_width, height)


    def update_text_size(self, size: int):
        """Updates the text size"""
        self.text_size = size
        self.font = pygame.font.SysFont(self.font.name, self.text_size)
        max_width = 0
        for line in self.text.splitlines():
            if self.font.size(line)[0] > max_width:
                max_width = self.font.size(line)[0]

        height = 0
        for line in self.text.splitlines():
            height = height + self.font.size(line)[1]
        self.update_wh(max_width, height)


    def get_text_size(self):
        """Returns the text size"""
        return self.text_size
    def get_font(self):
        """Returns the font name"""
        return self.font.name


    def draw_spec(self, screen: pygame.surface.Surface):
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

    def draw_spec(self, screen: pygame.surface.Surface):
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
    def draw_spec(self, window: pygame.surface.Surface):
        pygame.draw.rect(window, self.color, self.rect)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        window.blit(text_surf, text_rect)

class ScreenTextBox(ScreenObject):
    def __init__(self, x: int, y: int, width: int, height: int, max_len: int = None, color: tuple[int, int, int] = (255, 255, 255), default_text: str = "Type here",
                 default_text_color: tuple[int, int, int] = (175, 175, 175), text_color: tuple[int, int, int] = (0, 0, 0), text_size: int = 20, text_font: str = "Arial"):

        super().__init__(x, y, width, height)
        self.default_text = default_text
        self.color = color,
        self.default_text_color = default_text_color
        self.text_color = text_color
        self.font = pygame.font.SysFont(text_font, text_size)
        self.max_len = max_len

        self.text = ""

    def add_text(self, char: str):
        if char == "\b":
            if len(self.text) != 0:
                self.text = self.text[:len(self.text) - 1]
        else:
            if self.font.size(self.text + char)[0] <= self.rect.width - 3:
                self.text = self.text + char

    def get_text(self):
        return self.text

    def update_color(self, color: tuple[int, int, int]):
        self.color = color

    def draw_spec(self, window: pygame.surface.Surface):
        pygame.draw.rect(window, self.color, self.rect)

        if len(self.text) != 0:
            text_surf = self.font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(topleft=self.rect.topleft)
        else:
            text_surf = self.font.render(self.default_text, True, self.default_text_color)
            text_rect = text_surf.get_rect(topleft=self.rect.topleft)

        text_rect.x = text_rect.x + 3
        window.blit(text_surf, text_rect)
