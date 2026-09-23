from PygameEX import keyboard
from PygameEX import ScreenObject

class Screen:
    def __init__(self, clear_color: tuple[int, int, int] = (0, 0, 0)):
        self.clear_color = clear_color
        self.elements: list[ScreenObject] = []
        self.external_interrupts = {"keyboard": keyboard.init_interrupt_dict()}

    def set_clear_color(self, color: tuple[int, int, int]):
        self.scclear_color = color

    def add_element(self, element: ScreenObject):
        self.elements.append(element)

    def remove_element(self, element: ScreenObject):
        self.elements.pop(self.elements.index(element))

    def get_element_index(self, element: ScreenObject):
        return self.elements.index(element)

    def element_on_screen(self, element: ScreenObject):
        return element in self.elements

    def move_element_forward(self, element: ScreenObject, places: int = 1):
        element_index = self.elements.index(element)
        element = self.elements.pop(element_index)
        self.elements.insert(element_index + places, element)

    def register_keyboard_interrupt(self, key: keyboard.Keys, function):
        self.external_interrupts["keyboard"][key] = function