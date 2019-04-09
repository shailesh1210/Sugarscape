import random as rd
import tkinter.messagebox as box
import math as m
from itertools import product
import copy


class World(object):
    def __init__(self, canvas, width, height, grid_size, pop, radius):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.radius = radius

        self.min_gx, self.min_gy = 0, 0
        self.max_gx, self.max_gy = self.grid_size-1, self.grid_size-1

        self.dx = width/grid_size
        self.dy = height/grid_size

        self.agent_pop = pop

    def initialize(self):
        self.create_grid()
        self.create_resource()
        self.create_agent()

    def run(self):

        for res in self.non_zero_resources:
            sugar_lvl = res.get_sugar_level()
            capacity = res.get_capacity()

            if sugar_lvl <= capacity:
                res.grow()

        for agent in self.agent_list:
            if agent.is_alive():
                agent.execute()
            else:
                agent.remove()

    def create_grid(self):
        """
        -Creates grid coordinates (maps cartesian coordinates with tkinter coordinates)
        -Creates grid_occupancy to check if the grid is occupied by an agent, value is False
         if empty and True if occupied
        """
        self.grid_occupancy = {}
        self.coords_map = {}

        tk_x = 0
        for x in range(self.grid_size):
            tk_y = 0
            for y in range(self.grid_size):
                self.grid_occupancy[(x, y)] = False
                self.coords_map[(x, y)] = (tk_x, tk_y)

                tk_y += self.dy
            tk_x += self.dx

    def create_resource(self):
        '''
        Creates a pattern for resource distribution in north-east
        and south-west quadrant of grid
        Steps:
        1. Find mid-point (mid) on diagonal of grid between (0, height)
        and (width, 0)
        2. Find mid-point on NE quadrant between mid and NE coordinates
        3. Find mid-point on SE quadrant between mid and SW coordinates
        4. Calculate max distance for NE and SW
        5. Create a tuple with (x, y, dist) for NE and SW
        6. Iterate through grid coordinates to set sugar level in grid
        :return:
        '''

        #sugar_colors = {1: "#FFFFCC", 2: "#FFFFCC",
                        #3: "#FFFF99", 4: "#FFFF99",
                        #5: "#FFFF66", 6: "#FFFF66",
                        #7: "#FFFF33", 8: "#FFFF33",
                        #9: "#FFFF00", 10: "#FFFF00"}

        sugar_colors = {1: "#FF6666", 2: "#FF6666",
                        3: "#FF3333", 4: "#FF3333",
                        5: "#FF0000", 6: "#FF0000",
                        7: "#CC0000", 8: "#CC0000",
                        9: "#990000", 10: "#990000"}

        ne_pos = (self.width, 0)
        sw_pos = (0, self.height)

        mid = (self.width/2, self.height/2)

        north_mid_x, north_mid_y = self.mid_point(ne_pos, mid)
        south_mid_x, south_mid_y = self.mid_point(sw_pos, mid)

        max_dist_north = (self.radius/self.width) * self.distance(max(north_mid_x, self.width-north_mid_x),
                                                                  max(north_mid_y, self.height-north_mid_y))
        max_dist_south = (self.radius/self.width) * self.distance(max(south_mid_x, self.width-south_mid_x),
                                                                  max(south_mid_y, self.height-south_mid_y))

        north_pos = (north_mid_x, north_mid_y, max_dist_north)
        south_pos = (south_mid_x, south_mid_y, max_dist_south)

        self.pos = [north_pos, south_pos]
        self.resources = {}
        self.non_zero_resources = []

        for x, y in product(range(self.grid_size), range(self.grid_size)):
            self.resources[(x, y)] = 0

        for pos in self.pos:
            for x, y in product(range(self.grid_size), range(self.grid_size)):
                idx = "sugar" + str(x*self.grid_size + y)
                resource = Resource(world=self,
                                    canvas=self.canvas,
                                    colors=sugar_colors,
                                    idx=idx,
                                    x=x,
                                    y=y)

                if not self.resources[(x, y)]:
                    resource.set_capacity(pos)
                    self.resources[(x, y)] = resource
                else:
                    prev_resource = self.resources[(x, y)]
                    new_resource = Resource(world=self,
                                            canvas=self.canvas,
                                            colors=sugar_colors,
                                            idx=idx,
                                            x=x,
                                            y=y)
                    new_resource.set_capacity(pos)

                    c1 = prev_resource.get_capacity()
                    c2 = new_resource.get_capacity()

                    if c2 > c1:
                        resource.set_new_capacity(c2)
                        self.resources[(x, y)] = resource

                if self.resources[(x, y)].get_capacity() > 0:
                    self.resources[(x, y)].draw()

        for key in self.resources:
            if self.resources[key].capacity > 0:
                self.non_zero_resources.append(self.resources[key])


    def create_agent(self):
        self.agent_list = []
        if self.agent_pop > self.grid_size*self.grid_size:
            box.showerror("Error", "Agent population exceeds world size")
        else:
            idx = 0
            while idx < self.agent_pop:
                x = rd.randint(0, self.grid_size-1)
                y = rd.randint(0, self.grid_size-1)

                if not self.is_occupied(x, y):
                    agent = Agent(self,
                                  self.canvas,
                                  idx="agent" + str(idx),
                                  x=x,
                                  y=y,
                                  color="#000066")

                    agent.draw()

                    self.agent_list.append(agent)
                    self.add_occupancy(x, y)

                    idx += 1

    def is_occupied(self, x, y):
        return self.grid_occupancy[(x, y)]

    def add_occupancy(self, x, y):
        self.grid_occupancy[(x, y)] = True

    def remove_occupancy(self, x, y):
        self.grid_occupancy[(x, y)] = False

    def mid_point(self, pos1, pos2):
        mid = ((pos1[0] + pos2[0]) / 2, (pos1[1] + pos2[1]) / 2)
        return mid[0], mid[1]

    def distance(self, x, y):
        return m.sqrt(x*x + y*y)

    def get_xy_tkinter(self, x, y):
        coords = self.coords_map[(x, y)]
        return coords[0], coords[1]

    def get_min_grid_xy(self):
        return self.min_gx, self.min_gy

    def get_max_grid_xy(self):
        return self.max_gx, self.max_gy

    def get_dx(self):
        return self.dx

    def get_dy(self):
        return self.dy

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_grid_size(self):
        return self.grid_size

    def get_resource(self, x, y):
        return self.resources[(x, y)]

    def get_agent_count(self):
        return len(self.agent_list)


