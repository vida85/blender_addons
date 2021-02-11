import bpy
import bmesh
import random

from .Rooftop_structures import rooftop_structures
from ..tools.blender_tools import (makegrid, makecube, mode,
                                   modify, modify_args, apply_modifier,
                                   apply_obj, remove_duplicates, a_mat,
                                   rotate, transform, set_origin_to_3D_cursor,
                                   de_select, makeplane, move_it, dup,
                                   update, inset, extrude, extrude_normals,
                                   custom_bevel, smooth, dimension, join_objs,
                                   bm, selection, select_me, re_size, dissolve_e,
                                   subdivide, location)

texture = ['Building', 'Pillar', 'Column', 'Windows', 'Roof', 'Metal']

building_x = 0
building_z = 0

def roof(building_x, building_z):
    makeplane(building_x)
    a_mat('Roof')
    transform('z', building_z, 'location')

    mode('edit')
    extrude(z=2, t='face')
    inset(.3)
    extrude(z=-1, t='face')
    mode('object')

    obj = bpy.context.object
    bpy.ops.object.modifier_add(type='BEVEL')
    obj.modifiers["Bevel"].segments = 4
    bpy.ops.object.modifier_apply(modifier="Bevel")
    obj.name = 'business_roof'

def first_floor(size, ext=1):
    ##--------------------------------------------
    ##--First Floor Structure
    makeplane(size)

    mode('EDIT')
    selection('FACE') # FACE SELECT
    extrude(0, 0, .1)
    inset(.1) # INSET FACE SELECTED
    extrude(0,0,ext)

    inset(0.1, .001) # INSET FACE SELECTED
    extrude(0, 0, ext*3)
    de_select(False, 'EDIT')
    
    ##New MATERIAL  
    de_select(True, 'EDIT')
    a_mat(texture[0])
    de_select(False, 'EDIT')

    ##### Select Faces #####
    s = bm().faces
    s.ensure_lookup_table()
    for i in range(1,10):
        s[i].select = True
    update()
    for i in range(11,18):
        s[i].select = True
    update()
    a_mat(texture[1])
    de_select(False, 'EDIT')

    for i in [10,19,20,21]:
        s[i].select = True
    update()

    ##SUBDIVIDE
    mode('EDIT')
    subdivide(6)
    de_select(False, 'EDIT')
    
    ##### Select Faces #####
    f_select = [35, 36, 37, 38, 39, 47, 48, 49, 50, 51, 59, 60, 61, 62, 63, 83, 84, 85, 86, 87, 95, 96, 97, 98, 99,
                107, 108, 109, 110, 111, 131, 132, 133, 134, 135, 143, 144, 145, 146, 147, 155, 156, 157, 158, 159,
                227, 228, 229, 230, 231, 239, 240, 241, 242, 243, 251, 252, 253, 254, 255]

    s = bm().faces
    s.ensure_lookup_table()
    for i in f_select:
        s[i].select = True
    update()
    
    ##EXTRUDE NORMALS 
    extrude_normals(random.choice([-.1, -.2, -.3])) # making Windows

def complex_window(c_coll, n_coll):

    bpy.ops.mesh.separate(type='SELECTED')
    bpy.ops.object.editmode_toggle()

    de_select(False, 'Object')
    obj = list(c_coll.objects)[-1]
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    bpy.ops.object.editmode_toggle()
    
    modify('Wireframe')
    modify_args('Wireframe').use_boundary = True
    modify_args('Wireframe').offset       = .48
    modify_args('Wireframe').thickness    = .05
    modify_args('Wireframe').use_replace  = False
    apply_modifier('Wireframe')

    ## --- Flattens Frames
    modify('BEVEL')
    apply_modifier('Bevel')
    remove_duplicates()

    de_select(False, 'EDIT')
    face_index = list(range(0, 59)) + [1547]
    s = bm().faces
    s.ensure_lookup_table()
    for i in face_index:
        s[i].select = True
    update()
    a_mat(texture[3])

    de_select(False, 'EDIT')
    
    bpy.ops.mesh.select_linked_pick(deselect=False, delimit={'SEAM'}, index=5985)
    bpy.ops.mesh.select_similar(type='AREA', threshold=0.01)
    a_mat(texture[5])

    mode('Object')
    de_select(True, 'Object')
    bpy.ops.object.join()

def raise_floors(floor, n_coll):
    ##MODIFIER BEVEL
    modify('BEVEL')
    modify_args('Bevel').width = 0.02
    modify_args('Bevel').segments = 4
    apply_modifier('Bevel')

    modify('ARRAY')
    modify_args('Array').relative_offset_displace[0] = 0
    modify_args('Array').relative_offset_displace[2] = 1
    modify_args('Array').count = floor
    apply_modifier("Array")
    
    building_z = dimension('z')
    building_x = dimension('x')

    ##--------------------------------------------
    ##--Add Roof
    roof(building_x, building_z)
    # business_towers(n_coll)

    return building_z

def business_towers(new_coll):
    #### --------------------------------------------
    #### -- Create second tower on skyscrappers -----
    de_select(False, 'Object')
    ob = bpy.data.collections[new_coll.name_full].objects[-1]
    if ob.name_full.startswith('Business') and ob.dimensions.x < 20 and ob.dimensions.y < 20:
        ob.select_set(True)
        bpy.context.view_layer.objects.active = ob # make selected obj ACTIVE
        
        x, y, z = ob.location.x, ob.location.y, ob.dimensions.z*2
        dimensions_x, dimensions_y, dimensions_z = ob.dimensions.x/1.5, ob.dimensions.y/1.5, ob.dimensions.z/2

        dup()
        bpy.context.object.name = 'Business_Tower'
        ob.select_set(True)

        bpy.context.object.location   = (x, y, random.choice([z/2.5, z/3.4, z/3.3, z/3.2]))
        bpy.context.object.dimensions = (dimensions_x, dimensions_y, dimensions_z)
        
        bpy.ops.object.join()
        set_origin_to_3D_cursor()
        bpy.context.object.select_set(False)

def business(floors, c_coll, n_coll):
    global building_x
    global building_z
    size = random.choice([16, 18, 20, 22, 24])
    floor = random.choice(list(range(2, int(floors/2))))

    ##--------------------------------------------
    ##--First Floors
    first_floor(size)

    ##--------------------------------------------
    ##--Add Windows
    complex_window(c_coll, n_coll)
    
    ##--------------------------------------------
    ##--Add Floors
    mode('Object')
    raise_floors(floor, n_coll)

    ##--------------------------------------------
    ##--Join all objs
    de_select(True, 'OBJECT')
    bpy.ops.object.join()
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    
    first_obj = bpy.context.object
    rooftop_structures(first_obj, building_x, bpy.context.object.dimensions.z)

    de_select(True, 'OBJECT')
    bpy.ops.object.join()
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    ##--------------------------------------------

    ##--Name obj
    mode('Object')
    obj = bpy.context.object
    obj.name = f'Business'

    
