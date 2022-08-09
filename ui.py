bl_info = {
    "name": "Raytracing Vehicle",
    "author": "meeww",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "3D Viewport > Scene > Raytracing AI",
    "description": "Adds a raytracing ai.",
    "warning": "",
    "doc_url": "",
    "category": "Add Raytracing AI",
}
import bpy
import math


class Globals():
    running = 0;
    stopping = 0;
    debug = 0;
class Properties(bpy.types.PropertyGroup):
    max_speed :  bpy.props.FloatProperty(default = 1,name = "Max Speed",soft_min = 0, soft_max = 90);   
    max_acceleration :  bpy.props.FloatProperty(default = 1,name = "Max Acceleration",soft_min = 0, soft_max = 90); 
    steering_force : bpy.props.FloatProperty(default = 1,name = "Steering Force",soft_min = 0, soft_max = 1);    

def runButton(context,mytool):
    C = bpy.context 
    
                       # custom property from Object "RUN PROGRAM"
    def runProgram(scene):
        running = Globals.running
        stopping = Globals.stopping;
        if running or stopping:                                                    # run program if custom property run = 1

            rayCollection = bpy.data.collections['Controllers'];        #raycast controller object
            
            for colls in rayCollection.children:                        #run for every car
                
                for obj in colls.children:   
                    
                    if 'Car Constraints' in obj.name:                   #locate constraints collection
                        
                        for constraints in obj.children:
                            
                            if 'Motors' in constraints.name:            #locate motors collection
                                for motors in constraints.objects:
                                    if 'SteeringMotor' in motors.name:
                                        steering = motors;              #get motor constraints
                                    if 'FL_Motor' in motors.name:
                                        motorFL = motors;
                                    if 'FR_Motor' in motors.name:
                                        motorFR = motors;   
                                    if 'RL_Motor' in motors.name:
                                        motorRL = motors;
                                    if 'RR_Motor' in motors.name:
                                        motorRR = motors;      
                                    
                for obj in colls.objects:                             
                    if 'raycast_Controller' in obj.name:
                        memoryObject = C.view_layer.objects.active      #depsgraph requires setting an object to active
                        C.view_layer.objects.active = obj;              #so we save the current selected object to memory 
                                                                        #so that we can reset it back afterwards.
                        
                        deps = obj.evaluated_get(C.evaluated_depsgraph_get())  #depsgraph gets the active object's custom properties
                        detector = deps.data                                   #save data to variable
                        
                        C.view_layer.objects.active = memoryObject;     #reset active selected object
                        
                        
                        #get sensor values
                        hitL= detector.attributes['hit_L'].data[0].value   #retieve each custom property by name
                        hitR= detector.attributes['hit_R'].data[0].value   #geometry nodes adds custom properties to all vertices,
                        hitF= detector.attributes['hit_F'].data[0].value   #but we only need it once so we select the 0th vertex
                        hitD= detector.attributes['hit_D'].data[0].value   #and take it's properties. It's inefficient but it works.
                        velocity= detector.attributes['velocity'].data[0].value
                        steeringForce = detector.attributes['steeringForce'].data[0].value
                        isRigid= detector.attributes['isRigidBody'].data[0].value
                        
                        
                        if hitL == 0: # prevent infinite length rays being counted as hit at 0
                            hitL = 250;
                        if hitR == 0:
                            hitR = 250;
                        if hitF ==0:
                            hitF = 250;
                        if hitD == 0:
                            hitD = 250;
                            
                        if Globals.debug ==1:      #print raycast info if "RUN PROGRAM"'s custom
                            print(obj.name + " -")
                            print("    Left raycast is : " + str(hitL))                   #property "debug" is equal to 1.
                            print("    Right raycast is : " + str(hitR))
                            print("    Front raycast is : " + str(hitF))
                            print("    Down raycast is : " + str(hitD))
                            print(" ") 
                        print(isRigid);
                        if isRigid == 0:
                            if running ==1:
                                print((2/(hitL*hitL)-2/(hitR*hitR)) *steeringForce*mytool.steering_force)

                                steering.rigid_body_constraint.motor_ang_target_velocity=(2/(hitL*hitL)-2/(hitR*hitR)) *steeringForce*mytool.steering_force;
                            if hitD: 
         
                                brake = 1-stopping;
                            #current car setup is RWD
                                motorFL.rigid_body_constraint.motor_ang_target_velocity = 0;  
                                motorFL.rigid_body_constraint.motor_ang_max_impulse = brake;         
                                motorFR.rigid_body_constraint.motor_ang_target_velocity = 0;
                                motorFR.rigid_body_constraint.motor_ang_max_impulse = brake;
                                
                                #RWD Motors
                                motorRL.rigid_body_constraint.motor_ang_target_velocity = (hitF-0.5)*100*mytool.max_speed;
                                motorRL.rigid_body_constraint.motor_ang_max_impulse = velocity*200*brake*mytool.max_acceleration;                
                                motorRR.rigid_body_constraint.motor_ang_target_velocity = (hitF-0.5)*100*mytool.max_speed;
                                motorRR.rigid_body_constraint.motor_ang_max_impulse = velocity*200*brake*mytool.max_acceleration;
                                if stopping:
                                    Globals.stopping = 0;
                        else:
                            print("1")
                            if Globals.running ==1:
                                print("2")
                                obj.rotation_euler[2]-=(1/(hitL*hitL)-1/ (hitR*hitR))*0.005 * steeringForce*mytool.steering_force
                                angle = obj.rotation_euler[2];
                                if hitD:
                                    print("3")
                                    obj.location[0]-=math.sin(angle)*velocity*mytool.max_speed;
                                    obj.location[1]+=math.cos(angle)*velocity*mytool.max_speed;
        else:
            
            bpy.app.handlers.frame_change_pre.remove(runProgram)

          
    print("Raytracing-AI has started.")      # register program if "RUN PROGRAM"'s custom property "run" is equal to 1              
    bpy.app.handlers.frame_change_pre.append(runProgram)




