'''
Hier werden Globale Einstellungen eingegeben.
'''
__author__ = 'Sebastian Gehrmann'
# Arbeitsdauereinstellungen fuer Servicetechniker
max_arbeitsdauer = 10
soll_arbeitsdauer = 8
# Kernarbeitszeiten, in denen gearbeitet werden soll
zeiten_ab = 8
zeiten_bis = 19
# Zeit, die in die Zukunft geplant werden soll
planungshorizont = 28
#minimum Zeit, die ein Termin in der Zukunft liegt
min_planungshorizont = 7

'''
Der folgende Code ist fuer die schoenere Darstellung mit Matplotlib.
Dieser Code wurde von CS109 (Data Science) der Harvard University uebernommen und leicht veraendert.
'''
import matplotlib.pyplot as plt
from matplotlib import rcParams

#Farbenblindfreundliche Farben
dark2_colors = [(0.10588235294117647, 0.6196078431372549, 0.4666666666666667),
                (0.8509803921568627, 0.37254901960784315, 0.00784313725490196),
                (0.4588235294117647, 0.4392156862745098, 0.7019607843137254),
                (0.9058823529411765, 0.1607843137254902, 0.5411764705882353),
                (0.4, 0.6509803921568628, 0.11764705882352941),
                (0.9019607843137255, 0.6705882352941176, 0.00784313725490196),
                (0.6509803921568628, 0.4627450980392157, 0.11372549019607843)]


def set_plt_options():
    #colorbrewer2 Dark2 qualitative color table

    rcParams['figure.figsize'] = (6, 6)
    rcParams['figure.dpi'] = 150
    rcParams['axes.color_cycle'] = dark2_colors
    rcParams['lines.linewidth'] = 2
    rcParams['axes.facecolor'] = 'white'
    rcParams['font.size'] = 14
    rcParams['patch.edgecolor'] = 'white'
    rcParams['patch.facecolor'] = dark2_colors[0]
    rcParams['font.family'] = 'StixGeneral'


def remove_border(axes=None, top=False, right=False, left=True, bottom=True):
    """
    Minimize chartjunk by stripping out unnecesasry plot borders and axis ticks

    The top/right/left/bottom keywords toggle whether the corresponding plot border is drawn
    """
    ax = axes or plt.gca()
    ax.spines['top'].set_visible(top)
    ax.spines['right'].set_visible(right)
    ax.spines['left'].set_visible(left)
    ax.spines['bottom'].set_visible(bottom)

    #turn off all ticks
    ax.yaxis.set_ticks_position('none')
    ax.xaxis.set_ticks_position('none')

    #now re-enable visibles
    if top:
        ax.xaxis.tick_top()
    if bottom:
        ax.xaxis.tick_bottom()
    if left:
        ax.yaxis.tick_left()
    if right:
        ax.yaxis.tick_right()


