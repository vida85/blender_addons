bl_info = {
    "name": "BLENDER CITY",
    "author": "Davi Silveira <vidasilveira85@gmail.com>",
    "version": (1),
    "blender": (2,90,1),
    "category": "Add Mesh",
    "location": "Operator Search",
    "description": "Building a quick city",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
}


import bpy
import bmesh
from random import randint, choices, uniform


class MESH_OT_city(bpy.types.Operator):
    """Build a Wall of Bricks"""
    bl_idname = "mesh.city"
    bl_label = "BLENDER CITY Properties"
    bl_options = {'REGISTER', 'UNDO'}
    

    num_buildings: bpy.props.IntProperty(
        name= 'number of buildings',
        description="Enter number of buildings to build",
        default=7,
        min=1, soft_max=100,
    )
    
    num_roof_structures: bpy.props.IntProperty(
        name= 'number of roof structures',
        description="number of roof structures per building",
        default=3,
        min=1, soft_max=10,
    )
    
    max_height: bpy.props.IntProperty(
        name= 'Max height of buildings',
        description="Maximum height of buildings",
        default=15,
        min=1, soft_max=20,
    )

    support_pillars: bpy.props.IntProperty(
        name= 'Min height for pillars',
        description="Minium height of buildings with outside pillars",
        default=13,
        min=1, soft_max=10,
    )

    user_y_cordinate: bpy.props.BoolProperty(
        name= 'Align buildings on Axis',
        description="Buildings align in a straight line along Y axis",
        default=True,
    )

    sides: bpy.props.EnumProperty(
        name= 'Pick a Side',
        description="Buildings align along Y on the Left or Right side",
        items=(
            ('Left', 'Left', 'Left', '', 0),
            ('Right', 'Right', 'Right', '', 1),
        ),
        default='Left',
    )

    def execute(self, context):
        """Prepare Outliner"""
        bpy.ops.object.select_all(action='SELECT') # select all
        bpy.ops.object.hide_view_set(unselected=False) # hide all
        
        current_collections = bpy.context.collection # list of all collections
        new_collection = bpy.data.collections.new('bCity') # new collection
        bpy.context.scene.collection.children.link(new_collection) # show in OUTLINER
        
        """Blender City Builder v.2"""
        num_of_building = self.num_buildings
        num_of_structures = self.num_roof_structures
        maximum = self.max_height

        user_y = self.user_y_cordinate
        side = self.sides

        support_pillar = self.support_pillars

        x_location = 0
        file_number = 0 # building numbering
        
        ## buildings ##
        for _ in range(num_of_building):
            file_number += 1
            x = randint(1, 4)
            y = randint(1, 4)
            z = randint(1, maximum)
            
            x_location += 9
            
            building = bpy.ops.mesh
            building.primitive_cube_add(size=2) # make CUBE

            bpy.ops.object.editmode_toggle() # Enter Edit Mode
            bpy.ops.transform.translate(value=(0, 0, 1)) # Raise to X floor set origin point on the bottom
            bpy.ops.object.editmode_toggle() # Exit Edit Mode

            bpy.ops.transform.resize(value=(x, y, z)) # random builing resize
            
            if user_y == True:
                if side == 'Left':
                    bpy.ops.transform.translate(value=(x_location + x, y, 0)) # move CUBE along X & line up building on Y
                if side == 'Right':
                    bpy.ops.transform.translate(value=(x_location + x, -y, 0)) # move CUBE along X & line up building on -Y
            else:
                bpy.ops.transform.translate(value=(x_location + x, 0, 0)) # move CUBE along X
    
            bpy.ops.object.mode_set(mode = 'OBJECT')
            obj = bpy.context.active_object

            bpy.ops.object.editmode_toggle() # Enter Edit Mode
            bpy.ops.mesh.select_mode(type="FACE")
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.editmode_toggle() # Exit Edit Mode

            obj.data.polygons[5].select = True
            bpy.ops.object.editmode_toggle() # Enter Edit Mode
            

            if z >= 15: # extrude up
                bpy.ops.mesh.inset(thickness=0.3, depth=0)
                bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False},
                                                 TRANSFORM_OT_translate={"value":(0, 0, z - 4), "orient_type":'NORMAL',
                                                                         "orient_matrix":((0, 1, 0), (-1, 0, 0), (0, 0, 1)),
                                                                         "orient_matrix_type":'NORMAL', "constraint_axis":(False, False, True),
                                                                         "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH',
                                                                         "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False,
                                                                         "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0),
                                                                         "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False,
                                                                         "release_confirm":False, "use_accurate":False})
                bpy.ops.mesh.inset(thickness=0.1, depth=0)
                bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False},
                                                TRANSFORM_OT_translate={"value":(0, 0, -0.25), "orient_type":'NORMAL',
                                                                        "orient_matrix":((0, 1, 0), (-1, 0, 0), (0, 0, 1)),
                                                                        "orient_matrix_type":'NORMAL', "constraint_axis":(False, False, True),
                                                                        "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH',
                                                                        "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False,
                                                                        "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0),
                                                                        "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False,
                                                                        "release_confirm":False, "use_accurate":False})
            elif z >= 9: # extrude down
                bpy.ops.mesh.inset(thickness=0.1, depth=0)
                bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False},
                                                TRANSFORM_OT_translate={"value":(0, 0, -0.25), "orient_type":'NORMAL',
                                                                        "orient_matrix":((0, 1, 0), (-1, 0, 0), (0, 0, 1)),
                                                                        "orient_matrix_type":'NORMAL', "constraint_axis":(False, False, True),
                                                                        "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH',
                                                                        "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False,
                                                                        "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0),
                                                                        "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False,
                                                                        "release_confirm":False, "use_accurate":False})
            elif z == 7: # extrude up
                bpy.ops.mesh.inset(thickness=0.4, depth=0)
                bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False},
                                                 TRANSFORM_OT_translate={"value":(0, 0, z/2), "orient_type":'NORMAL',
                                                                         "orient_matrix":((0, 1, 0), (-1, 0, 0), (0, 0, 1)),
                                                                         "orient_matrix_type":'NORMAL', "constraint_axis":(False, False, True),
                                                                         "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH',
                                                                         "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False,
                                                                         "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0),
                                                                         "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False,
                                                                         "release_confirm":False, "use_accurate":False})
                bpy.ops.mesh.inset(thickness=0.1, depth=0)
                bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False},
                                                TRANSFORM_OT_translate={"value":(0, 0, -0.15), "orient_type":'NORMAL',
                                                                        "orient_matrix":((0, 1, 0), (-1, 0, 0), (0, 0, 1)),
                                                                        "orient_matrix_type":'NORMAL', "constraint_axis":(False, False, True),
                                                                        "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH',
                                                                        "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False,
                                                                        "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0),
                                                                        "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False,
                                                                        "release_confirm":False, "use_accurate":False})

            elif z >= 4: # extrude down
                bpy.ops.mesh.inset(thickness=0.07, depth=0)
                bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False},
                                                TRANSFORM_OT_translate={"value":(0, 0, -0.10), "orient_type":'NORMAL',
                                                                        "orient_matrix":((0, 1, 0), (-1, 0, 0), (0, 0, 1)),
                                                                        "orient_matrix_type":'NORMAL', "constraint_axis":(False, False, True),
                                                                        "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH',
                                                                        "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False,
                                                                        "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0),
                                                                        "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False,
                                                                        "release_confirm":False, "use_accurate":False})
            else: # extrude down
                bpy.ops.mesh.inset(thickness=0.03, depth=0)
                bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False},
                                                TRANSFORM_OT_translate={"value":(0, 0, -0.5), "orient_type":'NORMAL',
                                                                        "orient_matrix":((0, 1, 0), (-1, 0, 0), (0, 0, 1)),
                                                                        "orient_matrix_type":'NORMAL', "constraint_axis":(False, False, True),
                                                                        "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH',
                                                                        "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False,
                                                                        "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0),
                                                                        "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False,
                                                                        "release_confirm":False, "use_accurate":False})

            bpy.ops.object.editmode_toggle() # Exit Edit Mode
            
            size_x = round(uniform(.1, .3), 2) # the 2 is the decimal number to return for 'round'
            size_y = round(uniform(.1, .3), 2)
            size_z = z
            if z >= support_pillar: # if buildings are a certain length than it will have support structures
                ## Building Support FRONT ##
                for idx, _ in enumerate(range(x*2 + 1)):
                    # structure_x = round(uniform(-.8, .8), 2)
                    # structure_y = round(uniform(-.8, .8), 2)
                    structure_x = x
                    structure_y = y

                    bpy.ops.mesh.primitive_cube_add(size=2) # make CUBE

                    bpy.ops.object.editmode_toggle() # Enter Edit Modeax
                    bpy.ops.transform.translate(value=(0, 0, 1)) # Raise to X floor set origin point on the bottom
                    bpy.ops.object.editmode_toggle() # Exit Edit Mode
                    
                    if user_y == True:
                        if side == 'Left':
                            bpy.ops.transform.translate(value=(x_location - x, y, .15)) # move CUBE to building
                        if side == 'Right':
                            bpy.ops.transform.translate(value=(x_location - x, -y, .15)) # move CUBE to building
                    else:
                        bpy.ops.transform.translate(value=(x_location - x, 0, .15)) # move CUBE to building
                    
                    bpy.ops.transform.resize(value=(size_x, size_y, size_z)) # random resize
                    
                    structure_x += idx
                    bpy.ops.transform.translate(value=(structure_x, structure_y, -0.15)) # random move CUBE x, y
                ## Building Support SIDE ##
                for idx, _ in enumerate(range(y*2+ 1)):
                    # structure_x = round(uniform(-.8, .8), 2)
                    # structure_y = round(uniform(-.8, .8), 2)
                    structure_x = x
                    structure_y = y

                    bpy.ops.mesh.primitive_cube_add(size=2) # make CUBE

                    bpy.ops.object.editmode_toggle() # Enter Edit Modeax
                    bpy.ops.transform.translate(value=(0, 0, 1)) # Raise to X floor set origin point on the bottom
                    bpy.ops.object.editmode_toggle() # Exit Edit Mode
                    
                    if user_y == True:
                        if side == 'Left':
                            bpy.ops.transform.translate(value=(x_location - x, -y, .15)) # move CUBE to building
                        if side == 'Right':
                            bpy.ops.transform.translate(value=(x_location - x, -y*3, .15)) # move CUBE to building
                    else:
                        bpy.ops.transform.translate(value=(x_location - x, -y*2, .15)) # move CUBE to building
                    
                    bpy.ops.transform.resize(value=(size_x, size_y, size_z)) # random resize
                    
                    structure_y += idx
                    bpy.ops.transform.translate(value=(structure_x, structure_y, -0.15)) # random move CUBE x, y
                ## Building Support OTHER SIDE ##
                for idx, _ in enumerate(range(y*2 + 1)):
                    # structure_x = round(uniform(-.8, .8), 2)
                    # structure_y = round(uniform(-.8, .8), 2)
                    structure_x = x
                    structure_y = y

                    bpy.ops.mesh.primitive_cube_add(size=2) # make CUBE

                    bpy.ops.object.editmode_toggle() # Enter Edit Modeax
                    bpy.ops.transform.translate(value=(0, 0, 1)) # Raise to X floor set origin point on the bottom
                    bpy.ops.object.editmode_toggle() # Exit Edit Mode
                    
                    if user_y == True:
                        if side == 'Left':
                            bpy.ops.transform.translate(value=(x_location + x, -y, .15)) # move CUBE to building
                        if side == 'Right':
                            bpy.ops.transform.translate(value=(x_location + x, -y*3, .15)) # move CUBE to building
                    else:
                        bpy.ops.transform.translate(value=(x_location + x, -y*2, .15)) # move CUBE to building
                    
                    bpy.ops.transform.resize(value=(size_x, size_y, size_z)) # random resize
                    
                    structure_y += idx
                    bpy.ops.transform.translate(value=(structure_x, structure_y, -0.15)) # random move CUBE x, y
                ## Building Support BACK ##
                for idx, _ in enumerate(range(x*2 + 1)):
                    # structure_x = round(uniform(-.8, .8), 2)
                    # structure_y = round(uniform(-.8, .8), 2)
                    structure_x = x
                    structure_y = y
                    bpy.ops.mesh.primitive_cube_add(size=2) # make CUBE

                    bpy.ops.object.editmode_toggle() # Enter Edit Modeax
                    bpy.ops.transform.translate(value=(0, 0, 1)) # Raise to X floor set origin point on the bottom
                    bpy.ops.object.editmode_toggle() # Exit Edit Mode
                    
                    if user_y == True:
                        if side == 'Left':
                            bpy.ops.transform.translate(value=(x_location - x, -y, .15)) # move CUBE to building
                        if side == 'Right':
                            bpy.ops.transform.translate(value=(x_location - x, -y*3, .15)) # move CUBE to building
                    else:
                        bpy.ops.transform.translate(value=(x_location - x, -y*2, .15)) # move CUBE to building
                    
                    bpy.ops.transform.resize(value=(size_x, size_y, size_z)) # random resize
                    
                    structure_x += idx
                    bpy.ops.transform.translate(value=(structure_x, structure_y, -0.15)) # random move CUBE x, y
            # Building Roof Structures
            for _ in range(num_of_structures):
                value_x = round(uniform(-.8, .8), 2)
                value_y = round(uniform(-.8, .8), 2)
                
                size_x = round(uniform(.1, .2), 2)
                size_y = round(uniform(.1, .2), 2)
                size_z = round(uniform(.01, .15), 2)
                
                bpy.ops.mesh.primitive_cube_add(size=2) # make CUBE

                bpy.ops.object.editmode_toggle() # Enter Edit Mode
                bpy.ops.transform.translate(value=(0, 0, 1)) # Raise to X floor set origin point on the bottom
                bpy.ops.object.editmode_toggle() # Exit Edit Mode

                if z >= 15:
                    if user_y == True:
                        if side == 'Left':
                            bpy.ops.transform.translate(value=(x_location + x, y, z*3 - 4)) # move CUBE to building
                            bpy.ops.transform.resize(value=(size_x, size_y, size_z)) # random resize
                            bpy.ops.transform.translate(value=(round(value_x/2, 2), round(value_y/2, 2), -0.15)) # random move CUBE x, y
                        if side == 'Right':
                            bpy.ops.transform.translate(value=(x_location + x, -y, z*3 - 4)) # move CUBE to building
                            bpy.ops.transform.resize(value=(size_x, size_y, size_z)) # random resize
                            bpy.ops.transform.translate(value=(round(value_x/2, 2), round(value_y/2, 2), -0.15)) # random move CUBE x, y
                    else:
                        bpy.ops.transform.translate(value=(x_location + x, 0, z*3 - 4)) # move CUBE to building
                        bpy.ops.transform.resize(value=(size_x, size_y, size_z)) # random resize
                        bpy.ops.transform.translate(value=(value_x, value_y, -0.15)) # random move CUBE x, y
                elif z == 7: # extrude up
                    if user_y == True:
                        if side == 'Left':
                            bpy.ops.transform.translate(value=(x_location + x, y, z*2 + z/2)) # move CUBE to building
                            bpy.ops.transform.resize(value=(size_x, size_y, size_z)) # random resize
                            bpy.ops.transform.translate(value=(round(value_x/2, 2), round(value_y/2, 2), -0.15)) # random move CUBE x, y
                        if side == 'Right':
                            bpy.ops.transform.translate(value=(x_location + x, -y, z*2 + z/2)) # move CUBE to building
                            bpy.ops.transform.resize(value=(size_x, size_y, size_z)) # random resize
                            bpy.ops.transform.translate(value=(round(value_x/2, 2), round(value_y/2, 2), -0.15)) # random move CUBE x, y
                    else:
                        bpy.ops.transform.translate(value=(x_location + x, 0, z*2 + z/2)) # move CUBE to building
                        bpy.ops.transform.resize(value=(size_x, size_y, size_z)) # random resize
                        bpy.ops.transform.translate(value=(round(value_x/2, 2), round(value_y/2, 2), -0.15)) # random move CUBE x, y
                else:
                    if user_y == True:
                        if side == 'Left':
                            bpy.ops.transform.translate(value=(x_location + x, y, z*2)) # move CUBE to building
                            bpy.ops.transform.resize(value=(size_x, size_y, size_z)) # random resize
                            bpy.ops.transform.translate(value=(value_x, value_y, -0.15)) # random move CUBE x, y
                        if side == 'Right':
                            bpy.ops.transform.translate(value=(x_location + x, -y, z*2)) # move CUBE to building
                            bpy.ops.transform.resize(value=(size_x, size_y, size_z)) # random resize
                            bpy.ops.transform.translate(value=(value_x, value_y, -0.15)) # random move CUBE x, y
                    else:
                        bpy.ops.transform.translate(value=(x_location + x, 0, z*2)) # move CUBE to building
                        bpy.ops.transform.resize(value=(size_x, size_y, size_z)) # random resize
                        bpy.ops.transform.translate(value=(value_x, value_y, -0.15)) # random move CUBE x, y

                #bpy.ops.object.add_named(linked=False, name=f"structure{str(s_order)}")
            
            # select all MESH objs and JOINS them
            bpy.ops.object.select_by_type(extend=False, type='MESH')
            bpy.ops.object.join()

            new_collection.objects.link(bpy.context.object) # adding building obj to new collection
            current_collections.objects.unlink(bpy.context.object) # unlinking building obj from current collection
            
            for obj in bpy.context.selected_objects: # rename objs
                obj.name = f'Building_{file_number}'
            
            bpy.ops.object.hide_view_set(unselected=False) # hide all
            
        bpy.ops.object.hide_view_clear() # UNHIDE all
        bpy.ops.object.select_all(action='DESELECT') # deselect all
            
        return {'FINISHED'} # or {'CAANCELED'}


