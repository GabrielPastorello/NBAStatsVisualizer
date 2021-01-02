from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import shotchartdetail

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib import cm
from matplotlib.patches import Circle, Rectangle, Arc, ConnectionPatch
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import LinearSegmentedColormap, ListedColormap, BoundaryNorm
from matplotlib.path import Path
from matplotlib.patches import PathPatch

from tkinter import *
from ttkthemes import themed_tk as tk
from tkinter import font
from PIL import ImageTk,Image

def get_player_info(player_name, season_id, season_progress):

    # player dictionary
    nba_players = players.get_players()
    player_dict = [player for player in nba_players if player['full_name'] == player_name][0]

    player_regular_info = playercareerstats.PlayerCareerStats(player_id=int(player_dict['id']), per_mode36='PerGame')
    player_regular_info_df = player_regular_info.get_data_frames()[0]

    season = player_regular_info_df[player_regular_info_df['SEASON_ID'] == season_id]
    PTS = float(season['PTS'])
    REB = float(season['REB'])
    AST = float(season['AST'])
    FG_PCT = round(float(season['FG_PCT']*100), 2)
    FG3_PCT = round(float(season['FG3_PCT']*100), 2)
    FT_PCT = round(float(season['FT_PCT']*100), 2)
    STL = float(season['STL'])
    BLK = float(season['BLK'])
    TOV = float(season['TOV'])

    stats = 'PTS: ' + str(PTS)+'\nREB: ' + str(REB)+'\nAST: ' + str(AST)+'\nFG%: ' + str(FG_PCT)+'%\n3PT%: ' + str(FG3_PCT)+'%\nFT%: ' + str(FT_PCT)+'%\nSTL: ' + str(STL)+'\nBLK: ' + str(BLK)+'\nTOV: ' + str(TOV)

    return stats

def stats_window(player_name, season_id, season_progress):
    try:
        if season_progress != 'Regular Season':
            popupmsg_stats()
        else:   
            stats = get_player_info(player_name, season_id, season_progress)
            newWindow = Toplevel(screen)
            newWindow.geometry('350x290')
            newWindow.title(player_name + ' Stats ' + season_progress)
            newWindow.iconbitmap('nba.ico')
            newWindow.config(background='#17408B')
            stats_name = player_name + ' ' + season_id + ' Stats'
            
            title = Text(newWindow, height=1, borderwidth=0, font=('Trebuchet MS', 14, 'bold'), background='#17408B', fg='white')
            title.tag_configure("center", justify='center')
            title.insert(1.0, stats_name, 'center')
            title.tag_add("center", "1.0", "end")
            title.pack(pady=15)
            title.configure(state="disabled")
            title.configure(inactiveselectbackground=title.cget("selectbackground"))

            stats_screen = Text(newWindow, height=9, borderwidth=0, font=('Helvetica', 14), background='#17408B', fg='white')
            stats_screen.tag_configure("center", justify='center')
            stats_screen.insert(1.0, stats, 'center')
            stats_screen.tag_add("center", "1.0", "end")
            stats_screen.pack(pady=10)
            stats_screen.configure(state="disabled")
            stats_screen.configure(inactiveselectbackground=stats_screen.cget("selectbackground"))
    except:
        popupmsg_stats()
        

def get_player_shotchartdetail(player_name, season_id, season_progress):

    # player dictionary
    nba_players = players.get_players()
    player_dict = [player for player in nba_players if player['full_name'] == player_name][0]

    # career dataframe
    career = playercareerstats.PlayerCareerStats(player_id=player_dict['id'])
    career_df = career.get_data_frames()[0]

    # team id during the season
    team_id = career_df[career_df['SEASON_ID'] == season_id]['TEAM_ID']

    # shotchartdetail endpoints
    shotchartlist = shotchartdetail.ShotChartDetail(team_id=int(team_id),
                                                    player_id=int(player_dict['id']),
                                                    season_type_all_star=season_progress,
                                                    season_nullable=season_id,
                                                    context_measure_simple='FGA').get_data_frames()

    return shotchartlist[0], shotchartlist[1]

def draw_court(ax=None, color="blue", lw=1, outer_lines=False):

    if ax is None:
        ax = plt.gca()

    # Basketball Hoop
    hoop = Circle((0,0), radius=7.5, linewidth=lw, color=color, fill=False)
    # Backboard
    backboard = Rectangle((-30, -12.5), 60, 0, linewidth=lw, color=color)
    # The paint
    # outer box
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color, fill=False)
    # inner box
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color, fill=False)
    # Free Throw Top Arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180, linewidth=lw, color=color, fill=False)
    # Free Bottom Top Arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color)
    # Restricted Zone
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color)
    # Three Point Line
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw, color=color)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw, color=color)
    # Center Court
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0, linewidth=lw, color=color)
    # list of court shapes
    court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw, bottom_free_throw, restricted, corner_three_a, corner_three_b, three_arc, center_outer_arc, center_inner_arc]
    #outer_lines=True
    if outer_lines:
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw, color=color, fill=False)
        court_elements.append(outer_lines)

    for element in court_elements:
        ax.add_patch(element)

