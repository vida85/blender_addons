import bpy
import bmesh
import random

from ..tools.blender_tools import (makegrid, makecube, mode,
                                   modify, modify_args, apply_modifier,
                                   apply_obj, remove_duplicates, a_mat,
                                   rotate, transform, set_origin_to_3D_cursor,
                                   de_select, makeplane, move_it, dup,
                                   update, inset, extrude, extrude_normals,
                                   custom_bevel, smooth, dimension, join_objs,
                                   bm, selection, select_me, re_size)

####-----------------------------------------------
####-- Start
building_z   = 0

column_sizes = random.choice([.25]) 
row_sizes    = random.choice([.25])

offset       = 1
p_thickness  = .25

def roof(floor, p_thickness):
    makeplane(dimension('x'))
    a_mat('Roof')
    transform('x', dimension('x')/2, 'location')
    transform('y', dimension('y')/2 + p_thickness, 'location')
    transform('z', building_z, 'location')

    mode('edit')
    extrude(z=2, t='face')
    inset(.3)
    extrude(z=-1, t='face')
    mode('object')

    bpy.ops.object.modifier_add(type='BEVEL')
    bpy.context.object.modifiers["Bevel"].segments = 4
    bpy.ops.object.modifier_apply(modifier="Bevel")

    re_size((1 + p_thickness/10, 1 + p_thickness/10, 1))

def ground_floor(ground_size, floor):
    makeplane(ground_size)
    a_mat('Building')
    transform('x', dimension('x')/2, 'location')
    transform('y', dimension('y')/2, 'location')
    set_origin_to_3D_cursor()
    transform('y', p_thickness*2, 'location')
    transform('x', 1, 'scale')

    modify('Solidify')
    apply_modifier('Solidify')

    modify('Array')
    modify_args('Array').relative_offset_displace[0] = 0
    modify_args('Array').relative_offset_displace[2] = 300
    modify_args('Array').count = floor - 1
    apply_modifier('Array')

    roof(floor, p_thickness * 2)

def apartment(floors, c_coll, n_coll):
    floor = random.choice(list(range(2, floors)))
    global building_z
    for i in range(2):
        ### ---------------------
        ### making Pillars ------
        ### ---------------------
        makecube(2)
        a_mat('Building')

        if i == 0 or i == 2:
            ### ---- Rows are Horizontal
            ### ---- FIRST ROW
            transform('x', row_sizes, 'scale')
            transform('z', row_sizes, 'scale')
            transform('y', 1.5, 'scale')
            set_origin_to_3D_cursor()

            apply_obj(True, True, True)
            rotate('z', -90)
            apply_obj(True, True, True)
        
            transform('x', dimension('x')/2, 'location')
            transform('y', dimension('y')/2+random.choice([0, .2, .3, .4, p_thickness]), 'location')
            transform('z', dimension('y')/2, 'location')
            set_origin_to_3D_cursor()

            if floor in [16, 18, 20, 30]:
                modify('BEVEL')
                modify_args("Bevel").segments = 12
                modify_args("Bevel").profile  = .85
                apply_modifier("Bevel")
                bpy.ops.object.shade_smooth()
                bpy.context.object.data.use_auto_smooth = True

            ### ---- SECOND ROW
            dup()
            transform('x', (dimension('x')+p_thickness*2), 'location')
        else:
            #### ---- Columns are Vertical
            transform('x', column_sizes, 'scale')
            transform('y', column_sizes*offset, 'scale')
            transform('z', 1, 'location')
            set_origin_to_3D_cursor()
            transform('x', dimension('x')/2, 'location')
            transform('y', dimension('y')/2+random.choice([0, .2, .3, .4, p_thickness]), 'location')
            set_origin_to_3D_cursor()

            transform('z', 1.5, 'scale')
            transform('x', 3, 'location')

            if floor in [16, 18, 20, 30]:
                modify('BEVEL')
                modify_args("Bevel").segments = 12
                modify_args("Bevel").profile  = .85
                apply_modifier("Bevel")
                bpy.ops.object.shade_smooth()
                bpy.context.object.data.use_auto_smooth = True

        makeplane(3)
        a_mat('Windows')
        transform('x', dimension('x')/2, 'location')
        transform('y', dimension('y')/2, 'location')
        set_origin_to_3D_cursor()
        rotate('x', -90)
        transform('y', p_thickness*2, 'location')
        if i == 1:
            transform('x', dimension('x')+p_thickness*2, 'location')

    de_select(True, 'object')
    join_objs()

    if floor in [10, 12, 14]:
        modify('BEVEL')
        modify_args("Bevel").segments = 12
        modify_args("Bevel").profile  = .85
        apply_modifier("Bevel")
        bpy.ops.object.shade_smooth()
        bpy.context.object.data.use_auto_smooth = True

    modify('Array')
    modify_args('Array').relative_offset_displace[0] = 1
    modify_args('Array').count = 6
    apply_modifier('Array')

    modify('Array')
    modify_args('Array').relative_offset_displace[0] = 0
    modify_args('Array').relative_offset_displace[1] = 1
    modify_args('Array').count = floor
    apply_modifier('Array')

    set_origin_to_3D_cursor()

    ground_size = dimension('x')
    for count in range(3):
        if count == 0:
            dup()
            rotate('z', -90)
            transform('x', dimension('x')+p_thickness*2, 'location')
            transform('y', p_thickness*2, 'location')

        if count == 1:
            dup()
            apply_obj(True, True, True)
            rotate('z', 180)
            transform('x', dimension('y'), 'location')
            transform('y', dimension('y')+p_thickness*4, 'location')
            set_origin_to_3D_cursor()
        if count == 2:
            dup()
            rotate('z', 90)
            transform('y', dimension('y')+p_thickness*2, 'location')
            transform('x', -p_thickness*2, 'location')

    building_z = dimension('z')
    ground_floor(ground_size, floor)
    
    de_select(True, 'object')
    join_objs()
    set_origin_to_3D_cursor()

    re_size((random.choice([.4, .5, .6]), random.choice([.3, .4, .5]), bpy.context.object.scale.z/2))
    bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')
    transform('z', dimension('z')/2, 'location')
    set_origin_to_3D_cursor()

    smooth(True) # shade smooth
    bpy.context.object.name = 'Apartment'
