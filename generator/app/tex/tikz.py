import json

# CALCULATIONS FOR HEIGHTS AND WIDTHS
def calculate_min_width(data):
    '''
    Minimum width is the sum of all fixed space/padding based on the json-config file, including titles, offsets, paddings, etc.
    So basically: everything except for the images.
    '''
    num_cols = data['num_columns']

    min_width = data['column_space'] * (num_cols - 1)# + (muliplied by num -1)
    min_width += data['padding']['left'] # +
    min_width += data['padding']['right'] # +
    if (data['element_config']['captions']['east']['width'] > 0.0): # + (muliplied by num)
        min_width += data['element_config']['captions']['east']['offset'] * num_cols # if width # else ignore (muliplied by num)
        min_width += data['element_config']['captions']['east']['width'] * num_cols
    if (data['element_config']['captions']['west']['width'] > 0.0): # + (muliplied by num)
        min_width += data['element_config']['captions']['west']['offset'] * num_cols # if width # else ignore (muliplied by num)
        min_width += data['element_config']['captions']['west']['width'] * num_cols
    if (data['titles']['east']['width'] > 0.0): # + 
        min_width += data['titles']['east']['offset'] + data['titles']['east']['width']
    if (data['titles']['west']['width'] > 0.0): # + 
        min_width += data['titles']['west']['offset'] + data['titles']['west']['width']
    if (data['row_titles']['east']['width'] > 0.0): # + 
        min_width += data['row_titles']['east']['offset'] + data['row_titles']['east']['width']
    if (data['row_titles']['west']['width'] > 0.0): # + 
        min_width += data['row_titles']['west']['offset'] + data['row_titles']['west']['width']
    
    return min_width

def calculate_min_height(data):
    '''
    Minimum height is the sum of all fixed space/padding based on the json-config file, including titles, offsets, paddings, etc.
    So basically: everything except for the images.
    '''
    num_rows = data['num_rows']

    min_height = data['row_space'] * (num_rows -1)
    min_height += data['padding']['top']
    min_height += data['padding']['bottom']
    if (data['element_config']['captions']['north']['height'] > 0.0):
        min_height += data['element_config']['captions']['north']['height'] * num_rows
        min_height += data['element_config']['captions']['north']['offset'] * num_rows
    if (data['element_config']['captions']['south']['height'] > 0.0):
        min_height += data['element_config']['captions']['south']['height'] * num_rows
        min_height += data['element_config']['captions']['south']['offset'] * num_rows
    if (data['titles']['north']['height'] > 0.0):
        min_height += data['titles']['north']['height'] + data['titles']['north']['offset']
    if (data['titles']['south']['height'] > 0.0):
        min_height += data['titles']['south']['height'] + data['titles']['south']['offset']
    if (data['column_titles']['north']['height'] > 0.0):
        min_height += data['column_titles']['north']['height'] + data['column_titles']['north']['offset']
    if (data['column_titles']['south']['height'] > 0.0):
        min_height += data['column_titles']['south']['height'] + data['column_titles']['south']['offset']

    return min_height

def calculate_fixed_inner_height(data):
    '''
    Fixed inner height is the sum of spacing between all images, which also includes element captions 
    '''
    num_rows = data['num_rows']

    inner_height = data['row_space'] * (num_rows -1)
    if (data['element_config']['captions']['north']['height'] > 0.0):
        inner_height += data['element_config']['captions']['north']['height'] * (num_rows -1)
        inner_height += data['element_config']['captions']['north']['offset'] * (num_rows -1)
    if (data['element_config']['captions']['south']['height'] > 0.0):
        inner_height += data['element_config']['captions']['south']['height'] * (num_rows -1)
        inner_height += data['element_config']['captions']['south']['offset'] * (num_rows -1)

    return inner_height

def calculate_fixed_inner_width(data):
    '''
    Fixed inner width is the sum of spacing between all images, which also includes element captions 
    '''
    num_columns = data['num_columns']

    inner_width = data['column_space'] * (num_columns -1)
    if (data['element_config']['captions']['east']['width'] > 0.0):
        inner_width += data['element_config']['captions']['east']['width'] * (num_columns -1)
        inner_width += data['element_config']['captions']['east']['offset'] * (num_columns -1)
    if (data['element_config']['captions']['west']['width'] > 0.0):
        inner_width += data['element_config']['captions']['west']['width'] * (num_columns -1)
        inner_width += data['element_config']['captions']['west']['offset'] * (num_columns -1)

    return inner_width

