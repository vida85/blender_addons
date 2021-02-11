import bpy
import bmesh
import random
from mathutils import Vector

from .buildings.Business import business, business_towers
from .buildings.Apartment import apartment
from .buildings.Skyscrapers import skyscraper, skyscraper_towers
from .buildings.Office import office, office_2

from .tools.blender_tools import dup, de_select

ground_material   = set()
roof_material     = set()
building_material = set()
GROUND, ROOF, BUILDING, PILLARS, COLUMNS, WINDOWS, FIRESCAPE = 'Ground', 'Roof', 'Building', 'Pillars', 'Columns', 'Windows', 'firescape'

def grid(x_location, y_location, current_coll, new_coll):  
    grid_list = []
    obj_info = {}
    funcs = []

    ####--Rotation values
    rotation_90 = 1.570796
    rotation_180 = 3.141593

    scene = bpy.context.scene
    tool  = scene.tools
    
    ####--Random Memory
    # random.seed(tool.random_memory)
    ####--OBJ
    obj = bpy.ops.object

    ####-----Populate list with user BOOL choice
    if tool.business_building:
        funcs.append(business)
    if tool.apartment_building:
        funcs.append(apartment)
    if tool.office_building:
        funcs.append(office)
        funcs.append(office_2)
    if tool.skyscraper_building:
        funcs.append(skyscraper)
    
    bpy.context.scene.cursor.location = (0, 0, 0)
    bpy.context.scene.cursor.rotation_euler = (0, 0, 0)

    for ob in bpy.context.selectable_objects:
        ob.hide_set(True)

    ####--Call Functions to Run Script
    ####--------------------------------------------
    ####-- Create buildings ------------------------
    for count in range(x_location * y_location):
        call = random.choice(funcs)

        if 'apartment' in str(call):
            call(tool.apartment_floors, current_coll, new_coll)
        elif 'office' in str(call):
            call(tool.office_floors, current_coll, new_coll)
        elif 'skyscraper' in str(call):
            call(tool.skyscraper_floors, current_coll, new_coll)
        elif 'business' in str(call):
            call(tool.business_floors, current_coll, new_coll)

        print()
        print(f"Building {bpy.context.object.name_full}: {count+1} out of {x_location * y_location}")
        print()

        obj = bpy.context.object
        new_coll.objects.link(obj) # adding building obj to new collection
        current_coll.objects.unlink(obj) # unlinking building obj from current collection
        
        bpy.ops.object.hide_view_set(unselected=False) # hide object

    tool.counter = f"{count+1} / {x_location * y_location}"

    bpy.ops.object.hide_view_clear() # unhide everything

    skyscraper_towers(new_coll) # add second tower ONLY to selective skyscrappers
    # business_towers(new_coll) # add second tower ONLY to selective skyscrappers

########################################################################
########################################################################
########################################################################
########################################################################
    ###--variable locations
    current_x = -tool.density
    current_cell = Vector((0,0,0))
    for _ in range(x_location):
        #
        current_x += tool.density
        current_cell[1] = 0
        #
        for _ in range(y_location):
            #
            current_cell = Vector((current_x, current_cell[1] + tool.density, 0))
            storeCell = random.randint(0,1)
            if tool.random_placement:
                if storeCell == 1:
                    grid_list.append(Vector((current_cell[0],current_cell[1],current_cell[2])))
            else:
                grid_list.append(Vector((current_cell[0],current_cell[1],current_cell[2])))
    
    ###---Move objects to locations:
    for idx, obj in enumerate(new_coll.objects):
        try:
            obj.location = grid_list[idx]
            obj_info[obj.name_full] = [obj.location, obj.scale, obj.dimensions, obj.name_full]
        except IndexError:
            obj.select_set(True)
            bpy.ops.object.delete()

        ###---Rotating the new object:
        if tool.rotation_variation:
            r = random.randint(0,2)
            if r == 1:
                choice = random.randint(0,3)
                try:
                    if choice == 0:
                        #-- 90+
                        current_euler = obj.rotation_euler
                        current_euler[2] += rotation_90
                        obj.rotation_euler = current_euler
                    if choice == 1:
                        #-- 90-
                        current_euler = obj.rotation_euler
                        current_euler[2] -= rotation_90
                        obj.rotation_euler = current_euler
                    if choice == 2:
                        #-- 180
                        current_euler = obj.rotation_euler
                        current_euler[2] += rotation_180
                        obj.rotation_euler = current_euler
                except ReferenceError:
                    print('StructRNA of type Obj has been removed...')
    
    # ###---Move objects to locations:
    # ###---obj_info[obj.name_full] = [obj.location, obj.scale, obj.dimensions]
    # for _, value_lst in obj_info.items():
    #     de_select(False, 'Object')
    #     rooftop_structures(value_lst[-1])
    #     obj = bpy.context.object
    #     try:
    #         if 'business' in obj.name_full.lower():
    #             obj.location = value_lst[0][0], value_lst[0][1], value_lst[2][2] - 1
    #         else:
    #             obj.location = value_lst[0][0], value_lst[0][1], value_lst[2][2]
    #     except IndexError:
    #         obj.select_set(True)
    #         bpy.ops.object.delete()

    obj_info = {}
    grid_list = []
    ###------------------------------------
    ###--Select only newly created objs
    bpy.ops.object.select_all(action='DESELECT')
    for ob in list(bpy.data.collections[new_coll.name_full].objects):
        ob.select_set(True)
