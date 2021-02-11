import bpy
import bmesh
import random

from blender_tools import dimension, array, modify, de_select, mode, makeplane, makecube, \
                       transform, selection, extrude, extrude_normals, inset, rotate, \
                       bm, update, subdivide, apply_modifier, hide, dup, \
                       dissolve_e, re_size, move_it, a_mat

ground_material   = set()
roof_material     = set()
building_material = set()
GROUND, ROOF, BUILDING, PILLARS, COLUMNS, WINDOWS = 'Ground', 'Roof', 'Building', 'Pillars', 'Columns', 'Windows'

##SIMPLE BUILDING SQUARE 1
def building_square(size, kind, floors, align, align_option, layout_check, distance, current_collections, new_collection, a_option, a_check):
    print('square_1')
    floor = random.randint(1, floors)
    pillar = random.choice([.01, .1, .05, .03])
    windows = random.choice([-.08, -.1, -.15, -.12])
    col = random.choice([.05, .1, .07])
    ##############################################################################
    ###################### GROUND ################################################
    ##############################################################################
    ##MAKES PLANE, EXTRUDE
    ground = size*1.4
    makeplane(ground) # MAKES PLANE
    a_mat(GROUND, ground_material)

    ##############################################################################
    ###################### FLOOR #################################################
    ##############################################################################
    ##MAKES PLANE, EXTRUDE
    makeplane(size) # MAKES PLANE
    mode('EDIT') # EDIT MODE
    selection('FACE') # FACE SELECT
    extrude(0, 0, .1)

    a_mat(ROOF, roof_material)
    ##############################################################################
    ###################### ROOF ##################################################
    ##############################################################################
    ##MODIFIER ARRAY
    mode('OBJECT')
    modify('ARRAY')
    array('x', 0)
    array('z', floor*30)
    apply_modifier('Array')

    mode('EDIT')
    de_select(False, 'EDIT')
    
    s = bm().faces
    s.ensure_lookup_table()
    s[7].select = True
    update()

    extrude(z=1)
    inset(.3)
    extrude(z=-.6)
    
    
    ##############################################################################
    ###################### BUILDING ######## FIRST FLOOR #########################
    ##############################################################################
    ##MAKE PLANE, EXTRUDES, INSETS, EXTRUDES
    mode('OBJECT')
    makeplane(size-.3, z=.05)
    mode('EDIT')
    extrude(0,0,1)
    inset(pillar) # INSET FACE SELECTED
    extrude(0, 0, 2)
    de_select(False, 'EDIT')
    
    a_mat(BUILDING, building_material)
    ##############################################################################
    ###################### BUILDING ######## FIRST FLOOR ###### PILLARS ##########
    ##############################################################################
    ##### Select Faces #####
    s = bm().faces
    s.ensure_lookup_table()
    for i in range(2,10):
        s[i].select = True
    update()
    ##New MATERIAL
    a_mat(PILLARS, building_material)
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
    ###################### SUBDIVIDE ######## FIRST FLOOR #########################

    ##############################################################################
    ###################### VARIATIONS ############################################
    ##############################################################################

    if kind == 'col':
        ##### Select Faces #####
        f_select = [1, 11, 12, 13, 14, 17, 20, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 84, 85,
                    86, 87, 88, 89, 90, 91, 92, 93, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131,
                    132, 133, 134, 137, 140, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 174, 175, 176, 177, 178, 179, 180, 181,
                    182, 183, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245,
                    246, 247, 248, 249, 250, 251, 252, 253, 254, 257, 260, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 294, 295,
                    296, 297, 298, 299, 300, 301, 302, 303, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 354, 355, 356, 357, 358, 359,
                    360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 494, 497, 500, 503, 504, 505, 506, 507, 508, 509,
                    510, 511, 512, 513, 534, 535, 536, 537, 538, 539, 540, 541, 542, 543, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573,
                    594, 595, 596, 597, 598, 599, 600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613]
        s = bm().faces
        s.ensure_lookup_table()
        for i in f_select:
            s[i].select = True
        update()
        a_mat(COLUMNS, building_material)

        ##EXTRUDE NORMALS 
        extrude_normals(col) # making Col
        de_select(False, 'EDIT')

        ##############################################################################
        ###################### BUILDING ######## FIRST FLOOR ###### WINDOWS ##########
        ##############################################################################
        ##### Select Faces #####
        mode('EDIT')
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
        a_mat(WINDOWS, building_material)

        ##EXTRUDE NORMALS 
        extrude_normals(windows) # making Windows

        ##############################################################################
        ###################### BUILDING ######## FIRST FLOOR ###### MODIFIER #########
        ##############################################################################
        ##MODIFIER BEVEL
        mode('OBJECT')
        modify('BEVEL')
        bpy.context.object.modifiers["Bevel"].width = 0.02
        bpy.context.object.modifiers["Bevel"].segments = 4
        apply_modifier('Bevel')

        modify('ARRAY')
        array('x', 0)
        array('z', 1, floor)
        apply_modifier("Array")
    else:
        ##############################################################################
        ###################### BUILDING ######## FIRST FLOOR ###### WINDOWS ##########
        ##############################################################################
        ##### Select Faces #####
        mode('EDIT')
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
        a_mat(WINDOWS, building_material)

        ##EXTRUDE NORMALS 
        extrude_normals(windows) # making Windows

        ##############################################################################
        ###################### BUILDING ######## FIRST FLOOR ###### MODIFIER #########
        ##############################################################################
        ##MODIFIER BEVEL
        mode('OBJECT')
        modify('BEVEL')
        bpy.context.object.modifiers["Bevel"].width = 0.02
        bpy.context.object.modifiers["Bevel"].segments = 4
        apply_modifier('Bevel')

        modify('ARRAY')
        array('x', 0)
        array('z', 1, floor)
        apply_modifier("Array")
    
    ##############################################################################
    ###################### BUILDING ######## FINISHING ###### JOIN ALL OBJS ######
    ##############################################################################
    ##Select All & Join to one obj
    de_select(True, 'OBJECT')
    bpy.ops.object.join()

    if layout_check == 'line':
        ##MOVING OBJS
        transform('y', ground+distance[-1])
        distance.append(ground+dimension('y')+distance[-1])
        if a_check:
            '''Checkbox ticked'''
            if a_option == 'right':
                transform('x', size/2 * 1.4)
                rotate('z', 180)
            if align_option == 'left':
                transform('x', -size/2 * 1.4)

        new_collection.objects.link(bpy.context.object) # adding building obj to new collection
        current_collections.objects.unlink(bpy.context.object) # unlinking building obj from current collection
        
        for obj in bpy.context.selected_objects: # rename objs
            obj.name = f'Building'

    else:
        new_collection.objects.link(bpy.context.object) # adding building obj to new collection
        current_collections.objects.unlink(bpy.context.object) # unlinking building obj from current collection
        distance.append(ground+dimension('y')+distance[-1])
        for obj in bpy.context.selected_objects: # rename objs
            obj.name = f'Building'

