# pyfense_entities.py
# contains the layer on which all enemies and towers are placed (layer)
import pyglet

import cocos
from cocos.director import *
from pyglet.window import key

from pyfense_tower import *
from pyfense_enemy import *
from pyfense_projectile import *
from pyfense_hud import *

# Just for testing different enemies
import random

import pyfense_particles


class PyFenseEntities(cocos.layer.Layer, pyglet.event.EventDispatcher):
    is_event_handler = True

    def __init__(self, path, startTile):
        super().__init__()
        self.enemies = []
        self.spawnedEnemies = 0
        self.diedEnemies = 0
        self.towers = []
        self.projectiles = []
        self.schedule(self.update)
        self.path = path
        self.startTile = startTile

        # update runs every tick
    def update(self, dt):
        self.hasEnemyReachedEnd()

    def nextWave(self, waveNumber):
        self.schedule_interval(self.addEnemy, 1, self.startTile, self.path)
        self.spawnedEnemies = 0
        self.diedEnemies = 0

    def buildTower(self, tower):
        tower.push_handlers(self)
        self.towers.append(tower)
        self.add(tower, z=2)
        return tower.attributes["cost"]
                
    def getTowerAt(self, position):
        for tower in self.towers:
            if tower.position == position:
                return tower
        
    def removeTower(self, position):
        tower = self.getTowerAt(position)
        self.remove(tower)
        self.towers.remove(tower)
        return tower.attributes["cost"]

    def on_projectile_fired(self, tower, target, projectileimage, towerNumber,
                            rotation, projectileVelocity, damage):
        projectile = PyFenseProjectile(tower, target, projectileimage,
                                       towerNumber, rotation,
                                       projectileVelocity, damage)
        self.projectiles.append(projectile)
        projectile.push_handlers(self)
        self.add(projectile, z=1)

    def on_enemy_hit(self, projectile, target, towerNumber):
        explosion = eval('pyfense_particles.Explosion' + str(towerNumber) + '()')
        explosion.position = target.position
        self.add(explosion, z = 4)
        clock.schedule_once(lambda dt, x: self.remove(x), 1 ,explosion)
        target.healthPoints -= projectile.damage
        self.remove(projectile)
        self.projectiles.remove(projectile)
        target.updateHealthBar()
        if target in self.enemies and target.healthPoints <= 0:
            self.remove(target.healthBar)
            self.remove(target)
            self.enemies.remove(target)
            deathAnimation = pyfense_particles.Death()
            deathAnimation.position = target.position
            self.add(deathAnimation, z = 4)
            clock.schedule_once(lambda dt, x: self.remove(x), 2, deathAnimation)
            self.diedEnemies += 1
            self.dispatch_event('on_enemy_death', target)
            self.isWaveFinished()

    def isWaveFinished(self):
        # TODO: change hardcoded enemies per wave number
        # to be read from cfg file, wave specific
        if self.spawnedEnemies >= 10:
            self.unschedule(self.addEnemy)
            if self.diedEnemies == self.spawnedEnemies:
                self.dispatch_event('on_next_wave')

    def addEnemy(self, dt, startTile, path):
        # Just for testing different enemies
        number = random.randint(0, 1)
        position = startTile
        enemy = PyFenseEnemy(position, number, 1, 1, path) #constructor: (position, enemyname, lvl, wave, path)
        self.enemies.append(enemy)
        self.spawnedEnemies += 1
        self.add(enemy, z=1)
        self.add(enemy.healthBar, z=3)
        self.isWaveFinished()
        
    # Removes enemy from entity when no action is running,
    # ie the enemy has reached
    def hasEnemyReachedEnd(self):
        if self.enemies and not self.enemies[0].actions:
            self.dispatch_event('on_enemy_reached_goal')
            self.remove(self.enemies[0])
            self.remove(self.enemies[0].healthBar)
            self.enemies.remove(self.enemies[0])
            self.diedEnemies += 1
            self.isWaveFinished()
            
    #Overrites the Esc key and quits the game on "Q"        
    def on_key_press( self, k, m ):
        if k == key.ESCAPE:
            print("Pause Menu to be implemented")
            return True
        if k == key.Q:
            director.pop()


PyFenseEntities.register_event_type('on_next_wave')
PyFenseEntities.register_event_type('on_enemy_death')
PyFenseEntities.register_event_type('on_enemy_reached_goal')