class Resource(object):
    MAX_CAPACITY = 10
    GROWTH_RATE = 3

    def __init__(self, world, canvas, colors, idx, x, y):
        self.idx = idx
        self.world = world
        self.canvas = canvas
        self.colors = colors

        self.x, self.y = x, y
        self.tk_x, self.tk_y = self.world.get_xy_tkinter(x, y)

        self.capacity = 0
        self.sugar_level = 0

    def grow(self):
        if self.sugar_level < self.capacity:
            self.sugar_level += Resource.GROWTH_RATE

        if self.sugar_level > self.capacity:
            self.sugar_level = self.capacity
        #self.sugar_level = self.capacity

        if self.sugar_level > 0:
            self.canvas.update_rectangle(self.idx, self.colors[self.sugar_level])
            # self.draw()

    def set_capacity(self, ref_pos):
        pos_tx, pos_ty, max_dist = ref_pos[0], ref_pos[1], ref_pos[2]
        dist = self.world.distance(pos_tx-self.tk_x, pos_ty-self.tk_y)

        capacity = 1 + Resource.MAX_CAPACITY * (1 - dist/max_dist)
        if capacity < 0:
            self.capacity = 0
        else:
            self.capacity = int(min(capacity, Resource.MAX_CAPACITY))
            self.sugar_level = copy.copy(self.capacity)

    def set_new_capacity(self, c):
        self.capacity = c
        self.sugar_level = copy.copy(self.capacity)

    def set_sugar_level(self, sugar):
        self.sugar_level = sugar

    def get_capacity(self):
        return self.capacity

    def get_sugar_level(self):
        return self.sugar_level

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def draw(self):

        xmin, ymin = self.tk_x, self.tk_y
        xmax, ymax = xmin + self.world.get_dx(), ymin + self.world.get_dy()

        self.canvas.create_rectangle(x_min=xmin,
                                     y_min=ymin,
                                     x_max=xmax,
                                     y_max=ymax,
                                     color=self.colors[self.sugar_level],
                                     tag=self.idx)


