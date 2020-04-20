#from tkinter.filedialog import askopenfilename, askdirectory
import threading
import tkinter as tk
from tkinter import ttk, filedialog, font

import tkthread as tkt  # TkThread

# from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from src.youtube_download import YouTubeDownloader

# Implement the default Matplotlib key bindings.
'''from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure'''
#import queue
import re
import os
import pyglet
import requests
from PIL import ImageTk, Image

class GeniusBot:
    hex_color_background = '#3E4A57'
    progress_bar = None
    value = 0
    max_value = 0
    w_text = None
    tkt = None
    url_list = []
    root = None
    youtube_downloader = None
    save_location = os.getcwd()
    style = None
    font = None
    tabControl = None
    version = "1.02"

    def __init__(self, root_main, tkt_main):
        self.root = root_main
        self.tkt = tkt_main
        self.init_font()
        self.init_icon()
        #self.root.geometry("500x700")
        #self.root.minsize(500, 700)
        self.init_styles()
        self.init_main_frame()
        #self.init_youtube_frame()
        self.youtube_downloader = YouTubeDownloader()

    def init_font(self):
        self.fontpath = f'{os.pardir}/fonts/OpenSans/OpenSans-Regular.ttf'
        self.fontpath_alt = f'{os.curdir}/fonts/OpenSans/OpenSans-Regular.ttf'
        if os.path.isfile(self.fontpath):
            pyglet.font.add_file(self.fontpath)
            action_man = pyglet.font.load('OpenSans')
            self.font = tk.font.Font(family="OpenSans", size=10)
            #self.font = tk.font.Font(family="Times New Roman", size=12)
            print("Using Open_Sans")
        elif os.path.isfile(self.fontpath_alt):
            pyglet.font.add_file(self.fontpath_alt)
            action_man = pyglet.font.load('OpenSans')
            self.font = tk.font.Font(family="OpenSans", size=10)
            #self.font = tk.font.Font(family="Times New Roman", size=12)
            print("Using Open_Sans")
        else:
            print("Using Times new Roman")
            self.font = tk.font.Font(family="Times New Roman", size=10)

    def init_icon(self):
        self.iconpath = f'{os.pardir}/img/geniusbot.ico'
        if os.path.isfile(self.iconpath):
            print("File Found")
        else:
            self.iconpath = f'{os.pardir}/GeniusBot/img/geniusbot.ico'
        print(self.iconpath)
        self.root.iconbitmap(self.iconpath)

    def init_styles(self):
        self.style = ttk.Style()
        self.style.theme_create("GeniusBot", parent="alt", settings={
            "TNotebook": {"configure": {"tabmargins": [1, 5, 1, 0]}, "background": "white"},
            "TNotebook.Tab": {
                "configure": {"padding": [5, 1], "background": "black"},
                "map": {"background": [("selected", "black")],
                        "expand": [("selected", [1, 1, 1, 0])]}}})
        self.style.configure("TFrame", forground="black", font=self.font, background=self.hex_color_background)
        self.style.configure("TButton", foreground="#081e2a", font=self.font, background=self.hex_color_background)
        self.style.configure("Add.TButton", foreground="green", font=self.font, background="green")
        self.style.configure("Open.TButton", foreground="orange", font=self.font, background="orange")
        self.style.configure("Remove.TButton", foreground="red", font=self.font, background="red")
        self.style.configure("TLabel", foreground="black", font=self.font, background=self.hex_color_background)
        self.style.configure("Status.TLabel", foreground="white", font=self.font, background=self.hex_color_background)
        self.style.configure("Title.TLabel", foreground="white", background=self.hex_color_background, font=("OpenSans", 21), anchor="center")
        self.style.configure("SecondTitle.TLabel", font=tk.font.Font(family="OpenSans", size=14), anchor="center", foreground="white")
        self.style.configure("Version.TLabel", font=tk.font.Font(family="OpenSans", size=14), anchor="center", foreground="#0099d8")
        self.style.configure('.', font=self.font, foreground="white")
        self.style.configure("Notes.TLabel", font=self.font, anchor="center", foreground="white")
        self.style.configure("TMenubutton", font=self.font, anchor="center", foreground="black")
        self.style.configure("File.TLabel", background=self.hex_color_background, foreground="white", font=self.font, borderwidth=5, relief="ridge")
        self.style.configure("Top.TFrame", background=self.hex_color_background, font=self.font)
        self.style.configure("TNotebook", font=self.font, background=self.hex_color_background, borderwidth=0)
        self.style.configure("TNotebook.Tab", font=self.font, background=self.hex_color_background, foreground="black", lightcolor="grey", borderwidth=2)

    def init_main_frame(self):
        # Frame UI
        tk.Grid.rowconfigure(self.root, 0, minsize=1, weight=1)
        tk.Grid.columnconfigure(self.root, 0, minsize=1, weight=1)
        self.main_frame = ttk.Frame(self.root)
        tk.Grid.rowconfigure(self.main_frame, 0, minsize=1, weight=0)
        tk.Grid.rowconfigure(self.main_frame, 1, minsize=1, weight=1)
        tk.Grid.rowconfigure(self.main_frame, 2, minsize=1, weight=0)
        tk.Grid.columnconfigure(self.main_frame, 0, minsize=1, weight=1)
        self.main_frame.grid(row=0, column=0, sticky='NSEW')
        self.title = tk.StringVar()
        self.title.set("GeniusBot")
        self.title_frame = ttk.Frame(self.main_frame)
        tk.Grid.rowconfigure(self.title_frame, 0, minsize=1, weight=0)
        tk.Grid.columnconfigure(self.title_frame, 0, minsize=1, weight=1)
        self.title_label = ttk.Label(self.title_frame, textvariable=self.title, style="Title.TLabel")
        self.tabControl = ttk.Notebook(self.main_frame)
        self.notification_frame = ttk.Frame(self.main_frame)
        #self.home_tab = tk.Frame(self.tabControl)
        #self.web_archive = tk.Frame(self.tabControl)
        self.report_merger_tab = tk.Frame(self.tabControl)
        self.ftp_interface_tab = tk.Frame(self.tabControl)
        self.title_frame.grid(row=0, column=0, sticky='NSEW')
        self.notification_frame.grid(row=5, column=0, sticky='NSEW')
        #Sets up Status Bar
        self.status = tk.StringVar()
        self.status.set(f"Welcome {os.getlogin()}! Please navigate to a tab to begin using GeniusBot!")
        self.status_label = tk.Label(self.notification_frame, bg=self.hex_color_background, fg="white", bd=1, textvariable=self.status, anchor='w', relief=tk.SUNKEN)
        self.status_label.grid(column=0, row=0, sticky='NSEW', columnspan=1)
        self.init_home_frame()
        self.init_youtube_frame()
        self.init_web_archive_frame()
        self.tabControl.add(self.home_frame, text="Home")
        self.tabControl.add(self.youtube_archive_frame, text="YouTube Archive")
        self.tabControl.add(self.web_archive_frame, text="Web Archive")
        self.tabControl.add(self.report_merger_tab, text="Report Merger")
        self.tabControl.add(self.ftp_interface_tab, text="FTP Interface")
        self.tabControl.grid(column=0, row=1, sticky='NSEW')

    def init_home_frame(self):
        self.home_frame = tk.Frame(self.tabControl)
        tk.Grid.rowconfigure(self.home_frame, 0, minsize=1, weight=0)
        tk.Grid.rowconfigure(self.home_frame, 1, minsize=1, weight=0)
        tk.Grid.rowconfigure(self.home_frame, 2, minsize=1, weight=0)
        tk.Grid.columnconfigure(self.home_frame, 0, minsize=1, weight=1)
        self.top_frame_home = ttk.Frame(self.home_frame)
        #self.tabControl.pack(expand=1, fill="both")
        tk.Grid.rowconfigure(self.top_frame_home, 0, minsize=1, weight=0)
        tk.Grid.rowconfigure(self.top_frame_home, 1, minsize=1, weight=0)
        tk.Grid.rowconfigure(self.top_frame_home, 2, minsize=1, weight=0)
        tk.Grid.columnconfigure(self.top_frame_home, 0, minsize=1, weight=1)
        self.home_title = tk.StringVar()
        self.home_title.set("GeniusBot is a world class tool that allows you to do a lot of useful \nthings from a compact and portable application\n1. YouTube Archive\n2. Web Archive\n2. Report Merger\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        self.home_title_label = ttk.Label(self.top_frame_home, textvariable=self.home_title, style="Notes.TLabel")
        self.top_frame_home.grid(row=1, column=0, sticky='NSEW')
        self.home_title_label.grid(column=0, row=0, columnspan=3)

    def init_youtube_frame(self):
        self.youtube_archive_frame = tk.Frame(self.tabControl)
        tk.Grid.rowconfigure(self.youtube_archive_frame, 0, minsize=1, weight=0)
        tk.Grid.rowconfigure(self.youtube_archive_frame, 1, minsize=1, weight=0)
        tk.Grid.rowconfigure(self.youtube_archive_frame, 2, minsize=1, weight=0)
        tk.Grid.rowconfigure(self.youtube_archive_frame, 3, minsize=1, weight=1)
        tk.Grid.rowconfigure(self.youtube_archive_frame, 4, minsize=1, weight=0)
        tk.Grid.rowconfigure(self.youtube_archive_frame, 5, minsize=1, weight=0)
        tk.Grid.columnconfigure(self.youtube_archive_frame, 0, minsize=1, weight=1)
        self.top_frame = ttk.Frame(self.youtube_archive_frame)
        #self.tabControl.pack(expand=1, fill="both")
        tk.Grid.rowconfigure(self.top_frame, 0, minsize=1, weight=0)
        tk.Grid.rowconfigure(self.top_frame, 1, minsize=1, weight=0)
        tk.Grid.rowconfigure(self.top_frame, 2, minsize=1, weight=0)
        tk.Grid.columnconfigure(self.top_frame, 0, minsize=1, weight=1)
        self.middle_button_frame = ttk.Frame(self.youtube_archive_frame)
        tk.Grid.rowconfigure(self.middle_button_frame, 0, minsize=1, weight=0)
        tk.Grid.columnconfigure(self.middle_button_frame, 0, minsize=1, weight=1)
        tk.Grid.columnconfigure(self.middle_button_frame, 1, minsize=1, weight=1)
        tk.Grid.columnconfigure(self.middle_button_frame, 2, minsize=1, weight=1)
        tk.Grid.columnconfigure(self.middle_button_frame, 3, minsize=1, weight=1)
        self.middle_frame = ttk.Frame(self.youtube_archive_frame)
        tk.Grid.rowconfigure(self.middle_frame, 0, minsize=1, weight=0)
        tk.Grid.rowconfigure(self.middle_frame, 1, minsize=1, weight=1)
        tk.Grid.columnconfigure(self.middle_frame, 0, minsize=1, weight=1)
        self.bottom_frame = ttk.Frame(self.youtube_archive_frame)
        tk.Grid.rowconfigure(self.bottom_frame, 0, minsize=1, weight=1)
        tk.Grid.columnconfigure(self.bottom_frame, 0, minsize=1, weight=1)
        tk.Grid.columnconfigure(self.bottom_frame, 1, minsize=1, weight=1)

        tk.Grid.rowconfigure(self.notification_frame, 0, minsize=1, weight=1)
        tk.Grid.columnconfigure(self.notification_frame, 0, minsize=1, weight=1)
        # Buttons
        self.add_url_button = ttk.Button(self.middle_button_frame, text="Add", style='Add.TButton', width=12, command=self.add_url)
        self.add_url_button.grid(column=0, row=1, sticky='NSEW', padx=5, pady=10)
        self.remove_url_button = ttk.Button(self.middle_button_frame, text="Remove", style='Remove.TButton', width=12, command=self.remove_url)
        self.remove_url_button.grid(column=1, row=1, sticky='NSEW', padx=5, pady=10)
        self.openfile_button = ttk.Button(self.middle_button_frame, text="Open File", style='Open.TButton', width=12, command=self.open_file)
        self.openfile_button.grid(column=2, row=1, sticky='NSEW', padx=5, pady=10)
        self.save_location_button = ttk.Button(self.middle_button_frame, text="Save Location", width=18, command=self.choose_save_location)
        self.save_location_button.grid(column=3, row=1, sticky='NSEW', padx=5, pady=10)
        self.download_button_video = ttk.Button(self.bottom_frame, text="Download Video", command=self.download_videos)
        self.download_button_video.grid(column=0, row=3, sticky='NSEW', padx=5, pady=10)
        self.download_button_audio = ttk.Button(self.bottom_frame, text="Download Audio", command=self.download_audios)
        self.download_button_audio.grid(column=1, row=3, sticky='NSEW', padx=15, pady=10)

        # Labels
        #self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
        self.queue_title = tk.StringVar()
        self.queue_title.set("Download Queue")
        self.queue_title_label = ttk.Label(self.middle_frame, textvariable=self.queue_title, style="Notes.TLabel")
        self.queue_title_label.grid(column=0, row=0, columnspan=3)
        self.youutube_links_text = tk.StringVar()
        self.youutube_links_text.set(r'Enter YouTube Link(s) ⮟')
        self.youutube_links_label = ttk.Label(self.top_frame, textvariable=self.youutube_links_text, style="Notes.TLabel")
        self.youutube_links_label.grid(column=0, row=0, columnspan=2, sticky='W')
        self.youutube_channels_text = tk.StringVar()
        self.youutube_channels_text.set(r'Enter YouTube Channel or User ⮞')
        self.youutube_channels_label = ttk.Label(self.top_frame, textvariable=self.youutube_channels_text, style="Notes.TLabel")
        self.youutube_channels_label.grid(column=0, row=4, columnspan=2, sticky='W')
        self.percentage_text = tk.StringVar()
        self.percentage_text.set(f"{self.value}/{self.max_value} | {(self.value/(self.max_value+1))*100}%")
        self.percentage_label = ttk.Label(self.bottom_frame, textvariable=self.percentage_text, style="Notes.TLabel")
        self.percentage_label.grid(column=0, row=2, columnspan=2)
        self.percentage_title = tk.StringVar()
        self.percentage_title.set("Percentage")
        self.percentage_title_label = ttk.Label(self.bottom_frame, textvariable=self.percentage_title, style="Notes.TLabel")
        self.percentage_title_label.grid(column=0, row=0, columnspan=2)

        # ListBox
        self.url_listbox = tk.Listbox(self.middle_frame, height=12)
        self.url_listbox.grid(column=0, row=1, columnspan=3, rowspan=3, sticky='NSEW')
        tk.Grid.columnconfigure(self.url_listbox, 0, weight=1)

        # Entries
        self.url_entry = tk.Text(self.top_frame, height=9)
        self.channel_entry = tk.Text(self.top_frame, height=1, width=33)
        #tk.Grid.columnconfigure(self.url_entry, 0, weight=1)
        self.channel_entry.bind("<Tab>", self.focus_next_widget)
        self.channel_entry.grid(column=1, row=4, columnspan=2, stick='NSEW')
        self.url_entry.bind("<Tab>", self.focus_next_widget)
        self.refresh_list()
        self.url_entry.grid(column=0, row=2, columnspan=3, sticky='NSEW')

        # Progress Bar
        self.progress_bar = ttk.Progressbar(
            self.bottom_frame, orient="horizontal",
            length=300, mode="determinate"
        )
        self.progress_bar.grid(column=0, row=1, padx=15, pady=10, columnspan=3, sticky='NSEW')
        self.top_frame.grid(row=1, column=0, sticky='NSEW')
        self.middle_button_frame.grid(row=2, column=0, sticky='NSEW')
        self.middle_frame.grid(row=3, column=0, sticky='NSEW')
        self.bottom_frame.grid(row=4, column=0, sticky='NSEW')
        self.title_label.grid(column=0, row=0, sticky='NSEW', columnspan=1, padx=10, pady=10)

    def init_web_archive_frame(self):
        self.web_archive_frame = tk.Frame(self.tabControl)
        tk.Grid.rowconfigure(self.web_archive_frame, 0, minsize=1, weight=1)
        tk.Grid.columnconfigure(self.web_archive_frame, 0, minsize=1, weight=0)
        tk.Grid.columnconfigure(self.web_archive_frame, 1, minsize=1, weight=1)
        self.web_archive_selection_frame = ttk.Frame(self.web_archive_frame)
        tk.Grid.rowconfigure(self.web_archive_selection_frame, 0, minsize=1, weight=0)
        tk.Grid.rowconfigure(self.web_archive_selection_frame, 1, minsize=1, weight=0)
        tk.Grid.rowconfigure(self.web_archive_selection_frame, 2, minsize=1, weight=0)
        tk.Grid.rowconfigure(self.web_archive_selection_frame, 3, minsize=1, weight=1)
        tk.Grid.rowconfigure(self.web_archive_selection_frame, 4, minsize=1, weight=0)
        tk.Grid.rowconfigure(self.web_archive_selection_frame, 5, minsize=1, weight=0)
        tk.Grid.columnconfigure(self.web_archive_selection_frame, 0, minsize=1, weight=1)
        self.web_archive_config_frame = ttk.Frame(self.web_archive_frame)
        tk.Grid.rowconfigure(self.web_archive_config_frame, 0, minsize=1, weight=0)
        tk.Grid.columnconfigure(self.web_archive_config_frame, 0, minsize=1, weight=0)
        self.top_web_frame = ttk.Frame(self.web_archive_selection_frame)
        #self.tabControl.pack(expand=1, fill="both")
        tk.Grid.rowconfigure(self.top_web_frame, 0, minsize=1, weight=0)
        tk.Grid.rowconfigure(self.top_web_frame, 1, minsize=1, weight=0)
        tk.Grid.rowconfigure(self.top_web_frame, 2, minsize=1, weight=0)
        tk.Grid.columnconfigure(self.top_web_frame, 0, minsize=1, weight=1)
        self.middle_web_button_frame = ttk.Frame(self.web_archive_selection_frame)
        tk.Grid.rowconfigure(self.middle_web_button_frame, 0, minsize=1, weight=0)
        tk.Grid.columnconfigure(self.middle_web_button_frame, 0, minsize=1, weight=1)
        tk.Grid.columnconfigure(self.middle_web_button_frame, 1, minsize=1, weight=1)
        tk.Grid.columnconfigure(self.middle_web_button_frame, 2, minsize=1, weight=1)
        tk.Grid.columnconfigure(self.middle_web_button_frame, 3, minsize=1, weight=1)
        self.middle_web_frame = ttk.Frame(self.web_archive_selection_frame)
        tk.Grid.rowconfigure(self.middle_web_frame, 0, minsize=1, weight=0)
        tk.Grid.rowconfigure(self.middle_web_frame, 1, minsize=1, weight=1)
        tk.Grid.columnconfigure(self.middle_web_frame, 0, minsize=1, weight=1)
        self.bottom_web_frame = ttk.Frame(self.web_archive_selection_frame)
        tk.Grid.rowconfigure(self.bottom_web_frame, 0, minsize=1, weight=1)
        tk.Grid.columnconfigure(self.bottom_web_frame, 0, minsize=1, weight=1)
        tk.Grid.columnconfigure(self.bottom_web_frame, 1, minsize=1, weight=1)

        tk.Grid.rowconfigure(self.notification_frame, 0, minsize=1, weight=1)
        tk.Grid.columnconfigure(self.notification_frame, 0, minsize=1, weight=1)
        # Buttons
        self.web_add_url_button = ttk.Button(self.middle_web_button_frame, text="Add", style='Add.TButton', width=9, command=self.add_url)
        self.web_add_url_button.grid(column=0, row=1, sticky='NSEW', padx=5, pady=10)
        self.web_remove_url_button = ttk.Button(self.middle_web_button_frame, text="Remove", style='Remove.TButton', width=9, command=self.remove_url)
        self.web_remove_url_button.grid(column=1, row=1, sticky='NSEW', padx=5, pady=10)
        self.web_openfile_button = ttk.Button(self.middle_web_button_frame, text="Open File", style='Open.TButton', width=9, command=self.open_file)
        self.web_openfile_button.grid(column=2, row=1, sticky='NSEW', padx=5, pady=10)
        self.web_save_location_button = ttk.Button(self.middle_web_button_frame, text="Save Location", width=15, command=self.choose_save_location)
        self.web_save_location_button.grid(column=3, row=1, sticky='NSEW', padx=5, pady=10)
        self.web_download_button = ttk.Button(self.bottom_web_frame, text="Begin Archive", command=self.download_videos)
        self.web_download_button.grid(column=0, row=3, columnspan=2, sticky='NSEW', padx=15, pady=10)

        # Labels
        #self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
        self.web_queue_title = tk.StringVar()
        self.web_queue_title.set("Download Queue")
        self.web_queue_title_label = ttk.Label(self.middle_web_frame, textvariable=self.web_queue_title, style="Notes.TLabel")
        self.web_queue_title_label.grid(column=0, row=0, columnspan=1)
        self.web_config_title = tk.StringVar()
        self.web_config_title.set("Configure Archive")
        self.web_config_title_label = ttk.Label(self.web_archive_config_frame, textvariable=self.web_config_title, style="Notes.TLabel")
        self.web_config_title_label.grid(column=0, row=0, columnspan=1)
        self.web_links_text = tk.StringVar()
        self.web_links_text.set(r'Enter Web Link(s) ⮟')
        self.web_links_label = ttk.Label(self.top_web_frame, textvariable=self.web_links_text, style="Notes.TLabel")
        self.web_links_label.grid(column=0, row=0, columnspan=1, sticky='W')
        self.web_percentage_text = tk.StringVar()
        self.web_percentage_text.set(f"{self.value}/{self.max_value} | {(self.value/(self.max_value+1))*100}%")
        self.web_percentage_label = ttk.Label(self.bottom_web_frame, textvariable=self.percentage_text, style="Notes.TLabel")
        self.web_percentage_label.grid(column=0, row=2, columnspan=2)
        self.web_percentage_title = tk.StringVar()
        self.web_percentage_title.set("Percentage")
        self.web_percentage_title_label = ttk.Label(self.bottom_web_frame, textvariable=self.web_percentage_title, style="Notes.TLabel")
        self.web_percentage_title_label.grid(column=0, row=0, columnspan=2)

        # ListBox
        self.web_url_listbox = tk.Listbox(self.middle_web_frame, height=12)
        self.web_url_listbox.grid(column=0, row=1, columnspan=2, rowspan=3, sticky='NSEW')
        tk.Grid.columnconfigure(self.url_listbox, 0, weight=1)

        # Entries
        self.web_url_entry = tk.Text(self.top_web_frame, height=9)
        self.web_url_entry.bind("<Tab>", self.focus_next_widget)
        self.refresh_list()
        self.web_url_entry.grid(column=0, row=2, columnspan=2, sticky='NSEW')

        # Progress Bar
        self.web_progress_bar = ttk.Progressbar(
            self.bottom_web_frame, orient="horizontal",
            mode="determinate"
        )
        self.web_archive_selection_frame.grid(column=1, row=0, columnspan=1, sticky='NSEW')
        self.web_archive_config_frame.grid(column=0, row=0, columnspan=1, sticky='NSEW')
        self.web_progress_bar.grid(column=0, row=1, padx=15, pady=10, columnspan=2, sticky='NSEW')
        self.top_web_frame.grid(row=1, column=0, sticky='NSEW')
        self.middle_web_button_frame.grid(row=2, column=0, sticky='NSEW')
        self.middle_web_frame.grid(row=3, column=0, sticky='NSEW')
        self.bottom_web_frame.grid(row=4, column=0, sticky='NSEW')
        #self.title_label.grid(column=0, row=0, sticky='NSEW', columnspan=1, padx=10, pady=10)

    def run(self, func, name=None):
        threading.Thread(target=func, name=name).start()

    # This class handles [TAB] Key to move to next Widget
    def focus_next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return("break")

    def choose_save_location(self):
        self.save_location = tk.filedialog.askdirectory()
        print("Save Filepath: ", self.save_location)
        self.youtube_downloader.set_save_path(self.save_location)

    def open_file(self):
        name = tk.filedialog.askopenfilename(initialdir=os.getcwd(),
                               filetypes=(("Text File", "*.txt"), ("All Files", "*.*")),
                               title="Choose a file."
                               )
        # Using try in case user types in unknown file or closes without choosing a file.
        try:
            youtube_urls = open(name, 'r')
            print("youtube_urls", youtube_urls)
            print("Length of Links Before Open File: ", len(self.url_list))
            for url in youtube_urls:
                self.url_list.append(url)
            self.refresh_list()
            self.max_value = len(self.url_list)
            self.percentage_text.set(f"{self.value}/{self.max_value} | {(self.value / self.max_value) * 100}%")
            self.status.set(f'Queued {self.max_value} videos from file: {name}')
        except:
            print("No file exists")
            self.status.set(f'File Not Found')

    def refresh_list(self):
        self.url_listbox.delete(0, tk.END)
        self.url_list = list(dict.fromkeys(self.url_list))
        for items in self.url_list:
            self.url_listbox.insert(tk.END, items)

    def add_url(self):
        # Get Channel
        parse_channel_addition=""
        parse_channel_addition = self.channel_entry.get("1.0", tk.END)
        print("Parsed Addition: ", parse_channel_addition)
        if re.sub(r'[^A-Za-z0-9_./:&-?!=]', '', parse_channel_addition) != "":
            parse_channel_addition = parse_channel_addition.rstrip()
            self.youtube_downloader.get_channel_videos(parse_channel_addition)
            parse_addition_array = self.youtube_downloader.get_link()
            self.youtube_downloader.reset_links()
            for url in parse_addition_array:
                if re.sub(r'[^A-Za-z0-9_./:&-?!=]', '', url) != "":
                    self.status.set(f'Added URLs to Queue')
                    temp = re.sub(r'[^A-Za-z0-9_./:&-?!=]', '', url)
                    print("Appended: ", temp)
                    self.url_list.append(temp)
                else:
                    print("Bad URL: ", url)
                    self.status.set(f'Paste Some YouTube Links First! (CTRL+V) {url}')
            self.url_list = list(dict.fromkeys(self.url_list))
            self.channel_entry.delete("1.0", tk.END)
            self.refresh_list()
            self.max_value = len(self.url_list)
            self.percentage_text.set(f"{self.value}/{self.max_value} | {(self.value / self.max_value) * 100}%")
            self.status.set(f'Queued {self.max_value} videos')
        # Get Videos
        parse_addition = self.url_entry.get("1.0", tk.END)
        if re.sub(r'[^A-Za-z0-9_./:&?!=-]', '', parse_addition) != "":
            parse_addition_array = parse_addition.splitlines()
            for url in parse_addition_array:
                if re.sub(r'[^A-Za-z0-9_./:&?!=-]', '', url) != "":
                    self.status.set(f'Added URLs to Queue')
                    temp = re.sub(r'[^A-Za-z0-9_./:&?!=-]', '', url)
                    self.url_list.append(temp)
                else:
                    print("Bad URL: ", url)
                    self.status.set(f'Paste Some YouTube Links First! (CTRL+V) {url}')
            self.url_list = list(dict.fromkeys(self.url_list))
            self.url_entry.delete("1.0", tk.END)
            self.refresh_list()
            self.max_value = len(self.url_list)
            self.percentage_text.set(f"{self.value}/{self.max_value} | {(self.value / self.max_value) * 100}%")
            self.status.set(f'Queued {self.max_value} videos')

    def remove_url(self):
        if self.url_listbox.curselection():
            url = self.url_listbox.get(self.url_listbox.curselection())
            url = url.rstrip()
            self.status.set(f'Removed URL: {url}')
            print("Removing URL: ", self.url_listbox.get(self.url_listbox.curselection()))
            self.url_list.remove(self.url_listbox.get(self.url_listbox.curselection()))
            self.refresh_list()
            self.max_value = len(self.url_list)
            if self.max_value == 0:
                self.percentage_text.set(f"{self.max_value}/{self.max_value} | {(0) * 100}%")
                self.progress_bar['value'] = 0
                self.value = 0
            else:
                self.percentage_text.set(f"{self.max_value}/{self.max_value} | {(self.value / self.max_value) * 100}%")
                self.progress_bar['value'] = self.max_value
                self.value = self.max_value
            self.status.set(f'Queued {self.max_value} videos')
        else:
            print("Click on a link to remove")
            self.status.set(f'Click on a URL to remove')

    def download_video_threaded(self, tkt_wrap):
        self.url_list = list(filter(None, self.url_list))
        self.url_list = list(dict.fromkeys(self.url_list))
        self.max_value = len(self.url_list)
        if self.max_value > 0:
            self.status.set(f'Downloading {len(self.url_list)} URL(s)')
            #self.tabControl.tab(2, state="disabled")
            #self.tabControl.tab(3, state="disabled")
            self.download_button_video["state"] = "disabled"
            self.download_button_audio["state"] = "disabled"
            self.add_url_button["state"] = "disabled"
            self.remove_url_button["state"] = "disabled"
            self.openfile_button["state"] = "disabled"
            self.save_location_button["state"] = "disabled"
            self.value = 0
            th = threading.current_thread()
            self.progress_bar['maximum'] = self.max_value
            self.progress_bar['value'] = 0
            self.percentage_text.set(f"{self.value}/{self.max_value} | {(self.value / self.max_value) * 100}%")
            i = 0
            for url in self.url_list:
                self.youtube_downloader.append_link(url)
                print("Links Sent: ", self.youtube_downloader.get_link())
                self.youtube_downloader.download_hd_videos()
                self.youtube_downloader.reset_links()
                txt = 'Progress: %02i' % (i + 1)
                print(th, txt)  # send to terminal
                self.value = i + 1
                self.percentage_text.set(f"{self.value}/{self.max_value} | {(self.value / self.max_value) * 100}%")
                self.progress_bar['value'] = i + 1
                print("Value: ", self.value)
                print("Max Value: ", self.max_value)
                # tkt_wrap(entry.delete, '0', 'end')
                # tkt_wrap(entry.set(txt))
                self.status.set(f'Completed {self.value}/{self.max_value}')
                i += 1
            self.tabControl.tab(2, state="normal")
            self.tabControl.tab(3, state="normal")
            self.download_button_video["state"] = "enabled"
            self.download_button_audio["state"] = "enabled"
            self.add_url_button["state"] = "enabled"
            self.remove_url_button["state"] = "enabled"
            self.openfile_button["state"] = "enabled"
            self.save_location_button["state"] = "enabled"
            self.status.set(f'Downloaded {self.value} video(s)!')
        else:
            print("No Videos Added")
            self.status.set(f'Add Some Videos First!')

    def download_audio_threaded(self, tkt_wrap):
        self.url_list = list(filter(None, self.url_list))
        self.url_list = list(dict.fromkeys(self.url_list))
        self.max_value = len(self.url_list)
        if self.max_value > 0:
            self.status.set(f'Downloading {len(self.url_list)} URL(s)')
            self.download_button_video["state"] = "disabled"
            self.download_button_audio["state"] = "disabled"
            self.add_url_button["state"] = "disabled"
            self.remove_url_button["state"] = "disabled"
            self.openfile_button["state"] = "disabled"
            self.save_location_button["state"] = "disabled"
            self.value = 0
            th = threading.current_thread()
            self.progress_bar['maximum'] = self.max_value
            self.progress_bar['value'] = 0
            self.percentage_text.set(f"{self.value}/{self.max_value} | {(self.value / self.max_value) * 100}%")
            i = 0
            for url in self.url_list:
                self.youtube_downloader.append_link(url)
                self.youtube_downloader.download_audio()
                self.youtube_downloader.reset_links()
                txt = 'Progress: %02i' % i
                print(th, txt)  # send to terminal
                self.value = i + 1
                self.percentage_text.set(f"{self.value}/{self.max_value} | {(self.value / self.max_value) * 100}%")
                self.progress_bar['value'] = i + 1
                print("Value: ", self.value)
                print("Max Value: ", self.max_value)
                # tkt_wrap(entry.delete, '0', 'end')
                # tkt_wrap(entry.set(txt))
                self.status.set(f'Completed {self.value}/{self.max_value}')
                i += 1
            self.download_button_video["state"] = "enabled"
            self.download_button_audio["state"] = "enabled"
            self.add_url_button["state"] = "enabled"
            self.remove_url_button["state"] = "enabled"
            self.openfile_button["state"] = "enabled"
            self.save_location_button["state"] = "enabled"
            self.status.set(f'Downloaded {self.value} audio!')
        else:
            print("No Videos Added")
            self.status.set(f'Add Some Videos First!')

    def download_videos(self):
        self.run(lambda: self.download_video_threaded(self.tkt.nosync), name='NoSync')

    def download_audios(self):
        self.run(lambda: self.download_audio_threaded(self.tkt.nosync), name='NoSync')


root = tk.Tk()
root.minsize(width=500, height=700)
root.title("GeniusBot")
root.geometry("500x700")
#root.resizable(width="false", height="false")

#root.minsize(500, 700)
#root.maxsize(width=600, height=800)
tkthread = tkt.TkThread(root)  # make the thread-safe callable
main_ui = GeniusBot(root, tkthread)
root.mainloop()
