import bpy

from bpy.props import IntProperty, StringProperty, BoolProperty, FloatProperty

class Blueprint_Properties(bpy.types.PropertyGroup):
    counter: StringProperty(
        name= "Building",
        default= "0/0", 
    )

    density: IntProperty(
        name = "Density",
        description = "How far apart building are to each other",
        default = 30,
        min = 1,
        max = 100
    )

####---------------------------------------------------
####---Buildings
    apartment_building: BoolProperty(
        name = "Apartment Buildings",
        description = "Variety of Apartment Complexes",
        default = True
    )

    office_building: BoolProperty(
        name = "Office Buildings",
        description = "Variety of Office Buildings",
        default = True
    )

    business_building: BoolProperty(
        name = "Business Buildings",
        description = "Variety of Business Buildings",
        default = True
    )
    
    skyscraper_building: BoolProperty(
        name = "Skyscraper Buildings",
        description = "Variety of Skyscrapers",
        default = False
    ) 
####---------------------------------------------------

####---------------------------------------------------
####---Buildings Floors
    apartment_floors: IntProperty(
        name = "Maximum Floors",
        description = "How many floors per Apartment",
        default = 14,
        min = 3,
        max = 100
    )

    office_floors: IntProperty(
        name = "Maximum Floors",
        description = "How many floors per Office Building",
        default = 25,
        min = 5,
        max = 100
    )

    skyscraper_floors: IntProperty(
        name = "Maximum Floors",
        description = "How many floors per Skyscraper",
        default = 53,
        min = 30,
        max = 100
    )

    business_floors: IntProperty(
        name = "Maximum Floors",
        description = "How many floors per Business",
        default = 30,
        min = 10,
        max = 100
    )
####---------------------------------------------------

    random_placement: BoolProperty(
        name = "Placement",
        description = "Randomize whether a building will be placed",
        default = False
    )

    rotation_variation: BoolProperty(
        name = "Rotation",
        description = "Allow variation in the rotation of objects",
        default = False
    )

    x_location: IntProperty(
        name= "X Location",
        description="Number of buildings to build in X axis",
        default=4, min=1, soft_max=10, max=20
    )

    y_location: IntProperty(
        name= "Y Location",
        description="Number of buildings to build in X axis",
        default=4, min=1, soft_max=10, max=20
    )

    # random_memory: IntProperty(
    #     name = "Random Memory",
    #     description = "Random Versions",
    #     default = 1,
    #     min = 1,
    #     max = 100
    # )