def shot_chart(data, title="", color="b", xlim=(-250, 250), ylim=(422.5, -47.5), line_color="#00158f",
               court_color="#f5f5f5", court_lw=2, outer_lines=False,
               flip_court=False, gridsize=None,
               ax=None, despine=False):

    if ax is None:
        ax = plt.gca()
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)

    if not flip_court:
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
    else:
        ax.set_xlim(xlim[::-1])
        ax.set_ylim(ylim[::-1])

    ax.tick_params(labelbottom="off", labelleft="off")
    ax.set_title(title, fontsize=18)

    # draws the court using the draw_court()
    draw_court(ax, color=line_color, lw=court_lw, outer_lines=outer_lines)

    # separate color by make or miss
    x_missed = data[data['EVENT_TYPE'] == 'Missed Shot']['LOC_X']
    y_missed = data[data['EVENT_TYPE'] == 'Missed Shot']['LOC_Y']

    x_made = data[data['EVENT_TYPE'] == 'Made Shot']['LOC_X']
    y_made = data[data['EVENT_TYPE'] == 'Made Shot']['LOC_Y']

    # Plot missed shots
    ax.scatter(x_missed, y_missed, c='r', cmap='coolwarm_r')
    # Plot made shots
    ax.scatter(x_made, y_made, c='g', cmap='coolwarm_r')

    # Set the spines to match the rest of court lines, makes outer_lines
    # somewhat unnecessary
    for spine in ax.spines:
        ax.spines[spine].set_lw(court_lw)
        ax.spines[spine].set_color(line_color)

    if despine:
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)

    return ax

def popupmsg_shotchart(msg, season_id):
    msg = str(msg)
    if msg == 'list index out of range':
        response = messagebox.showinfo("Error", "It was not possible to create your shot chart:\n\nMake sure you typed the player name correctly")
    if msg == "cannot convert the series to <class 'int'>" and season_id != 'Career':
        response = messagebox.showinfo("Error", "It was not possible to create your shot chart:\n\nMake sure you selected a valid season")

def popupmsg_stats():
    response = messagebox.showinfo("Error", "It was not possible to show the stats for this player:\n\nMake sure you typed the player name correctly and selected a valid season;\nStats are only avaliable for regular season")

def myClick():
    player_name = e.get()
    season_id = clicked.get()
    if len(season_id) > 7:
        season_id = season_id[2:9]
    season_progress = clicked2.get()
    try:
        stats_window(player_name, season_id, season_progress)
    except:
        popupmsg_stats()

def myClick2():
    player_name = e.get()
    season_id = clicked.get()
    if len(season_id) > 7:
        season_id = season_id[2:9]
    season_progress = clicked2.get()
    try:
        player_shotchart_df, league_avg = get_player_shotchartdetail(player_name, season_id, season_progress)

        shot_chart(player_shotchart_df, title=player_name+' Shot Chart ' + season_id + '\n' + season_progress)

        plt.rcParams['figure.figsize'] = (12, 11)
        plt.show()
    except (TypeError, IndexError) as er:
        popupmsg_shotchart(er, season_id)
    
screen = tk.ThemedTk()
screen.get_themes()
screen.set_theme("breeze")

width_of_window = 500
height_of_window = 470

screen_width = screen.winfo_screenwidth()
screen_height = screen.winfo_screenheight()

x_coordinate = int((screen_width/2) - (width_of_window/2))
y_coordinate = int((screen_height/2) - (height_of_window/2))

screen.geometry("{}x{}+{}+{}".format(width_of_window, height_of_window, x_coordinate, y_coordinate))
screen.title("NBA Stats Visualizer")
screen.iconbitmap('nba.ico')
screen.config(background='#17408B')

img = Image.open("logo-nba.png")
resized = img.resize((70,70), Image.ANTIALIAS)
img = ImageTk.PhotoImage(resized)
Label(screen, image=img, background='#17408B').pack(pady=10)

Label(screen, text="Player Name:", font=('Helvetica', 14, 'bold'), background='#17408B', fg='white').pack()
e = Entry(screen, borderwidth=4)
e.pack()
e.config(fg='black')
#e.insert(0, "Player name here") # initial message (optional)

options = ["1996-97",
            "1997-98",
            "1998-99",
            "1999-00",
            "2000-01",
            "2001-02",
            "2002-03",
            "2003-04",
            "2004-05",
            "2005-06",
            "2006-07",
            "2007-08",
            "2008-09",
            "2009-10",
            "2010-11",
            "2011-12",
            "2012-13",
            "2013-14",
            "2014-15",
            "2015-16",
            "2016-17",
            "2017-18",
            "2018-19",
            "2019-20",
            "2020-21"] # all seasons with valid data

clicked = StringVar()
clicked.set(options[-1:])

season_frame = Frame(screen)
season_frame.pack(pady=20)
season_frame.config(background='#17408B')

season_frame_ = LabelFrame(season_frame, text="Select a Season:", font=('Helvetica', 10, 'bold'), background='#17408B', fg='white')
season_frame_.grid(row=0, column=0, padx=50)
    
drop = OptionMenu(season_frame_, clicked, *options)
drop.pack(pady=10)
drop.config(highlightbackground='#17408B', fg='black')

reg_or_offs = ['Regular Season', 'Playoffs', 'Pre Season']

clicked2 = StringVar()
clicked2.set(reg_or_offs[0])

drop = OptionMenu(season_frame_, clicked2, *reg_or_offs)
drop.pack(pady=10)
drop.config(highlightbackground='#17408B', fg='black')

myButton2 = Button(screen, text="View Stats", command=myClick, fg='black', font=('Helvetica', 14, 'bold'))
myButton2.pack(pady=10)

myButton2 = Button(screen, text="Generate Shot Chart", command=myClick2, fg='black', font=('Helvetica', 14, 'bold'))
myButton2.pack(pady=10)

screen.mainloop()