class Agent(object):
    MAX_VISION = 6
    MAX_METABOLISM = 6
    MIN_SUGAR, MAX_SUGAR = 5, 25
    MOVEMENT = [(-1, 0), (1, 0), (0, 1), (0, -1)]

    def __init__(self, world, canvas, idx, x, y,  color):
        self.world = world
        self.canvas = canvas

        self.idx = idx

        self.x = x
        self.y = y
        self.color = color

        self.tk_x, self.tk_y = self.world.get_xy_tkinter(self.x, self.y)

        self.vision = rd.randint(1, Agent.MAX_VISION)
        self.metabolism = rd.randint(1, Agent.MAX_METABOLISM)
        self.wealth = rd.randint(Agent.MIN_SUGAR, Agent.MAX_SUGAR)

        self.alive = True

    def execute(self):
        if self.alive:
            self.move()
            self.eat()

    def remove(self):
        self.world.agent_list.remove(self)
        self.canvas.delete_circle(self.idx)

    def move(self):
        """
        Agent searches for location with highest sugar and moves
        there
        Steps:
        1. Get list of surrounding resources covered by agent's vision
        2. Iterate through neighboring resources to find location with
        maximum sugar.
        3. Remove agent from its current location
        4. Move agent to new location and update it's x, y coordinates
        """

        max_x, max_y = self.find_xy_max_sugar()

        self.world.remove_occupancy(self.x, self.y)
        self.x, self.y = max_x, max_y
        self.world.add_occupancy(self.x, self.y)

        old_tk_x, old_tk_y = self.tk_x, self.tk_y
        self.tk_x, self.tk_y = self.world.get_xy_tkinter(self.x, self.y)

        self.canvas.move_circle(self.idx, self.tk_x - old_tk_x, self.tk_y - old_tk_y)
        self.draw()


    def eat(self):
        resource = self.world.resources[(self.x, self.y)]
        self.wealth += (resource.get_sugar_level() - self.metabolism)

        resource.set_sugar_level(0)

        if self.wealth < 0:
            self.alive = False

    def find_xy_max_sugar(self):
        resources = self.get_surrounding_resources()
        rd.shuffle(resources)

        max_sugar = 0
        max_x, max_y = self.x, self.y

        for res in resources:
            x, y = res.getX(), res.getY()
            if not self.world.is_occupied(x, y):
                sugar_level = res.get_sugar_level()
                if sugar_level > max_sugar:
                    max_sugar = sugar_level
                    max_x, max_y = x, y
        return max_x, max_y

    def get_surrounding_resources(self):
        surrounding_resources = []

        min_pos_x, min_pos_y = self.world.get_min_grid_xy()
        max_pos_x, max_pos_y = self.world.get_max_grid_xy()
        grid_size = self.world.get_grid_size()

        for d in Agent.MOVEMENT:

            vis = 0
            dir_x, dir_y = d[0], d[1]
            x, y = self.x, self. y

            while vis < self.vision:
                x, y = x + dir_x, y + dir_y

                if x > max_pos_x:
                    x = x - grid_size
                elif x < min_pos_x:
                    x = x + grid_size

                if y > max_pos_y:
                    y = y - grid_size
                elif y < min_pos_y:
                    y = y + grid_size

                resource = self.world.get_resource(x, y)
                surrounding_resources.append(resource)
                vis += 1

        return surrounding_resources

    def is_alive(self):
        return self.alive

    def draw(self):
        xmin, ymin = self.tk_x-self.world.get_dx()/2, self.tk_y-self.world.get_dy()/2
        xmax, ymax = self.tk_x+self.world.get_dx()/2, self.tk_y+self.world.get_dy()/2

        self.canvas.create_circle(x_min=xmin,
                                  y_min=ymin,
                                  x_max=xmax,
                                  y_max=ymax,
                                  color=self.color,
                                  tag=self.idx,
                                  stip="gray75")
