from .element_data import *
import matplotlib
matplotlib.use('pgf')
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

# ------ HELPER -------
def _check_axis(axis):
    if not (axis in ['x', 'y']):
        raise Error('Incorrect axis. Try: "x" or "y".')

def _default_rotation(axis):
    if axis == 'x':
        return 'horizontal'
    return 'vertical'

def _interpret_rotation(rotation):
    if rotation == 0:
        return 'horizontal'
    if rotation == 90 or rotation == -90:
        return 'vertical'
    if rotation in ['horizontal', 'vertical']:
        return rotation
    raise Error('Incorrect rotation value. Try: 0/(-)90 or "horizontal"/"vertical".')

def _setup_fonts(plt, font_properties):
    plt.rcParams.update({
    "text.usetex": True,     # use inline math for tikz
    "pgf.rcfonts": False,    # don't setup fonts from rc parameters
    "pgf.texsystem": "pdflatex",
    "font.family": font_properties['font_family'],
    "pgf.preamble": "\n".join([
            r"\usepackage[utf8]{inputenc}",
            r"\usepackage[T1]{fontenc}",
            r"\usepackage{"+font_properties['tex_package']+"}"
        ])
    })

def _calculate_inch_fig_size(width_mm, height_mm):
    return (width_mm * 0.03937007874, height_mm * 0.03937007874)

def _scaleRGB(rgb_list):
    return (rgb_list[0] * 1.0/255.0, rgb_list[1] * 1.0/255.0, rgb_list[2] * 1.0/255.0)

def _mplot_color(rgb_list):
    r,g,b = rgb_list[0] / 255., rgb_list[1] / 255., rgb_list[2] / 255.
    return (r,g,b)

def _label_alignment(rotation : str):
    if rotation=='horizontal': 
        return 'top'
    return 'bottom'

def _plot_lines(ax, data, colors, linewidth):
    i = 0
    for d in data:
        color = _mplot_color(colors[i])
        ax.plot(d[0], d[1], linewidth=linewidth, color=color) 
        i += 1

def _apply_axis_range(ax, axis, axis_properties):
    try:
        axis_range = axis_properties['range'][0], axis_properties['range'][1]
    except:
        axis_range = None

    if axis_range is not None:
        if axis == 'x':
            ax.set_xlim(axis_range)
        else:
            ax.set_ylim(axis_range)

def _apply_x_axes_properties(ax, x_axis_props):
    '''
    Because matplotlib has different function names for each axes, we also need two functions for the two axes.
    '''
    if x_axis_props['use_log_scale']:
        ax.set_xscale('log')

    if x_axis_props['ticks'] is not None:
        ax.set_xticks(x_axis_props['ticks'])
        if not x_axis_props['use_scientific_notations']: # can only apply if we have specific ticks
            ax.set_xticklabels(x_axis_props['ticks'])
    
    ax.xaxis.set_minor_formatter(FormatStrFormatter(""))

def _apply_y_axes_properties(ax, y_axis_props):
    '''
    Because matplotlib has different function names for each axes, we also need two functions for the two axes.
    '''

    if y_axis_props['use_log_scale']:
        ax.set_yscale('log')

    if y_axis_props['ticks'] is not None:
        ax.set_yticks(y_axis_props['ticks'])
        if not y_axis_props['use_scientific_notations']: # can only apply if we have specific ticks
            ax.set_yticklabels(y_axis_props['ticks'])
    
    ax.yaxis.set_minor_formatter(FormatStrFormatter(""))