def calculate_body_width(data):
    '''
    body means: all images and their spaces/padding inbetween the images.
    Careful: Frames are not considered if frame line widht > spaces/paddings! TODO 
    Not included are: column/row titles and titles as well as their corresping offsets.
    '''
    return calculate_fixed_inner_width(data) + data['num_columns'] * data['element_config']['img_width']

def calculate_body_height(data):
    '''
    body means: all images and their spaces/padding inbetween the images.
    Careful: Frames are not considered if frame line widht > spaces/paddings! TODO  
    Not included are: column/row titles and titles as well as their corresping offsets.
    '''
    return calculate_fixed_inner_height(data) + data['num_rows'] * data['element_config']['img_height']

def calculate_total_width(data):
    total_width = calculate_body_width(data)
    if (data['element_config']['captions']['east']['width'] > 0.0):
        total_width += data['element_config']['captions']['east']['width']
        total_width += data['element_config']['captions']['east']['offset']
    if (data['element_config']['captions']['west']['width'] > 0.0):
        total_width += data['element_config']['captions']['west']['width']
        total_width += data['element_config']['captions']['west']['offset']

    if data['row_titles']['west']['width']!=0.0:
        total_width += data['row_titles']['west']['width'] + data['row_titles']['west']['offset']
    if data['row_titles']['east']['width']!=0.0:
        total_width += data['row_titles']['east']['width'] + data['row_titles']['east']['offset']

    if data['titles']['west']['width']!=0.0:
        total_width += data['titles']['west']['width'] + data['titles']['west']['offset']
    if data['titles']['east']['width']!=0.0:
        total_width += data['titles']['east']['width'] + data['titles']['east']['offset']
    
    total_width += data['padding']['left'] + data['padding']['right']
    return total_width 

def calculate_total_height(data):
    total_height = calculate_body_height(data)

    if data['column_titles']['north']['height']!=0.0:
        total_height += data['column_titles']['north']['height'] + data['column_titles']['north']['offset']
    if data['column_titles']['south']['height']!=0.0:
        total_height += data['column_titles']['south']['height'] + data['column_titles']['south']['offset']

    if data['titles']['north']['height']!=0.0:
        total_height += data['titles']['north']['height'] + data['titles']['north']['offset']
    if data['titles']['south']['height']!=0.0:
        total_height += data['titles']['south']['height'] + data['titles']['south']['offset']
    
    total_height += data['padding']['top'] + data['padding']['bottom']
    return total_height

def calculate_vertical_figure_title_height(data):
    vert_title_height = calculate_body_height(data)

    if data['column_titles']['north']['height']!=0.0:
        vert_title_height += data['column_titles']['north']['height'] + data['column_titles']['north']['offset']
    if data['column_titles']['south']['height']!=0.0:
        vert_title_height += data['column_titles']['south']['height'] + data['column_titles']['south']['offset']

    return vert_title_height

def calculate_and_overwrite_img_resolution_based_on_total_width(data):
    num_cols = data['num_columns']
    num_rows = data['num_rows']
    total_width = data['total_width']
    width_to_height_ratio = data['img_height_px'] / data['img_width_px']

    min_height = calculate_min_height(data)
    min_width = calculate_min_width(data)
    width_left_per_img = (total_width - min_width) / num_cols
    if width_left_per_img < 1.0:
        if width_left_per_img < 0.0:
            print('consider less columns or allow as total_width more than '+ str(total_width) + 
            ', because the image width of all images are below 0.0 ' + data['units']+ '. ')
        else: 
            print('consider less columns or allow as total_width more than '+ str(total_width) + 
            ', because the image width of all images are below 1.0 ' + data['units']+ 
            '. If that is fine by you then ignore this message.')

    # force width/height ratio of origin img 
    data['element_config']['img_width'] = width_left_per_img
    data['element_config']['img_height'] = width_left_per_img * width_to_height_ratio

