import pygame
from enum import Enum

class Keys(Enum):
    K_1 = pygame.K_1
    K_2 = pygame.K_2
    K_3 = pygame.K_3
    K_4 = pygame.K_4
    K_5 = pygame.K_5
    K_6 = pygame.K_6
    K_7 = pygame.K_7
    K_8 = pygame.K_8
    K_9 = pygame.K_9
    K_0 = pygame.K_0

    K_EXCLAIM = pygame.K_EXCLAIM
    K_AT = pygame.K_AT
    K_HASHTAG = pygame.K_HASH
    K_DOLLAR = pygame.K_DOLLAR
    K_PERCENT = pygame.K_PERCENT
    K_CARET = pygame.K_CARET
    K_AMPERSAND = pygame.K_AMPERSAND
    K_ASTERISK = pygame.K_ASTERISK
    K_LPARENTHESIS = pygame.K_LEFTPAREN
    K_RPARENTHESIS = pygame.K_RIGHTPAREN

    K_q = pygame.K_q
    K_w = pygame.K_w
    K_e = pygame.K_e
    K_r = pygame.K_r
    K_t = pygame.K_t
    K_y = pygame.K_y
    K_u = pygame.K_u
    K_i = pygame.K_i
    K_o = pygame.K_o
    K_p = pygame.K_p

    K_a = pygame.K_a
    K_s = pygame.K_s
    K_d = pygame.K_d
    K_f = pygame.K_f
    K_g = pygame.K_g
    K_h = pygame.K_h
    K_j = pygame.K_j
    K_k = pygame.K_k
    K_l = pygame.K_l

    K_z = pygame.K_z
    K_x = pygame.K_x
    K_c = pygame.K_c
    K_v = pygame.K_v
    K_b = pygame.K_b
    K_n = pygame.K_n
    K_m = pygame.K_m

    K_MINUS = pygame.K_MINUS
    K_UNDERSCORE = pygame.K_UNDERSCORE
    K_EQUAL = pygame.K_EQUALS
    K_PLUS = pygame.K_PLUS
    K_BACKSPACE = pygame.K_BACKSPACE
    K_LBRACKET = pygame.K_LEFTBRACKET
    K_RBRACKET = pygame.K_RIGHTBRACKET
    K_LBRACE = "LBRACE"
    K_RBRACE = "RBRACE"
    K_BACKSLASH = pygame.K_BACKSLASH
    K_PIPE = "PIPE"

    K_SEMICOLON = pygame.K_SEMICOLON
    K_COLON = pygame.K_COLON
    K_SQUOTE = pygame.K_QUOTE
    K_DQUOTE = "DQUOTE"
    K_ENTER = pygame.K_RETURN
    K_COMMA = pygame.K_COMMA
    K_LESS = pygame.K_LESS
    K_PERIOD = pygame.K_PERIOD
    K_GREATER = pygame.K_GREATER
    K_SLASH = pygame.K_SLASH
    K_QUESTION = pygame.K_QUESTION
    K_RSHIFT = pygame.K_RSHIFT

    K_UP = pygame.K_UP
    K_LEFT = pygame.K_LEFT
    K_DOWN = pygame.K_DOWN
    K_RIGHT = pygame.K_RIGHT
    K_RCTRL = pygame.K_RCTRL
    K_RALT = pygame.K_RALT
    K_SPACE = pygame.K_SPACE
    K_LALT = pygame.K_LALT
    K_SUPER = pygame.K_LSUPER
    K_LCTRL = pygame.K_LCTRL

    K_LSHIFT = pygame.K_LSHIFT
    K_CAPSLOCK = pygame.K_CAPSLOCK
    K_TAB = pygame.K_TAB
    K_BACKQUOTE = pygame.K_BACKQUOTE
    K_TIDLE = "TIDLE"
    K_ESCAPE = pygame.K_ESCAPE
    K_PRINTSCREEN = pygame.K_PRINTSCREEN
    K_INSERT = pygame.K_INSERT
    K_DELETE = pygame.K_DELETE

    K_F1 = pygame.K_F1
    K_F2 = pygame.K_F2
    K_F3 = pygame.K_F3
    K_F4 = pygame.K_F4
    K_F5 = pygame.K_F5
    K_F6 = pygame.K_F6
    K_F7 = pygame.K_F7
    K_F8 = pygame.K_F8
    K_F9 = pygame.K_F9
    K_F10 = pygame.K_F10
    K_F11 = pygame.K_F11
    K_F12 = pygame.K_F12

def assign_key(keycode):
    extra_keycodes =    [pygame.K_BACKQUOTE, pygame.K_QUOTE, pygame.K_LEFTBRACKET, pygame.K_RIGHTBRACKET, pygame.K_BACKSLASH]
    shift_replacments = ["TIDLE",            "DQUOTE",       "LBRACE",             "RBRACE",              "PIPE"]
    mods = pygame.key.get_mods()
    if (keycode in extra_keycodes) and (mods & pygame.KMOD_SHIFT == 1):
        return Keys(shift_replacments[extra_keycodes.index(keycode)])
    else:
        return Keys(keycode)

def init_interrupt_dict():
    interrupt_dict = {}
    for key in Keys:
        interrupt_dict[key] = None

    return interrupt_dict
