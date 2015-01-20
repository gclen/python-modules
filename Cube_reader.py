#!/usr/bin/python

#--------------------------------------------------------------
#This will take a cubefile and return a dictionary that contains all
#of the information in the header. This includes voxel positions and atomic 
#coordinates. 
#
# E.g. import Cube_reader
# header_example=Cube_reader.header_Read(name_of_cube_file)
#
#This will return a nested dictionary
#The first level keys are 'voxel_info' and 'atom_info'
#The second level keys for voxel_info are ['origin','voxel_x','voxel_y','voxel_z]
#'origin' as '_dummy' as its third level key (acts as a placeholder)
#'voxel_x' has 'num_voxels' and 'voxel_step_sizes' as its third level keys
#
#'atom_info' has 'tot_atom_num' as a second level key with the third level key
#being '_dummy'
#'atoms' is also a second level key with the corresponding third level keys
#being the atomic numbers. The values for each atomic numbers is a list of 
#tuples containing the coordinates of the atom
#--------------------------------------------------------------


#Import the Autovivify module from this directory to create the data structure
import Autovivify 
import numpy as np

def header_Read(input_cube_file):
    
    #Create a data structure to hold the header information
    header_info=Autovivify.construct(3,list)
    #Open up the cubefile for reading
    cube_file=open(input_cube_file,'r')
    #Set a line counter
    line_count=1
    
    #Parse the rest of the header 
    for line in cube_file:
        #The first two lines are skipped since they are always comments
        if line_count<=2:
            pass
        #The third line contains the number of atoms and origin of voxel positions
        elif line_count==3:
            line_split=line.split()
            #Get the number of atoms from the next line to determine header size
            #The number is listed as negative so the absolute value must be taken
            num_atoms=abs(float(line_split[0]))
            #Put the total number of atoms into the dictionary 
            header_info['atom_info']['tot_atom_num']['_dummy'].append(num_atoms)
            #Add the voxel origin info into the dictionary
            #The coordinates are added as a tuple (x_0,y_0,z_0)
            #Also need to convert string to float
            header_info['voxel_info']['origin']['_dummy'].append((float(line_split[1]),float(line_split[2]),float(line_split[3])))
        #The next 3 lines contain the width of the voxels in each direction and number of voxel
        #The fourth line corresponds to voxels in the x direction
        elif line_count==4:
            line_split=line.split()
            #Add total number of voxels in x into dictionary
            header_info['voxel_info']['voxel_x']['num_voxels'].append(float(line_split[0]))
            #Add the step sizes in each direction into the dictionary
            #Need to convert string to float
            vox_step_sizes=(float(line_split[1]),float(line_split[2]),float(line_split[3]))
            header_info['voxel_info']['voxel_x']['voxel_step_sizes'].append(vox_step_sizes)
        #The fifth line corresponds to voxels in the y direction
        elif line_count==5:
            line_split=line.split()
            #Add total number of voxels in x into dictionary
            header_info['voxel_info']['voxel_y']['num_voxels'].append(float(line_split[0]))
            #Add the step sizes in each direction into the dictionary
            #Need to convert string to float
            vox_step_sizes=(float(line_split[1]),float(line_split[2]),float(line_split[3]))            
            header_info['voxel_info']['voxel_y']['voxel_step_sizes'].append(vox_step_sizes)
        #The sixth line corresponds to the voxels in the z direction
        elif line_count==6:
            line_split=line.split()
            #Add total number of voxels in x into dictionary
            header_info['voxel_info']['voxel_z']['num_voxels'].append(float(line_split[0]))
            #Add the step sizes in each direction into the dictionary
            #Need to convert string to float
            vox_step_sizes=(float(line_split[1]),float(line_split[2]),float(line_split[3]))            
            header_info['voxel_info']['voxel_z']['voxel_step_sizes'].append(vox_step_sizes)

        #For the rest of the lines add the atom info and coordinates to the dictionary 
        elif 7<=line_count<=num_atoms+6:
            line_split=line.split()
            #The first number in the line is the atomic number which will be used as a key
            #The second number is the atomic charge so that number will be skipped
            #All atoms of that type will have their coordinates stored as tuples 
            atomic_num=line_split[0]
            atomic_coords=(float(line_split[2]),float(line_split[3]),float(line_split[4]))
            #Add the atom info into the dictionary
            header_info['atom_info']['atoms'][atomic_num].append(atomic_coords)
            
        #After the header break out of the loop
        elif line_count>num_atoms+6:
            break

        line_count+=1

    #Close the cubefile
    cube_file.close()

    return header_info


#Read the cube file into a 1-D numpy array
def cube_Read(input_cube_file,header_info):

    #Get the number of atoms in the system 
    num_atoms=header_info['atom_info']['tot_atom_num']['_dummy'][0]
    #Get the number of voxels in the X direction 
    num_X=header_info['voxel_info']['voxel_x']['num_voxels'][0]
    #Get the number of voxels in the Y direction
    num_Y=header_info['voxel_info']['voxel_y']['num_voxels'][0]
    #Get the number of voxels in the Z direction
    num_Z=header_info['voxel_info']['voxel_z']['num_voxels'][0]
    #Get the total number of points
    tot_points=int(num_X*num_Y*num_Z)
    #Initialize a numpy array of proper size 
    density_array=np.zeros(tot_points)
    #Initialize a counter for the array
    index=0

    #Open the cube file
    cube_file=open(input_cube_file,'r')

    #Skip the header 
    for _ in range(int(num_atoms+7)):
        next(cube_file)

    #Loop over the rest of the cube file 
    for line in cube_file:
        #Split the line to get a list of density values
        density_vals=line.split()
        #Put the values into the numpy array
        for value in density_vals:
            #Put value into array 
            density_array[index]=value
            #Increment index
            index+=1

    #Close the cube file
    cube_file.close()
    
    #Return the array
    return density_array