def calculate_and_overwrite_img_resolution_based_on_total_height(data):
    # TODO test function at some point
    num_cols = data['num_columns']
    num_rows = data['num_rows']
    total_height = data['total_height'] 
    heigth_to_width_ratio = data['img_width_px'] / data['img_height_px']

    min_height = calculate_min_height(data)
    min_width = calculate_min_width(data)

    height_left_per_img = (total_height - min_height) / num_rows
    if height_left_per_img < 1.0:
        if height_left_per_img < 0.0:
            print('consider less rows or allow as total_height more than '+ str(total_height) + 
            ', because the image height of the images are below 0.0 ' + data['units']+ '. ')
        else: 
            print('consider less rows or allow as total_height more than '+ str(total_height) + 
            ', because the image height of the images are below 1.0 ' + data['units']+ 
            '. If that is fine by you then ignore this message.')
    
    # force width/height ratio of origin img 
    data['element_config']['img_width'] = height_left_per_img * heigth_to_width_ratio
    data['element_config']['img_height'] = height_left_per_img

def calculate_h_offset_for_title(title_offset, caption_config, row_config):
    offset = title_offset
    if caption_config['width']!=0.0:
        offset += caption_config['width'] + caption_config['offset']
    if row_config['width']!=0.0:
        offset += row_config['width'] + row_config['offset']

    return offset
# END CALCULAITONS



# BEGIN minor utitities for TIKZ generation
def read_optional(data, key, default=None):
    try:
        return data[key]
    except KeyError:
        return default

def is_horizontal(position):
    position0 = position.split(' ')[0]
    if position0=='south' or position0=='north':
        return True
    return False

def is_vertical(position):
    return not is_horizontal(position)

def opposite(position):
    if position=='west':
        return 'east'
    if position=='east':
        return 'west'
    if position=='north':
        return 'south'
    return 'north'

def load_nth_color(color_list, num, idx):
    import numpy as np

    # convert to numpy array to determine shape and force proper data type
    color_array = np.array(color_list, dtype=int)

    if np.any(color_array > 255) or np.any(color_array < 0):
        raise 'Invalid color values'

    if color_array.shape == (3,):
        return color_list # single color
    elif color_array.shape[1] == 3 and color_array.shape[0] >= num:
        return color_list[idx] # ith color of list
    else:
        raise 'Number of colors does not match the number of rows / columns' 

def gen_tikZ_frame(rgb_list, line_width):
    color = gen_tikZ_rgb255(rgb_list)
    return 'draw='+color+', line width='+str(line_width)+', '

def gen_tikZ_rgb255(rgb_list):
    return '{rgb,255:red,'+str(rgb_list[0])+';green,'+str(rgb_list[1])+';blue,'+str(rgb_list[2])+'}'

def gen_frame_specs(element_content):
    try:
        if element_content['frame']['line_width'] == 0.0:
            return ''
        return gen_tikZ_frame(element_content['frame']['color'], element_content['frame']['line_width'])
    except:
        print("frame specs error")

def gen_LaTeX_fontsize(fontsize, line_space):
    line_space = float(fontsize) * line_space
    return '\\fontsize{'+str(fontsize)+'pt}{'+str(fontsize)+'pt}'
# END minor utitities for TIKZ generation


# GENERATING TIKZ NODES
### BEGIN generating basic nodes ###
def gen_plain_node(width, height, name, parent_name = None, position = None, anchor='center', additional_params=''):
    ''' 
    Creates code for a TikZ node. A 'plain' node is a node that does not hold any information (no text, no img), so its mostly used to generate offsets.
    additional params: e.g. 'fill=blue, ' or 'draw, '. You can also combine them like 'fill=blue, draw, '. Important is, that you do not forget the comma 
    at the end. 
    '''
    pos = '(0,0)' 
    if parent_name and position:
        pos = '('+ parent_name + '.' + position +')'
    
    return '\\node[anchor='+ anchor +', minimum width='+ str(width) +'mm, minimum height='+ str(height) +'mm, ' \
        + additional_params+' inner sep=0, outer sep=0] ('+ name +') at ' + pos + ' {}; \n'

def gen_text_node(width, height, text, parent_name, fontsize, position='center', anchor='center', alignment='centering', rotation=0, text_color=None):
    '''
    Creates a node that contains text-based content. In case, the text does not fit in a box of given width and height, the text is 'clipped off'. 
    This makes sure that the text-field has the correct width and height. Width or height can be changed in the json-config.
    '''
    begin_clipping = '\\begin{scope}\n\\clip ('+parent_name+'.south west) rectangle ('+parent_name+'.north east);\n'
    type_field = parent_name.split('-')[0]

    if rotation != 0:
        if type_field=='east' or type_field=='west':
            width, height = height, width

    txt_color=''
    if text_color is not None and text_color!=[0,0,0]:
        txt_color='text='+gen_tikZ_rgb255(text_color)+', '

    node = '\\node[anchor='+ anchor +', minimum width='+ str(width) +'mm, minimum height='+ str(height) +'mm, rotate='+str(rotation)+\
        ', '+ txt_color +'inner sep=0, outer sep=0] at ('+parent_name+'.'+position+') \n'
    node_content = '{\\begin{minipage}[c]['+str(height)+'mm]{'+str(width)+'mm} '+ fontsize + ' \\selectfont \\'+alignment+' \n'+text+'\n\\end{minipage}};\n'
    end_clipping = '\\end{scope}'

    return begin_clipping + node + node_content + end_clipping + '\n'

