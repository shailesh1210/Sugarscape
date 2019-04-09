import tkinter as tk
import itertools as itr
import math as m

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Sugarscape import World


class Frame:
    def __init__(self, window):
        self.frame = tk.Frame(window,
                              borderwidth=5)

    def get_frame(self, row, col):
        self.frame.grid(row=row, column=col, sticky="n")
        return self.frame


class Plot:
    def __init__(self, frame):
        self.frame = frame
        self.plot_names = ["Population", "Average Wealth", "Average Vision", "Average Metabolism"]
        self.plots = {}

        num_rows = num_cols = int(len(self.plot_names)/2)
        for i, j in itr.product(range(num_rows), range(num_cols)):
            idx = i*num_cols + j
            plot, plot_canvas = self.plot_widget(i, j, idx)
            self.plots[plot_canvas] = plot

    def plot_widget(self, row, col, idx):
        plot = Figure(figsize=(3, 3))

        sub_plot = plot.add_subplot(111)
        sub_plot.grid()
        sub_plot.set_title(self.plot_names[idx])

        plot_canvas = FigureCanvasTkAgg(plot, self.frame)
        plot_canvas.get_tk_widget().grid(row=row, column=col, padx=2, pady=2, sticky="n")

        return sub_plot, plot_canvas

    def draw(self, xlist, ylist):
        idx = 0
        for canvas, plt in self.plots.items():
            plt.cla()
            plt.plot(xlist, ylist, color="orange")
            plt.set_title(self.plot_names[idx])
            plt.grid()

            canvas.draw()

            idx += 1

    def clear(self):
        idx = 0
        for canvas, plt in self.plots.items():
            plt.cla()
            plt.set_title(self.plot_names[idx])
            plt.grid()

            canvas.draw()

            idx += 1


class Label:
    def __init__(self, frame, row, col):
        self.label = tk.Label(frame,
                              font="Arial 10",
                              width=20,
                              height=3,
                              justify="left",
                              relief="raised")
        self.label.grid(row=row, column=col)

    def set_text(self, text):
        self.label["text"] = text

    def set_width(self, width):
        self.label["width"] = width

    def set_height(self, height):
        self.label["height"] = height

    def set_relief(self, relief):
        self.set_relief["relief"] = relief


class Scale:
    def __init__(self, frame, row, col):
        self.scale = tk.Scale(frame,
                              from_=1,
                              to=100,
                              resolution=1,
                              orient="horizontal",
                              relief="raised",
                              length=340,
                              tickinterval=99)
        self.scale.grid(row=row, column=col, columnspan=3)

    def set_range(self, fro, to):
        self.scale["from_"] = fro
        self.scale["to"] = to

    def set_orientation(self, orient):
        self.scale["orientation"] = orient

    def set_relief(self, relief):
        self.scale["relief"] = relief

    def set_length(self, length):
        self.scale["length"] = length

    def set_tick_interval(self, interval):
        self.scale["tickinterval"] = interval

    def set_value(self, value):
        self.scale.set(value)

    def get_value(self):
        return self.scale.get()


class Button:
    def __init__(self, frame, row, col):
        self.button = tk.Button(frame,
                                font="Arial 10",
                                width=20,
                                height=3,
                                borderwidth=3,
                                relief="raised")

        self.button.grid(row=row, column=col, pady=20, sticky="w")

    def set_text(self, text):
        self.button["text"] = text

    def set_width(self, width):
        self.button["width"] = width

    def set_height(self, height):
        self.button["height"] = height

    def set_relief(self, relief):
        self.button["relief"] = relief

    def set_command(self, command):
        self.button["command"] = command


class Canvas:
    def __init__(self, frame, row, col):
        self.canvas = tk.Canvas(frame,
                                width=100,
                                height=100,
                                background="#E0E0E0")
        self.canvas.grid(row=row, column=col)

    def set_width(self, width):
        self.canvas["width"] = width

    def set_height(self, height):
        self.canvas["height"] = height

    def set_bg_color(self, color):
        self["background"] = color

    def create_rectangle(self, x_min, y_min, x_max, y_max, color, tag, stip=""):
        self.canvas.create_rectangle(x_min, y_min, x_max, y_max,
                                     fill=color, tag=tag, outline=color,
                                     stipple=stip)

    def update_rectangle(self, idx,  color):
        self.canvas.itemconfig(idx, fill=color, outline=color)

    def create_circle(self, x_min, y_min, x_max, y_max, color, tag, stip=""):
        self.canvas.create_oval(x_min, y_min, x_max, y_max,
                                fill=color, tag=tag, outline=color,
                                stipple=stip)

    def move_circle(self, idx, x, y):
        self.canvas.move(idx, x, y)

    def delete_circle(self, idx):
        self.canvas.delete(idx)

    def delete(self):
        self.canvas.delete("all")


