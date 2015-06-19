"""
Manages highscore
"""
import pyglet
from pyglet.window import key
from pyglet import font

import cocos
from cocos.layer import *
from cocos.director import director
from cocos.text import *
from cocos.scene import Scene
import pyfense



font.add_directory('data/Orbitron')
_font_ = 'Orbitron Light'

def new_score(name, wave):
    highscore = readFile("data/highscore.txt")
    for i, entry in enumerate(highscore):
        if entry[0][0] == "#":
            continue
        else:
            if int(entry[1]) <= wave:
                continue
            else:
                #TODO write file to be implemented
                return True
    return False


def check_score(wave):

    highscore = readFile("data/highscore.txt")
    for i, entry in enumerate(highscore):
        if entry[0][0] == "#":
            continue
        else:
            if int(entry[1]) <= wave:
                continue
            else:
                return True
    return False


def get_score():

    highscore = readFile("data/highscore.txt")
    return highscore


def readFile(fileName):

    with open(fileName, "r") as openedFile:
        openedFile.readline()
        fileData = openedFile.readlines()
        splittedData = [row.split(", ") for row in fileData]
    return splittedData


class PyFenseLost(Scene):

    def __init__(self, reachedWave):
        super().__init__()
        self.wave = reachedWave
        self.add(LostLayer(self.wave), z=1)


class LostLayer(Layer):

    is_event_handler = True

    def __init__(self, wave):
        super().__init__()
        self.wave = wave
        self.in_highscore = check_score(wave)

        w, h = director.get_window_size()
        text1 = Label('+++ You Lost! +++',
                      font_name=_font_,
                      font_size=20,
                      anchor_x='center',
                      anchor_y='center')
        text1.position = w/2., h/2. + 25
        text2 = Label('You reached wave %d' % wave,
                      font_name=_font_,
                      font_size=20,
                      anchor_x='center',
                      anchor_y='center')
        text2.position = w/2., h/2.
        self.add(text1)
        self.add(text2)

    def on_key_press(self, k, m):
        if k in (key.ENTER, key.ESCAPE, key.SPACE, key.Q):
            if self.in_highscore:
                director.replace(Scene(SubmitScore(self.wave)))
            else:
                director.pop()
            return True

    def on_mouse_release(self, x, y, b, m):
            if self.in_highscore:
                director.replace(Scene(SubmitScore(self.wave)))
            else:
                director.pop()
            return True


class SubmitScore(Layer):

    is_event_handler = True

    def __init__(self, wave):
        super().__init__()
        w, h = director.get_window_size()
        self.wave = wave

        self.font_title = {}
        self.font_title['font_size'] = 72
        self.font_title['anchor_y'] = 'top'
        self.font_title['anchor_x'] = 'center'
        title = Label('GameOver', **self.font_title)
        title.position = (w/2., h)
        self.add(title, z=1)

        self.font_label = {}
        self.font_label['font_size'] = 40
        self.font_label['anchor_y'] = 'top'
        self.font_label['anchor_x'] = 'center'

        label = Label('Enter your name:', **self.font_label)
        label.position = (w/2., 600.)
        self.add(label)

        self.name = Label('', color=(192, 192, 192, 255), **self.font_label)
        self.name.position = (w/2., 530.)
        self.add(self.name)

    def on_key_press(self, k, m):

        if k == key.BACKSPACE:
            self.name.element.text = self.name.element.text[0:-1]
            return True
        elif k == key.ENTER:
            if len(self.name.element.text) <= 2:
                w, h = director.get_window_size()
                label = Label('Name too short:', **self.font_label)
                label.position = (w/2., 600.)
                self.add(label)
            else:
                new_score(self.name, self.wave)
                director.pop()
            return True
        elif k == key.ESCAPE:
            director.pop()
        return False

    def on_text(self, t):

        if t == '\r':
            return True

        self.name.element.text += t