def _set_labels(fig, ax, labels, fontsize, pad): 
    '''
    Sets fontsize (pt), labels and their rotation.
    The labels are placed at each end of the axes so that we don't waste too much space.
    The correct label position will be calculated automatically.
    Currently the user needs to find suitable ticks, so that labels and ticks don't overlap!
    '''
    axis_labels = labels
    ax.set_xlabel(axis_labels['x']['text'], fontsize=fontsize, ha="right", 
                  va=_label_alignment(axis_labels['x']['rotation']), rotation=axis_labels['x']['rotation'])
    ax.set_ylabel(axis_labels['y']['text'], fontsize=fontsize, ha="right", 
                  va=_label_alignment(axis_labels['y']['rotation']), rotation=axis_labels['y']['rotation'])

    # compute axis size in points
    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    width, height = bbox.width * 72, bbox.height * 72

    # compute relative padding
    lwX = ax.spines['bottom'].get_linewidth()
    # TODO if use_scientific_notations is True, then take ~70% of fontsize * ~1/4 and add it to the padding

    lwY = 0 #ax.spines['left'].get_linewidth()

    # coordinates in percentage of the figure main body size!
    ax.xaxis.set_label_coords(1, -(pad - lwX) / height)

    # coordinates in percentage of the figure main body size!
    ax.yaxis.set_label_coords(-(pad - lwY) / width, 1)

def _apply_axes_properties_and_labels(fig, ax, axis_properties, labels, config, fontsize):
    _apply_axis_range(ax, 'x', axis_properties)
    _apply_axis_range(ax, 'y', axis_properties)

    if not config['has_right_axis']: 
        ax.spines['right'].set_visible(False)
        ax.yaxis.set_ticks_position('left')
    if not config['has_upper_axis']: 
        ax.spines['top'].set_visible(False)
        ax.xaxis.set_ticks_position('bottom')

    tick_lw_pt = config['tick_linewidth_pt']
    plt.tick_params(width=tick_lw_pt, length=(tick_lw_pt * 4), labelsize=fontsize, pad=(tick_lw_pt * 2))
    _set_labels(fig, ax, labels, fontsize, pad=(tick_lw_pt * 6))
    # if use_scientific_notations True, displaystyle is used in pgf --> offset of ticks changes 

    _apply_x_axes_properties(ax, axis_properties['x'])
    _apply_y_axes_properties(ax, axis_properties['y'])

def _place_marker(ax, marker_data):
    try:
        vlines = marker_data['vertical_lines']
    except:
        vlines = []

    for vl in vlines:
        ax.axvline(x=vl['pos'], color=_scaleRGB(vl['color']), linewidth=vl['linewidth_pt'], linestyle=vl['linestyle'])