def stopButton(context):
    if Globals.running == 1:
        Globals.running = 0;
        Globals.stopping = 1;
        print("Raytracing-AI has been stopped.")
        bpy.context.scene.frame_current+=1;
        bpy.context.scene.frame_current-=1;
                    
    else:
        print("Raytracing-AI has already been stopped.")

def resetButton(context):
    bpy.context.scene.frame_current=0;
    for obj in bpy.context.scene.objects:
        if "raycast_Controller" in obj.name:
            obj.location[0] = 0;
            obj.location[1] = 0;
            obj.location[2] = 0;
            obj.rotation_euler[0] = 0;
            obj.rotation_euler[1] = 0;
            obj.rotation_euler[2] = math.pi/2;

def debugButton(context):
    if Globals.debug == 0:
        Globals.debug = 1;
        print("Raytracing-AI will now output debug information.")
    else:
        Globals.debug = 0;
        print("Raytracing-AI will no longer output debug information.")   
                 


class Run_AI(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "raytracer.run"
    bl_label = "Toggle Run"


    def execute(self, context):
        if Globals.running == 0:
            Globals.running = 1;
            Globals.stopping = 0;
            runButton(context,bpy.context.scene.my_tool);
            
        elif Globals.running == 1:
            Globals.running = 0;
            Globals.stopping = 1;
            stopButton(context);
            
        return {'FINISHED'}

class Stop_AI(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "raytracer.stop"
    bl_label = "Force Stop"
    
    

    def execute(self, context):
        stopButton(context)
        return {'FINISHED'}

class Reset_AI(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "raytracer.reset"
    bl_label = "Reset"
    
    def execute(self,context):
        resetButton(context);
        return {'FINISHED'}    

class Debug_AI(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "raytracer.debug"
    bl_label = "Debug"
    
    def execute(self,context):
        debugButton(context);
        return {'FINISHED'}

 


class LayoutDemoPanel(bpy.types.Panel):
    bl_label = "Raytracing AI"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout

        scene = context.scene




        # Different sizes in a row
        if Globals.running == 1:
            layout.label(text="The script is now running.")
        elif Globals.running == 0:
            layout.label(text="The script is not currently running.")
            
        row = layout.row(align=True)
        sub = row.row()
        sub.scale_x = 1.0
        sub.operator("raytracer.run")
        sub.operator("raytracer.reset")
        

        row = layout.row()
        row.operator("raytracer.debug")
        row.scale_x=2
        if Globals.debug ==1:   
            row.label(text="Outputting debug info to console.")
        elif Globals.debug ==0:
            row.label(text="Not outputting debug info")
        
        row = layout.row()
        row.operator('raytracer.stop')
        mytool = scene.my_tool
        row = layout.row()
        row.prop(mytool,"max_speed");
        row.prop(mytool,"max_acceleration");
        row=layout.row();
        row.prop(mytool,"steering_force");

def register():
    

    
    bpy.utils.register_class(Properties)
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=Properties);
    bpy.utils.register_class(Run_AI)
    bpy.utils.register_class(Reset_AI)
    bpy.utils.register_class(Stop_AI)
    bpy.utils.register_class(Debug_AI)
    bpy.utils.register_class(LayoutDemoPanel)

def unregister():
    bpy.utils.unregister_class(LayoutDemoPanel)
    bpy.utils.unregister_class(Run_AI)
    bpy.utils.unregister_class(Reset_AI)
    bpy.utils.unregister_class(Stop_AI)
    bpy.utils.unregister_class(Debug_AI)
    
    bpy.utils.unregister_class(Properties)
    del bpy.types.Scene.my_tool;


if __name__ == "__main__":
    register()