def gen_img_node(width, height, img_path, name, parent_name=None, position=None, anchor='center', additional_params=None):
    '''
    Creates a node that contains an image. No cropping will be done to the image: The image can distorted, if the width/height ratio is not fitted proberly. 
    addtional params: e.g. 'draw=blue, line width=0.3mm, ' If you want an RGB color, there are functions provided that generates Tikz-friendly 'code'.
    '''
    pos = '(0,0)' 
    if parent_name and position:
        pos = '('+ parent_name + '.' + position +')'

    if additional_params is None:
        additional_params=''

    return '\\node[anchor='+ anchor +', '+ additional_params +' minimum width='+ str(width) +'mm, minimum height='+ str(height) +\
            'mm, inner sep = 0, outer sep = 0] ('+ name +') at '+ pos +' {\\includegraphics[width='+str(width)+'mm, height='+str(height)+'mm]{'+ img_path +'}}; \n'
### END generating basic nodes ###


### BEGIN helper node functions ###
def gen_node_north(width, height, name, parent_name, offset, offset_name, content, fontsize, alignment='centering', rotate_text=0, background_color=None, text_color=None):
    return gen_node_helper('north', 'south', **locals())

def gen_node_south(width, height, name, parent_name, offset, offset_name, content, fontsize, alignment='centering', rotate_text=0, background_color=None, text_color=None):
    return gen_node_helper('south', 'north', **locals())

def gen_node_west(width, height, name, parent_name, offset, offset_name, content, fontsize, alignment='centering', rotate_text=90, background_color=None, text_color=None):
    return gen_node_helper('west', 'east', **locals())

def gen_node_east(width, height, name, parent_name, offset, offset_name, content, fontsize, alignment='centering', rotate_text=90, background_color=None, text_color=None):
    return gen_node_helper('east', 'west', **locals())

def gen_node_helper(position, anchor, width, height, name, parent_name, offset, offset_name, content, fontsize, alignment='centering', 
                    rotate_text=0, background_color=None, text_color=None):
    space_node = ''
    if offset > 0.0: # offset node
        if offset_name is None:
            offset_name = name+'-space'

        space_node = gen_plain_node(width=0.0, height=offset, name=offset_name, parent_name=parent_name, position=position, anchor=anchor)
        if is_vertical(position) or 'west-group-field' in name or 'east-group-field' in name:
            space_node = gen_plain_node(width=offset, height=0.0, name=offset_name, parent_name=parent_name, position=position, anchor=anchor)

        parent_name = offset_name

    # container node
    bg_color=''
    if background_color is not None:
        bg_color='fill='+gen_tikZ_rgb255(background_color)+', '
    container_node = gen_plain_node(width, height, name=name, parent_name=parent_name, position=position, anchor=anchor, additional_params=bg_color)

    # text/content node
    content_node = ''
    if content != '':
        content_node = gen_text_node(width, height, content, parent_name=name, position='center', anchor='center', fontsize=fontsize, alignment=alignment, 
                                           rotation=rotate_text, text_color=text_color)

    return space_node + container_node + content_node
### END helper node functions ###


### BEGIN space/padding nodes ###
def add_outer_horizontal_padding(margin, num_columns, position, has_title, has_row_field, str_appendix=''):
    '''
    Adds a padding between title (or other outer content) and the edge of the figure if so desired.
    '''
    if str_appendix != '':
        str_appendix = '-' + str_appendix

    if position=='east':
        parent_name = position+'-field'+str_appendix+'-1-'+str(num_columns)
    else: # west
        parent_name = position+'-field'+str_appendix+'-1-1'

    if has_title:
        parent_name = position+'-group-field'+str_appendix+''
    elif has_row_field:
        parent_name = position+'-row-field'+str_appendix+'-1'
    
    return gen_space_helper(margin, parent_name, position)

