import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import common

BUTTON_FONT = ("Arial", 12, "bold")
BUTTON_CLICKED_FONT = ("Arial", 12, "bold", "underline")
LABEL_FONT = ("Arial", 10, "bold")
BACKGROUND_COLOR = "#0071aa"
TEXT_COLOR = "white"
SUBMIT_BUTTON_COLOR = "#2e8969"
ACTIVE_COLOR = "darkgreen"
DEFAULT_WIDTH = 15

class Interface:
    def __init__(self, root, action_handler):
        self.root = root
        self.root.title('IMPAKT')
        self.root.geometry('800x600')
        self.root.config(bg="white")

        self.create_header()
        self.create_widgets_frame()
        self.create_plot()

        self.action_handler = action_handler

        # start from market analysis widget
        self.create_market_analysis_widgets()
        self.update_button_style("market_analysis")

    def create_header(self):
        header = tk.Frame(self.root, bg=BACKGROUND_COLOR, height=100)
        header.pack(fill="x", pady=0)
        header.pack_propagate(False)

        header_label = tk.Label(header, text="IMPAKT   |", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=("Arial", 20, "bold"))
        header_label.grid(row=0, column=0, padx=10, pady=15)

        self.button_market_analysis = tk.Button(
            header, 
            text='Market Analysis', 
            command=lambda: [self.show_widgets('market_analysis'), self.update_button_style('market_analysis')],
            borderwidth=0,
            relief="flat",
            fg=TEXT_COLOR,
            bg=BACKGROUND_COLOR,
            font=BUTTON_FONT,
            activebackground=BACKGROUND_COLOR,
            activeforeground=TEXT_COLOR
        )
        self.button_market_analysis.grid(row=0, column=1, padx=12)

        self.button_currency_changes_histogram = tk.Button(
            header, 
            text='Currency Changes Histogram', 
            command=lambda: [self.show_widgets('currency_changes_histogram'), self.update_button_style('currency_changes_histogram')],
            borderwidth=0,
            relief="flat",
            fg=TEXT_COLOR,
            bg=BACKGROUND_COLOR,
            font=BUTTON_FONT,
            activebackground=BACKGROUND_COLOR,
            activeforeground=TEXT_COLOR
        )
        self.button_currency_changes_histogram.grid(row=0, column=2, padx=12)

        header.grid_rowconfigure(0, weight=1)

    def create_widgets_frame(self):
        self.frame_widgets = tk.Frame(self.root, bg="white")
        self.frame_widgets.pack(anchor="w", padx=10, pady=10)

    def create_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(5, 4))


        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=20)

    def update_plot(self, fig):
        self.clear_plot()

        plt.tight_layout()
        self.canvas.figure = fig
        self.canvas.draw_idle()

    def clear_plot(self):
        if self.canvas.figure:
            plt.close(self.canvas.figure)
            
        self.canvas.get_tk_widget().destroy()
        self.create_plot()

    def show_widgets(self, function_type):
        for widget in self.frame_widgets.winfo_children():
            widget.grid_forget()

        self.clear_plot()

        if function_type == 'market_analysis':
            self.create_market_analysis_widgets()

        elif function_type == 'currency_changes_histogram':
            self.create_currency_changes_histogram_widgets()


    def create_market_analysis_widgets(self):
        self.create_label("Base currency", 0, 0)
        self.base_currency_dropdown = self.create_dropdown_list(common.CURRENCIES, common.DEFAULT_BASE_CURRENCY, 1, 0)
        
        self.create_label("Quote currency", 0, 1)
        self.quote_currency_dropdown = self.create_dropdown_list(common.CURRENCIES, common.DEFAULT_QUOTE_CURRENCY, 1, 1)
        
        self.create_label("Data from last", 0, 2)
        self.data_range_dropdown = self.create_dropdown_list(list(common.DATA_RANGES.keys()), common.DEFAULT_DATA_RANGE, 1, 2)

        button = self.create_submit_button(1, 3)
        button.config(command=lambda: self.handle_create_market_analysis_button_click())

    def handle_create_market_analysis_button_click(self):
        base_currency = self.base_currency_dropdown.get()
        quote_currency = self.quote_currency_dropdown.get()
        data_range = self.data_range_dropdown.get()

        self.action_handler.handle_create_market_analysis(base_currency, quote_currency, data_range)


    def create_currency_changes_histogram_widgets(self):
        self.create_label("Base currency", 0, 0)
        self.base_currency_dropdown = self.create_dropdown_list(common.CURRENCIES, common.DEFAULT_BASE_CURRENCY, 1, 0)
        
        self.create_label("Quote currency", 0, 1)
        self.quote_currency_dropdown = self.create_dropdown_list(common.CURRENCIES, common.DEFAULT_QUOTE_CURRENCY, 1, 1)
        
        self.create_label("Start date", 0, 2)
        self.start_date_picker = self.create_date_picker(common.DEFAULT_DATA_PICKER_VALUE, 1, 2)

        self.create_label("Report type", 0, 3)
        self.report_type_dropdown = self.create_dropdown_list(list(common.CURRENCY_CHANGES_HISTOGRAM_REPORT_TYPES.keys()),
                                    common.DEFAULT_CURRENCY_CHANGES_HISTOGRAM_REPORT_TYPE,
                                    1, 3)

        button = self.create_submit_button(1, 4)
        button.config(command=lambda: self.handle_currency_changes_histogram_button_click())


    def handle_currency_changes_histogram_button_click(self):
        base_currency = self.base_currency_dropdown.get()
        quote_currency = self.quote_currency_dropdown.get()
        start_date = self.start_date_picker.get_date()
        report_type = self.report_type_dropdown.get()

        self.action_handler.handle_create_currency_changes_histogram(base_currency, quote_currency, start_date, report_type)


    def create_label(self, text, row, col):
        label = tk.Label(self.frame_widgets, text=text, font=LABEL_FONT, fg='gray', bg="white", anchor='w')
        label.grid(row=row, column=col, padx=5, pady=0, sticky='w')
        return label

    def create_dropdown_list(self, values, default_value, row, col):
        combobox = ttk.Combobox(self.frame_widgets, values=values, state="readonly", width=DEFAULT_WIDTH)
        combobox.set(default_value)
        combobox.grid(row=row, column=col, padx=5, pady=0)
        return combobox

    def create_date_picker(self, default_date, row, col):
        date_picker = DateEntry(self.frame_widgets, 
                                width=DEFAULT_WIDTH, 
                                background="white", 
                                foreground="black", 
                                borderwidth=2, 
                                date_pattern='yyyy-mm-dd')
        date_picker.set_date(default_date)
        date_picker.grid(row=row, column=col, padx=5, pady=0)
        return date_picker

    def create_submit_button(self, row, col):
        button = tk.Button(
            self.frame_widgets,
            text='SUBMIT',
            bg=SUBMIT_BUTTON_COLOR,
            fg='white',
            font=('Arial', 8, 'bold'),
            activebackground=ACTIVE_COLOR,
            activeforeground='white',
            width=10,
        )
        button.grid(row=row, column=col, padx=5)
        return button

    def update_button_style(self, selected_button):
        self.reset_button_style()

        if selected_button == "currency_changes_histogram":
            self.button_currency_changes_histogram.config(font=BUTTON_CLICKED_FONT)
        elif selected_button == "market_analysis":
            self.button_market_analysis.config(font=BUTTON_CLICKED_FONT)

    def reset_button_style(self):
        self.button_market_analysis.config(bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=BUTTON_FONT, relief="flat")
        self.button_currency_changes_histogram.config(bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=BUTTON_FONT, relief="flat")

    def show_error_message(self, title, message):
        error_window = tk.Toplevel(self.root)
        error_window.title(title)
        error_window.geometry('300x150')
        error_window.config(bg="white")

        label = tk.Label(error_window, text=message, font=LABEL_FONT, fg='black', bg="white", wraplength=280)
        label.pack(pady=20)

        button = tk.Button(
            error_window,
            text='OK',
            bg=SUBMIT_BUTTON_COLOR,
            fg='white',
            font=('Arial', 10, 'bold'),
            activebackground=ACTIVE_COLOR,
            activeforeground='white',
            command=error_window.destroy
        )
        button.pack(pady=10)