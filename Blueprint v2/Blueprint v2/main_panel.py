import bpy

class OBJECT_PT_Blueprint(bpy.types.Panel):
    bl_label       = "Blueprint"
    bl_idname      = "OBJECT_PT_blueprint"
    
    bl_space_type  = "VIEW_3D"
    bl_region_type = "UI"
    bl_category    = "Blueprint"

    def draw(self, context):
        layout = self.layout
        tool = context.scene.tools

        row = layout.row()
        box = row.box()

        box.label(text='Select Buildings')
        if tool.apartment_building:
            box.prop(tool, "apartment_building", icon='CHECKBOX_HLT')
            box.prop(tool, "apartment_floors", icon='CHECKBOX_HLT')
        else:
            box.prop(tool, "apartment_building", icon='CHECKBOX_DEHLT')

        if tool.office_building:
            box.prop(tool, "office_building", icon='CHECKBOX_HLT')
            box.prop(tool, "office_floors", icon='CHECKBOX_HLT')
        else:
            box.prop(tool, "office_building", icon='CHECKBOX_DEHLT')

        if tool.business_building:
            box.prop(tool, "business_building", icon='CHECKBOX_HLT')
            box.prop(tool, "business_floors", icon='CHECKBOX_HLT')
        else:
            box.prop(tool, "business_building", icon='CHECKBOX_DEHLT')

        if tool.skyscraper_building:
            box.prop(tool, "skyscraper_building", icon='CHECKBOX_HLT')
            box.prop(tool, "skyscraper_floors", icon='CHECKBOX_HLT')
        else:
            box.prop(tool, "skyscraper_building", icon='CHECKBOX_DEHLT')

        layout.separator()
        layout.use_property_split = True

        col = layout.column(align=True)
        box = col.box()
        box.label(text='Random Location Options', icon='LIGHTPROBE_GRID')
        box.prop(tool, "random_placement", icon='SNAP_GRID')
        box.prop(tool, "rotation_variation", icon='DRIVER_ROTATIONAL_DIFFERENCE')
        
        layout.separator()

        col = layout.column(align=True)  
        col.label(text='Grid Properties', icon='SNAP_GRID')
        col.prop(tool, "x_location", icon='AXIS_SIDE')
        col.prop(tool, "y_location", icon='AXIS_FRONT')
        
        col = layout.column()
        col.prop(tool, "density", icon='GROUP_VERTEX')

        layout.separator()
        
        col = layout.column()
        box = col.box()
        # box.prop(tool, "random_memory", icon='MEMORY')
        box.scale_y = 1.5
        box.operator("mesh.blueprint", text='Build'.upper(), icon='MOD_BUILD')
        row = layout.row()
        row.prop(tool, "counter")