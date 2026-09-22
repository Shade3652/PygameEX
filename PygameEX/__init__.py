import pygame
from .screen_object import *
from .keyboard import *
from enum import Enum

class PygameEX:
    def __init__(self, screen_w: int, screen_h: int, title: str = "Pygame Project", clear_color: tuple[int, int, int] = (0, 0, 0)):
        pygame.init()
        self.window = pygame.display.set_mode((screen_w, screen_h))
        pygame.display.set_caption(title)

        self.clear_color = clear_color
        self.elements = []
        self.external_interrupts = {"keyboard": keyboard.init_interrupt_dict()}

        self.screens = ["Screen 0"]
        self.screen_data = [[]]
        self.screen_interrupts = [{}]

        self.transcendental_elements = []

        self.active_screen = 0
        self.event_queue = []

    def get_events(self):
        return_queue = self.event_queue
        self.event_queue = []
        return return_queue

    def refresh(self):
        self.window.fill(self.clear_color)
        for element in self.elements:
            element.draw(self.window)
        for element in self.transcendental_elements:
            element.draw(self.window)
        pygame.display.flip()

        for pygame_event in pygame.event.get():
            try:
                event = _Event(pygame_event)
                if event.type == event_types.LEFT_CLICK:
                    for element in self.elements:
                        if type(element) == ScreenButton:
                            (x, y) = event.pos
                            if element.click_callback != None and element.was_clicked(x, y, self):
                                element.click_callback()

                    for element in self.transcendental_elements:
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

    def set_clear_color(self, color: tuple[int, int, int]):
        self.clear_color = color

    def add_element(self, element: ScreenObject):
        self.elements.append(element)

    def remove_element(self, element: ScreenObject):
        self.elements.pop(self.elements.index(element))

    def add_transcendental_element(self, element: ScreenObject):
        self.transcendental_elements.append(element)

    def remove_transcendental_element(self, element: ScreenObject):
        self.transcendental_elements.pop(self.transcendental_elements.index(element))

    def get_element_index(self, element: ScreenObject):
        return self.elements.index(element)

    def element_on_screen(self, element: ScreenObject):
        return element in self.elements or element in self.transcendental_elements

    def move_element_forward(self, element: ScreenObject, places: int = 1):
        element_index = self.elements.index(element)
        element = self.elements.pop(element_index)
        self.elements.insert(element_index + places, element)

    def create_screen(self, name: str):
        self.screens.append(name)
        self.screen_data.append([])
        self.screen_interrupts.append({"keyboard": keyboard.init_interrupt_dict()})

    def get_current_screen(self):
        return self.screens[self.active_screen]

    def swap_screens(self, new_screen_name: str):
        self.screen_data[self.active_screen] = self.elements
        self.screen_interrupts[self.active_screen] = self.external_interrupts

        self.active_screen = self.screens.index(new_screen_name)

        self.elements = self.screen_data[self.active_screen]
        self.external_interrupts = self.screen_interrupts[self.active_screen]

    def destroy_screen(self, screen_name: str):
        current_screen_name = self.screens[self.active_screen]
        screen_to_pop = self.screens.index(screen_name)
        self.screens.pop(screen_to_pop)
        self.screen_data.pop(screen_to_pop)
        self.screen_interrupts.pop(screen_to_pop)
        self.active_screen = self.screens.index(current_screen_name)

    def screen_exists(self, screen_name: str):
        return screen_name in self.screens

    def get_mouse_pos(self):
        return pygame.mouse.get_pos()

    def register_keyboard_interrupt(self, key: keyboard.Keys, function):
        self.external_interrupts["keyboard"][key] = function



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