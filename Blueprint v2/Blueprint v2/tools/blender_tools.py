import bpy
import bmesh

#----------------------------------------------------------------#
# FUNCTIONS --- BUILDING TOOLS
#----------------------------------------------------------------#
def location(obj):
    return list(obj.location)
def face_add():
    return bpy.ops.mesh.edge_face_add()

def remove_duplicates():
    try:
        mode('EDIT')
        de_select(True, 'EDIT')
        return bpy.ops.mesh.remove_doubles()
    except:
        de_select(True, 'EDIT')
        return bpy.ops.mesh.remove_doubles()

def custom_bevel(seg, affected):
    """[Custom Bevels]
    Args:
        seg (INT): [segments...]
        affected (STR): ['EDGES', 'FACES', 'VERTS']
    """
    return bpy.ops.mesh.bevel(offset_type='WIDTH', offset=0.0199165, offset_pct=0, segments=seg, 
                              profile=0.522857, affect=affected, material=-1)

def join_objs():
    try:
        return bpy.ops.object.join()
    except RuntimeError:
        return bpy.ops.edit_object.join()
        
def smooth(auto_smooth=False):
    """shade smooth obj and option for auto_smooth

    Args:
        auto_smooth (bool, optional): [option for auto_smooth]. Defaults to False.

    """
    if auto_smooth:
        bpy.context.object.data.use_auto_smooth = True
        return bpy.ops.object.shade_smooth()
    else:
        return bpy.ops.object.shade_smooth()

def set_origin_to_3D_cursor():
    return bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

def apply_obj(LOCATION=False, ROTATION=False, SCALE=False):
    """Apply rotation, scale, location

    Args:
        loc (bool, optional): True [Apply location]. Defaults to False.
        rot (bool, optional): True [Apply rotation]. Defaults to False.
        scale (bool, optional): True [Apply scale]. Defaults to False.

    """
    return bpy.ops.object.transform_apply(location=LOCATION, rotation=ROTATION, scale=SCALE)

def makegrid(x=1, y=1, z=1):
    return bpy.ops.mesh.primitive_grid_add(x_subdivisions=3, y_subdivisions=3, size=2,
                                           enter_editmode=False, align='WORLD',
                                           location=(0, 0, 0), scale=(x,y,z))

def a_mat(name):
    mat = bpy.data.materials.get(name)

    if mat is None:
        mat = bpy.data.materials.new(name)
        bpy.context.object.data.materials.append(mat)
    else:
        bpy.context.object.data.materials.append(mat)
    assign_mat(mat, name)

def assign_mat(mat, name):
    if len(bpy.context.object.material_slots) == 0:
        index = len(bpy.context.object.material_slots)
    else:
        index = len(bpy.context.object.material_slots) - 1
    
    bpy.context.object.active_material_index = index
    bpy.ops.object.material_slot_assign()

