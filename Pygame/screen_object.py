import pygame

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

    def update_pos(self, new_x, new_y):
        self.rect = pygame.Rect(new_x, new_y, self.get_width(), self.get_height())
    def update_wh(self, new_w, new_h):
            self.rect = pygame.Rect(self.rect.left, self.rect.top, new_w, new_h)


class ScreenText(ScreenObject):
    def __init__(self, text, x, y, text_font = "Arial", text_size = 20, color = (0, 0, 0)):

        self.font = pygame.font.SysFont(text_font, text_size)
        self.color = color
        self.text_size = text_size

        (width, height) = self.font.size(text)

        super().__init__(x, y, width, height)
        self.text = text


    def update_text(self, text):
        self.text = text
        (width, height) = self.font.size(text)
        self.rect = pygame.Rect(self.rect.left, self.rect.top, width, height)

    def update_font(self, font):
        self.font = pygame.font.SysFont(font, self.text_size)
        (width, height) = self.font.size(self.text)
        self.update_wh(width, height)

    def update_text_size(self, size):
            self.text_size = size
            self.font = pygame.font.SysFont(self.font.name, self.text_size)
            (width, height) = self.font.size(self.text)
            self.update_wh(width, height)
    

    def draw(self, screen):
        text_surf = self.font.render(self.text, True, self.color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

class ScreenImage(ScreenObject):
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path)
        (width, height) = self.image.get_size()

        super().__init__(x, y, width, height)

    def resize_image(self, width, height):
        self.image = pygame.transform.scale(self.image, (width, height))
        (width, height) = self.image.get_size()
        self.update_wh(width, height)

    def scale_image(self, scale_factor):
            self.image = pygame.transform.scale(self.image, (int(self.get_width() * scale_factor), int(self.get_height() * scale_factor)))
            (width, height) = self.image.get_size()
            self.update_wh(width, height)

    def draw(self, screen):
        screen.blit(self.image, (self.get_x(), self.get_y()))



class ScreenButton(ScreenObject):

    #Initializes a button with the desired parameretrs & flags
    def __init__(self, x, y, width, height, text, text_size = 20, text_font = "Arial", text_color = (0, 0, 0), color = (255, 255, 255), click_callback = None):
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
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def was_clicked(self, x, y, window):
        return  self.rect.collidepoint((x, y)) and self in window.elements
