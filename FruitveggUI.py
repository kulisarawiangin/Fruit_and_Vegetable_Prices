import tkinter.ttk as ttk
import matplotlib
import time
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from Fruitvegg import *
import tkinter as tk


class FruitveggUI(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        data = Fruitvegg()
        self.df = data.re()
        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="news")
        self.select_choice = 'item and price'
        self.select_item = 'apples'
        self.select_plottype = 'basic plotting'
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.create_widgets()
        self.update_plots()


    def create_widgets(self):
        """
        Create the window to illustrate the data.
        """
        self.frame_filter = ttk.LabelFrame(self, text="Select Filters")
        self.frame_filter.grid(row=2, column=0, sticky="NEWS")
        label1 = ttk.Label(self.frame_filter, text="Item")
        label1.grid(row=0, column=0)
        self.cb_select_item = ttk.Combobox(self.frame_filter, state="readonly")
        self.cb_select_item.bind('<<ComboboxSelected>>', self.update_filters)
        self.cb_select_item.grid(row=1, column=0, padx=10, pady=10)
        self.cb_select_item.config(values=sorted(list(self.df.item.unique())))

        label2 = ttk.Label(self.frame_filter, text="Graph type")
        label2.grid(row=0, column=1)
        self.cb_select_plottype = ttk.Combobox(self.frame_filter, state="readonly")
        self.cb_select_plottype.bind('<<ComboboxSelected>>', self.update_filters)
        self.cb_select_plottype.grid(row=1, column=1, padx=10, pady=10)
        lst = ['histogram', 'area plotting', 'box plotting', 'basic plotting']
        self.cb_select_plottype.config(values=lst)
        self.btn_quit = ttk.Button(self, text="Quit")
        self.btn_quit.bind('<Button-1>', lambda x:self.exithandler())
        self.btn_quit.grid(row=8, column=0, pady=10)
        self.btn_clear = ttk.Button(self, text="Clear")
        self.btn_clear.bind('<Button-1>', lambda x:self.clearhandler())
        self.btn_clear.grid(row=7, column=0, pady=10)
        self.DATA = tk.StringVar

        ## create Matplotlib figure and plotting axes
        self.fig_select= Figure()
        self.axes_select = self.fig_select.add_subplot()

        # create a canvas to host the figure and place it into the main window
        self.fig_canvas1 = FigureCanvasTkAgg(self.fig_select, master=self)
        self.fig_canvas1.get_tk_widget().grid(row=0, column=0,
                                              sticky="news", padx=10, pady=10)

        # subframe for waiting
        self.frame1 = ttk.LabelFrame(self)
        self.frame1.grid(row=3, column=0, sticky="news", padx=5, pady=5)
        self.frame1.rowconfigure(0, weight=1)
        self.frame1.rowconfigure(1, weight=1)
        self.frame1.columnconfigure(0, weight=1)
        self.bar1 = ttk.Progressbar(self.frame1, length=250, mode="determinate")
        self.status1 = ttk.Label(self.frame1, text="Stopped")
        self.start1 = ttk.Button(self.frame1, text="Start")
        self.start1.bind('<Button-1>', lambda x: self.run_task())
        self.bar1.grid(row=4, column=0, sticky="sew", padx=10)
        self.status1.grid(row=5, column=0, sticky="wn", padx=10)
        self.start1.grid(row=4, column=1, rowspan=2, padx=10, pady=10)
        self.set = ttk.Label(self.frame1)

    def run_task(self):
        """
        run the bar while waiting for the data to illustrate.
        """
        self.task()

    def task(self):
        if self.cb_select_item.get() == '' and self.cb_select_plottype.get() == '':
            self.set.config(text='You must select filter')
            self.set.grid(row=5, column=0,sticky="wn", padx=10)
            self.status1.config(text="Done.")
            self.start1.config(state="enabled")
        if self.cb_select_plottype.get() == '' or self.cb_select_item.get() == '':
            self.set.config(text='You must select filter')
            self.set.grid(row=5, column=0,sticky="wn", padx=10)
            self.status1.config(text="Done.")
            self.start1.config(state="enabled")
        if self.cb_select_item.get() != '' and self.cb_select_plottype.get() != '':
            self.start1.config(state="disabled")
            self.status1.config(text="Running for yor graph...")
            self.after(33, lambda: self.task_step(0))

    def task_step(self, step):
        time.sleep(0.1)
        self.bar1.config(value=step)
        if step < 100:
            self.after(33, lambda: self.task_step(step + 2))
        else:
            self.task_done()

    def task_done(self):
        """
        when the bar is done, the data will illustrate.
        """
        self.status1.config(text="Done.")
        self.start1.config(state="enabled")
        self.set.config(text='')
        self.plot_select()
        self.fig_canvas1.draw()
        print(self.DATA)


    def update_plots(self):
        """
        update graph
        """
        self.plot_select()

    def update_filters(self, ev):
        """
        update the filter of dataframe to plot.
        :param ev:
        """
        if ev.widget == self.cb_select_item:
            self.select_item = self.cb_select_item.get()
            self.DATA = price(self.select_item)
        self.update_plots()

    def plot_basic(self):
        """
        illustrate when user select the basic plotting.
        """
        df = self.df
        filter = df[df['item'] == self.select_item]
        filter.plot(y='price', x='date', ax=self.axes_select)
        self.axes_select.set(xlabel='date')

    def plot_hist(self):
        """
        illustrate when user select the histogram plotting.
        """
        df = self.df
        filter = df[df['item'] == self.select_item]
        filter.price.plot.hist(bins=40, color='blue', ax=self.axes_select)

    def plot_area(self):
        """
        illustrate when user select the area plotting.
        """
        df = self.df
        filter = df[df['item'] == self.select_item]
        filter.plot.area(y='price', x='date', ax=self.axes_select, color='pink')
        self.axes_select.set(xlabel='date')
        self.axes_select.set_ylabel('price')

    def plot_box(self):
        """
        illustrate when user select the box plotting.
        """
        df = self.df
        filter = df[df['item'] == self.select_item]
        filter.plot.box(y='price', x='date', ax=self.axes_select)

    def plot_select(self):
        """
        illustrate the type of graph that select by user.
        """
        self.axes_select.clear()
        self.fig_select.subplots_adjust(bottom=0.25)
        if self.cb_select_plottype.get() == 'histogram':
            self.plot_hist()
        elif self.cb_select_plottype.get() == 'area plotting':
            self.plot_area()
        elif self.cb_select_plottype.get() == 'box plotting':
            self.plot_box()
        elif self.cb_select_plottype.get() == 'basic plotting':
            self.plot_basic()
        self.axes_select.set(title=f"{self.cb_select_item.get()} price 2017-2022")

    def run(self):
        self.mainloop()

    def clearhandler(self):
        """
        Clears all previous data selected by the user.
        """
        self.set.config(text='')
        self.cb_select_item.set('')
        self.cb_select_plottype.set('')
        self.bar1.config(value=0)
        self.status1.config(text="Stopped")
        self.axes_select.clear()
        self.axes_select.set(title=f"{self.cb_select_item.get()} price 2017-2022")
        self.fig_canvas1.draw()

    def exithandler(self):
        """
        exit from screen.
        """
        self.destroy()


@tracer
def price(n):
    """
    :param n:  item that select by user.
    :return: price of item
    """
    app = Fruitvegg()
    data = app.re()
    if n == '':
        print('')
    read = data[data['item'] == n].price
    return read