def re_size(value):
    """[resize obj]

    Args:
        value ([INT]): [example (x, y, z) == 1, 1, 1]

    Returns:
        [type]: [description]
    """
    return bpy.ops.transform.resize(value=(value), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

def move_it(x, y, z):
    """Moves OBJ to new location

    Args:
        x ([INT]): [Moves along X]
        y ([INT]): [Moves along Y]
        z ([INT]): [Moves along Z]

    """
    return bpy.ops.transform.translate(value=(x, y, z), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

def dimension(val=''):
    """Returns the dimensions of an obj

    Args:
        val ([STR]): [pick ONE 'x', 'y', or 'z']

    """
    if val == 'z':
        return bpy.context.object.dimensions.z
    elif val == 'y':
        return bpy.context.object.dimensions.y
    elif val == 'x':
        return bpy.context.object.dimensions.x
    else:
        return bpy.context.object.dimensions

def modify_args(name):
    """change parameters of a Modifier

    Args:
        name (STR): 'Wireframe', 'Array', 'Bevel', etc
    
    Return:
        instance of modifier
    """
    name = name.title()
    try:
        return bpy.context.object.modifiers[name]
    except KeyError:
        return "Please set name to a valid Modifier: 'Wireframe', 'Array', 'Bevel', etc"

def modify(mod):
    """[add modifier]

    Args:
        mod (STR): Options -- [WIREFRAME, ARRAY, BEVEL, etc]

    """
    mod = mod.upper()
    return bpy.ops.object.modifier_add(type=mod)

def de_select(bool, mode):
    """Select All or DeSelect All

    Args:
        bool (BOOL): [True == SELECT ALL, False == DESELECT ALL]
        mode (STR):  ['OBJECT' for obj mode, 'EDIT' for edit mode]

    """
    mode = mode.lower()
    if mode == 'object':
        if bool:
            return bpy.ops.object.select_all(action="SELECT")
        else:
            return bpy.ops.object.select_all(action='DESELECT')
    if mode == 'edit':        
        if bool:
            return bpy.ops.mesh.select_all(action="SELECT")
        else:
            return bpy.ops.mesh.select_all(action='DESELECT')
    return "nothing was selected, please pick 'mode'"

def mode(env):
    """[summary]
    Args:
        env ([STR]): ['object', 'edit', 'sculp']
    """
    env = env.upper()
    return bpy.ops.object.mode_set(mode=env)

def makeplane(s, x=0, y=0, z=0):
    return bpy.ops.mesh.primitive_plane_add(size=s, enter_editmode=False, align='WORLD', location=(x, y, z))

def makecube(s, loc=(0,0,0), x=1, y=1, z=1):
    """[Makes a Cube]

    Args:
        s ([INT]): [Size of Cube]
        loc (INT): (x, y, z) coordinates. Defaults to (0, 0, 0).
        x (int, optional): [Scale of X]. Defaults to 1.
        y (int, optional): [Scale of Y]. Defaults to 1.
        z (int, optional): [Scale of Z]. Defaults to 1.

    """
    return bpy.ops.mesh.primitive_cube_add(size=s, enter_editmode=False, align='WORLD', location=(loc), scale=(x, y, z))

def transform(axis, value, movement='location', delta=False,):
    """move obj in context x, y, z, for location,
       rotation, or scale

    Args:
        axis ([STR]): [x, y, z]
        value ([INT]): [amount to move obj]
        movement (str, optional): [movement to apply, 'location', 'rotation', 'scale']. Defaults to 'location'.
        delta (bool, optional): [True uses Detal Transform]. Defaults to False.

    Returns:
            obj instance
    """
    if movement == 'location':
        if delta:
            if axis == 'x':
                bpy.context.object.delta_location[0] = value
            if axis == 'y':
                bpy.context.object.delta_location[1] = value
            if axis == 'z':
                bpy.context.object.delta_location[2] = value
        else:
            if axis == 'x':
                bpy.context.object.location[0] = value
            if axis == 'y':
                bpy.context.object.location[1] = value
            if axis == 'z':
                bpy.context.object.location[2] = value
    elif movement == 'rotation':
        if delta:
            if axis == 'x':
                bpy.context.object.delta_rotation[0] = value
            if axis == 'y':
                bpy.context.object.delta_rotation[1] = value
            if axis == 'z':
                bpy.context.object.delta_rotation[2] = value
        else:
            if axis == 'x':
                bpy.context.object.rotation[0] = value
            if axis == 'y':
                bpy.context.object.rotation[1] = value
            if axis == 'z':
                bpy.context.object.rotation[2] = value
    elif movement == 'scale':
        if delta:
            if axis == 'x':
                bpy.context.object.delta_scale[0] = value
            if axis == 'y':
                bpy.context.object.delta_scale[1] = value
            if axis == 'z':
                bpy.context.object.delta_scale[2] = value
        else:
            if axis == 'x':
                bpy.context.object.scale[0] = value
            if axis == 'y':
                bpy.context.object.scale[1] = value
            if axis == 'z':
                bpy.context.object.scale[2] = value
        
def selection(kind):
    """[EDIT mode Selection type]

    Args:
        kind ([STR]): ['FACE', 'EDGE', 'VERT']

    Returns:
        [type]: [description]
    """
    kind = kind.upper()
    if kind == 'FACE':
        return bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
    elif kind == 'EDGE':
        return bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')
    elif kind == 'VERT':
        return bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')

def extrude(x=0, y=0, z=0, t='face'):
    """Extrudes along Axis
    Args:
        x (int, optional): [X direction]. Defaults to 0.
        y (int, optional): [Y direction]. Defaults to 0.
        z (int, optional): [Z direction]. Defaults to 0.
    
    """
    if t == 'face':
        return bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False},
                TRANSFORM_OT_translate={"value":(x, y, z), "orient_type":'NORMAL', "orient_matrix":((0, -1, 0), (1, 0, -0), (0, 0, 1)), "orient_matrix_type":'NORMAL',
                "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1,
                "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False,
                "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False,
                "use_accurate":False})
    if t == 'edge':
        return bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False},
                TRANSFORM_OT_translate={"value":(x, y, z), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL',
                "constraint_axis":(False, True, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1,
                "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False,
                "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False,
                "use_accurate":False, "use_automerge_and_split":False})

