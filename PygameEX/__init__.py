import pygame
from .screen_object import *
from .keyboard import *
from enum import Enum
from .screen import *

class PygameEX:
    def __init__(self, window_w: int, window_h: int, title: str = "Pygame Project", screen: Screen = None):
        pygame.init()
        self.window = pygame.display.set_mode((window_w, window_h))
        pygame.display.set_caption(title)

        self.screen = screen
        self.elements: list[ScreenObject] = []
        self.external_interrupts = {"keyboard": keyboard.init_interrupt_dict()}

        self.event_queue = []

    def get_events(self):
        return_queue = self.event_queue
        self.event_queue = []
        return return_queue

    def refresh(self):
        self.window.fill(self.screen.clear_color)
        for element in self.screen.elements:
            element.draw(self.window)
        for element in self.elements:
            element.draw(self.window)
        pygame.display.flip()

        for pygame_event in pygame.event.get():
            try:
                event = _Event(pygame_event)
                if event.type == event_types.LEFT_CLICK:
                    for element in self.screen.elements:
                        if type(element) == ScreenButton:
                            (x, y) = event.pos
                            if element.click_callback != None and element.was_clicked(x, y, self):
                                element.click_callback()

                    for element in self.elements:
                        if type(element) == ScreenButton:
                            (x, y) = event.pos
                            if element.click_callback != None and element.was_clicked(x, y, self):
                                element.click_callback()

                if event.type == event_types.KEY_PRESS:
                    if not self.external_interrupts["keyboard"][event.key] == None:
                        self.external_interrupts["keyboard"][event.key]()
                self.event_queue.append(event)
            except ValueError:
                #This event is not implemented in the wrapper yet, so just ignore it :D
                pass

    def add_element(self, element: ScreenObject):
        self.elements.append(element)

    def remove_element(self, element: ScreenObject):
        self.elements.pop(self.elements.index(element))

    def get_element_index(self, element: ScreenObject):
        return self.elements.index(element)

    def element_on_window(self, element: ScreenObject):
        return element in self.elements or element in self.screen.elements

    def move_element_forward(self, element: ScreenObject, places: int = 1):
        element_index = self.elements.index(element)
        element = self.elements.pop(element_index)
        self.elements.insert(element_index + places, element)

    def get_current_screen(self):
        return self.screen

    def get_mouse_pos(self):
        return pygame.mouse.get_pos()

    def register_keyboard_interrupt(self, key: keyboard.Keys, function):
        self.external_interrupts["keyboard"][key] = function

    def use_screen(self, screen: Screen):
        self.screen = screen



class event_types(Enum):
    QUIT = pygame.QUIT
    LEFT_CLICK = "left_click"
    SCROLL_WHEEL_CLICK = "scroll_wheel_click"
    RIGHT_CLICK = "right_click"
    KEY_PRESS = "key_press"


#Prefixed with an underscore so that if you run "from Pygame import *", it isn't auto imported.
class _Event:
    def __init__(self, type_: pygame.event):
        self.type = self.assign_event_type(type_)

    def assign_event_type(self, pygame_event: pygame.event):
        one_to_one = [pygame.QUIT]
        processing =           [pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN]
        processing_functions = [self.__mouse_button,    self.__key_press]


        if pygame_event.type in one_to_one:
            return event_types(pygame_event.type)
        else:
            return processing_functions[processing.index(pygame_event.type)](pygame_event)

    def __mouse_button(self, event: event_types):

        self.pos = event.pos

        if event.button == 1:
            return event_types("left_click")
        elif event.button == 2:
            return event_types("scroll_wheel_click")
        elif event.button == 3:
            return event_types("right_click")

    def __key_press(self, event: event_types):
            self.key = keyboard.assign_key(event.key)

            return event_types("key_press")