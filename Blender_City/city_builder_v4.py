bl_info = {
    "name": "easy city",
    "author": "Davi Silveira <vidasilveira85@gmail.com>",
    "version": (1, 7),
    "blender": (2,90,1),
    "category": "Add Mesh",
    "location": "Operator Search",
    "description": "We Building This City",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
}

import bpy
import bmesh
import random



class MESH_OT_city(bpy.types.Operator):
    """Build Buildings"""

    bl_idname = "mesh.city"
    bl_label = "EASY CITY"
    bl_options = {'REGISTER', 'UNDO'}

    max_building: bpy.props.IntProperty(
        name='Num of buildings',
        description="Enter number",
        default=5,
        min=1, soft_max=50,
    )
    floors_on_building: bpy.props.IntProperty(
        name='Max floors',
        description="Enter number of floors",
        default=7,
        min=1, soft_max=50,
    )

    size_of_building: bpy.props.IntProperty(
        name='Max size',
        description="Enter number of buildings to build",
        default=10,
        min=5, soft_max=30,
    )


    def execute(self, context):
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

        def array(axis, value, num=2):
            """[summary]

            Args:
                axis ([STR]): [description]
                value ([type]): [description]
                num (int, optional): [description]. Defaults to 2.
            """
            if axis == 'x':
                bpy.context.object.modifiers["Array"].relative_offset_displace[0] = value
            if axis == 'y':
                bpy.context.object.modifiers["Array"].relative_offset_displace[1] = value
            if axis == 'z':
                bpy.context.object.modifiers["Array"].relative_offset_displace[2] = value
            bpy.context.object.modifiers["Array"].count = num


        def modify(mod):
            return bpy.ops.object.modifier_add(type=mod)

        def de_select(bool, mode):
            """Select All or DeSelect All

            Args:
                bool (BOOL): [True == SELECT ALL, False == DESELECT ALL]
                mode (STR):  ['OBJECT' for obj mode, 'EDIT' for edit mode]

            """
            if mode == 'OBJECT':
                if bool:
                    return bpy.ops.object.select_all(action="SELECT")
                else:
                    return bpy.ops.object.select_all(action='DESELECT')
            if mode == 'EDIT':        
                if bool:
                    return bpy.ops.mesh.select_all(action="SELECT")
                else:
                    return bpy.ops.mesh.select_all(action='DESELECT')
            return "nothing was selected, please pick 'mode'"


        def mode(env):
            return bpy.ops.object.mode_set(mode=env)


        def makeplane(s, x=0, y=0, z=0):
            return bpy.ops.mesh.primitive_plane_add(size=s, enter_editmode=False, align='WORLD', location=(x, y, z))

        def makecube(s, lx=0, ly=0, lz=0, x=1, y=1, z=1):
            """[Makes a Cube]

            Args:
                s ([INT]): [Size of Cube]
                lx (int, optional): [Location X]. Defaults to 0.
                ly (int, optional): [Location Y]. Defaults to 0.
                lz (int, optional): [Location Z]. Defaults to 0.
                x (int, optional): [Scale of X]. Defaults to 1.
                y (int, optional): [Scale of Y]. Defaults to 1.
                z (int, optional): [Scale of Z]. Defaults to 1.

            """
            return bpy.ops.mesh.primitive_cube_add(size=s, enter_editmode=False, align='WORLD', location=(lx, ly, lz), scale=(x, y, z))

        def moveobj(x=0,y=0,z=0):
            return bpy.ops.transform.translate(value=(x, y, z), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)


        def selection(kind):
            """[EDIT mode Selection type]

            Args:
                kind ([STR]): ['FACE', 'EDGE', 'VERT']

            Returns:
                [type]: [description]
            """
            if kind == 'FACE':
                return bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
            elif kind == 'EDGE':
                return bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')
            elif kind == 'VERT':
                return bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')

        def extrude(x=0, y=0, z=0):
            """Extrudes along Axis

            Args:
                x (int, optional): [X direction]. Defaults to 0.
                y (int, optional): [Y direction]. Defaults to 0.
                z (int, optional): [Z direction]. Defaults to 0.
            
            """
            return bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False},
                                                    TRANSFORM_OT_translate={"value":(x, y, z), "orient_type":'NORMAL', "orient_matrix":((0, -1, 0), (1, 0, -0), (0, 0, 1)), "orient_matrix_type":'NORMAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

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
                val ([INT]): [90, 180]

            """
            if val == 180:
                return bpy.ops.transform.rotate(value=3.14159, orient_axis=axis, orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
            elif val == 90:
                return bpy.ops.transform.rotate(value=1.5708, orient_axis=axis, orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
            else:
                print('no rotation was picked... 180, 90')

        def bm():
            obj = bpy.context.edit_object
            me = obj.data
            return bmesh.from_edit_mesh(me)

        def update():
            return bmesh.update_edit_mesh(bpy.context.edit_object.data, True)

        def subdivide(val):
            """[summary]

            Args:
                val ([INT]): [number of subdivide]

            """
            return bpy.ops.mesh.subdivide(number_cuts=val)

        def apply_modifier(val):
            """[applies the modifer to obj]

            Args:
                val ([STR]): ["Array", "Bevel", etc]

            """
            return bpy.ops.object.modifier_apply(modifier=val)

        def add_material(named, index_assign = -1):
            """[add new material with name and index optinal]

            Args:
                named ([STR]): [Name of Material]
                index_assign (int, optional): [index of Material slot starts at 0]. Defaults to -1.

            """
            if index_assign == -1:
                material = bpy.data.materials.new(name=named) # new material
                return bpy.context.edit_object.data.materials.append(material)
            else:
                material = bpy.data.materials.new(name=named) # new material
                bpy.context.edit_object.data.materials.append(material)
                bpy.context.object.active_material_index = index_assign
                return bpy.ops.object.material_slot_assign()

        def hide(bool):
            """Hides Everything or UnHides everything.
            Only with Selected Iteams 

            Args:
                bool ([BOOL]): [True: Hides, False: UnHides]

            """
            if bool:
                return bpy.ops.object.hide_view_set()
            else:
                return bpy.ops.object.hide_view_clear()

        ################################################################################################
        """Prepare Outliner START"""
        de_select(True, 'OBJECT')
        hide(True)
        """Prepare Outliner END"""
        current_collections = bpy.context.collection # list of all collections
        new_collection = bpy.data.collections.new('Buildings') # new collection
        bpy.context.scene.collection.children.link(new_collection) # show in OUTLINER
        ################################################################################################
        ################################################################################################
        ################################################################################################
        locations = {}

        lst = [0]
        def move(x):
            lst.append(x + lst[-1])
            return lst[-1]
        
        ##SIMPLE BUILDING | Flat
        def building_one(sizes=self.size_of_building, floors=self.floors_on_building, max_b=self.max_building, m=2):
            print('1')
            size = random.randint(5, sizes)
            floor = random.randint(1, floors)
            
            ##MAKES PLANE, EXTRUDE
            makeplane(size) # MAKES PLANE
            mode('EDIT') # EDIT MODE
            selection('FACE') # FACE SELECT
            extrude(0, 0, .1)
            
            ##MAKE PLANE, EXTRUDES, INSETS, EXTRUDES
            mode('OBJECT')
            makeplane(size-.3, z=.05)
            mode('EDIT')
            extrude(0,0,1)
            inset(0.01) # INSET FACE SELECTED
            extrude(0, 0, 2)
            de_select(False, 'EDIT')
            
            ##New MATERIAL  
            de_select(True, 'EDIT')
            add_material('building')
            de_select(False, 'EDIT')
            
            ##### Select Faces #####
            s = bm().faces
            s.ensure_lookup_table()
            for i in range(2,10):
                s[i].select = True
            update()
            add_material('pillars', 1)
            de_select(False, 'EDIT')
            
            ##MODIFIER ARRAY
            mode('OBJECT')
            modify('ARRAY')
            array('x', 0)
            array('z', 1, floor)
            
            ##### Select Faces #####
            mode('EDIT')
            s = bm().faces
            s.ensure_lookup_table()
            for i in range(11,14):
                s[i].select = True
            s[1].select = True
            update()
            
            ##SUBDIVIDE
            subdivide(10)
            de_select(False, 'EDIT')


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
            add_material('windows', 2)

            ##EXTRUDE NORMALS 
            extrude_normals(-.1) # making Windows

            ##MODIFIER BEVEL
            mode('OBJECT')
            modify('BEVEL')
            bpy.context.object.modifiers["Bevel"].width = 0.02
            bpy.context.object.modifiers["Bevel"].segments = 4
            ##MODIFIER ARRAY
            apply_modifier("Array")

            ##MAKE CUBE ROOF OBJ##
            makecube((size-.3)*2, z=1/9.7, lz=dimension('z'))
            mode('EDIT')
            moveobj(z=dimension('z')/2)
            de_select(False, 'EDIT')

            s = bm().faces
            s.ensure_lookup_table()
            s[5].select = True
            inset(.2, 0)
            extrude(z=-floor*.345)

            ##MODIFIER BEVEL
            modify('BEVEL')
            bpy.context.object.modifiers["Bevel"].width = 0.02
            bpy.context.object.modifiers["Bevel"].segments = 5

            ##MAKES PLANE
            mode('OBJECT')
            makeplane(size*1.5) # MAKES PLANE

            ##Select All & Join to one obj
            de_select(True, 'OBJECT')
            bpy.ops.object.join()

            ##MOVING OBJS
            moveobj(x=-(size*1.5)/2)
            moveobj(y=m)
            m += size*1.5

            new_collection.objects.link(bpy.context.object) # adding building obj to new collection
            current_collections.objects.unlink(bpy.context.object) # unlinking building obj from current collection
            
            for obj in bpy.context.selected_objects: # rename objs
                obj.name = f'Building'

            ##HIDE OBJ
            hide(True)
        ##SIMPLE BUILDING | Flat
        def building_one_A(sizes=self.size_of_building, floors=self.floors_on_building, max_b=self.max_building, m=2):
            print('1A')
            size = random.randint(5, sizes)
            floor = random.randint(1, floors)
            
            ##MAKES PLANE, EXTRUDE
            makeplane(size) # MAKES PLANE
            mode('EDIT') # EDIT MODE
            selection('FACE') # FACE SELECT
            extrude(0, 0, .1)
            
            ##MAKE PLANE, EXTRUDES, INSETS, EXTRUDES
            mode('OBJECT')
            makeplane(size-.3, z=.05)
            mode('EDIT')
            extrude(0,0,1)
            inset(0.005) # INSET FACE SELECTED
            extrude(0, 0, 2)
            de_select(False, 'EDIT')
            
            ##New MATERIAL  
            de_select(True, 'EDIT')
            add_material('building')
            de_select(False, 'EDIT')
            
            ##### Select Faces #####
            s = bm().faces
            s.ensure_lookup_table()
            for i in range(2,10):
                s[i].select = True
            update()
            add_material('pillars', 1)
            de_select(False, 'EDIT')
            
            ##MODIFIER ARRAY
            mode('OBJECT')
            modify('ARRAY')
            array('x', 0)
            array('z', 1, floor)
            
            ##### Select Faces #####
            mode('EDIT')
            s = bm().faces
            s.ensure_lookup_table()
            for i in range(11,14):
                s[i].select = True
            s[1].select = True
            update()
            
            ##SUBDIVIDE
            subdivide(10)
            de_select(False, 'EDIT')


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
            add_material('windows', 2)

            ##EXTRUDE NORMALS 
            extrude_normals(-.1) # making Windows

            ##MODIFIER BEVEL
            mode('OBJECT')
            modify('BEVEL')
            bpy.context.object.modifiers["Bevel"].width = 0.02
            bpy.context.object.modifiers["Bevel"].segments = 4
            ##MODIFIER ARRAY
            apply_modifier("Array")

            ##MAKE CUBE ROOF OBJ##
            makecube((size-.3)*2, z=1/9.7, lz=dimension('z'))
            mode('EDIT')
            moveobj(z=dimension('z')/2)
            de_select(False, 'EDIT')

            s = bm().faces
            s.ensure_lookup_table()
            s[5].select = True
            inset(.2, 0)
            extrude(z=-floor*.345)

            ##MODIFIER BEVEL
            modify('BEVEL')
            bpy.context.object.modifiers["Bevel"].width = 0.02
            bpy.context.object.modifiers["Bevel"].segments = 5

            ##MAKES PLANE
            mode('OBJECT')
            makeplane(size*1.5) # MAKES PLANE

            ##Select All & Join to one obj
            de_select(True, 'OBJECT')
            bpy.ops.object.join()

            ##MOVING OBJS
            moveobj(x=-(size*1.5)/2)
            moveobj(y=m)
            m += size*1.5

            new_collection.objects.link(bpy.context.object) # adding building obj to new collection
            current_collections.objects.unlink(bpy.context.object) # unlinking building obj from current collection
            
            for obj in bpy.context.selected_objects: # rename objs
                obj.name = f'Building'

            ##HIDE OBJ
            hide(True)

        ##SIMPLE v2 BUILDING | Horizontal ROWs
        def building_two(sizes=self.size_of_building, floors=self.floors_on_building, max_b=self.max_building, m=2):
            print('2')
            size = random.randint(5, sizes)
            floor = random.randint(1, floors)

            ##MAKES PLANE, EXTRUDE
            makeplane(size) # MAKES PLANE
            mode('EDIT') # EDIT MODE
            selection('FACE') # FACE SELECT
            extrude(0, 0, .1)
            
            ##MAKE PLANE, EXTRUDES, INSETS, EXTRUDES
            mode('OBJECT')
            makeplane(size-.3, z=.05)
            mode('EDIT')
            extrude(0,0,1)
            inset(0.1, .001) # INSET FACE SELECTED
            extrude(0, 0, 2)
            de_select(False, 'EDIT')
            
            ##New MATERIAL  
            de_select(True, 'EDIT')
            add_material('building')
            de_select(False, 'EDIT')
            
            ##### Select Faces #####
            s = bm().faces
            s.ensure_lookup_table()
            for i in range(2,10):
                s[i].select = True
            update()
            add_material('pillars', 1)
            de_select(False, 'EDIT')
            
            ##MODIFIER ARRAY
            mode('OBJECT')
            modify('ARRAY')
            array('x', 0)
            array('z', 1, floor)
            
            ##### Select Faces #####
            mode('EDIT')
            s = bm().faces
            s.ensure_lookup_table()
            for i in range(11,14):
                s[i].select = True
            s[1].select = True
            update()
            
            ##SUBDIVIDE
            subdivide(10)
            de_select(False, 'EDIT')


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
            add_material('windows', 2)

            ##EXTRUDE NORMALS 
            extrude_normals(-.1) # making Windows

            ##MODIFIER BEVEL
            mode('OBJECT')
            modify('BEVEL')
            bpy.context.object.modifiers["Bevel"].width = 0.02
            bpy.context.object.modifiers["Bevel"].segments = 4
            ##MODIFIER ARRAY
            apply_modifier("Array")

            ##MAKE CUBE ROOF OBJ##
            makecube((size-.3)*2, z=1/9.7, lz=dimension('z'))
            mode('EDIT')
            moveobj(z=dimension('z')/2)
            de_select(False, 'EDIT')

            s = bm().faces
            s.ensure_lookup_table()
            s[5].select = True
            inset(.2, 0)
            extrude(z=-floor*.345)

            ##MODIFIER BEVEL
            modify('BEVEL')
            bpy.context.object.modifiers["Bevel"].width = 0.02
            bpy.context.object.modifiers["Bevel"].segments = 5

            ##MAKES PLANE
            mode('OBJECT')
            makeplane(size*1.5) # MAKES PLANE

            ##Select All & Join to one obj
            de_select(True, 'OBJECT')
            bpy.ops.object.join()

            ##MOVING OBJS
            moveobj(x=-(size*1.5)/2)
            moveobj(y=m)
            m += size*1.5

            new_collection.objects.link(bpy.context.object) # adding building obj to new collection
            current_collections.objects.unlink(bpy.context.object) # unlinking building obj from current collection
            
            for obj in bpy.context.selected_objects: # rename objs
                obj.name = f'Building'

            ##HIDE OBJ
            hide(True)
        ##SIMPLE v2 BUILDING | Horizontal ROWs
        def building_two_A(sizes=self.size_of_building, floors=self.floors_on_building, max_b=self.max_building, m=2):
            print('2A')
            size = random.randint(5, sizes)
            floor = random.randint(1, floors)

            ##MAKES PLANE, EXTRUDE
            makeplane(size) # MAKES PLANE
            mode('EDIT') # EDIT MODE
            selection('FACE') # FACE SELECT
            extrude(0, 0, .1)
            
            ##MAKE PLANE, EXTRUDES, INSETS, EXTRUDES
            mode('OBJECT')
            makeplane(size-.3, z=.05)
            mode('EDIT')
            extrude(0,0,1)
            inset(0.1, .001) # INSET FACE SELECTED
            extrude(0, 0, 2)
            de_select(False, 'EDIT')
            
            ##New MATERIAL  
            de_select(True, 'EDIT')
            add_material('building')
            de_select(False, 'EDIT')
            
            ##### Select Faces #####
            s = bm().faces
            s.ensure_lookup_table()
            for i in range(2,10):
                s[i].select = True
            update()
            add_material('pillars', 1)
            de_select(False, 'EDIT')
            
            ##MODIFIER ARRAY
            mode('OBJECT')
            modify('ARRAY')
            array('x', 0)
            array('z', 1, floor)
            
            ##### Select Faces #####
            mode('EDIT')
            s = bm().faces
            s.ensure_lookup_table()
            for i in range(11,14):
                s[i].select = True
            s[1].select = True
            update()
            
            ##SUBDIVIDE
            subdivide(10)
            de_select(False, 'EDIT')


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
            add_material('windows', 2)

            ##EXTRUDE NORMALS 
            extrude_normals(-.1) # making Windows

            ##MODIFIER BEVEL
            mode('OBJECT')
            modify('BEVEL')
            bpy.context.object.modifiers["Bevel"].width = 0.02
            bpy.context.object.modifiers["Bevel"].segments = 4
            ##MODIFIER ARRAY
            apply_modifier("Array")

            ##MAKE CUBE
            makecube((size-.3)*2, z=1/9.7, lz=dimension('z'))
            mode('EDIT')
            moveobj(z=dimension('z')/2)
            de_select(False, 'EDIT')

            s = bm().faces
            s.ensure_lookup_table()
            s[5].select = True
            inset(.2, 0)
            extrude(z=-floor*.345)

            ##MODIFIER BEVEL
            modify('BEVEL')
            bpy.context.object.modifiers["Bevel"].width = 0.02
            bpy.context.object.modifiers["Bevel"].segments = 5

            ##MAKES PLANE
            mode('OBJECT')
            makeplane(size*1.5) # MAKES PLANE

            ##Select All & Join to one obj
            de_select(True, 'OBJECT')
            bpy.ops.object.join()

            ##MOVING OBJS
            moveobj(x=-(size*1.5)/2)
            moveobj(y=m)
            m += size*1.5

            new_collection.objects.link(bpy.context.object) # adding building obj to new collection
            current_collections.objects.unlink(bpy.context.object) # unlinking building obj from current collection
            
            for obj in bpy.context.selected_objects: # rename objs
                obj.name = f'Building'

            ##HIDE OBJ
            hide(True)

        ##SIMPLE v3 BUILDING | Vertical COLs
        def building_three(sizes=self.size_of_building, floors=self.floors_on_building, max_b=self.max_building, m=2):
            print('3')
            size = random.randint(5, sizes)
            floor = random.randint(1, floors)
            
            ##MAKES PLANE, EXTRUDE
            makeplane(size) # MAKES PLANE
            mode('EDIT') # EDIT MODE
            selection('FACE') # FACE SELECT
            extrude(0, 0, .1)
            
            ##MAKE PLANE, EXTRUDES, INSETS, EXTRUDES
            mode('OBJECT')
            makeplane(size-.3, z=.05)
            mode('EDIT')
            extrude(0,0,1)
            inset(0.1) # INSET FACE SELECTED
            extrude(0, 0, 2)
            de_select(False, 'EDIT')
            
            ##New MATERIAL  
            de_select(True, 'EDIT')
            add_material('building')
            de_select(False, 'EDIT')
            
            ##### Select Faces #####
            s = bm().faces
            s.ensure_lookup_table()
            for i in range(2,10):
                s[i].select = True
            update()

            # ##New MATERIAL
            # add_material('pillars', 1)
            # de_select(False, 'EDIT')
            
            ##MODIFIER ARRAY
            mode('OBJECT')
            modify('ARRAY')
            array('x', 0)
            array('z', 1, floor)
            
            ##### Select Faces #####
            mode('EDIT')
            s = bm().faces
            s.ensure_lookup_table()
            for i in range(11,14):
                s[i].select = True
            s[1].select = True
            update()
            
            ##SUBDIVIDE
            subdivide(10)
            de_select(False, 'EDIT')

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
            add_material('col', 1)

            ##EXTRUDE NORMALS 
            extrude_normals(random.choice([.05, .1, .15])) # making Col
            de_select(False, 'EDIT')

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
            add_material('windows', 3)

            ##EXTRUDE NORMALS 
            extrude_normals(-.1) # making Windows
            
            
            ##MODIFIER BEVEL
            mode('OBJECT')
            modify('BEVEL')
            bpy.context.object.modifiers["Bevel"].width = 0.02
            bpy.context.object.modifiers["Bevel"].segments = 4
            ##MODIFIER ARRAY
            apply_modifier("Array")

            ##MAKE CUBE
            makecube((size-.3)*2, z=1/9.7, lz=dimension('z'))
            mode('EDIT')
            moveobj(z=dimension('z')/2)
            de_select(False, 'EDIT')

            s = bm().faces
            s.ensure_lookup_table()
            s[5].select = True
            inset(.2, 0)
            extrude(z=-floor*.345)

            ##MODIFIER BEVEL
            modify('BEVEL')
            bpy.context.object.modifiers["Bevel"].width = 0.02
            bpy.context.object.modifiers["Bevel"].segments = 5

            ##MAKES PLANE
            mode('OBJECT')
            makeplane(size*1.5) # MAKES PLANE

            ##Select All & Join to one obj
            de_select(True, 'OBJECT')
            bpy.ops.object.join()

            ##MOVING OBJS
            moveobj(x=-(size*1.5)/2)
            moveobj(y=m)
            m += size*1.5

            new_collection.objects.link(bpy.context.object) # adding building obj to new collection
            current_collections.objects.unlink(bpy.context.object) # unlinking building obj from current collection
            
            for obj in bpy.context.selected_objects: # rename objs
                obj.name = f'Building'
            
            ##HIDE OBJ
            hide(True)
        ##SIMPLE v3 BUILDING | Vertical COLs
        def building_three_A(sizes=self.size_of_building, floors=self.floors_on_building, max_b=self.max_building, m=2):
            print('3A')
            size = random.randint(5, sizes)
            floor = random.randint(1, floors)
            
            ##MAKES PLANE, EXTRUDE
            makeplane(size) # MAKES PLANE
            mode('EDIT') # EDIT MODE
            selection('FACE') # FACE SELECT
            extrude(0, 0, .1)
            
            ##MAKE PLANE, EXTRUDES, INSETS, EXTRUDES
            mode('OBJECT')
            makeplane(size-.3, z=.05)
            mode('EDIT')
            extrude(0,0,1)
            inset(0.1) # INSET FACE SELECTED
            extrude(0, 0, 2)
            de_select(False, 'EDIT')
            
            ##New MATERIAL  
            de_select(True, 'EDIT')
            add_material('building')
            de_select(False, 'EDIT')
            
            ##### Select Faces #####
            s = bm().faces
            s.ensure_lookup_table()
            for i in range(2,10):
                s[i].select = True
            update()

            ##New MATERIAL
            add_material('pillars', 1)
            de_select(False, 'EDIT')
            
            ##MODIFIER ARRAY
            mode('OBJECT')
            modify('ARRAY')
            array('x', 0)
            array('z', 1, floor)
            
            ##### Select Faces #####
            mode('EDIT')
            s = bm().faces
            s.ensure_lookup_table()
            for i in range(11,14):
                s[i].select = True
            s[1].select = True
            update()
            
            ##SUBDIVIDE
            subdivide(10)
            de_select(False, 'EDIT')

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
            add_material('col', 1)

            ##EXTRUDE NORMALS 
            extrude_normals(random.choice([.05, .1,])) # making Col
            de_select(False, 'EDIT')

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
            add_material('windows', 3)

            ##EXTRUDE NORMALS 
            extrude_normals(-.1) # making Windows
            
            
            ##MODIFIER BEVEL
            mode('OBJECT')
            modify('BEVEL')
            bpy.context.object.modifiers["Bevel"].width = 0.02
            bpy.context.object.modifiers["Bevel"].segments = 4
            ##MODIFIER ARRAY
            apply_modifier("Array")

            ##MAKE CUBE
            makecube((size-.3)*2, z=1/9.7, lz=dimension('z'))
            mode('EDIT')
            moveobj(z=dimension('z')/2)
            de_select(False, 'EDIT')

            s = bm().faces
            s.ensure_lookup_table()
            s[5].select = True
            inset(.2, 0)
            extrude(z=-floor*.345)

            ##MODIFIER BEVEL
            modify('BEVEL')
            bpy.context.object.modifiers["Bevel"].width = 0.02
            bpy.context.object.modifiers["Bevel"].segments = 5

            ##MAKES PLANE
            mode('OBJECT')
            makeplane(size*1.5) # MAKES PLANE

            ##Select All & Join to one obj
            de_select(True, 'OBJECT')
            bpy.ops.object.join()

            ##MOVING OBJS
            moveobj(x=-(size*1.5)/2)
            moveobj(y=m)
            m += size*1.5

            new_collection.objects.link(bpy.context.object) # adding building obj to new collection
            current_collections.objects.unlink(bpy.context.object) # unlinking building obj from current collection
            
            for obj in bpy.context.selected_objects: # rename objs
                obj.name = f'Building'
            
            ##HIDE OBJ
            hide(True)

        ##SIMPLE v4 BUILDING | Vertical COLs
        def building_four(sizes=self.size_of_building, floors=self.floors_on_building, max_b=self.max_building, m=2):
            print('4')
            size = random.randint(5, sizes)
            floor = random.randint(1, floors)
            
            ##MAKES PLANE, EXTRUDE
            makeplane(size) # MAKES PLANE
            mode('EDIT') # EDIT MODE
            selection('FACE') # FACE SELECT
            extrude(0, 0, .1)
            
            ##MAKE PLANE, EXTRUDES, INSETS, EXTRUDES
            mode('OBJECT')
            makeplane(size-.3, z=.05)
            mode('EDIT')
            extrude(0,0,1)
            inset(0.1) # INSET FACE SELECTED
            extrude(0, 0, 2)
            de_select(False, 'EDIT')
            
            ##New MATERIAL  
            de_select(True, 'EDIT')
            add_material('building')
            de_select(False, 'EDIT')
            
            ##### Select Faces #####
            s = bm().faces
            s.ensure_lookup_table()
            for i in range(2,10):
                s[i].select = True
            update()

            ##New MATERIAL
            add_material('pillars', 1)
            de_select(False, 'EDIT')
            
            ##MODIFIER ARRAY
            mode('OBJECT')
            modify('ARRAY')
            array('x', 0)
            array('z', 1, floor)
            
            ##### Select Faces #####
            mode('EDIT')
            s = bm().faces
            s.ensure_lookup_table()
            for i in range(11,14):
                s[i].select = True
            s[1].select = True
            update()
            
            ##SUBDIVIDE
            subdivide(10)
            de_select(False, 'EDIT')

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
            add_material('col', 1)

            ##EXTRUDE NORMALS 
            extrude_normals(random.choice([.05, .1, .15])) # making Col
            de_select(False, 'EDIT')

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
            add_material('windows', 3)

            ##EXTRUDE NORMALS 
            extrude_normals(-.1) # making Windows
            
            
            ##MODIFIER BEVEL
            mode('OBJECT')
            modify('BEVEL')
            bpy.context.object.modifiers["Bevel"].width = 0.02
            bpy.context.object.modifiers["Bevel"].segments = 4
            ##MODIFIER ARRAY
            apply_modifier("Array")

            ##MAKE CUBE
            makecube((size-.3)*2, z=1/9.7, lz=dimension('z'))
            mode('EDIT')
            moveobj(z=dimension('z')/2)
            de_select(False, 'EDIT')

            s = bm().faces
            s.ensure_lookup_table()
            s[5].select = True
            inset(.2, 0)
            extrude(z=-.4)

            ##MODIFIER BEVEL
            modify('BEVEL')
            bpy.context.object.modifiers["Bevel"].width = 0.02
            bpy.context.object.modifiers["Bevel"].segments = 5

            ##MAKES PLANE
            mode('OBJECT')
            makeplane(size*1.5) # MAKES PLANE

            ##Select All & Join to one obj
            de_select(True, 'OBJECT')
            bpy.ops.object.join()
            ##############################################
            #################SECOND STORY#################
            ##############################################    
            ##MAKE PLANE, EXTRUDES, INSETS, EXTRUDES
            mode('OBJECT')
            makeplane(size*.6666)
            mode('EDIT')
            extrude(0,0,1)
            inset(0.1) # INSET FACE SELECTED
            extrude(0, 0, 2)
            de_select(False, 'EDIT')
            
            ##New MATERIAL  
            de_select(True, 'EDIT')
            add_material('building')
            de_select(False, 'EDIT')
            
            ##### Select Faces #####
            s = bm().faces
            s.ensure_lookup_table()
            for i in range(2,10):
                s[i].select = True
            update()

            ##New MATERIAL
            add_material('pillars', 1)
            de_select(False, 'EDIT')
            
            ##MODIFIER ARRAY
            mode('OBJECT')
            modify('ARRAY')
            array('x', 0)
            array('z', 1, round(floor*1.6, 2))
            
            ##### Select Faces #####
            mode('EDIT')
            s = bm().faces
            s.ensure_lookup_table()
            for i in range(11,14):
                s[i].select = True
            s[1].select = True
            update()
            
            ##SUBDIVIDE
            subdivide(10)
            de_select(False, 'EDIT')

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
            add_material('col', 1)

            ##EXTRUDE NORMALS 
            extrude_normals(random.choice([.05, .1, .15])) # making Col
            de_select(False, 'EDIT')

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
            add_material('windows', 3)

            ##EXTRUDE NORMALS 
            extrude_normals(-.1) # making Windows
            
            
            ##MODIFIER BEVEL
            mode('OBJECT')
            modify('BEVEL')
            bpy.context.object.modifiers["Bevel"].width = 0.02
            bpy.context.object.modifiers["Bevel"].segments = 4
            ##MODIFIER ARRAY
            apply_modifier("Array")

            ##MAKE CUBE
            makecube(((size-.3)*.6666)*2, z=1/9.7, lz=dimension('z'))
            mode('EDIT')
            moveobj(z=dimension('z')/2)
            de_select(False, 'EDIT')

            s = bm().faces
            s.ensure_lookup_table()
            s[5].select = True
            inset(.2, 0)
            extrude(z=-floor*.2)

            ##MODIFIER BEVEL
            mode('OBJECT')
            modify('BEVEL')
            bpy.context.object.modifiers["Bevel"].width = 0.02
            bpy.context.object.modifiers["Bevel"].segments = 5

            ##Select All & Join to one obj
            de_select(True, 'OBJECT')
            bpy.ops.object.join()

            ##MOVING OBJS
            moveobj(x=-(size*1.5)/2)
            moveobj(y=m)
            m += size*1.5

            new_collection.objects.link(bpy.context.object) # adding building obj to new collection
            current_collections.objects.unlink(bpy.context.object) # unlinking building obj from current collection
            
            for obj in bpy.context.selected_objects: # rename objs
                obj.name = f'Building'

            ##HIDE OBJ
            hide(True)
        ##SIMPLE v4 BUILDING | Horizontal ROWs
        def building_four_A(sizes=self.size_of_building, floors=self.floors_on_building, max_b=self.max_building, m=2):
            print('4A')
            size = random.randint(5, sizes)
            floor = random.randint(1, floors)

            ##MAKES PLANE, EXTRUDE
            makeplane(size) # MAKES PLANE
            mode('EDIT') # EDIT MODE
            selection('FACE') # FACE SELECT
            extrude(0, 0, .1)
            
            ##MAKE PLANE, EXTRUDES, INSETS, EXTRUDES
            mode('OBJECT')
            makeplane(size-.3, z=.05)
            mode('EDIT')
            extrude(0,0,1)
            inset(0.1, .001) # INSET FACE SELECTED
            extrude(0, 0, 2)
            de_select(False, 'EDIT')
            
            ##New MATERIAL  
            de_select(True, 'EDIT')
            add_material('building')
            de_select(False, 'EDIT')
            
            ##### Select Faces #####
            s = bm().faces
            s.ensure_lookup_table()
            for i in range(2,10):
                s[i].select = True
            update()
            add_material('pillars', 1)
            de_select(False, 'EDIT')
            
            ##MODIFIER ARRAY
            mode('OBJECT')
            modify('ARRAY')
            array('x', 0)
            array('z', 1, floor)
            
            ##### Select Faces #####
            mode('EDIT')
            s = bm().faces
            s.ensure_lookup_table()
            for i in range(11,14):
                s[i].select = True
            s[1].select = True
            update()
            
            ##SUBDIVIDE
            subdivide(10)
            de_select(False, 'EDIT')


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
            add_material('windows', 2)

            ##EXTRUDE NORMALS 
            extrude_normals(-.1) # making Windows

            ##MODIFIER BEVEL
            mode('OBJECT')
            modify('BEVEL')
            bpy.context.object.modifiers["Bevel"].width = 0.02
            bpy.context.object.modifiers["Bevel"].segments = 4
            ##MODIFIER ARRAY
            apply_modifier("Array")

            ##MAKE CUBE
            makecube((size-.3)*2, z=1/9.7, lz=dimension('z'))
            mode('EDIT')
            moveobj(z=dimension('z')/2)
            de_select(False, 'EDIT')

            s = bm().faces
            s.ensure_lookup_table()
            s[5].select = True
            inset(.2, 0)
            extrude(z=-.4)

            ##MODIFIER BEVEL
            modify('BEVEL')
            bpy.context.object.modifiers["Bevel"].width = 0.02
            bpy.context.object.modifiers["Bevel"].segments = 5

            ##MAKES PLANE
            mode('OBJECT')
            makeplane(size*1.5) # MAKES PLANE

            ##Select All & Join to one obj
            de_select(True, 'OBJECT')
            bpy.ops.object.join()
            ##############################################
            #################SECOND STORY#################
            ##############################################  
            ##MAKE PLANE, EXTRUDES, INSETS, EXTRUDES
            mode('OBJECT')
            makeplane(size*.666, lz= z=.05)
            mode('EDIT')
            extrude(0,0,1)
            inset(0.1, .001) # INSET FACE SELECTED
            extrude(0, 0, 2)
            de_select(False, 'EDIT')
            
            ##New MATERIAL  
            de_select(True, 'EDIT')
            add_material('building')
            de_select(False, 'EDIT')
            
            ##### Select Faces #####
            s = bm().faces
            s.ensure_lookup_table()
            for i in range(2,10):
                s[i].select = True
            update()
            add_material('pillars', 1)
            de_select(False, 'EDIT')
            
            ##MODIFIER ARRAY
            mode('OBJECT')
            modify('ARRAY')
            array('x', 0)
            array('z', 1, round(floor*1.45, 2))
            
            ##### Select Faces #####
            mode('EDIT')
            s = bm().faces
            s.ensure_lookup_table()
            for i in range(11,14):
                s[i].select = True
            s[1].select = True
            update()
            
            ##SUBDIVIDE
            subdivide(10)
            de_select(False, 'EDIT')


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
            add_material('windows', 2)

            ##EXTRUDE NORMALS 
            extrude_normals(-.1) # making Windows

            ##MODIFIER BEVEL
            mode('OBJECT')
            modify('BEVEL')
            bpy.context.object.modifiers["Bevel"].width = 0.02
            bpy.context.object.modifiers["Bevel"].segments = 4
            ##MODIFIER ARRAY
            apply_modifier("Array")

            ##MAKE CUBE
            makecube(((size-.3)*.6666)*2, z=1/9.7, lz=dimension('z'))
            mode('EDIT')
            moveobj(z=dimension('z')/2)
            de_select(False, 'EDIT')

            s = bm().faces
            s.ensure_lookup_table()
            s[5].select = True
            inset(.2, 0)
            extrude(z=-floor*.2)

            ##MODIFIER BEVEL
            mode('OBJECT')
            modify('BEVEL')
            bpy.context.object.modifiers["Bevel"].width = 0.02
            bpy.context.object.modifiers["Bevel"].segments = 5


            ##Select All & Join to one obj
            de_select(True, 'OBJECT')
            bpy.ops.object.join()

            ##MOVING OBJS
            moveobj(x=-(size*1.5)/2)
            moveobj(y=m)
            m += size*1.5

            new_collection.objects.link(bpy.context.object) # adding building obj to new collection
            current_collections.objects.unlink(bpy.context.object) # unlinking building obj from current collection
            
            for obj in bpy.context.selected_objects: # rename objs
                obj.name = f'Building'

            ##HIDE OBJ
            hide(True)

        for i in range(self.max_building):
            funcs = [building_one, building_one_A, building_two, building_two_A, building_three, building_three_A, building_four, building_four_A]
            random.choice(funcs)(m=move(self.size_of_building*2))
            locations[i] = dimension()

        hide(False)
        return {'FINISHED'} # or {'CAANCELED'}


class VIEW3D_PT_city(bpy.types.Panel):
    bl_label = "Easy Building"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "City Builder"


    def draw(self, context):
        """draw something on screen"""
        layout = self.layout

        scene = context.scene

        layout.label(text='Building Generator')
        row = layout.row()
        row.scale_y = 2.0
        row.operator("mesh.city")


        col = layout.column(align=True)

        buildings = col.operator('mesh.city',
                        text='Building Generator',
                        icon='CON_SAMEVOL',)


def register():
    bpy.utils.register_class(MESH_OT_city)
    bpy.utils.register_class(VIEW3D_PT_city)


def unregister():
    bpy.utils.register_class(MESH_OT_city)
    bpy.utils.register_class(VIEW3D_PT_city)



if __name__ == "__main__":
    register()