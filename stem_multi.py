# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 10:46:13 2019

@author: jru025
"""

import numpy as np


def set_mag(vector, new_mag):
    mag = np.linalg.norm(vector)
    vx = vector[0] * (new_mag/mag)
    vy = vector[1] * (new_mag/mag)
    return np.array([vx,vy])

def limit_mag(vector, max_mag):
    if np.linalg.norm(vector) > max_mag:
        return(set_mag(vector, max_mag))
    else:
        return(vector)

# 
class Stalks:
    def __init__(self, display_width = 300, display_height = 300):
        self.display_width = display_width
        self.display_height = display_height
        self.position=np.hstack([np.random.randint(0,self.display_width), np.random.randint(0, self.display_height)])

        
        



class Stem:
    def __init__(self, display_width = 300, display_height = 300, stalk_x= 150, stalk_y=150):
        
        self.display_width = display_width
        self.display_height = display_height
        self.shades=[[0,0], [self.display_width,0], [0,self.display_height],[self.display_width,self.display_height]]
        self.sun= np.hstack([self.display_width/2, self.display_height/2]) 
        self.stalk_x=stalk_x
        self.stalk_y=stalk_y
        
        
        self.position = np.hstack([self.stalk_x, self.stalk_y])        
        self.max_force = 3
        self.max_speed = 1
        self.min_speed = 0.001
       # self.perception = 50
        self.velocity = np.random.uniform(-0.001,0.001,2)
      #  self.velocity = [0.1,0.1]
        self.acceleration = np.zeros(2)
        self.alive = True
     #   self.max_boids_considered = 5
        self.edges()
    
    def grow(self):
        self.velocity += self.acceleration
        self.position = self.position + self.velocity
        self.velocity = self.velocity + self.acceleration
        self.velocity = limit_mag(self.velocity, self.max_speed)
        
        self.acceleration *= 0.01
        
    
    def stear(self, stems): # add stalk avoidance! 
        steering = np.zeros(2)


        effectors = []
        for stem in stems:
            if stem != self:
                effectors.append(stem)
       
        
        if len(effectors) > 0:
            for stem in effectors:
                diff = self.position - stem.position
                diff = diff / ((np.linalg.norm(self.position - stem.position)**2) + 0.00000001)
                steering += diff
            
            steering = steering / len(effectors)
            
        steering = set_mag(steering, self.max_speed)
        steering -= self.velocity
        steering = limit_mag(steering, self.max_force)
        
        self.acceleration += steering
       
        self.acceleration = limit_mag(self.acceleration, self.max_force)    
      
    def avoid_shade(self):
       steering = np.zeros(2)
       if len(self.shades) > 0:
            for shade in self.shades:
                diff = self.position - shade
                diff = diff / ((np.linalg.norm(self.position - shade)**2) + 0.00000001)
                steering += diff
            
            steering = steering / len(self.shades)
       steering = set_mag(steering, self.max_speed)
       steering -= self.velocity
       steering = limit_mag(steering, self.max_force)
        
       self.acceleration += steering*1
       
       self.acceleration = limit_mag(self.acceleration, self.max_force)  

    
    def go_to_light(self):
       steering = np.zeros(2)
       diff = self.position - self.sun
       diff = diff / ((np.linalg.norm(self.position - self.sun)**2) + 0.00000001)
       steering -= diff
            
            
       steering = set_mag(steering, self.max_speed)
       steering -= self.velocity
       steering = limit_mag(steering, self.max_force)
        
       self.acceleration += steering*1
       
       self.acceleration = limit_mag(self.acceleration, self.max_force)  
      
     
        
    def edges(self):
        for i, p in zip([0,1], [self.display_width,self.display_height]):
            if self.position[i] < 0:
                self.position[i] = p
            elif self.position[i] > p:
                self.position[i] = 0
        
        