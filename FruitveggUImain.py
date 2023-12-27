import matplotlib
matplotlib.use('TkAgg')
from FruitveggUI import *


class FruitVeg(tk.Tk):
    def __init__(self):
        super().__init__()
        data = Fruitvegg()
        self.df = data.re()
        self.title("Fruit and Vegetable")
        self.select_choice = 'item and price'
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.create_widgets()
        self.update_plots()

    def create_widgets(self):
        """
        Create the window to illustrate the data.
        """
        self.frame = ttk.LabelFrame(self, text="Select Section")
        self.frame.grid(row=5, column=0, sticky="NEWS")
        label = ttk.Label(self.frame, text="Section")
        label.grid(row=6, column=0)
        self.cb_select_choice = ttk.Combobox(self.frame, state="readonly")
        self.cb_select_choice.bind('<<ComboboxSelected>>', self.update_filters)
        self.cb_select_choice.grid(row=11, column=0, padx=10, pady=10)
        mych = ['category pie chart', 'item and price']
        self.cb_select_choice.config(values=mych)

        self.btn_quit = ttk.Button(self, text="Quit")
        self.btn_quit.bind('<Button-1>', lambda x: self.exithandler())
        self.btn_quit.grid(row=8, column=0, pady=10)
        self.btn_clear = ttk.Button(self, text="Clear")
        self.btn_clear.bind('<Button-1>', lambda x: self.clearhandler())
        self.btn_clear.grid(row=7, column=0, pady=10)

        ## create Matplotlib figure and plotting axes
        self.fig_select = Figure()
        self.axes_select = self.fig_select.add_subplot()

        # create a canvas to host the figure and place it into the main window
        self.fig_canvas1 = FigureCanvasTkAgg(self.fig_select, master=self)
        self.fig_canvas1.get_tk_widget().grid(row=0, column=0,
                                              sticky="news", padx=10, pady=10)

    def update_plots(self):
        """
        update graph.
        """
        self.plot_select()

    def update_filters(self, ev):
        """
        update the filter of dataframe to plot.
        """
        if ev.widget == self.cb_select_choice:
            self.select_choice = self.cb_select_choice.get()
        self.update_plots()

    def plot_select(self):
        """
        illustrate the type of graph that select by user.
        """
        self.axes_select.clear()
        self.fig_select.subplots_adjust(bottom=0.25)
        self.axes_select.clear()
        if self.cb_select_choice.get() == 'category pie chart':
            data = self.df['category'].value_counts()
            data.plot.pie(ax=self.axes_select,startangle=90,explode=[0,0.1,0.2,0.3], autopct='%1.1f%%')
            self.axes_select.set(xlabel=f"number of fruit and vegetable in category")
            self.fig_canvas1.draw()
        if self.cb_select_choice.get() == 'item and price':
            app = FruitveggUI(tk.Tk())
            app.run()

    def run(self):
        self.mainloop()

    def clearhandler(self):
        """
        Clears all previous data selected by the user.
        """
        self.cb_select_choice.set('')
        self.axes_select.clear()
        self.fig_canvas1.draw()

    def exithandler(self):
        """
        exit from the screen
        """
        self.quit()








