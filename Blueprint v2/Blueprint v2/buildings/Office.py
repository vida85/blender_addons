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
                                   subdivide)

texture = ['Building', 'Pillar', 'Column', 'Windows', 'Roof']
####-----------------------------------------------
####-- Start
def office(floors, c_coll, n_coll):
    floor  = random.choice(list(range(5, floors)))
    size   = 10
    pillar = random.choice([.01, .1, .05, .03])

    ##############################################################################
    ###################### FLOOR #################################################
    ##############################################################################
    ##MAKES PLANE, EXTRUDE
    makeplane(size, x=.05) # MAKES PLANE
    mode('EDIT') # EDIT MODE
    selection('FACE') # FACE SELECT
    extrude(0, 0, .1)

    a_mat('Roof')
    ###################### EXTEND FLOOR on Y #####################################
    ##MODIFIER ARRAY
    mode('OBJECT')
    modify('ARRAY')
    modify_args('Array').relative_offset_displace[0] = -1
    apply_modifier('Array')
    
    ##############################################################################
    ###################### ROOF ##################################################
    ##############################################################################
    ##MODIFIER ARRAY
    mode('OBJECT')
    modify('ARRAY')
    modify_args('Array').relative_offset_displace[0] = 0
    modify_args('Array').relative_offset_displace[2] = floor*30
    modify_args('Array').count = 2
    apply_modifier('Array')
    
    ##### Select Faces #####
    mode('EDIT')
    de_select(True, 'EDIT')
    bpy.ops.mesh.remove_doubles()
    de_select(False, 'EDIT')

    s = bm().faces
    s.ensure_lookup_table()
    s[12].select = True
    s[18].select = True
    update()
    
    dup() # duplicate
    dissolve_e() # dissolve edges

    s.ensure_lookup_table()
    s[22].select = True
    update()

    extrude(z=1)
    inset(.3)
    extrude(z=-.6)

    ##############################################################################
    ###################### BUILDING ######## FIRST FLOOR #########################
    ##############################################################################
    ##MAKE PLANE, EXTRUDES, INSETS, EXTRUDES
    mode('OBJECT')
    makeplane(size-.1, z=.05) ############################################################## --- change to zero???? touch floor
    a_mat('Building')
    
    mode('EDIT')
    extrude(0,0,1)
    inset(-pillar) # INSET FACE SELECTED
    extrude(0, 0, 2)
    de_select(False, 'EDIT')

    ##############################################################################
    ###################### BUILDING ######## FIRST FLOOR ###### PILLARS ##########
    ##############################################################################
    ##### Select Faces #####
    s = bm().faces
    s.ensure_lookup_table()
    for i in range(2,10):
        s[i].select = True
    update()

    a_mat('Pillars')
    de_select(False, 'EDIT')
    ###################### SUBDIVIDE ######## FIRST FLOOR #########################
    ##### Select Faces #####
    mode('EDIT')
    s = bm().faces
    s.ensure_lookup_table()
    for i in range(11,14):
        s[i].select = True
    s[1].select = True
    update()
    subdivide(10)
    de_select(False, 'EDIT')

    ##############################################################################
    ###################### BUILDING ######## FIRST FLOOR ###### WINDOWS ##########
    ##############################################################################
    ##### Select Faces #####
    
    f_select = [35, 36, 37, 38, 39, 40, 41, 42, 43, 45, 46, 47, 48, 49, 50, 51, 52, 53, 65, 66, 67, 68, 69, 70, 71, 72, 73, 75, 76, 77,
                78, 79, 80, 81, 82, 83, 95, 96, 97, 98, 99, 100, 101, 102, 103, 105, 106, 107, 108, 109, 110, 111, 112, 113, 155, 156,
                157, 158, 159, 160, 161, 162, 163, 165, 166, 167, 168, 169, 170, 171, 172, 173, 185, 186, 187, 188, 189, 190, 191, 192,
                193, 195, 196, 197, 198, 199, 200, 201, 202, 203, 215, 216, 217, 218, 219, 220, 221, 222, 223, 225, 226, 227, 228, 229,
                230, 231, 232, 233, 275, 276, 277, 278, 279, 280, 281, 282, 283, 285, 286, 287, 288, 289, 290, 291, 292, 293, 305, 306,
                307, 308, 309, 310, 311, 312, 313, 315, 316, 317, 318, 319, 320, 321, 322, 323, 335, 336, 337, 338, 339, 340, 341, 342,
                343, 345, 346, 347, 348, 349, 350, 351, 352, 353, 515, 516, 517, 518, 519, 520, 521, 522, 523, 525, 526, 527, 528, 529,
                530, 531, 532, 533, 545, 546, 547, 548, 549, 550, 551, 552, 553, 555, 556, 557, 558, 559, 560, 561, 562, 563, 575, 576,
                577, 578, 579, 580, 581, 582, 583, 585, 586, 587, 588, 589, 590, 591, 592, 593]

    s = bm().faces
    s.ensure_lookup_table()
    for i in f_select:
        s[i].select = True
    update()
    ##New MATERIAL
    a_mat(texture[3])

    ##EXTRUDE NORMALS 
    extrude_normals(random.choice([-.05, -.1, -.15, -.2])) # making Windows
    
    ##############################################################################
    ###################### BUILDING ######## FIRST FLOOR ###### MODIFIER #########
    ##############################################################################
    ##MODIFIER ARRAY
    mode('OBJECT')
    
    modify('ARRAY')
    modify_args('Array').relative_offset_displace[0] = -1
    apply_modifier('Array')
    
    ##ADD MIDDLE SECTION JOINING BOTH BUILDING INTO ONE
    mode('EDIT')
    selection('EDGE')   
    de_select(False, 'EDIT')
    
    s = bm().edges
    s.ensure_lookup_table()
    s[26].select = True
    s[27].select = True
    for i in range(128, 148):
        s[i].select = True
    update()
    extrude(y=-pillar*2)
    ##ADD MIDDLE SECTION JOINING BOTH BUILDING INTO ONE
    
    ##MODIFIER BEVEL
    mode('OBJECT')
    modify('BEVEL')
    modify_args("Bevel").width = 0.02
    modify_args("Bevel").segments = 4
    apply_modifier('Bevel')

    ##RAISE up TO FLOOR AMOUNT
    modify('ARRAY')
    modify_args('Array').relative_offset_displace[0] = 0
    modify_args('Array').relative_offset_displace[2] = 1
    modify_args('Array').count = floor
    apply_modifier("Array")

    ##############################################################################
    ###################### BUILDING ######## FINISHING ###### JOIN ALL OBJS ######
    ##############################################################################
    ##Select All & Join to one obj
    de_select(True, 'OBJECT')
    bpy.ops.object.join()
    obj = bpy.context.object
    obj.name = f'office_a_roof'

    bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')

    transform('z', dimension('z')/2, 'location')
    transform('x', (dimension('x')/2)/10, 'location')
    set_origin_to_3D_cursor()
    
    rooftop_structures(obj, dimension('x'), dimension('z'))
    de_select(True, 'OBJECT')
    bpy.ops.object.join()
    set_origin_to_3D_cursor()
    
    bpy.context.object.name = 'Office_a'

