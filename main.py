import pygame
import random

'''
the class that constructs the application window, will be a 25x25 grid
'''
class appWindow():
    
    #global variable, width of the application window
    WIDTH = 700
    
    #intialize the app window with parameters
    def __init__(self, coordinatePoint):
        self.animation_speed = 8
        self.grid_size = 25 #25x25 grid
        self.box_width = 35 #size of each box in the maze/grid
        self.coordinatePoint = coordinatePoint 
        self.new_wall = False
        self.delete_wall = False
        
        #creates a maze of all 0s, empty maze with no walls
        self.coordinatePoint.maze = [[0 for x in range(self.grid_size)] 
                            for y in range(self.grid_size)]
    
        pygame.init()
        self.win = pygame.display.set_mode((self.WIDTH, self.WIDTH))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Jerry Su's Algorithm Visualizer")
    
    #main method of AppWindow Class
    def main(self, running=False):
        self.clock.tick(60) #refresh 60 times per second

        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
                
        # place wall if user clicks or holds down mouse
        if not running:
            if self.new_wall == True:
                self.place_wall()
            elif self.delete_wall == True:
                self.remove()

        # get mouse and key presses and handle the inputs accordingly


        # updates the grid and then update the display

        pygame.display.update()
    
# main loop
if __name__ == "__main__":
    app = appWindow()
    while True:
        app.main()