def add_outer_vertical_padding(margin, position, num_rows, has_title, has_column_field, str_appendix=''):
    '''
    Adds a padding between title (or other outer content) and the edge of the figure if so desired.
    '''
    if str_appendix != '':
        str_appendix = '-' + str_appendix
    
    if position=='south':
        parent_name = position+'-field'+str_appendix+'-'+str(num_rows)+'-1'
    else: # north
        parent_name = position+'-field'+str_appendix+'-1-1'
    
    if has_title:
        parent_name = position+'-group-field'+str_appendix+''
    elif has_column_field:
        parent_name = position+'-column-field'+str_appendix+'-1'

    return gen_space_helper(margin, parent_name, position)

def gen_space_helper(margin, parent_name, position):
    '''
    Only manages the outer padding ('top', 'bottom', 'left', 'right')
    '''
    if margin==0.0:
        return ''
    name = position+'-space'

    if is_vertical(position):
        width, height = margin, 0.0
    else: 
        width, height = 0.0, margin
    
    return gen_node_helper(position, opposite(position), width, height, name, parent_name, offset=0.0, offset_name=None, content='', fontsize='')

def add_all_outer_paddings(data, str_appendix=''):
    padding_nodes = add_outer_horizontal_padding(margin=data['padding']['left'], position='west', num_columns=data['num_columns'], 
                                    has_title=(data['titles']['west']['width']!=0.0), has_row_field=(data['row_titles']['west']['width']!=0.0), str_appendix=str_appendix)
    padding_nodes += add_outer_horizontal_padding(margin=data['padding']['right'], position='east', num_columns=data['num_columns'], 
                                    has_title=(data['titles']['east']['width']!=0.0), has_row_field=(data['row_titles']['east']['width']!=0.0), str_appendix=str_appendix)
    padding_nodes += add_outer_vertical_padding(margin=data['padding']['top'], position='north', num_rows=data['num_rows'], 
                                    has_title=(data['titles']['north']['height']!=0.0), has_column_field=(data['column_titles']['north']['height']!=0.0), str_appendix=str_appendix)
    padding_nodes += add_outer_vertical_padding(margin=data['padding']['bottom'], position='south', num_rows=data['num_rows'], 
                                    has_title=(data['titles']['south']['height']!=0.0), has_column_field=(data['column_titles']['south']['height']!=0.0), str_appendix=str_appendix)
    return padding_nodes
### END space/padding nodes ###


### BEGIN generating titles (figure title + row/column titles) ###
def gen_horizontal_figure_title(position, num_rows, width, title_config, column_config, str_appendix='', txt_alignment='centering'):
    if str_appendix != '':
        str_appendix = '-' + str_appendix
    
    if title_config['height']==0.0:
        return ''

    if position=='south':
        parent_name = position+'-field'+ str_appendix +'-'+str(num_rows)+'-1'
        name='south-group-field'+ str_appendix +''
    else: #north
        parent_name = position+'-field'+ str_appendix +'-1-1'
        name='north-group-field'+ str_appendix +''
    
    if column_config['height']!=0.0:
        parent_name = position+'-column-field'+ str_appendix +'-1'

    anchor = opposite(position)+' west'
    position = position+' west'

    return gen_node_helper(position, anchor, width, title_config['height'], name=name, parent_name=parent_name, offset=title_config['offset'], offset_name=None, 
                           content=title_config['content'], fontsize=gen_LaTeX_fontsize(title_config['fontsize'],title_config['line_space']), alignment=txt_alignment, 
                           rotate_text=title_config['rotation'], background_color=title_config['background_color'], text_color=title_config['text_color'])

def gen_vertical_figure_title(position, num_columns, height, title_config, title_offset, column_north_config, str_appendix='', txt_alignment='centering'):
    if str_appendix != '':
        str_appendix = '-' + str_appendix
    
    if title_config['width']==0.0:
        return ''

    if position=='east':
        supplement = str(num_columns)
        name='east-group-field'+ str_appendix +''
    else: #west
        supplement = '1'
        name='west-group-field'+ str_appendix +''
    parent_name = 'north-field'+ str_appendix +'-1-' + supplement

    if column_north_config['height']!=0.0:
        parent_name = 'north-column-field'+ str_appendix +'-' + supplement

    anchor = 'north '+opposite(position)
    position = 'north '+position

    return gen_node_helper(position, anchor, title_config['width'], height, name=name, parent_name=parent_name, offset=title_offset, offset_name=None, 
                           content=title_config['content'], fontsize=gen_LaTeX_fontsize(title_config['fontsize'],title_config['line_space']), alignment=txt_alignment, 
                           rotate_text=title_config['rotation'], background_color=title_config['background_color'], text_color=title_config['text_color'])