def office_2(floors, c_coll, n_coll):
    floor  = random.choice(list(range(5, floors)))
    size   = 10
    pillar = random.choice([.01, .1, .05, .03])
    col    = random.choice([.05, .1, .07])

    ##############################################################################
    ###################### FLOOR #################################################
    ##############################################################################
    ##MAKES PLANE, EXTRUDE
    makeplane(size, x=.05) # MAKES PLANE
    mode('EDIT') # EDIT MODE
    selection('FACE') # FACE SELECT
    extrude(0, 0, .1)

    a_mat(texture[-1])
    ###################### EXTEND FLOOR on Y #####################################
    ##MODIFIER ARRAY
    mode('OBJECT')
    modify('ARRAY')
    modify_args('Array').relative_offset_displace[0] = -1
    apply_modifier('Array')
    
    ##############################################################################
    ###################### ROOF ##################################################
    ##############################################################################
    ##MODIFIER ARRAY
    mode('OBJECT')
    modify('ARRAY')
    modify_args('Array').relative_offset_displace[0] = 0
    modify_args('Array').relative_offset_displace[2] = floor*30
    modify_args('Array').count = 2
    apply_modifier('Array')
    
    ##### Select Faces #####
    mode('EDIT')
    de_select(True, 'EDIT')
    bpy.ops.mesh.remove_doubles()
    de_select(False, 'EDIT')

    s = bm().faces
    s.ensure_lookup_table()
    s[12].select = True
    s[18].select = True
    update()
    
    dup() # duplicate
    dissolve_e() # dissolve edges

    s.ensure_lookup_table()
    s[22].select = True
    update()

    extrude(z=1)
    inset(.3)
    extrude(z=-.6)

    ##############################################################################
    ###################### BUILDING ######## FIRST FLOOR #########################
    ##############################################################################
    ##MAKE PLANE, EXTRUDES, INSETS, EXTRUDES
    mode('OBJECT')
    makeplane(size-.1, z=.05) ############################################################## --- change to zero???? touch floor
    a_mat('Building')
    
    mode('EDIT')
    extrude(0,0,1)
    inset(-pillar) # INSET FACE SELECTED
    extrude(0, 0, 2)
    de_select(False, 'EDIT')

    ##############################################################################
    ###################### BUILDING ######## FIRST FLOOR ###### PILLARS ##########
    ##############################################################################
    ##### Select Faces #####
    s = bm().faces
    s.ensure_lookup_table()
    for i in range(2,10):
        s[i].select = True
    update()

    a_mat('Pillars')
    de_select(False, 'EDIT')
    ###################### SUBDIVIDE ######## FIRST FLOOR #########################
    ##### Select Faces #####
    mode('EDIT')
    s = bm().faces
    s.ensure_lookup_table()
    for i in range(11,14):
        s[i].select = True
    s[1].select = True
    update()
    subdivide(10)
    de_select(False, 'EDIT')

    ##### Select Faces #####
    f_select = [11, 12, 134, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 244, 245, 246, 247, 248, 249,
                250, 251, 252, 253, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 494, 504, 505, 506, 507, 508, 509, 510,
                511, 512, 513]

    s = bm().faces
    s.ensure_lookup_table()
    for i in f_select:
        s[i].select = True
    update()
    a_mat('Columns_1')
    
    ##EXTRUDE NORMALS 
    extrude_normals(col) # making Col
    de_select(False, 'EDIT')

    ##### Select Faces #####
    f_select = [1, 254, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 604, 605, 606, 607, 608, 609, 610, 611,
                612, 613]

    s = bm().faces
    s.ensure_lookup_table()
    for i in f_select:
        s[i].select = True
    update()
    a_mat('Columns_2')
    
    ##EXTRUDE NORMALS 
    extrude_normals(col) # making Col
    de_select(False, 'EDIT')

    ##############################################################################
    ###################### BUILDING ######## FIRST FLOOR ###### WINDOWS ##########
    ##############################################################################
    ##### Select Faces #####
    f_select = [166, 167, 168, 169, 170, 171, 172, 173, 176, 177, 178, 179, 180, 181, 182, 183, 186, 187, 188, 189, 190,
                191, 192, 193, 206, 207, 208, 209, 210, 211, 212, 213, 216, 217, 218, 219, 220, 221, 222, 223, 226, 227,
                228, 229, 230, 231, 232, 233, 286, 287, 288, 289, 290, 291, 292, 293, 296, 297, 298, 299, 300, 301, 302,
                303, 306, 307, 308, 309, 310, 311, 312, 313, 326, 327, 328, 329, 330, 331, 332, 333, 336, 337, 338, 339,
                340, 341, 342, 343, 346, 347, 348, 349, 350, 351, 352, 353, 526, 527, 528, 529, 530, 531, 532, 533, 536,
                537, 538, 539, 540, 541, 542, 543, 546, 547, 548, 549, 550, 551, 552, 553, 566, 567, 568, 569, 570, 571,
                572, 573, 576, 577, 578, 579, 580, 581, 582, 583, 586, 587, 588, 589, 590, 591, 592, 593]

    s = bm().faces
    s.ensure_lookup_table()
    for i in f_select:
        s[i].select = True
    update()
    ##New MATERIAL
    a_mat('Windows')

    ##EXTRUDE NORMALS 
    extrude_normals(random.choice([-.05, -.1, -.15, -.2])) # making Windows

    ##############################################################################
    ###################### BUILDING ######## FIRST FLOOR ###### MODIFIER #########
    ##############################################################################
    ##MODIFIER ARRAY
    mode('OBJECT')
    transform('x', dimension('x')/2.2, 'location')
    set_origin_to_3D_cursor()
    modify('Mirror')
    apply_modifier('Mirror')
    transform('x', -dimension('x')/3.9, 'location')
    
    #MODIFIER BEVEL
    modify('BEVEL')
    modify_args("Bevel").width = 0.02
    modify_args("Bevel").segments = 4
    apply_modifier('Bevel')
    
    ##RAISE up TO FLOOR AMOUNT
    modify('ARRAY')
    modify_args('Array').relative_offset_displace[0] = 0
    modify_args('Array').relative_offset_displace[2] = 1
    modify_args('Array').count = floor
    apply_modifier("Array")

    mode('object')
    de_select(True, 'OBJECT')
    bpy.ops.object.join()

    choice = random.choice([0, 1])
    if bpy.context.object.dimensions.z < 50:
        if choice:
            bpy.context.object.scale[1] = 2
        else:
            bpy.context.object.scale[0] = .5
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    bpy.context.object.name = 'Office_b'
