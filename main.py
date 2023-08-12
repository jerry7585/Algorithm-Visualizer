import pygame

from node import Node

class appWindow():

    '''
        initial declartion
    '''
    def __init__(self, coords):

        # gui variables
        self.grid_size = 20
        self.box_width = 35
        self.coords = coords
        self.placing_walls = False
        self.removing_walls = False

        self.coords.maze = [[0 for x in range(self.grid_size)] 
                            for y in range(self.grid_size)]

        # start pygame application
        pygame.init()
        self.win = pygame.display.set_mode((700, 700))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Jerry Su's Algorithm Visualizer")

    ''' 
        main function for app
    '''
    def main(self, running=False):
        
        self.clock.tick(60)

        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
                
        # if the mouse button was pressed down continue placing walls
        if not running:
            if self.placing_walls == True:
                self.place_wall()
            elif self.removing_walls == True:
                self.remove()

        # get mouse and key presses
        self.input_key(running)

        # redraw and update the display
        self.redraw()
        pygame.display.update()
        

    ''' 
        handles key and mouse presses
    '''
    def input_key(self, running):

        run_keys = {"d", "b", "s"}
        start_end_keys = {"1", "2"}

        # gets key presses
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # key presses
            if event.type == pygame.KEYDOWN:
                key = chr(event.key)
                if running == False:
                    # run algorithm d for dfs | b for bfs | s for djikstra
                    if key in run_keys: 
                        self.run_algorithm(key)  
                                    
                    # 1 = start and 2 = end
                    elif key in start_end_keys:
                        self.place_startend(key)


            # mouse button down PLACE WALLS
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if running == False:
                    # place walls
                    if event.button == 1: # left click
                        self.placing_walls = True
                        
                    # remove walls
                    elif event.button == 3: # right click
                        self.removing_walls = True

            # mouse button up detects when the mouse click ends so it doesnt place/remove walls forever
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: # left up
                    self.placing_walls = False
                    
                elif event.button == 3: # right up
                    self.removing_walls = False

    '''
        Function to redraw the grid
    '''
    def redraw(self):

        self.win.fill((124, 252, 0))
        self.draw_points()
        self.draw_grid()


    '''
        Initial creation of the grid
    '''
    def draw_grid(self):
        line_image = pygame.image.load("images/wall.png") 
        for i in range(self.grid_size-1):
            pygame.draw.rect(self.win, (101, 67, 33), (((i+1)*self.box_width), 0, 4, 700)) #draws the veritcal lines
            pygame.draw.rect(self.win, (101, 67, 33), (0,((i+1)*self.box_width), 700, 4)) #draws the horizontal lines
            
         
    ''' 
        used to draw the boxed given colors and position
    '''
    def draw_box(self, box, color):
        boxX, boxY = box
        pygame.draw.rect(self.win, color, (boxX*self.box_width, boxY*self.box_width, self.box_width, self.box_width))
        
    ''' 
        draws all the squares for the walls, checkpoints, travel path
    '''
    def draw_points(self):
        
        brown_walls = (139, 69, 19)
        gray_path = (128, 128, 128)
        skyblue_surrounding_path = (135, 206, 235)
        final_path = (255, 255, 255)
        red_start_end = (255, 0, 0)
        
        #the  walls color
        for wall in self.coords.walls:
            self.draw_box(wall, brown_walls)
            
        # the actual path the nodes are going through
        for node in self.coords.closed_list:
            self.draw_box(node.position, gray_path)
            
        # the nodes around the current node that can be checked 
        for node in self.coords.open_list:
            self.draw_box(node.position, skyblue_surrounding_path)

        #path at the end, the shortest path derived from the algorithm
        for wall in self.coords.final_path:
            self.draw_box(wall, final_path)
        
        #adds the 1(starting point) and 2(finishing point)
        for i,point in enumerate(self.coords.end_point):
            if point != "None":
                boxX, boxY = point
                center = ((boxX*self.box_width+(self.box_width/2)), (boxY*self.box_width+(self.box_width/2)))
                self.draw_box(point, red_start_end)
                self.display_text(str(i+1), final_path, center, int(self.box_width))


    '''
        functions to place startend, walls and removing them
    '''
    def place_startend(self, index):
        boxX = int((self.mouse_x + 2) / self.box_width)
        boxY = int((self.mouse_y + 2) / self.box_width)
        coords = boxX, boxY
        if (coords != self.coords.start and 
            coords != self.coords.end and
            coords not in self.coords.walls and 
            coords not in self.coords.end_point):
            
            while len(self.coords.end_point) <= int(index)-1:
                self.coords.end_point.append("None")
            self.coords.end_point[int(index)-1] = coords

    def place_wall(self):
        boxX = int((self.mouse_x + 2) / self.box_width)
        boxY = int((self.mouse_y + 2) / self.box_width)
        coords = boxX, boxY
        if (coords != self.coords.start and coords != self.coords.end
                and coords not in self.coords.walls and coords
                not in self.coords.end_point):
            self.coords.walls.append(coords)


    def remove(self):
        boxX = int((self.mouse_x + 2) / self.box_width)
        boxY = int((self.mouse_y + 2) / self.box_width)
        coords = boxX, boxY
        if coords in self.coords.walls:
            self.coords.walls.remove(coords)
        elif coords in self.coords.end_point:
            self.coords.end_point.remove(coords)
        elif coords == self.coords.start:
            self.coords.start = None
        elif coords == self.coords.end:
            self.coords.end = None


    # function that prepares for a pathfind and runs pathfind function
    def run_algorithm(self, key):
        self.coords.remove_last()
        self.placing_walls == False
        self.removing_walls == False

        # create the maze array and remove missed checkpoint numbers
        self.coords.create_maze(app)
        end_point = self.coords.end_point[:]
        end_point = [point for point in end_point if point != "None"]

        # iterate through every checkpoint and pathfind to it
        for i,point in enumerate(end_point):
            if i != len(end_point)-1:
                
                start = point
                end = end_point[i+1]

                new_path = pathfind(self.coords.maze, start, end,
                                    self, self.coords, key)
                if new_path == None:
                    new_path = []
                    
                self.coords.final_path.extend(new_path)

    # displays text given text, color and position/size
    def display_text(self, txt, color, center, size):
        font = pygame.font.Font(None, size)
        text_surf = font.render(txt, True, color)
        text_rect = text_surf.get_rect()
        text_rect.center = (center)
        self.win.blit(text_surf, text_rect)

