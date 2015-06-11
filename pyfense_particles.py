import cocos
import cocos.particle
from cocos.particle import ParticleSystem, Color
from cocos.euclid import Point2

import pyglet
import random



class Death(ParticleSystem):

    pic = pyglet.image.load('assets/particle.png')
    texture = pic.get_texture()

    # total particles
    total_particles = 2000

    # duration
    duration = 0.1

    # gravity
    gravity = Point2(0, 0)

    # angle
    angle = 90
    angle_var = 360

    # radial
    radial_accel = -150
    radial_accel_var = 20

    # speed of particles
    speed = 250
    speed_var = 50

    # emitter variable position
    pos_var = Point2(5, 5)

    # life of particles
    life = 0.9
    life_var = 0.1

    # emits per frame
    emission_rate = total_particles / life

    # color of particles
    # start_color = Color(1.0, 0.3, 0, 0.7)
    # start_color_var = Color(0.0, 0.1, 0., 0.4)
    # end_color = Color(1.0, 1, 1, 0)
    # end_color_var = Color(0, 0, 0, 0.2)

    start_color = Color(1, 0.53, 0, 1.0)
    start_color_var = Color(0.0, 0.0, 0.0, 0.0)
    end_color = Color(1, 1, 1, 0)
    end_color_var = Color(0.0, 0.0, 0.0, 0.05)

    # size, in pixels
    size = 15
    size_var = 3

    # blend additive
    blend_additive = True

    # color modulate
    color_modulate = True


class Explosion(ParticleSystem):


    # total particles
    total_particles = 500

    # duration
    duration = 0.05

    # gravity
    gravity = Point2(0, 0)

    # angle
    angle = 90.0
    angle_var = 360

    # radial
    radial_accel = -200
    radial_accel_var = 40

    # speed of particles
    speed = 100
    speed_var = 80

    # emitter variable position
    pos_var = Point2(5, 5)

    # life of particles
    life = 0.18
    life_var = 0.1

    # emits per frame
    emission_rate = total_particles / life

    # color of particles
    start_color = Color(0.76, 0.25, 0.12, 1.0)
    start_color_var = Color(0.0, 0.0, 0.0, 0.0)
    end_color = Color(0.0, 0.0, 0.0, 1.0)
    end_color_var = Color(0.0, 0.0, 0.0, 0.0)

    # size, in pixels
    size = 70.0
    size_var = 10.0

    # blend additive
    blend_additive = True

    # color modulate
    color_modulate = True