def gen_outer_row(position, row, data, str_appendix=''):
    '''
    Generates titles for each row: can be placed on the left and/or right side of the image blocks
    '''
    if str_appendix != '':
        str_appendix = '-' + str_appendix

    row_title = data['row_titles'][position]
    if row_title['width']==0.0:
        return ''
        
    name=position+'-row-field'+ str_appendix +'-'+str(row)
    parent_name='west-field'+ str_appendix +'-'+str(row)+'-1'
    if position=='east':
        parent_name='east-field'+ str_appendix +'-'+str(row)+'-'+str(data['num_columns'])
    
    bg_color_list = read_optional(row_title, 'background_colors', default=None)
    if bg_color_list is not None:
        bg_color = load_nth_color(bg_color_list, data['num_rows'], row-1)
    else:
        bg_color = None

    return gen_node_helper(position, opposite(position), row_title['width'], data['element_config']['img_height'], name=name, parent_name=parent_name, offset=row_title['offset'], offset_name=None, 
                           content=row_title['content'][row-1], fontsize=gen_LaTeX_fontsize(row_title['fontsize'],row_title['line_space']), alignment='centering', 
                           rotate_text=row_title['rotation'], background_color=bg_color, text_color=row_title['text_color'])

def gen_outer_col(position, column, data, str_appendix=''):
    '''
    Generates titles for each column: can be placed on top and/or at the bottom of the image blocks
    '''
    if str_appendix != '':
        str_appendix = '-' + str_appendix
    col_title = data['column_titles'][position]

    if col_title['height']==0.0:
        return ''
    
    name=position+'-column-field'+ str_appendix +'-'+str(column)
    parent_name='north-field'+ str_appendix +'-1-'+str(column)
    if position=='south':
        parent_name='south-field'+ str_appendix +'-'+str(data['num_rows'])+'-'+str(column)

    bg_color_list = read_optional(col_title, 'background_colors', default=None)
    if bg_color_list is not None:
        bg_color = load_nth_color(bg_color_list, data['num_columns'], column-1)
    else:
        bg_color = None
    
    return gen_node_helper(position, opposite(position), data['element_config']['img_width'], col_title['height'], name=name, parent_name=parent_name, offset=col_title['offset'], offset_name=None, 
                           content=col_title['content'][column-1], fontsize=gen_LaTeX_fontsize(col_title['fontsize'],col_title['line_space']), alignment='centering', 
                           rotate_text=col_title['rotation'], background_color=bg_color, text_color=col_title['text_color'])

def add_col_and_row_titles(data, str_appendix=''):
    c_r_title_nodes = ''

    for column in range(data['num_columns']):
        c_r_title_nodes += gen_outer_col('south', column+1, data, str_appendix=str_appendix)
        c_r_title_nodes += gen_outer_col('north', column+1, data, str_appendix=str_appendix)

    for row in range(data['num_rows']):
        c_r_title_nodes += gen_outer_row('west', row+1, data, str_appendix=str_appendix)
        c_r_title_nodes += gen_outer_row('east', row+1, data, str_appendix=str_appendix)
    
    return c_r_title_nodes

def add_big_titles(data, str_appendix=''):
    body_width = calculate_body_width(data)
    body_height = calculate_body_height(data)

    # horizontal
    title_nodes = gen_horizontal_figure_title('north', num_rows=data['num_rows'], width=body_width, title_config=data['titles']['north'], 
                                                    column_config=data['column_titles']['north'], str_appendix=str_appendix)
    title_nodes += gen_horizontal_figure_title('south', num_rows=data['num_rows'], width=body_width, title_config=data['titles']['south'], 
                                                    column_config=data['column_titles']['south'], str_appendix=str_appendix)

    # vertical
    offset_west_title = calculate_h_offset_for_title(title_offset=data['titles']['west']['offset'], caption_config=data['element_config']['captions']['west'], 
                                                     row_config=data['row_titles']['west'])
    title_nodes += gen_vertical_figure_title('west', num_columns=data['num_columns'], height=body_height, title_config=data['titles']['west'], 
                                                  title_offset=offset_west_title, column_north_config=data['column_titles']['north'], str_appendix=str_appendix)
    offset_east_title = calculate_h_offset_for_title(title_offset=data['titles']['east']['offset'], caption_config=data['element_config']['captions']['east'], 
                                                     row_config=data['row_titles']['east'])
    title_nodes += gen_vertical_figure_title('east', num_columns=data['num_columns'], height=body_height, title_config=data['titles']['east'],
                                                  title_offset=offset_east_title, column_north_config=data['column_titles']['north'], str_appendix=str_appendix)
    return title_nodes