class Visualization:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Sugarscape model")
        self.window.wm_resizable(0, 0)

        self.width = 700
        self.height = 700

        # Frame for inputs
        self.inputFrame = Frame(self.window).get_frame(row=0, col=0)
        self.inputs()
        self.buttons()

        # Frame for animation
        self.animationFrame = Frame(self.window).get_frame(row=0, col=1)
        self.animation()

        # Frame for graphs
        self.plotFrame = Frame(self.window).get_frame(row=0, col=2)
        self.plots()


    def inputs(self):
        max_agents = 500
        init_agents = 200

        # Creates label and scale for agent population
        self.num_label = Label(self.inputFrame, row=0, col=0)
        self.num_label.set_text("Initial Population")

        self.num_scale = Scale(self.inputFrame, row=0, col=1)
        self.num_scale.set_range(1, max_agents)
        self.num_scale.set_value(init_agents)
        self.num_scale.set_tick_interval(max_agents-1)

        max_ticks = 100
        init_ticks = 20

        # Creates label and scale for ticks
        self.ticks_label = Label(self.inputFrame, row=1, col=0)
        self.ticks_label.set_text("Ticks")

        self.ticks_scale = Scale(self.inputFrame, row=1, col=1)
        self.ticks_scale.set_range(1, max_ticks)
        self.ticks_scale.set_value(init_ticks)
        self.ticks_scale.set_tick_interval(max_ticks-1)

        # Creates label and scale for grid size
        self.grid_label = Label(self.inputFrame, row=2, col=0)
        self.grid_label.set_text("Grid Size")

        self.grid_scale = Scale(self.inputFrame, row=2, col=1)
        self.grid_scale.set_range(fro=50, to=100)
        self.grid_scale.set_value(value=50)
        self.grid_scale.set_tick_interval(interval=50)

        # Create label and scale for sugar radius
        self.radius_label = Label(self.inputFrame, row=3, col=0)
        self.radius_label.set_text("Radius")

        self.radius_scale = Scale(self.inputFrame, row=3, col=1)
        self.radius_scale.set_range(fro=200, to=400)
        self.radius_scale.set_value(value=250)
        self.radius_scale.set_tick_interval(interval=200)


    def buttons(self):
        self.initialize_btn = Button(self.inputFrame, row=4, col=0)
        self.initialize_btn.set_text("Initialize")
        self.initialize_btn.set_command(self.initialize)

        self.run_btn = Button(self.inputFrame, row=4, col=1)
        self.run_btn.set_text("Run")
        self.run_btn.set_relief("sunken")
        self.run_btn.set_command(self.run)

        self.quit_btn = Button(self.inputFrame, row=4, col=2)
        self.quit_btn.set_text("Quit")
        self.quit_btn.set_command(self.quit)


    def animation(self):
        self.animationCanvas = Canvas(self.animationFrame, row=0, col=0)
        self.animationCanvas.set_width(self.width)
        self.animationCanvas.set_height(self.height)

    def plots(self):
        self.graphs = Plot(self.plotFrame)

    def frame_widget(self, row, col):
        frame = tk.Frame(self.window,
                         borderwidth=5)
        frame.grid(row=row, column=col, sticky="n")
        return frame

    def initialize(self):
        self.graphs.clear()

        self.xlist = []
        self.ylist = []

        self.run_btn.set_relief("raised")
        self.animationCanvas.delete()

        grid_size = int(self.grid_scale.get_value())
        agent_pop = int(self.num_scale.get_value())
        radius = int(self.radius_scale.get_value())

        self.world = World(self.animationCanvas,
                           width=self.width,
                           height=self.height,
                           grid_size=grid_size,
                           pop=agent_pop,
                           radius=radius)
        self.world.initialize()

    def run(self):
        self.run_btn.set_relief("sunken")

        max_ticks = int(self.ticks_scale.get_value())
        t = 0

        while t < max_ticks:
            self.world.run()

            self.xlist.append(t)
            self.ylist.append(self.world.get_agent_count())

            self.graphs.draw(self.xlist, self.ylist)

            t += 1.0

    def quit(self):
        self.window.destroy()

    def loop(self):
        self.window.mainloop()


def main():
    visual = Visualization()
    visual.loop()


if __name__ == "__main__":
    main()