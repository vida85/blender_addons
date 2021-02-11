import bpy

from .tools.blender_tools import move_it, re_size, hide, de_select, dimension
from . grid_main import grid
from . main_properties import Blueprint_Properties
from bpy.props import IntProperty, StringProperty, BoolProperty, FloatProperty
class VIEW3D_OT_Blueprint(bpy.types.Operator):
    """Blueprint we built this city"""
    bl_label    = "Building Options".upper()
    bl_idname   = "mesh.blueprint"
    bl_category = "View"
    bl_context  = "objectmode"
    bl_options  = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ####--Pre Start
        de_select(True, 'OBJECT') # Select All Objs
        hide(True)
        # deactivate others
        for obj in bpy.data.objects:
            if obj.select_get() is True:
                obj.select_set(False)

        current_coll = bpy.context.collection # list of all collections
        new_coll = bpy.data.collections.new('Buildings') # new collection
        bpy.context.scene.collection.children.link(new_coll) # show in OUTLINER
        ####-----------------------------------------------------

        ####--Call Functions to Run Script
        tool = context.scene.tools
        
        # bpy.context.scene.tool_settings.use_snap = True
        grid(tool.x_location, tool.y_location, current_coll, new_coll)
        ####-----------------------------------------------------
        
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        tool = context.scene.tools

        row = layout.row()
        box = row.box()

        box.label(text='The Grid Blueprint', icon='LIGHTPROBE_GRID')
        
        layout.separator()

        col = layout.column(align=True)
        box = col.box()
        box.prop(tool, "density", icon='GROUP_VERTEX')
        
        box.label(text='Random Location Options')
        box.prop(tool, "random_placement", icon='SNAP_GRID')
        box.prop(tool, "rotation_variation", icon='DRIVER_ROTATIONAL_DIFFERENCE')
        
        col = layout.column(align=True)  
        col.label(text='Grid Properties', icon='SNAP_GRID')
        col.prop(tool, "x_location", icon='AXIS_SIDE')
        col.prop(tool, "y_location", icon='AXIS_FRONT')

        col = layout.column()
        box = col.box()
        box.prop(tool, "random_memory", icon='MEMORY')
        box.prop(tool, "counter")