### END generating titles (figure title + row/column titles) ###


### BEGIN generating img/element blocks ###
def gen_all_image_blocks(data, str_appendix=''):
    '''
    Generates tikz nodes for each element/image based on the number of columns and rows
    '''
    content = ''
    rowIndex = 1
    for row in data['elements_content']:
        colIndex = 1
        if rowIndex<=data['num_rows']:
            for elem in row:
                if colIndex<=data['num_columns']:
                    content += gen_one_img_block(element_config=data['element_config'], element_content=elem, row=rowIndex, column=colIndex, 
                                                row_spacing=data['row_space'], column_spacing=data['column_space'], str_appendix=str_appendix)
                    colIndex += 1
            rowIndex += 1
    return content

def draw_rectangle_on_img(img_name, inset_num, img_width, img_height, rel_pos_x1, rel_pos_y1, rel_pos_x2, rel_pos_y2, line_width, color=[255,255,255], dashed=False):
    offset_node = gen_plain_node(width=img_width * rel_pos_x1,height=img_height *rel_pos_y1, name='inset'+str(inset_num)+'-offset-'+img_name, parent_name=img_name, 
    position= "north west", anchor="north west", additional_params='')

    draw_params = 'draw='+str(gen_tikZ_rgb255(color))+', line width='+str(line_width)+'mm, '
    if dashed:
        draw_params = draw_params + 'dashed, '

    inset_node = gen_plain_node(width=img_width * (rel_pos_x2 - rel_pos_x1),height=img_height *(rel_pos_y2-rel_pos_y1), name='inset'+str(inset_num)+'-'+img_name, 
    parent_name='inset'+str(inset_num)+'-offset-'+img_name, position= "south east", anchor="north west", additional_params=draw_params)
    return offset_node + inset_node

def gen_inset_nodes(inset_configs, parent_name, parent_widht, parent_height):
    inset_nodes = ''
    if inset_configs['line_width'] > 0.0 and inset_configs['list']!=[]: # only draw if line width reasonable and list not empty
        inset_list = inset_configs['list']
        inset_num = 0
        for inset in inset_list:
            inset_num += 1
            inset_pos = inset['pos']
            inset_nodes += draw_rectangle_on_img(img_name=parent_name, inset_num=inset_num, img_width=parent_widht, img_height=parent_height, rel_pos_x1=inset_pos[0], 
            rel_pos_y1=inset_pos[1], rel_pos_x2=inset_pos[2], rel_pos_y2=inset_pos[3], line_width=inset_configs['line_width'], color=inset['color'], dashed=inset_configs['dashed'])

    return inset_nodes

