# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 13:07:11 2019

@author: jru025
"""


import pygame
import sys
import numpy as np
from stem_multi import Stem, Stalks
from video import make_video

from pygame.locals import *


def timerFunc(active=1):
    active+=1
   # print('increased stems to'+str(active))
    return(active)


class Simulation:
    def __init__(self, plants, stems):
        self.display_width = 600
        self.display_height = 600
        self.n_stalks=plants
        self.n_stems_per_stalk=stems
        
        self.display = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption("Plant life")
        
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.stalks= [Stalks(display_width=self.display_width, display_height=self.display_height) for x in range(self.n_stalks)]
        stalk1_x=self.stalks[0].position[0]
        stalk1_y=self.stalks[0].position[1]
        self.stems = [Stem(display_width=self.display_width, display_height=self.display_height, stalk_x=stalk1_x , stalk_y=stalk1_y) for x in range(self.n_stems_per_stalk)]
        if self.n_stalks >1:
            for ii in self.stalks[1:]:
                extra_stems = [Stem(display_width=self.display_width, display_height=self.display_height, stalk_x= ii.position[0], stalk_y=ii.position[1]) for x in range(self.n_stems_per_stalk)]
                self.stems = np.hstack([self.stems,extra_stems])
        self.stems= np.random.permutation(self.stems)
 
        self.active_stems= 1
   
    def run(self):
        
        pygame.time.set_timer(USEREVENT+1, 1000)
 #       save_screen = make_video(self.display)  # initiate the video generator
  #      video = False  # at start: video not active
                
        while self.running:
        
           # self.display.fill((0,0,0))
            for stalk in self.stalks:
                pygame.draw.circle(self.display, (200,201,70), (int(stalk.position[0]), int(stalk.position[1])), int(3))
    
            #draw stems:
            for stem in self.stems[:self.active_stems]:

                try:
                    
                    pygame.draw.circle(self.display, (97,201,97), (int(stem.position[0]), int(stem.position[1])), int(1))
                    stem.grow()
                    stem.stear(self.stems)
                    stem.go_to_light()
                  #  stem.avoid_shade()
                   
                    
                except Exception as e:
                    
                    pass
      
#            
            #Make closing out possible
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
                elif event.type == USEREVENT:
                    self.active_stems=timerFunc(self.active_stems) #calling the function wheever we get timer event.
#                elif event.type == pygame.KEYDOWN and event.key == pygame.K_v:
#                    video = not video
#                
#            if video:
#                next(save_screen)  # call the generator
#                print("IN main")  # delete, just for demonstration
#
  
            pygame.display.update()
            self.clock.tick(15)
            

        pygame.quit()

spawn_interval=500

pygame.init()
pygame.time.set_timer(USEREVENT, spawn_interval)
    
if __name__ == "__main__":
    simulation = Simulation(plants= 3, stems=6)
    simulation.run()