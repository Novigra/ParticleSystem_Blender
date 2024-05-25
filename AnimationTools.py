import bpy
import math
from bpy.types import (Panel,Operator)
from bpy.utils import register_class, unregister_class

bl_info = {
    "name": "AnimationTools",
    "author": "Mohammed Kenawy - 20102181",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > N",
    "description": "Help you animating",
    "warning": "",
    "doc_url": "",
    "category": "Add particle effects to a bouncing objects",
}

# Global Variables
# The object that we want to trace
Ball = None

# Number of Particles
Particles = 4

# Proportional Relationship between the object (ball) and the particles
Propo = 0.5

class ManageParticleSystem:
    
    def CalculateParticleFrames():
        global Ball
        # Get the Z axis component of the object animation
        if Ball:
            
            #print("test3....")
            # Stores the frames details of when the object "hits" the ground (Z component of a location = 0)
            Impact= []

            # Stores the frames details of when the object reaches the highest point (Apex level Z component location)
            Apex= []
            
            Curve = Ball.animation_data.action.fcurves
            ZCurve = next(
                        fcurve
                        for fcurve
                        in Curve
                        if fcurve.data_path == "location" and fcurve.array_index == 2
                        )
            Keyframes = ZCurve.keyframe_points
                
            # Get the apex (highest point on the Z axis component)
            PreviousApex = 0
            Threshold = 0.1
                
                
            for i in range(0, len(Keyframes) - 1):
                PreviousZComponent = Keyframes[i - 1].co[1]
                CurrentZComponent = Keyframes[i].co[1]
                NextZComponent = Keyframes[i + 1].co[1]
                    
                if CurrentZComponent > PreviousZComponent and CurrentZComponent > NextZComponent:
                    PreviousApex = CurrentZComponent
                        
                    # Set the impact (Z close to zero and put threshold in case if the target is missed) and apex frames
                if abs(CurrentZComponent) < Threshold:
                    Impact.append(Keyframes[i].co[0])
                    Apex.append(PreviousApex)
                    
                print(Impact)
                
            return Impact, Apex
                    
        else:
            print("Ball is null")               
            
    
    def SpawnParticle(Impact, Apex):
        # Setting frames for the particles (using zip "parallel execution" for convenience)
        for Frame, ApexHeight in zip(Impact, Apex):
            bpy.context.scene.frame_set(int(Frame))
            
            # Create Particle (planes for performance and easy to control)
            for i in range(Particles):
                bpy.ops.mesh.primitive_plane_add(size=1, location=(0,0,0))
                
                # I can just assign it, but it would lead to weird behaviour
                Plane = bpy.context.object
                
                # Setup Textures
                ManageParticleSystem.SetupTextures(Plane)
                
                #InitialInterpolation = (0,0,0)
                #InitialSpawnLocation = (0,0,0)
                
                BallLocation = Ball.matrix_world.translation
                InitialSpawnLocation = (
                                    BallLocation.x,
                                    BallLocation.y,
                                    0)
                                    
                Plane.location = InitialSpawnLocation
                Plane.keyframe_insert(data_path="location", frame=Frame)
                
                # Calcualte the highest (apex) so the object goes up and then down after reaching the apex 
                MidPoint = Frame + 5
                Distance = ApexHeight * Propo
                Angle = i * (2 * math.pi / Particles)
                MidDestinationLocation = (
                                    Distance * math.cos(Angle) / 2 + BallLocation.x,
                                    Distance * math.sin(Angle) / 2 + BallLocation.y,
                                    ApexHeight / 2)
                                    
                bpy.context.scene.frame_set(int(MidPoint))
                Plane.location = MidDestinationLocation
                Plane.keyframe_insert(data_path="location", frame=MidPoint)
                
                # Calculate the destination between the starting point to the end point
                DestinationPoint = Frame + 10
                DestinationLocation = (
                                Distance * math.cos(Angle) + BallLocation.x,
                                Distance * math.sin(Angle) + BallLocation.y,
                                0)
                                
                bpy.context.scene.frame_set(int(DestinationPoint))
                Plane.location = DestinationLocation
                Plane.keyframe_insert(data_path="location", frame=DestinationPoint)
                
                # Rotate the particles to the camera
                ManageParticleSystem.CameraRotation(Plane)
    
    
    def SetupTextures(obj):
        Material = bpy.data.materials.get("PlaneMat")
        
        if Material and obj.data.materials:
            obj.data.materials[0] = Material
        else:
            obj.data.materials.append(Material)
    
                
    # Rotate Planes to Camera            
    def CameraRotation(obj):
        Camera = bpy.context.scene.camera
        if Camera:
            CameraLocation = Camera.matrix_world.translation
            Direction = CameraLocation - obj.location
            Direction.normalize()
            
            if Direction.length_squared > 0.0:
                RotationMatrix = Direction.to_track_quat('Z', 'Y').to_matrix().to_4x4()
                obj.matrix_world = RotationMatrix
        
    
