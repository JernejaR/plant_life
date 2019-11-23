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

# add pitagoras for dist:
def pithagora(pos1, pos2):
    d=pos1-pos2
    dist= np.sqrt((d[0])**2+(d[1])**2)
    return(dist)


class Leaf:
    def __init__(self, display_width = 300, display_height = 300, sun_x= 150, sun_y=150, leaf_x=0, leaf_y=0):
        self.display_width = display_width
        self.display_height = display_height
        self.position=np.hstack([leaf_x, leaf_y])
        self.sun=np.hstack([sun_x, sun_y])
        self.distance_to_sun=pithagora(self.position,self.sun)
        max_dist=np.sqrt((self.display_width/2)**2+(self.display_width/2)**2)
        self.production=(self.distance_to_sun/max_dist)*0.5
        

class Stem:
    def __init__(self, display_width = 300, display_height = 300, stalk_x= 150, stalk_y=150):
        
        self.display_width = display_width
        self.display_height = display_height
    #    self.shades=[[0,0], [self.display_width,0], [0,self.display_height],[self.display_width,self.display_height]]
               
        self.stalk_x=stalk_x
        self.stalk_y=stalk_y
        # maybe drop the x y altogether
        self.stalk_position=np.hstack([self.stalk_x, self.stalk_y])
        self.position = np.hstack([self.stalk_x, self.stalk_y])
        
        self.dist_to_stalk=pithagora(self.position,self.stalk_position)
        
        self.max_force = 1
        self.max_speed = 1
        self.min_speed = 0.001
       # self.perception = 50
        self.velocity = np.random.uniform(-0.001,0.001,2)
      #  self.velocity = [0.1,0.1]
        self.acceleration = np.zeros(2)
        self.alive = True
        self.edges() 
    
    def grow(self):
       
        self.position = self.position + self.velocity
        self.velocity = self.velocity + self.acceleration
        self.velocity = limit_mag(self.velocity, self.max_speed)
        
       # self.acceleration *= 0.01
        
        self.dist_to_stalk = pithagora(self.position,self.stalk_position)
        self.edges()
        
#    def bremz(self):
#        bremza=1/np.absolute(self.dist_to_stalk)
#        self.acceleration*=(bremza*0.0005)
#        self.acceleration = limit_mag(self.acceleration, self.max_force)  
    
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
        
        self.acceleration += steering*1.02
       
        self.acceleration = limit_mag(self.acceleration, self.max_force)    
 

    
    def go_to_light(self, sun_x,sun_y):
       sun=np.hstack([sun_x,sun_y])
       steering = np.zeros(2)
       diff = self.position - sun
       diff = diff / ((np.linalg.norm(self.position - sun)**2) + 0.00000001)
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


class Stalk:
    def __init__(self, display_width = 300, display_height = 300, max_stems=6):
        self.display_width = display_width
        self.display_height = display_height
        self.position=np.hstack([np.random.randint(0,self.display_width), np.random.randint(0, self.display_height)])
        self.number_of_stems= 3
        self.number_of_leaves=1
        self.own_stems=[Stem(display_width=self.display_width, display_height=self.display_height, stalk_x=self.position[0] , stalk_y=self.position[1]) for x in range(self.number_of_stems)]
        self.max_stems= max_stems
        self.sun=[300,300] ############################ sun position
        self.leaves=[Leaf(display_width =  self.display_width, display_height =  self.display_width, sun_x= self.sun[0], sun_y=self.sun[1], leaf_x=self.position[0], leaf_y=self.position[1])]
        #self.reach=pithagora(self.position,self.sun)-10
        self.reach=min(200,(pithagora(self.position,self.sun)-10))
        
    def grow_stems(self, all_stems):
        
        distances=[]
        power=np.sum([ii.production for ii in self.leaves])
        print(power)
        for stem in self.own_stems:
            
            if stem.dist_to_stalk < self.reach:
                stem.max_speed = power*1
            
                stem.grow()
                stem.stear(all_stems)
                stem.go_to_light(sun_x=self.sun[0], sun_y=self.sun[1])
                distances.append(stem.dist_to_stalk)
            else:
                stem.alive = False
        
            
        if min(distances)>20 and self.number_of_stems<self.max_stems :  ######################### dist setting
            self.number_of_stems+=1
            extra_stem = Stem(display_width=self.display_width, display_height=self.display_height, stalk_x=self.position[0] , stalk_y=self.position[1])
            self.own_stems = np.hstack([self.own_stems,extra_stem])
                
        else:
            pass
        
    def grow_leaves(self, all_leaves):
        for stem in self.own_stems:
             if int(stem.dist_to_stalk) % 40 == 0 and int(stem.dist_to_stalk)!=0:
                 print('new stuff')
                 new_leaf=Leaf(display_width = self.display_width, display_height =  self.display_width, sun_x= self.sun[0], sun_y=self.sun[1], leaf_x=stem.position[0], leaf_y=stem.position[1])
               
                 
                 print(len(all_leaves))

                 difs=[]
                 for leaf in all_leaves:
                    diff = pithagora(new_leaf.position, leaf.position)
                    if diff!=0:
                        difs.append(diff)
                        
                 print(len(difs), min(difs))
                 if min(difs)>30:
                        
                    self.leaves=np.hstack([self.leaves,new_leaf])
                    self.number_of_leaves+=1
                 else:
                    pass
                                                

        #print(self.number_of_leaves)

        
        