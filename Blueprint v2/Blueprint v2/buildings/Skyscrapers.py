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

#######################################################################################
#### Make it from cube or copy other buildings formula and adapt skyscrapper style ####
#######################################################################################
def skyscraper(floors, c_coll, n_coll):
    # floor = random.choice([30, 40, 50, 60, 70, 80])
    floor = random.choice(list(range(30, floors)))
    size  = random.choice([30, 35, 40, 45, 50, 55])
    ### ------------------------------------------
    ### Creating SIDE of skyscrapper
    ### ------------------------------------------
    horizontal = random.choice([4,5,6,7,8])
    if size == 30 and floor > 50:
        size = 45
        makegrid(size)

    elif size == 35 and floor > 50:
        size = 50
        makegrid(size)
    elif size == 40 and floor > 50:
        size = 55
        makegrid(size)
    elif size == 45 and floor > 50:
        size = 60
        makegrid(size)
    else:
        if floor == 80:
            size = 60
        makegrid(size)

    ### ------------------------------------------
    ### Creating WINDOWS of skyscrapper
    ### ------------------------------------------
    mode('EDIT')

    ## --- Creates Window Frames
    modify('WIREFRAME')
    modify_args('Wireframe').use_boundary = True
    modify_args('Wireframe').offset       = .48
    modify_args('Wireframe').thickness    = .05
    apply_modifier('Wireframe')

    ## --- Flattens Frames
    modify('BEVEL')
    apply_modifier('Bevel')
    remove_duplicates()
    ### ------------------------------------------
    ### Assign Textures of skyscrapper
    ## --- Windows
    choice = random.choice([0, 1, 2, 3])
    if choice == 0:
        a_mat('Building') ## assign maerial
        mode('EDIT')
        ### ------------------------------------------

        makeplane(2.025)
        modify('ARRAY')
        modify_args('Array').count = horizontal
        apply_modifier('Array')
        ### ------------------------------------------
        ### Assign Textures of skyscrapper
        a_mat('Windows') ## assign maerial
    elif choice == 1:
        mode('EDIT')

        makeplane(1, x=.5, y=.5)
        makeplane(1, x=.5, y=-.5)
        ### Assign Textures of skyscrapper
        a_mat('Building') ## assign maerial

        makeplane(1, x=-.5, y=-.5)
        ### Assign Textures of skyscrapper
        a_mat('Windows') ## assign maerial

        makeplane(1, x=-.5, y=.5)
        ### Assign Textures of skyscrapper
        a_mat('Windows') ## assign maerial
        
        modify('ARRAY')
        modify_args('Array').count = horizontal
        apply_modifier('Array')
    elif choice == 2:
        mode('EDIT')

        makeplane(1, x=.5, y=.5)
        makeplane(1, x=-.5, y=.5)
        ### Assign Textures of skyscrapper
        a_mat('Building') ## assign maerial

        makeplane(1, x=.5, y=-.5)
        ### Assign Textures of skyscrapper
        a_mat('Windows') ## assign maerial

        makeplane(1, x=-.5, y=-.5)
        ### Assign Textures of skyscrapper
        a_mat('Windows') ## assign maerial
        
        modify('ARRAY')
        modify_args('Array').count = horizontal
        apply_modifier('Array')
    elif choice == 3:
        mode('EDIT')

        makeplane(1, x=.5, y=.5)
        makeplane(1, x=-.5, y=-.5)
        ### Assign Textures of skyscrapper
        a_mat('Building') ## assign maerial

        makeplane(1, x=.5, y=-.5)
        ### Assign Textures of skyscrapper
        a_mat('Windows') ## assign maerial

        makeplane(1, x=-.5, y=.5)
        ### Assign Textures of skyscrapper
        a_mat('Windows') ## assign maerial
        
        modify('ARRAY')
        modify_args('Array').count = horizontal
        apply_modifier('Array')

    ### --- Correct location and rotation of building walls/windows
    mode('OBJECT')
    rotate('X', -90) # rotate to horizontal alignment to ground
    apply_obj(ROTATION=True)

    transform('z', 1.0125, 'location') # move plane
    transform('x', 1.0125, 'location') # move plane
    set_origin_to_3D_cursor() # re-align origin
    
    ### ------------------------------------------
    ### Add heigth to skyscrapper floor+floor/2
    ### ------------------------------------------
    modify('ARRAY')
    modify_args('Array').relative_offset_displace[0] = 0 # Factor: X is now 0
    modify_args('Array').relative_offset_displace[2] = 1
    modify_args('Array').count = floor # Factor: Z is now variable floor
    apply_modifier('Array')

    
    ### ------------------------------------------
    ### Add WALLS of skyscrapper
    ### ------------------------------------------
    dup()
    move_it(dimension('x'), dimension('x'), 0)
    rotate('Z', 180)
    
    dup()
    rotate('Z', 90)
    move_it(0, -dimension('x'), 0)
    
    dup()
    move_it(-dimension('x'), dimension('x'), 0)
    rotate('Z', 180)
    
    de_select(True, 'OBJECT')
    join_objs() # Join all into one obj
    
    set_origin_to_3D_cursor() # re-align origin
    
    bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')
    
    ### ------------------------------------------
    ### Add ROOF of skyscrapper
    ### ------------------------------------------
    mode('OBJECT')
    building_z = dimension('z') 
    building_x = dimension('x')

    makeplane(building_x*1.01)
    transform('z', building_z/2, 'location')

    a_mat('Roof') ## assign maerial

    mode('EDIT')
    modify('SOLIDIFY')
    modify_args('Solidify').thickness = 0.05
    apply_modifier('Solidify')

    de_select(False, 'EDIT')

    s = bm().faces
    s.ensure_lookup_table()
    s[0].select = True
    update()

    inset(size*.001)
    extrude(z=size*.01)
    inset(size*.006)
    extrude(z=size*-.01)

    selection('EDGES')
    de_select(False, 'EDIT')

    s = bm().edges
    s.ensure_lookup_table()
    for num in [0, 1, 2, 3, 4, 5, 6, 7, 20, 21, 22, 23]:
        s[num].select = True
        update()

    custom_bevel(4, 'EDGES')
    mode('OBJECT')
    ### ------------------------------------------
    ### Add LEVELs of skyscrapper
    ### ------------------------------------------
    makeplane(building_x)
    transform('z', -building_z/2, 'location')
    
    for z in range(-int(round(building_z)/2), int(round(building_z)/2), 1):
        makeplane(building_x*.993, z=z)

    ### ------------------------------------------
    ### Line up skyscrapper
    ### ------------------------------------------
    de_select(True, 'OBJECT')
    join_objs()
    set_origin_to_3D_cursor()

    apply_obj(True)
    transform('z', building_z/2, 'location')
    set_origin_to_3D_cursor()

    if bpy.context.object.dimensions.x > 6 and bpy.context.object.dimensions.x < 8:
        new_xy = random.choice([2.2, 2.3, 2.4, 2.5])
        re_size((bpy.context.object.scale.x*new_xy, bpy.context.object.scale.y*new_xy, bpy.context.object.scale.z))

    if bpy.context.object.dimensions.x > 8 and bpy.context.object.dimensions.x < 10:
        new_xy = random.choice([2, 2.1, 2.2, 2.3])
        re_size((bpy.context.object.scale.x*new_xy, bpy.context.object.scale.y*new_xy, bpy.context.object.scale.z))
        
    if bpy.context.object.dimensions.x > 10 and bpy.context.object.dimensions.x < 13:
        new_xy = random.choice([2, 2.1])
        re_size((bpy.context.object.scale.x*new_xy, bpy.context.object.scale.y*new_xy, bpy.context.object.scale.z))

    smooth(True) # shade smooth
    bpy.context.object.name = 'Skyscrapper'

def skyscraper_towers(new_coll):
    #### --------------------------------------------
    #### -- Create second tower on skyscrappers -----
    bpy.ops.object.select_all(action='DESELECT')
    for ob in list(bpy.data.collections[new_coll.name_full].objects):
        if ob.name_full.startswith('Skyscrapper') and ob.dimensions.x > 20 and ob.dimensions.y > 20:
            ob.select_set(True)
            bpy.context.view_layer.objects.active = ob
            
            x, y, z = ob.location.x, ob.location.y, ob.dimensions.z*2
            dimensions_x, dimensions_y, dimensions_z = ob.dimensions.x/1.5, ob.dimensions.y/1.5, ob.dimensions.z/2

            dup()
            bpy.context.object.name = 'Sky_Tower'
            ob.select_set(True)

            bpy.context.object.location   = (x, y, random.choice([z/2.5, z/3.4, z/3.3, z/3.2]))
            bpy.context.object.dimensions = (dimensions_x, dimensions_y, dimensions_z)
            
            bpy.ops.object.join()
            set_origin_to_3D_cursor()
            bpy.context.object.select_set(False)
