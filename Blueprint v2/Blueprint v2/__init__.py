bl_info = {
    "name": "Blueprint",
    "author": "Davi Silveira <vidasilveira85@gmail.com>",
    "version": (1, 0, 8),
    "blender": (2, 90, 1),
    "category": "Add Mesh",
    "location": "VIEW3D > BLueprint > UI",
    "description": "We Built This City",
    "warning": "Still under development",
    "doc_url": "",
    "tracker_url": "",
}

import bpy

from . main_operator import VIEW3D_OT_Blueprint
from . main_panel import OBJECT_PT_Blueprint
from . main_properties import Blueprint_Properties

classes = (
    OBJECT_PT_Blueprint,
    VIEW3D_OT_Blueprint,
    Blueprint_Properties,
    )

#### -----------------------------------------
#### Register Classes
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.tools = bpy.props.PointerProperty(type=Blueprint_Properties)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.tools
#### -----------------------------------------