##SIMPLE BUILDING SQUARE 2
def building_square_2(size, kind, floors, align, align_option, layout_check, distance, current_collections, new_collection, a_option, a_check):
    print('square_2')
    obj = bpy.context.active_object
    floor = random.randint(1, floors)
    pillar = random.choice([.01, .1, .05, .03])
    windows = random.choice([-.08, -.1, -.15, -.12])
    col = random.choice([.05, .1, .07])

    ##############################################################################
    ###################### GROUND ################################################
    ##############################################################################
    ##MAKES PLANE, EXTRUDE
    ground = size*1.4
    makeplane(ground) # MAKES PLANE

    a_mat(GROUND, ground_material)
    ##############################################################################
    ###################### FLOOR #################################################
    ##############################################################################
    ##MAKES PLANE, EXTRUDE
    makeplane(size) # MAKES PLANE
    mode('EDIT') # EDIT MODE
    selection('FACE') # FACE SELECT
    extrude(0, 0, .1)

    a_mat(ROOF, roof_material)
    ##############################################################################
    ###################### ROOF ##################################################
    ##############################################################################
    ##MODIFIER ARRAY
    mode('OBJECT')
    modify('ARRAY')
    array('x', 0)
    array('z', floor*30)
    apply_modifier('Array')

    mode('EDIT')
    de_select(False, 'EDIT')
    
    s = bm().faces
    s.ensure_lookup_table()
    s[7].select = True
    update()

    extrude(z=1)
    inset(.3)
    extrude(z=-.6)
    

    ##############################################################################
    ###################### BUILDING ######## FIRST FLOOR #########################
    ##############################################################################
    ##MAKE PLANE, EXTRUDES, INSETS, EXTRUDES
    mode('OBJECT')
    makeplane(size-.3, z=.05)
    mode('EDIT')
    extrude(0,0,1)
    inset(pillar) # INSET FACE SELECTED
    extrude(0, 0, 2)
    de_select(False, 'EDIT')

    a_mat(BUILDING, building_material)
    ##############################################################################
    ###################### BUILDING ######## FIRST FLOOR ###### PILLARS ##########
    ##############################################################################
    ##### Select Faces #####
    s = bm().faces
    s.ensure_lookup_table()
    for i in range(2,10):
        s[i].select = True
    update()

    ##New MATERIAL
    a_mat(PILLARS, building_material)
    
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
    ###################### SUBDIVIDE ######## FIRST FLOOR #########################

    ##############################################################################
    ###################### VARIATIONS ############################################
    ##############################################################################

    if kind == 'col':
        ##### Select Faces #####
        f_select = [1, 11, 12, 13, 14, 17, 20, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 84, 85,
                    86, 87, 88, 89, 90, 91, 92, 93, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131,
                    132, 133, 134, 137, 140, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 174, 175, 176, 177, 178, 179, 180, 181,
                    182, 183, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245,
                    246, 247, 248, 249, 250, 251, 252, 253, 254, 257, 260, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 294, 295,
                    296, 297, 298, 299, 300, 301, 302, 303, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 354, 355, 356, 357, 358, 359,
                    360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 494, 497, 500, 503, 504, 505, 506, 507, 508, 509,
                    510, 511, 512, 513, 534, 535, 536, 537, 538, 539, 540, 541, 542, 543, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573,
                    594, 595, 596, 597, 598, 599, 600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613]
        s = bm().faces
        s.ensure_lookup_table()
        for i in f_select:
            s[i].select = True
        update()
        a_mat(COLUMNS, building_material)

        ##EXTRUDE NORMALS 
        extrude_normals(col) # making Col
        de_select(False, 'EDIT')

        ##############################################################################
        ###################### BUILDING ######## FIRST FLOOR ###### WINDOWS ##########
        ##############################################################################
        ##### Select Faces #####
        mode('EDIT')
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
        a_mat(WINDOWS, building_material)

        ##EXTRUDE NORMALS 
        extrude_normals(windows) # making Windows

        ##############################################################################
        ###################### BUILDING ######## FIRST FLOOR ###### MODIFIER #########
        ##############################################################################
        ##MODIFIER BEVEL
        mode('OBJECT')
        modify('BEVEL')
        bpy.context.object.modifiers["Bevel"].width = 0.02
        bpy.context.object.modifiers["Bevel"].segments = 4
        apply_modifier('Bevel')

        modify('ARRAY')
        array('x', 0)
        array('z', 1, floor)
        apply_modifier("Array")
    else:
        ##############################################################################
        ###################### BUILDING ######## FIRST FLOOR ###### WINDOWS ##########
        ##############################################################################
        ##### Select Faces #####
        mode('EDIT')
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
        a_mat(WINDOWS, building_material)

        ##EXTRUDE NORMALS 
        extrude_normals(windows) # making Windows

        ##############################################################################
        ###################### BUILDING ######## FIRST FLOOR ###### MODIFIER #########
        ##############################################################################
        ##MODIFIER BEVEL
        mode('OBJECT')
        modify('BEVEL')
        bpy.context.object.modifiers["Bevel"].width = 0.02
        bpy.context.object.modifiers["Bevel"].segments = 4
        apply_modifier('Bevel')

        modify('ARRAY')
        array('x', 0)
        array('z', 1, floor)
        apply_modifier("Array")

    ##############################################################################
    ###################### BUILDING ######## FINISHING ###### JOIN ALL OBJS ######
    ##############################################################################
    ##Select All & Join to one obj
    de_select(True, 'OBJECT')
    bpy.ops.object.join()

    if dimension('z') > 50 and dimension('z') < 65:
        de_select(True, 'OBJECT')
        modify('ARRAY')
        array('x', 0)
        array('y', 1)
        apply_modifier('Array')
        rotate('z', 180)

    if layout_check == 'line':
        ##MOVING OBJS
        transform('y', ground+distance[-1])
        distance.append(ground+dimension('y')+distance[-1])

        if a_check:
            '''Checkbox ticked'''
            if a_option == 'right':
                transform('x', size/2 * 1.4)
                rotate('z', 180)
            if align_option == 'left':
                transform('x', -size/2 * 1.4)

        new_collection.objects.link(bpy.context.object) # adding building obj to new collection
        current_collections.objects.unlink(bpy.context.object) # unlinking building obj from current collection
        
        for obj in bpy.context.selected_objects: # rename objs
            obj.name = f'Building'

    else:
        new_collection.objects.link(bpy.context.object) # adding building obj to new collection
        current_collections.objects.unlink(bpy.context.object) # unlinking building obj from current collection
        
        for obj in bpy.context.selected_objects: # rename objs
            obj.name = f'Building'