# ------ FINALLY --------
class MatplotLinePlot(Plot):
    def __init__(self, aspect_ratio, data) -> None:
        self.aspect_ratio = aspect_ratio
        self._data = data
        self._labels = {}
        self._axis_properties = {}
        self._markers = {}
        self._font = {
            "tex_package": "libertine",
            "font_family": "sans-serif",
            "fontsize_pt": 7
        }
        self._grid = {
            "color": [ 230, 230, 230 ],
            "linewidth_pt": 0.25,
            "linestyle": "-"
        }
        self._config = {
            "plot_linewidth_pt": 0.8,
            "tick_linewidth_pt": 0.6,
            "has_upper_axis": False,
            "has_right_axis": False
        }
        self._colors = [ 
                            [232, 181, 88],
                            [5, 142, 78],
                            [94, 163, 188],
                            [181, 63, 106], 
                            [255, 255, 255]
                        ]

    def get_colors(self):
        return self._colors

    def set_colors(self, color_list):
        '''
        color list contains a list of colors. A color is defined as [r,g,b] while each channel
        ranges from 0 to 255.
        '''
        self._colors = color_list

    def get_axis_label(self, axis=None):
        if axis is None:
            return self._labels
        _check_axis(axis)
        try:
            return self._labels[axis]
        except:
            raise Error('Label is not defined.')

    def set_axis_label(self, axis, txt, rotation=None):
        _check_axis(axis)

        if rotation is not None:
            rotation = _interpret_rotation(rotation)
        else:
            rotation = _default_rotation(axis)

        self._labels[axis] = {}
        self._labels[axis]['text'] = txt
        self._labels[axis]['rotation'] = rotation

    def get_axis_properties(self, axis):
        _check_axis(axis)
        try:
            return self._axis_properties[axis]
        except:
            raise Error('Label is not defined.')

    def set_axis_properties(self, axis, ticks, range=None, use_log_scale=True, use_scientific_notations=False):
        '''
        The user should find and define suitable ticks so that the labels and ticks don't overlap.
        Would be nice to do that automatically at some point.
        '''
        _check_axis(axis)
        if range is not None and len(range) != 2:
            raise Error('You need exactly two values to specify range: [min, max]')

        self._axis_properties[axis] = {}
        if range is not None:
            self._axis_properties[axis]['range'] = range
        self._axis_properties[axis]['ticks'] = ticks
        self._axis_properties[axis]['use_log_scale'] = use_log_scale
        self._axis_properties[axis]['use_scientific_notations'] = use_scientific_notations

    def get_v_line(self):
        try:
            test = self._markers['vertical_lines'][0]
            return self._markers['vertical_lines']
        except:
            return []

    def set_v_line(self, pos, color, linestyle, linewidth_pt=.8):
        '''
        Currently, we only implemented "vertical_lines"
        linestyle allows matplotlib inputs, e.g. (0,(4,6)) is valid.
        '''
        try:
            test = self._markers['vertical_lines'][0]
        except:
            self._markers['vertical_lines'] = []
        self._markers['vertical_lines'].append({
            'pos': pos,
            'color': color,
            "linestyle": linestyle,
            "linewidth_pt": linewidth_pt,
        })

    def get_font(self):
        return self._font

    def set_font(self, fontsize_pt=None, font_family=None, tex_package=None):
        if fontsize_pt is not None:
            self._font["fontsize_pt"] = fontsize_pt
        if font_family is not None:
            self._font["font_family"] = font_family
        if tex_package is not None:
            self._font["tex_package"] = tex_package

    def set_grid_properties(self, color=None, linewidth_pt=None, linestyle=None):
        if color is not None:
            self._grid["color"] = color
        if linewidth_pt is not None:
            self._grid["linewidth_pt"] = linewidth_pt
        if linestyle is not None:
            self._grid["linestyle"] = linestyle

    def show_upper_axis(self, show=True):
        self._config["has_upper_axis"] = show

    def show_right_axis(self, show=True):
        self._config["has_right_axis"] = show

    def set_linewidth(self, plot_line_pt=None, tick_line_pt=None):
        if plot_line_pt is not None:
            self._config['plot_linewidth_pt'] = plot_line_pt
        if tick_line_pt is not None:
            self._config['tick_linewidth_pt'] = tick_line_pt

    def _make(self, width_mm, height_mm, filename):
        _setup_fonts(plt, self._font) 
        figsize = _calculate_inch_fig_size(width_mm, height_mm)
        
        #constrained_layout: https://matplotlib.org/3.2.1/tutorials/intermediate/constrainedlayout_guide.html
        fig, ax = plt.subplots(figsize=figsize, constrained_layout=True)
        fig.set_constrained_layout_pads(w_pad=0, h_pad=0,
            hspace=0., wspace=0.)

        _plot_lines(ax, self._data, self._colors, self._config['plot_linewidth_pt'])
        _apply_axes_properties_and_labels(fig, ax, self._axis_properties, self._labels, self._config, self._font['fontsize_pt'])
        plt.grid(color=_scaleRGB(self._grid['color']), linestyle=self._grid['linestyle'], linewidth=self._grid['linewidth_pt'])
        _place_marker(ax, self._markers)
        plt.savefig(filename, pad_inches=0.0, dpi=500)

    def make_png(self, width_mm, height_mm, filename):
        self._make(width_mm, height_mm, filename)

    def make_pdf(self, width_mm, height_mm, filename):
        self._make(width_mm, height_mm, filename)