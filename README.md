# Blender-Raycasting-Agent
A raycasting ai for blender objects and rigid bodies.



Prerequisites:
  Install Blender 3.2.1>. This addon uses Named Attributes inside the Geometry Node editor which is a feature exclusive to new versions of Blender.
  
Installation:
  1. Open up the basisScene.blend file or append all of the collections (not ridid bodies and rigid body constraints) to a new file. (This should automatically append the geometry node setup, but if not you can always append it separately under the "NodeTree" section when appending.
  2. Install the raycasting addon:
     Open Edit>Preferences>Add-ons>Install and locate the ui.py file.
     Enable the addon by checking it. If no addon appears, type in "Raytracing Vehicle" into the search field.
  3. The addon is now installed. To access it, open up the scene properties inside of the right toolbar, scroll down to "Raytracing AI":
      Toggle Run - actives the script.
      Reset - resets the positions of all raycasting agents.
      Debug - Outputs info about the raycaster to the System_Console
      Force Stop - Useful if you intend on making coding changes. The script gets registered and will continue to run until it is stopped.
      Max Speed - A multiplier for the speed of the agent (works both for rigid body and non rigid body agents)
      Max Acceleration - A multiplier for how much force the motor can exert (only for rigid body agents)
      Steering Force - A multiplier for how much force the steering motor can exert (works both rigid body and non rigid body agents)
      
 Extra info:
 More info and controls for the raycasting agents can be accessed through the modifiers>Raycast Detectory node. Here you can invidually set the speed of the agents as well as change the ray length and angle.
 
 The agents are made to collide with any objects inside of the "Roads Collection" If you desire to change the environment, simply add passive rigid body objects (assuming you are using the physics car, otherwise don't worry), set the rigid body friction to 2.0 and place them inside the Roads Collection. 
 Alternatively I've added a geometry node setup to generate roads using a voronoi texture. You can change the parameters of it inside the modifier properties of the Road object.
 
 Unfortunately duplicating agents really only works for non rigid body agents. The limitation is due to the rigid body physics simulation not considering the newly duplicated "car" as a rigid body system and won't animate it.
 
 