def extrude_normals(val):
    return bpy.ops.mesh.extrude_region_shrink_fatten(MESH_OT_extrude_region={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False},
                                                TRANSFORM_OT_shrink_fatten={"value":val, "use_even_offset":True, "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "release_confirm":True, "use_accurate":False})

def inset(thick, depths=0):
    """insets any given face selected

    Args:
        thick ([int]): [how much to inset]
        depths ([int]): [to inset and move in the z direction]

    """
    return bpy.ops.mesh.inset(thickness=thick, depth=depths)

def rotate(axis, val):
    """[rotate obj on axis]

    Args:
        axis ([STR]): ['X', 'Y', 'Z']
        val ([INT]): 90 or 180 or -90 or -180

    """
    if val == 180:
        return bpy.ops.transform.rotate(value=3.14159, orient_axis=axis.upper(), orient_type='VIEW', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='VIEW', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
    elif val == -180:
        return bpy.ops.transform.rotate(value=-3.14159, orient_axis=axis.upper(), orient_type='VIEW', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='VIEW', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
    elif val == 90:
        return bpy.ops.transform.rotate(value=1.5708, orient_axis=axis.upper(), orient_type='VIEW', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='VIEW', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
    elif val == -90:
        return bpy.ops.transform.rotate(value=-1.5708, orient_axis=axis.upper(), orient_type='VIEW', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='VIEW', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
    else:
        print('no rotation was picked... 180, 90')

def bm():
    obj = bpy.context.edit_object
    me  = obj.data
    return bmesh.from_edit_mesh(me)

def select_me(t, num):
    obj = bpy.context.edit_object
    me  = obj.data

    if t == 'face':
        s = bmesh.from_edit_mesh(me).faces
    if t == 'edge':
        s = bmesh.from_edit_mesh(me).edges
    if t == 'vert':
        s = bmesh.from_edit_mesh(me).verts

    s.ensure_lookup_table()
    
    s[num].select = True

    return update()

def update():
    return bmesh.update_edit_mesh(bpy.context.edit_object.data, True)

def subdivide(cuts, frac=0):
    """
    Args:
        cuts ([INT]): [number of subdivide]
        frac ([INT]): [surface distortion]
    """
    return bpy.ops.mesh.subdivide(number_cuts=cuts, fractal=frac)

def apply_modifier(val):
    """[applies the modifer to obj]

    Args:
        val ([STR]): ["Array", "Bevel", etc]

    """
    val = val.title()
    try:
        return bpy.ops.object.modifier_apply(modifier=val)
    except RuntimeError:
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.modifier_apply(modifier=val)
        return bpy.ops.object.editmode_toggle()

def hide(bool):
    """Hides Everything or UnHides everything.
    Only with Selected Iteams 

    Args:
        bool ([BOOL]): [True: Hides, False: UnHides]

    """
    obj = bpy.context.object
    try:
        if bool:
            return obj.hide_set(bool)
        else:
            return obj.hide_set(bool)
    except AttributeError:
        return "Nothing to hide"

def dup():
    try:
        return bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'},
                                             TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL',
                                             "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)),
                                             "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False),
                                             "mirror":False, "use_proportional_edit":False,
                                             "proportional_edit_falloff":'SMOOTH', "proportional_size":1,
                                             "use_proportional_connected":False, "use_proportional_projected":False,
                                             "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0),
                                             "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False,
                                             "cursor_transform":False, "texture_space":False, "remove_on_cancel":False,
                                             "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
    except RuntimeError:
        return bpy.ops.mesh.duplicate_move(MESH_OT_duplicate={"mode":1}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})

def dissolve_e():
    return bpy.ops.mesh.dissolve_edges()

