# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 13:07:11 2019

@author: jru025
"""


import pygame
import numpy as np
from stem_multi_LEAVES import Stem, Stalk
from video import make_video

from pygame.locals import *



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
        
        self.stalks= [Stalk(display_width=self.display_width, display_height=self.display_height,max_stems=self.n_stems_per_stalk) for x in range(self.n_stalks)]
     #   stalk1_x=self.stalks[0].position[0]
    #    stalk1_y=self.stalks[0].position[1]
        all_stems=self.stalks[0].own_stems
        for ii in self.stalks[1:]:
            stems=ii.own_stems
            all_stems = np.hstack([all_stems,stems])
        self.stems=all_stems
        
        all_leaves=self.stalks[0].leaves
        for ii in self.stalks[1:]:
            leaves=ii.leaves
            all_leaves = np.hstack([all_leaves,leaves])
        self.leaves=all_leaves
        
       # self.sun=[300,300]
        
    def run(self):
        
    #    pygame.time.set_timer(USEREVENT+1, 1000)
        save_screen = make_video(self.display)  # initiate the video generator
        video = False  # at start: video not active
                
        while self.running:
        
           # self.display.fill((0,0,0))
            for stalk in self.stalks:
                pygame.draw.circle(self.display, (200,201,70), (int(stalk.position[0]), int(stalk.position[1])), int(3))
    
            
                try:
                    stalk.grow_stems(self.stems)     
                    stalk.grow_leaves(self.leaves)                          
                    
                except Exception as e:
                    print(e)
                    pass
                
            all_stems=self.stalks[0].own_stems
            for ii in self.stalks[1:]:
                stems=ii.own_stems
                all_stems = np.hstack([all_stems,stems])
            self.stems=all_stems
            
                              
            for stem in self.stems:
                if stem.alive == True:
                    pygame.draw.circle(self.display, (97,201,97), (int(stem.position[0]), int(stem.position[1])), int(1))
               
                
            for leaf in self.leaves:
                pygame.draw.circle(self.display, (97,201,97), (int(leaf.position[0]), int(leaf.position[1])), int(8))

            all_leaves=self.stalks[0].leaves
            for ii in self.stalks[1:]:
                leaves=ii.leaves
                all_leaves = np.hstack([all_leaves,leaves])
            self.leaves=all_leaves
            
            #Make closing out possible
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            #    elif event.type == USEREVENT:
             #       self.active_stems=timerFunc(self.active_stems) #calling the function wheever we get timer event.
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_v:
                    video = not video
#                
            if video:
                next(save_screen)  # call the generator
                print("IN main")  # delete, just for demonstration

  
            pygame.display.update()
            self.clock.tick(15)
            

        pygame.quit()


pygame.init()

    
if __name__ == "__main__":
    simulation = Simulation(plants= 5, stems=6)
    simulation.run()