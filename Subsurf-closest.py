#A simple script to add subsurface to anything with an image texture and change the interpolation to Closest
#discord: trospe#4805
#Feel free to use this in your projects
#THE CAPITAL COMMENTS WILL HELP GUIDE YOU IF YOU WANT TO CHANGE THE VALUES

import bpy

# Iterate through all the materials in the scene
for material in bpy.data.materials:
    
    # Check if the material has a node tree
    if material.node_tree is not None:
        
        # Change the texture to closest        
        material.use_nodes = True
        nodeTree = material.node_tree
        imageTextureNodes = [node for node in nodeTree.nodes if node.type == 'TEX_IMAGE']

        for imageNode in imageTextureNodes:
            imageNode.interpolation = 'Closest'
        
        # Check if the material has a Principled BSDF shader node
        if material.node_tree.nodes.get('Principled BSDF') is not None:
            
            # Get a reference to the Principled BSDF node
            principled_bsdf = material.node_tree.nodes['Principled BSDF']
            
            # Set the 'Base Color' of the Principled BSDF node to a new value
            if principled_bsdf.inputs['Base Color'].is_linked:
                # If the 'Base Color' input is connected to a texture node, get a reference to the texture node
                texture_node = principled_bsdf.inputs['Base Color'].links[0].from_node
                texture_output = texture_node.outputs['Color']
                # Connect the texture node to the 'Subsurface Color' input of the Principled BSDF node
                material.node_tree.links.new(principled_bsdf.inputs['Subsurface Color'], texture_output)
            else:
                # If the 'Base Color' input is not connected to a texture node, set its value to a new color
                
                #YOU CAN DELETE THIS LINE
                principled_bsdf.inputs['Base Color'].default_value = (1.0, 0.0, 0.0, 1.0)  # This will set the base color to red
            
            # THIS IS THE SUBSURFACE VALUE (0 to 1.0)
            principled_bsdf.inputs[1].default_value = 1.0
            
            #THIS IS THE SUBSURFACE RADIUS
            principled_bsdf.inputs[2].default_value[0] = 0.1
            principled_bsdf.inputs[2].default_value[1] = 0.1
            principled_bsdf.inputs[2].default_value[2] = 0.1
            
            # SET THE SUBSURFACE METHOD TO Christensen-Burley
            principled_bsdf.subsurface_method = 'BURLEY'
            