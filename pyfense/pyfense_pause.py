# pyfense_pause.py
# contains class layer which is displayed when pressing esc

from pyglet.window import key
from pyglet import font

import cocos
from cocos import scene
from cocos.director import director
from cocos.text import *
from cocos.layer import *

import pyfense_resources

font.add_directory('data/Orbitron')
_font_ = 'Orbitron Light'
picto_damage = "assets/explosion_pictogram-01_small.png"
picto_rate = "assets/firerate_pictogram-02_small.png"


class PyFensePause(scene.Scene):

    def __init__(self):
        super().__init__()
        self.add(PauseLayer(), z=1)


class PauseLayer(Layer):

    is_event_handler = True

    def __init__(self):
        super().__init__()
        w, h = director.get_window_size()

        text0 = Label(
            '+++ Game Paused +++',
            font_name=_font_,
            font_size=30,
            anchor_x='center',
            anchor_y='center')

        self.key_font = {}
        self.key_font['font_name'] = 'font_'
        self.key_font['font_size'] = 20
        self.key_font['anchor_x'] = 'center'
        self.key_font['anchor_y'] = 'center'

        text1 = Label('Press Esc to resume game',
                      **self.key_font)
        text2 = Label('Press Q to quit game',
                      **self.key_font)
        text3 = Label('Press F to toggle Fullscreen',
                      **self.key_font)
        text4 = Label('Press V to toggle Vsync',
                      **self.key_font)
        text5 = Label('Press X to toggle FPS',
                      **self.key_font)
        text6 = Label('Press S to toggle Sound',
                      **self.key_font)

        text0.position = w/2., h/2. + 50
        text1.position = w/2., h/2. - 1 * (self.key_font['font_size'] + 8)
        text2.position = w/2., h/2. - 2 * (self.key_font['font_size'] + 8)
        text3.position = w/2., h/2. - 3 * (self.key_font['font_size'] + 8)
        text4.position = w/2., h/2. - 4 * (self.key_font['font_size'] + 8)
        text5.position = w/2., h/2. - 5 * (self.key_font['font_size'] + 8)
        text6.position = w/2., h/2. - 6 * (self.key_font['font_size'] + 8)

        self.add(text0)
        self.add(text1)
        self.add(text2)
        self.add(text3)
        self.add(text4)
        self.add(text5)
        self.add(text6)

        # tower information

        self.damage_pic = pyfense_resources.loadImage(picto_damage)
        self.rate_pic = pyfense_resources.loadImage(picto_rate)

        self.towerDamagePic = []
        self.towerFireratePic = []
        self.towerThumbnails = []
        for i in range(0, 3):
            self.towerThumbnails.append(cocos.sprite.Sprite(
                pyfense_resources.tower[i][1]["image"]))

        text_font = {
            'bold': True,
            'anchor_x': "left",
            'anchor_y': 'center',
            'font_size': 11,
            'color': (255, 109, 45, 255)
            }

        label4 = cocos.text.Label(" ", **text_font)
        label5 = cocos.text.Label(" ", **text_font)
        label6 = cocos.text.Label(" ", **text_font)
        self.towerDamageTexts = [label4, label5, label6]

        text_font['color'] = (0, 124, 244, 255)

        label7 = cocos.text.Label(" ", **text_font)
        label8 = cocos.text.Label(" ", **text_font)
        label9 = cocos.text.Label(" ", **text_font)
        self.towerFirerateTexts = [label7, label8, label9]

        self.menuMin_x = w/2. - self.towerThumbnails[0].width * (4 / 3)
        self.menuMin_y = 250

        for picture in range(0, len(self.towerThumbnails)):
            self.towerThumbnails[picture].position = (
                self.menuMin_x +
                picture * self.towerThumbnails[picture].width +
                self.towerThumbnails[picture].width / 2, self.menuMin_y)

            self.towerDamagePic.append(
                cocos.sprite.Sprite(self.damage_pic))
            self.towerDamagePic[picture].position = (
                self.menuMin_x + picture *
                self.towerThumbnails[picture].width +
                self.towerThumbnails[picture].width / 1.5 - 27,
                self.menuMin_y - self.towerThumbnails[picture].width / 2 - 10)

            self.towerDamageTexts[picture].element.text = (
                str(pyfense_resources.tower[picture][1]["damage"] *
                    pyfense_resources.tower[picture][1]["firerate"] / 1.))
            self.towerDamageTexts[picture].position = (
                self.menuMin_x + picture *
                self.towerThumbnails[picture].width +
                self.towerThumbnails[picture].width / 1.5 - 2,
                self.menuMin_y - self.towerThumbnails[picture].width / 2 - 10)

            self.towerFireratePic.append(
                cocos.sprite.Sprite(self.rate_pic))
            self.towerFireratePic[picture].position = (
                self.menuMin_x + picture *
                self.towerThumbnails[picture].width +
                self.towerThumbnails[picture].width / 1.5 - 34,
                self.menuMin_y - self.towerThumbnails[picture].width / 2 - 30)

            self.towerFirerateTexts[picture].element.text = (
                str(pyfense_resources.tower[picture][1]["firerate"]))
            self.towerFirerateTexts[picture].position = (
                self.menuMin_x +
                picture*self.towerThumbnails[picture].width +
                self.towerThumbnails[picture].width / 1.5 - 2,
                self.menuMin_y - self.towerThumbnails[picture].width / 2 - 30)

            self.add(self.towerThumbnails[picture])
            self.add(self.towerDamageTexts[picture])
            self.add(self.towerFirerateTexts[picture])
            self.add(self.towerDamagePic[picture])
            self.add(self.towerFireratePic[picture])

    def on_key_press(self, k, m):
        if k in (key.ENTER, key.ESCAPE, key.SPACE):
            director.pop()
            return True
        elif k == key.F:
            director.window.set_fullscreen(not director.window.fullscreen)
            return True
        elif k == key.V:
            director.window.set_vsync(not director.window.vsync)
            return True
        elif k == key.X:
            director.show_FPS = not director.show_FPS
            return True
        elif k == key.S:
            pyfense_resources.sounds = not pyfense_resources.sounds
            return True
        elif k == key.Q:
            director.pop()
            director.pop()
            return True

    def on_mouse_release(self, x, y, b, m):
        director.pop()
        return True