##SIMPLE BUILDING SQUARE 3
def building_square_3(size, kind, floors, align, align_option, layout_check, distance, current_collections, new_collection, a_option, a_check):
    print('square_3!')
    floor = random.randint(1, floors)
    windows = random.choice([-.08, -.1, -.15, -.12])
    pillar = random.choice([.01, .1, .05, .03])
    col = random.choice([.05, .1, .07])

    ##############################################################################
    ###################### GROUND ################################################
    ##############################################################################
    ##MAKES PLANE, EXTRUDE
    ground = size*1.4
    makeplane(ground)

    a_mat(GROUND, ground_material)
    ##############################################################################
    ###################### FLOOR #################################################
    ##############################################################################
    ##MAKES PLANE, EXTRUDE
    makeplane(size) # MAKES PLANE
    mode('EDIT') # EDIT MODE
    selection('FACE') # FACE SELECT
    extrude(0, 0, .1)

    a_mat(ROOF, roof_material)
    ##############################################################################
    ###################### ROOF ##################################################
    ##############################################################################
    ##MODIFIER ARRAY
    mode('OBJECT')
    modify('ARRAY')
    array('x', 0)
    array('z', floor*30)
    apply_modifier('Array')

    mode('EDIT')
    de_select(False, 'EDIT')
    
    s = bm().faces
    s.ensure_lookup_table()
    s[7].select = True
    update()

    extrude(z=1)
    inset(.3)
    extrude(z=-.6)
    
    ##############################################################################
    ###################### BUILDING ######## FIRST FLOOR #########################
    ##############################################################################
    ##MAKE PLANE, EXTRUDES, INSETS, EXTRUDES
    mode('OBJECT')
    makeplane(size-.3, z=.05)
    
    ##New MATERIAL
    a_mat(BUILDING, building_material)

    mode('EDIT')
    extrude(0,0,1)
    inset(pillar) # INSET FACE SELECTED
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
        print(s[i])
    update()

    ##New MATERIAL
    a_mat(PILLARS, building_material)

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
    ###################### SUBDIVIDE ######## FIRST FLOOR #########################

    ##############################################################################
    ###################### VARIATIONS ############################################
    ##############################################################################
    
    if kind == 'col':
        ##### Select Faces #####
        f_select = [1, 11, 12, 13, 14, 17, 20, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 84, 85,
                    86, 87, 88, 89, 90, 91, 92, 93, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131,
                    132, 133, 134, 137, 140, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 174, 175, 176, 177, 178, 179, 180, 181,
                    182, 183, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245,
                    246, 247, 248, 249, 250, 251, 252, 253, 254, 257, 260, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 294, 295,
                    296, 297, 298, 299, 300, 301, 302, 303, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 354, 355, 356, 357, 358, 359,
                    360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 494, 497, 500, 503, 504, 505, 506, 507, 508, 509,
                    510, 511, 512, 513, 534, 535, 536, 537, 538, 539, 540, 541, 542, 543, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573,
                    594, 595, 596, 597, 598, 599, 600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613]
        s = bm().faces
        s.ensure_lookup_table()
        for i in f_select:
            s[i].select = True
        update()
        a_mat(COLUMNS, building_material)

        ##EXTRUDE NORMALS 
        extrude_normals(col) # making Col
        de_select(False, 'EDIT')
        
        ##############################################################################
        ###################### BUILDING ######## FIRST FLOOR ###### WINDOWS ##########
        ##############################################################################
        ##### Select Faces #####
        mode('EDIT')
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
        a_mat(WINDOWS, building_material)

        ##EXTRUDE NORMALS 
        extrude_normals(windows) # making Windows

        ##############################################################################
        ###################### BUILDING ######## FIRST FLOOR ###### MODIFIER #########
        ##############################################################################
        ##MODIFIER BEVEL
        mode('OBJECT')
        modify('BEVEL')
        bpy.context.object.modifiers["Bevel"].width = 0.02
        bpy.context.object.modifiers["Bevel"].segments = 4
        apply_modifier('Bevel')

        modify('ARRAY')
        array('x', 0)
        array('z', 1, floor)
        apply_modifier("Array")
    else:
        ##############################################################################
        ###################### BUILDING ######## FIRST FLOOR ###### WINDOWS ##########
        ##############################################################################
        ##### Select Faces #####
        mode('EDIT')
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
        a_mat(WINDOWS, building_material)

        ##EXTRUDE NORMALS 
        extrude_normals(windows) # making Windows
        
        ##############################################################################
        ###################### BUILDING ######## FIRST FLOOR ###### MODIFIER #########
        ##############################################################################
        ##MODIFIER BEVEL
        mode('OBJECT')
        modify('BEVEL')
        bpy.context.object.modifiers["Bevel"].width = 0.02
        bpy.context.object.modifiers["Bevel"].segments = 4
        apply_modifier('Bevel')

        modify('ARRAY')
        array('x', 0)
        array('z', 1, floor)
        apply_modifier("Array")
    
    ##############################################################################
    ###################### BUILDING ######## FINISHING ###### JOIN ALL OBJS ######
    ##############################################################################
    ##Select All & Join to one obj
    de_select(True, 'OBJECT')
    bpy.ops.object.join()

    if layout_check == 'line':
        ##MOVING OBJS
        transform('y', ground+distance[-1])
        distance.append(ground+dimension('y')+distance[-1])
        if a_check:
            '''Checkbox ticked'''
            if a_option == 'right':
                transform('x', size/2 * 1.4)
                rotate('z', 180)
            if align_option == 'left':
                transform('x', -size/2 * 1.4)

        new_collection.objects.link(bpy.context.object) # adding building obj to new collection
        current_collections.objects.unlink(bpy.context.object) # unlinking building obj from current collection
        
        for obj in bpy.context.selected_objects: # rename objs
            obj.name = f'Building'

    else:
        new_collection.objects.link(bpy.context.object) # adding building obj to new collection
        current_collections.objects.unlink(bpy.context.object) # unlinking building obj from current collection
        for obj in bpy.context.selected_objects: # rename objs
            obj.name = f'Building'