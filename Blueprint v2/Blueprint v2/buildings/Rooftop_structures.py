import bpy
import random

from ..tools.blender_tools import (makegrid, makecube, mode,
                                   modify, modify_args, apply_modifier,
                                   apply_obj, remove_duplicates, a_mat,
                                   rotate, transform, set_origin_to_3D_cursor,
                                   de_select, makeplane, move_it, dup,
                                   update, inset, extrude, extrude_normals,
                                   custom_bevel, smooth, dimension, join_objs,
                                   bm, selection, select_me, re_size, dissolve_e,
                                   subdivide, location)

texture = ['Building', 'Pillar', 'Column', 'Window', 'Roof', 'Metal']

def basic(x, z):
    makeplane(2)
    mode('edit')
    selection('FACE')
    extrude(z=0.05)
    inset(0.15)
    extrude(z=0.2)
    inset(0.1)
    extrude(z=0.3)
    extrude(z=0.1)
    extrude(z=0.3)
    extrude(z=0.2)
    inset(.025)
    extrude(z=-0.1)
    # modify('Bevel')
    # modify_args('Bevel').segments = 6

    de_select(False, 'Edit')
    s = bm().faces
    s.ensure_lookup_table()
    for i in [22,27,28,29]:
        s[i].select = True
    update()
    inset(.02, -.003)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.75, depth=.5, end_fill_type='TRIFAN', enter_editmode=False,
                                        align='WORLD', location=(0, 0, .9), scale=(1, 1, 1))
    
    rotate('Y', 180)
    de_select(False, 'Edit')
    s.ensure_lookup_table()
    s[75].select = True
    bpy.ops.mesh.select_similar(type='AREA', threshold=0.01)
    bpy.ops.mesh.select_nth()
    extrude(-.02)
    re_size((.9,.9,.9))

    mode('object')
    transform('z', z-1)

def placement(location, first_obj, x, z):
    for _ in range(3):
        basic(x, z)
        obj = bpy.context.object

        while True:
            obj_x = random.choice(list(range(int(first_obj.dimensions.x/2))))
            print(obj_x, ' and ', location)
            if obj_x in location:
                continue
            else:
                location.append(obj_x)
                obj.location[0] = obj_x
                break

        while True:
            obj_y = random.choice(list(range(int(first_obj.dimensions.y/2))))
            print(obj_y, ' and ', location)
            if obj_y in location:
                continue
            else:
                location.append(obj_y)
                obj.location[1] = obj_y
                break

def rooftop_structures(first_obj, x, z):
    location = []

    if first_obj.name_full.startswith('business_roof'):
        placement(location, first_obj, x, z)

    if first_obj.name_full.startswith('office_a_roof'):
        placement(location, first_obj, x, z)

    location = []