def gen_one_img_block(element_config, element_content, row, column, row_spacing, column_spacing, str_appendix, txt_align='centering'):
    '''
    A image block can contain up to 5 'content' nodes: the image node itself with the image and 4 nodes, which are in 
    each direction around the image node (north, east, south, west). You can leave the 'direction' nodes empty, if you want to.
    Per default, the width of north/south nodes will be the (img) width. The same applies for the height of east/west nodes.
    You can add a frame to the image. An example would look like this: frame_specs='draw=blue, line width=0.25mm, '. Be aware that you
    should have the line width at a maximum of corresponding spacing to other 'content' nodes, else the frame might overlap with your other 
    content directly around the img.
    '''
    img_width, img_height = element_config['img_width'], element_config['img_height']
    frame_specs = read_optional(element_content, 'frame', default='')
    if frame_specs != '':
        frame_specs = gen_frame_specs(element_content)
    
    north_config = element_config['captions']['north']
    south_config = element_config['captions']['south']
    east_config = element_config['captions']['east']
    west_config = element_config['captions']['west']

    tikz_content = ''
    if str_appendix == '':
        append = str(row)+'-'+str(column)
    else:
        append = str_appendix + '-' + str(row)+'-'+str(column)

    if column == 1: # creating the img block from top

        if row == 1: #create starting node
            tikz_content += gen_plain_node(img_width, north_config['height'], name='north-field-'+append)
            if element_content['north']!='':
                tikz_content += gen_text_node(img_width, north_config['height'], element_content['north'], parent_name='north-field-'+append, position='center', 
                                                  anchor='center', fontsize=gen_LaTeX_fontsize(north_config['fontsize'], north_config['line_space']), 
                                                  alignment=txt_align, rotation=north_config['rotation'], text_color=north_config['text_color'])
        else: #coming from top, meaning, we create a new row with corresponding spacing
            tikz_content += gen_node_south(img_width, north_config['height'], name='north-field-'+append, parent_name='south-field-'+str(row-1)+'-'+str(column), 
                                        offset=row_spacing, offset_name='row-space-'+str(row-1)+'-'+str(row), content=element_content['north'], 
                                        fontsize=gen_LaTeX_fontsize(north_config['fontsize'], north_config['line_space']), 
                                        alignment=txt_align, rotate_text=north_config['rotation'], background_color=None, text_color=north_config['text_color'])

        parent_name='north-field-'+append
        if north_config['offset']!=0.0:
            tikz_content += gen_plain_node(img_width, height=north_config['offset'], name='north-space-'+append, parent_name=parent_name, position='south', 
                                                anchor='north')
            parent_name='north-space-'+append

        tikz_content += gen_img_node(img_width, img_height, name='img-'+append, parent_name=parent_name, position='south', anchor='north', 
                                    img_path=element_content['filename'], additional_params=frame_specs)
        tikz_content += gen_node_west(west_config['width'], img_height, name='west-field-'+append, parent_name='img-'+append, offset=west_config['offset'], offset_name=None, 
                                  content=element_content['west'], fontsize=gen_LaTeX_fontsize(west_config['fontsize'], west_config['line_space']), 
                                  alignment=txt_align, rotate_text=west_config['rotation'], background_color=None, text_color=west_config['text_color'])
    
    else: # creating img block from left 
        tikz_content += gen_node_east(west_config['width'], img_height, name='west-field-'+append, parent_name='east-field-'+str(row)+'-'+str(column-1), offset=column_spacing, 
                                  offset_name='column-space-'+str(row)+'-'+str(column-1)+'-'+str(column), content=element_content['west'], 
                                  fontsize=gen_LaTeX_fontsize(west_config['fontsize'], west_config['line_space']), 
                                  alignment=txt_align, rotate_text=west_config['rotation'], background_color=None, text_color=west_config['text_color'])

        parent_name='west-field-'+append
        if west_config['offset']!=0.0: 
            tikz_content += gen_plain_node(width=west_config['offset'], height=img_height, name='west-space-'+append, parent_name=parent_name, position='east', 
                                              anchor='west')
            parent_name='west-space-'+append

        tikz_content += gen_img_node(img_width, img_height, name='img-'+append, parent_name=parent_name, position='east', anchor='west', 
                                     img_path=element_content['filename'], additional_params=frame_specs)
        tikz_content += gen_node_north(img_width, height=north_config['height'], name='north-field-'+append, parent_name='img-'+append, offset=north_config['offset'], 
                                       offset_name=None, content=element_content['north'], fontsize=gen_LaTeX_fontsize(north_config['fontsize'], north_config['line_space']), 
                                       alignment=txt_align, rotate_text=north_config['rotation'], background_color=None, text_color=north_config['text_color'])
    
    #creating east and south nodes are independent of where the parent node was connected
    tikz_content += gen_node_east(east_config['width'], img_height, name='east-field-'+append, parent_name='img-'+append, offset=east_config['offset'], offset_name=None, 
                              content=element_content['east'], fontsize=gen_LaTeX_fontsize(east_config['fontsize'],east_config['line_space']), alignment=txt_align, 
                              rotate_text=east_config['rotation'], background_color=None, text_color=east_config['text_color'])

    tikz_content += gen_node_south(img_width, height=south_config['height'], name='south-field-'+append, parent_name='img-'+append, offset=south_config['offset'], 
                                offset_name=None, content=element_content['south'], fontsize=gen_LaTeX_fontsize(south_config['fontsize'],south_config['line_space']), 
                                alignment=txt_align, rotate_text=south_config['rotation'], background_color=None, text_color=south_config['text_color'])

    
    #if inset is on img
    tikz_content += gen_inset_nodes(element_content['insets'], parent_name='img-'+append, parent_widht=img_width, parent_height=img_height)
    
    return tikz_content + '\n'
### END generating img/element blocks ###
# END TIKZ GEN