class coordinate():
    
    def __init__(self):
        self.start = None
        self.end = None
        self.walls = []
        self.maze = []
        self.open_list = []
        self.closed_list = []
        self.final_path = []
        self.end_point = []


    def remove_all(self):
        self.start = None
        self.end = None
        self.walls = []
        self.maze = []
        self.open_list = []
        self.closed_list = []
        self.final_path = []
        self.end_point = []


    def remove_last(self):
        self.maze = []
        self.open_list = []
        self.closed_list = []
        self.final_path = []


    # gets the furthest distance of a node from the (0, 0)
    def largest_distance(self):
        largest = 0
        for wall in self.walls:
            if wall[0] > largest: largest = wall[0]
            if wall[1] > largest: largest = wall[1]
        for point in self.end_point:
            if point[0] > largest: largest = point[0]
            if point[1] > largest: largest = point[1]
        return largest + 1


    # create the maze
    def create_maze(self, giu):   
        largest_distance = self.largest_distance()
        largest = 20
            
        self.maze = [[0 for x in range(largest)] for y in range(largest)]
        for wall in self.walls:
            try:
                wall_x, wall_y = wall
                self.maze[wall_x][wall_y] = 1
            except:
                pass


# function for pathfinding using dfs, bfs, dijkstra and astar
# Returns a list of tuples as a path from the given start to the given end in the given maze
def pathfind(maze, start, end, app, coords, key):
    
    # Create start and end points as the node
    start_node = Node(None, start)
    start_node.g = 0
    start_node.h = 0
    start_node.f = 0
    end_node = Node(None, end)
    end_node.g = 0
    end_node.h = 0
    end_node.f = 0

    # open list represents the path it can check all sides 1 around current node
    # closed list represents the current path it is taking
    open_list = []
    closed_list = []

    # first node, starting point 
    open_list.append(start_node)

    count = 0

    # Loop until you find the end
    while len(open_list) > 0:
        if count >= 9:
            count = 0
            
            if key == "d": # dfs, depth first search, checks the least recent node
                current_node = open_list[-1]
                current_index = len(open_list)-1
                
            elif key == "b": # bfs, breadth first search, checks most recent node
                current_node = open_list[0]
                current_index = 0               
                        
            elif key == "s": # dijkstra, s for shortest path algorithm, checks closest to starting value
                current_node = open_list[0]
                current_index = 0
                for index, item in enumerate(open_list):
                    if item.g < current_node.g:
                        current_node = item
                        current_index = index

            # adds current node to the closed list and removes from the open list
            open_list.pop(current_index)
            closed_list.append(current_node)

            #did we reach the end? if yes then return the shortest path in white
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                coords.open_list = open_list
                coords.closed_list = closed_list
                return path 

            # Generate possible node paths
            for curr_node in [(-1, 0), (0, 1), (1, 0), (0, -1)]: # up down left right nodes
                curr_node = (current_node.position[0] + curr_node[0],
                            current_node.position[1] + curr_node[1])

                # Make sure within range
                if (curr_node[0] > (len(maze) - 1) or curr_node[0] < 0
                        or curr_node[1] > (len(maze[len(maze)-1]) - 1)
                        or curr_node[1] < 0):
                    continue

                #check to see if it is a path(0)
                if maze[curr_node[0]][curr_node[1]] != 0:
                    continue

                #if the node is in the path, go to it which creates child node
                if Node(current_node, curr_node) in closed_list:
                    continue

                # child node
                child = Node(current_node, curr_node)

                passList = [False for closed_child in closed_list if child == closed_child]
                if False in passList:
                    continue
                
                if key == "e": # dijkstra, add one to g value
                    child.g = current_node.g + 1
                
                for open_node in open_list:
                    if child == open_node and child.g >= open_node.g:
                        break
                    
                else:
                    open_list.append(child)

        #update the lists and app window
        else:
            coords.open_list = open_list
            coords.closed_list = closed_list
            app.main(True)

        #increment count so there is a delay so user can see the progression
        count += 1

# main loop
if __name__ == "__main__":
    app = appWindow(coordinate())
    while True:
        app.main()