'''
class MyTest():
    @staticmethod
    def TestText():
        print("YESYESYES!!!")
'''

# Selecting any mesh (object)
class SelectorMeshOperator(bpy.types.Operator):
    bl_idname = "select.selector"
    bl_label = "Selecting Highlighted Object"
    
    def execute(self, context):
        global Ball
        
        SelectedObject = bpy.context.scene.objects.get(context.scene.selected_object_name)
        if SelectedObject:
            Ball = SelectedObject
            self.report({'INFO'}, f"Variable Set To {Ball.name}")
        else:
            self.report({'WARNING'}, "No Selected Objects")
        return {'FINISHED'}

# Execute spawn particles
class ButtonParticleOperator(bpy.types.Operator):
    bl_idname = "animate.button"
    bl_label = "Animation Object Operator"

    def execute(self, context):
        Impact, Apex= ManageParticleSystem.CalculateParticleFrames()
        
        if Impact and Apex:
            ManageParticleSystem.SpawnParticle(Impact, Apex)
        else:
            print("Impact Is Empty")
        return {'FINISHED'}

# Execute removing particles    
class ButtonRemoveParticlesOperator(bpy.types.Operator):
    bl_idname = "remove.button"
    bl_label = "Remove Particle Operator"
    
    def execute(self, context):
        # Get every object
        Objects = bpy.context.scene.objects
        
        # Get only the planes
        Planes = [
                obj
                for obj in Objects
                if obj.type == 'MESH' and obj.name.startswith("Plane")]
        
        for i in Planes:
            # Unlink is set to true as if you reloaded the scene, objects come back
            bpy.data.objects.remove(i, do_unlink=True)
            
        return {'FINISHED'}

# Handle Panel UI
class AnimationPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Animation Tools"
    bl_idname = "OBJECT_PT_AnimationTools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Animation Tools"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        
        row = layout.row()
        row.label(text="Select an object:")
        row.prop(scene, "selected_object_name", text="")
        row.operator(SelectorMeshOperator.bl_idname, text="Set Object")
        
        row = layout.row()
        row.label(text="Particle System", icon='WORLD_DATA')
        row.operator(ButtonParticleOperator.bl_idname, text="Spawn Particles")
        
        row = layout.row()
        row.label(text="Remove Particles", icon='PANEL_CLOSE')
        row.operator(ButtonRemoveParticlesOperator.bl_idname, text="Remove")


classes = [SelectorMeshOperator, ButtonParticleOperator, ButtonRemoveParticlesOperator, AnimationPanel]

def register():
    bpy.types.Scene.selected_object_name = bpy.props.EnumProperty(
        items=[(obj.name, obj.name, '') for obj in bpy.context.scene.objects if obj.type == 'MESH'],
        name="Select a mesh"
    )
    bpy.types.Scene.selected_object_variable = bpy.props.PointerProperty(type=bpy.types.Object)
    for i in classes:
        register_class(i)


def unregister():
    del bpy.types.Scene.selected_object_name
    del bpy.types.Scene.selected_object_variable
    
    for i in classes:
        unregister_class(i)    


if __name__ == "__main__":
    register()