class VIEW3D_PT_city(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "BLENDER CITY"
    bl_label = "Blender City Builder"

    def draw(self, context):
        """draw something on screen"""
        layout = self.layout
        col = layout.column(align=True)

        buildings = col.operator('mesh.city',
                        text='Building Generator',
                        icon='CON_SAMEVOL',)
        # buildings.num_buildings = 1
        # buildings.num_roof_structures = 1
        # buildings.max_height = 4



def mesh_add_menu_draw(self, context):
    self.layout.operator('mesh.city',
                        icon='SNAP_VOLUME')   

def register():
    bpy.utils.register_class(MESH_OT_city)
    bpy.utils.register_class(VIEW3D_PT_city)
    bpy.types.VIEW3D_MT_mesh_add.append(mesh_add_menu_draw)

def unregister():
    bpy.utils.register_class(MESH_OT_city)
    bpy.utils.register_class(VIEW3D_PT_city)
    bpy.types.VIEW3D_MT_mesh_add.remove(mesh_add_menu_draw)


if __name__ == "__main__":
    register()


'''Complex Building

bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

bpy.ops.transform.resize(value=(4, 1, 1))

obj = bpy.context.active_object
bpy.ops.object.editmode_toggle()
bpy.ops.mesh.select_all(action='DESELECT')
bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
bpy.ops.object.editmode_toggle()
obj.data.polygons[3].select = True
bpy.ops.object.editmode_toggle()

'''