# coding: utf-8
# Your code here!
# ================== modules to be imported ====================

#import tensorflow as tf
#import pdb;pdb.set_trace()
import matplotlib.pyplot as plt 
import matplotlib.image as img
import numpy as np
#from numpy import array

#from IPython import get_ipython
#get_ipython().run_line_magic('matplotlib', 'qt')
#get_ipython().run_line_magic('matplotlib', 'inline')

#import parsing_2d3d_files as parse
from mpl_toolkits.mplot3d import Axes3D

import matplotlib.tri as mtri
from new_parsing import VRML
import os
def scale(norm_val,max_value,min_value):
    range_val = max_value - min_value
    data = (norm_val*range_val) + min_value
    return data.round(4)

def max_min_coord(data):
    arr = np.array(data)
    max_list = np.amax(arr, axis = 0)
    min_list = np.amin(arr, axis = 0)
    return max_list,min_list

def display_texture(image):
    y_image,x_image,z_image = image.shape
    
    #display texture image
    plt.title("texture of face - texture file is input to 3D model file")
    plt.imshow(image)
    plt.show()
    
    #display texture image of nose - right image in stereoscopic texture image
    plt.title("texture of nose from face - from right face image from texture file")
    plt.imshow(image[960:1160,2350:2750,:])
    plt.show()
    
    #display texture image of nose - left image in stereoscopic texture image
    plt.title("texture of nose from face - from left face image from texture file")
    plt.imshow(image[975:1175,1150:1550,:])
    plt.show()
    
def display_face_nose_no_lighting(select_color,select_coord,select_coord_index,coord_index_triangle_to_texture_value_mapping,coord_Coordinate,coordIndex):
    # =============================================================================
    # Plotting face and nose with and without lighting
    # =============================================================================
    #Set up 3d graph figure parameters
    #get_ipython().run_line_magic('matplotlib', 'qt')
    #get_ipython().run_line_magic('matplotlib', 'inline')
    fig = plt.figure(figsize=(24, 12))
    
    #Set up subplot for nose portion of face with colors without lighting
    #Set up facecolors (colors of each face/triangle) for triangular surface plot (plot_trisurf)
    tri_colors1 = select_color
    
    # Set up triangulation object with x, y coordinates of vertices and the vertex indices of each triangle
    x1,y1,z1 = np.asarray(select_coord).T
    #print("max-min-x1-y1-z1:",max(x1),max(y1),max(z1),min(x1),min(y1),min(z1))
    triang1 = mtri.Triangulation(-y1, x1, triangles=select_coord_index)
    
    ax1 = fig.add_subplot(1, 2, 1, projection='3d')
    ax1.title.set_text('Nose - full size')
    
    # Set equal sizes to x, y, z axes lengths
    #ax.set_xlim3d(-500,-150)
    ax1.set_xlim3d(280,350)
    ax1.set_ylim3d(-120,-50)
    ax1.set_zlim3d(50,120)
    
    ax1.view_init(azim=0, elev=90) # set azimuth angle and elevation/altitude angle to get front view of human face
    
    ax1.plot_trisurf(triang1, z1, facecolors=tri_colors1, shade=False, antialiased=False)
    
    #garbage collection
    del select_coord_index, select_color, select_coord, triang1, tri_colors1, x1, y1, z1
    
    #Set up subplot for face with colors without lighting
    
    ax2 = fig.add_subplot(1, 2, 2, projection='3d')
    ax2.title.set_text('Face - without lighting')
    
    # Set equal sizes to x, y, z axes lengths
    ax2.set_xlim3d(150,500)
    ax2.set_ylim3d(-250,100)
    ax2.set_zlim3d(-175,175)
    
    ax2.view_init(azim=0, elev=90) # set azimuth angle and elevation/altitude angle to get front view of human face
    #ax2.view_init(azim=0, elev=45) # set azimuth angle and elevation/altitude angle to get side view of human face
    
    #Set up facecolors (colors of each face/triangle) for triangular surface plot (plot_trisurf)
    tri_colors2 = coord_index_triangle_to_texture_value_mapping
    
    # Set up triangulation object with x, y coordinates of vertices and the vertex indices of each triangle
    x,y,z = coord_Coordinate.T
    triang2 = mtri.Triangulation(-y, x, triangles=coordIndex)
    #triang2 = mtri.Triangulation(y, x, triangles=coordIndex)
    #triang2 = mtri.Triangulation(x, y, triangles=coordIndex)
    
    #Plot the human face surface with triangular surface plotting function (plot_tri_surf)
    #First plot without VRML lighting model applied to face colors
    ax2.plot_trisurf(triang2, z, facecolors=tri_colors2, shade=False, antialiased=False)
    
    # =============================================================================
    # #Set up subplot for face with colors with lighting
    # 
    # tri_verts = get_tri_verts(triang2, z) #get array of triplets of vertices from the list of triangles
    # normals = ax3._generate_normals(tri_verts) #get their normal vectors
    # normals = normalize_rows(normals) #normalize the normal vectors
    # =============================================================================
    # =============================================================================
    # # Approximated lighting equation for texture + headlight (VRML lighting model)
    # #
    # # Irgb = ITrgb × (N · L + specular_i)
    # # or Irgb = ITrgb × (N · L) + specular_i ?
    # # specular_i = OSrgb × ( N · ((L + v) / |L + v|))^(shininess × 128)
    # #
    # # ITrgb= colour from 3-4 component texture image
    # # OSrgb = Material specularColor
    # # v = normalized vector from point on geometry to viewer's position
    # # N = normalized normal vector at this point on geometry
    # # L = -ve direction of light source i = -(0,0,-1) = (0,0,1) for headlight (Directional light)
    # # shininess = Material shininess
    # # http://www.x-3-x.net/vrml/archive/annotatedVRML2/CH2.HTM#2.14
    # # https://www.web3d.org/documents/specifications/14772/V2.0/part1/concepts.html#4.14
    # 
    # #Calculate N.L (dot product of normalized normals to triangles and the direction to light source/headlight)
    # LightDirection = np.array([0,0,1])
    # NdotL = np.inner(normals,LightDirection)
    # NdotL = np.asarray(NdotL).reshape(-1,1)
    # NdotL = np.clip(NdotL,0.0,1.0) # clip it to [0.0, 1.0] range
    # #· = modified vector dot product: if dot product < 0, then 0.0, otherwise, dot product
    # 
    # #Calculate specular component of light reflection
    # #ViewerPosition = np.array([0,0,10])
    # ViewerPosition = np.array([0,0,10+int(max(z)+1)]) #set the viewer position (0, 0, 10) - from the nearest point from viewer for now
    # #print(max(z))
    # tri_centroids = get_tri_cendroids(tri_verts) # get centroids of triangles
    # tri_directionToViewer = ViewerPosition - tri_centroids
    # tri_directionToViewer = normalize_rows(tri_directionToViewer) # get normalized vector (direction) from centroid to viewer
    # tri_lightdir_plus_directionToViewer = tri_directionToViewer + LightDirection
    # tri_lightdir_plus_directionToViewer = normalize_rows(tri_lightdir_plus_directionToViewer) # get normalized light direction + direction to viewer
    # NdotNormLplusV = np.einsum('ij,ij->i',normals,tri_lightdir_plus_directionToViewer)
    # NdotNormLplusV = np.asarray(NdotNormLplusV).reshape(-1,1) # perform dot product of normalized normals to triangles and (normalized light direction + direction to viewer)
    # NdotNormLplusV_power128xShininess = np.power(NdotNormLplusV,shininess*128) # raise it to power of 128 x shininess
    # tri_specular = NdotNormLplusV_power128xShininess * specularColor # multiply by specularColor field to get specular color component of light relfection
    # 
    # # calculate light reflection at centroid of each triangle
    # # Irgb = ITrgb × (N · L + specular_i)
    # # or Irgb = ITrgb × (N · L) + specular_i ?
    # #final_tri_colors = tri_colors2 * (NdotL + tri_specular)
    # #final_tri_colors = tri_colors2 * NdotL + tri_specular
    # final_tri_colors = tri_colors2 * NdotL
    # #final_tri_colors = np.clip(final_tri_colors,0.0,1.0) # clip it to [0.0, 1.0] range
    # =============================================================================
    
    #garbage collection
    del coord_index_triangle_to_texture_value_mapping
    
    # =============================================================================
    # #Set up subplot for face with colors with lighting - VRML lighting model applied to face colors
    # # Plot the human face surface with triangular surface plotting function (plot_tri_surf)
    # ax4 = fig.add_subplot(2, 2, 4, projection='3d')
    # ax4.title.set_text('Face - with lighting')
    # 
    # # Set equal sizes to x, y, z axes lengths
    # ax4.set_xlim3d(150,500)
    # ax4.set_ylim3d(-250,100)
    # ax4.set_zlim3d(-175,175)
    # 
    # ax4.view_init(azim=0, elev=90) # set azimuth angle and elevation/altitude angle to get front view of human face
    # 
    # ax4.plot_trisurf(triang3, z, facecolors=final_tri_colors, shade=False, antialiased=False)
    # =============================================================================
    
    plt.show()
    
    # so we have the geometry, depth and texture information of the 3D dataset
    # Lighting factors have been parsed. Lighting needs to be applied to each pixel.
    # For that, rasterization needs to be done using geometry/triangles to pixel
    # conversion using barycentric interpolation and coloring of each pixel.
    
            
def apply_texture (uv_value,image,x_image,y_image) :
    u = float(uv_value[0])
    v = float(uv_value[1])
    u = int(u * x_image) 
    v = int(v * y_image)
    return image[v,u]

class inverse_renderer():
    def __init__(self,select_range = [(-np.inf,np.inf),(-np.inf,np.inf)]):
        self.select_range = select_range
        self.texture_dir = None
        pass
    
    def geometry_init(self,):
        #Variables used in the coming sections
        self.coordinate_triangle = []
        self.texture_triangle = []
        self.texture_triangle_face = []
        self.coord_index_to_texcoord_index_mapping = []
        self.coord_index_triangle_to_texture_value_mapping = []
    
        pass
    def texture_init(self):
        #Variables and constants for below sections
        self.rgb_scaling_factor = 255.0
        
        #variables for nose
        self.select_coord = []
        self.select_coord_index = []
        self.select_texcoord = []
        self.select_texcoord_index = []
        self.select_color = []
        
        self.select_coord_texcoord_mapping = []
        
#        self.my_count_select_coord_index = 0
        self.select_coord_index_dict = {}

    def read_Res_dictionary(self,wrl_fname,texture_dir,**kwargs):
        vrml_obj = VRML()
        vrml_obj.read(wrl_fname)
#        vrml_obj.display_image()
        self.Res_Dictionary = vrml_obj.Res_Dictionary
        self.texture_dir = texture_dir

        pass    

    def parse_Res_Dictionary(self,):
        # ================== Reading 3D model file, texture image ====================
        # Reading the texture Image 
        for key, value in self.Res_Dictionary['TransformInfo']['children']['shape']['appearance_Appearance'].items(): 
            if key == 'texture' :
                texture_file = value[1]
                self.texture_file = texture_file[1:-1]
            if key == 'specularColor' :
                self.specularColor = value
            if key == 'shininess' :
                self.shininess = value
        
        self.texture_image = img.imread(os.path.join(self.texture_dir,self.texture_file))  # image is now numpy array 
        self.texture_image = np.asarray(self.texture_image)
        self.y_image,self.x_image,self.z_image = self.texture_image.shape
        # display(image)
        
        #Retrieve geometry and texture info from 3D model file
        # - vertex coordinates, indices, texture coordinates, indices
        for key, value in self.Res_Dictionary['TransformInfo']['children']['shape']['geometry_IndexedFaceSet'].items(): 
            value = np.asarray(value)
            if key == 'texCoordIndex' :
                self.texCoordIndex = value 
            if key == 'creaseAngle' :
                self.creaseAngle = value 
            if key == 'coord_Coordinate' :
                self.coord_Coordinate = value 
            if key == 'texcoord_TextureCoordinate' :
                self.texcoord_TextureCoordinate = value 
            if key == 'coordIndex' :
                self.coordIndex = value

    
    def get_geometry(self,):
        self.geometry_init()
        #Variables and constants for below sections
        self.coordIndex = self.coordIndex[0]
        self.texCoordIndex = self.texCoordIndex[0]
        self.texcoord_TextureCoordinate = self.texcoord_TextureCoordinate[0]
        
        my_count_coordindex = 0

        my_count_limit = 10
        
        default_color = 0.0
        temp2 = [default_color, default_color, default_color]

        #First loop to retrieve geometry info - mapping of vertex coordinates and indices
        for x in self.coordIndex :
            if len(x) == 3 :
                a_1 = (self.coord_Coordinate[x[0]])
                b_1 = (self.coord_Coordinate[x[1]])
                c_1 = (self.coord_Coordinate[x[2]])
                
                temp = []
                temp.append(a_1)
                temp.append(b_1)
                temp.append(c_1)
                
                temp1 = []
                temp1.append(x)
                temp1.append(self.texCoordIndex[my_count_coordindex])
                temp1.append(temp)
                
                self.coord_index_to_texcoord_index_mapping.append(temp1)
                
                self.coord_index_triangle_to_texture_value_mapping.append(temp2)
                
                my_count_coordindex = my_count_coordindex + 1
                self.coordinate_triangle.append(temp)
        self.max_val,self.min_val = max_min_coord(self.coord_Coordinate)

    def get_texture(self,):
        x_lower_bound = scale(self.select_range[0][0],self.max_val[0],self.min_val[0])
        x_upper_bound = scale(self.select_range[0][1],self.max_val[0],self.min_val[0])
        y_lower_bound = scale(self.select_range[1][0],self.max_val[1],self.min_val[1])
        y_upper_bound = scale(self.select_range[1][1],self.max_val[1],self.min_val[1])

        self.texture_init()
        my_count_texcoordindex = 0
        my_count_select_coord_index = 0
        #Second loop to retrieve texture info and geometry info
        # - texture coordinates, indices and mapping to vertex coordinates, indices
        for x in self.texCoordIndex :
            if len(x) == 3 :
                uv1 = apply_texture(self.texcoord_TextureCoordinate[x[0]],self.texture_image,self.x_image,self.y_image)
                uv2 = apply_texture(self.texcoord_TextureCoordinate[x[1]],self.texture_image,self.x_image,self.y_image)
                uv3 = apply_texture(self.texcoord_TextureCoordinate[x[2]],self.texture_image,self.x_image,self.y_image)
                
                #face_uv = (uv1 + uv2 + uv3) / (3 * 256)
                face_uv = uv1 / 256
                
                temp = []
                temp.append(uv1)
                temp.append(uv2)
                temp.append(uv3)
                
                self.texture_triangle.append(temp)
                self.texture_triangle_face.append(face_uv)
                
                temp1 = self.coord_index_to_texcoord_index_mapping[my_count_texcoordindex][0]
                temp3 = self.coord_index_to_texcoord_index_mapping[my_count_texcoordindex][1]
                temp4 = self.coord_index_to_texcoord_index_mapping[my_count_texcoordindex][2]
        
                flag_all_coords_within_range = 0
                for i in range(3):
                    if ((self.coord_Coordinate[temp1[i]][0] > x_lower_bound and self.coord_Coordinate[temp1[i]][0] < x_upper_bound) and (self.coord_Coordinate[temp1[i]][1] > y_lower_bound and self.coord_Coordinate[temp1[i]][1] < y_upper_bound)) :
                        flag_all_coords_within_range += 1
        
                temp_tri_new_coord_indices = []
                for i in range(3):
                    self.coord_index_triangle_to_texture_value_mapping[temp1[i]] = temp[i] / self.rgb_scaling_factor
                    if (flag_all_coords_within_range == 3) :
                        self.select_coord.append(temp4[i])
                        self.select_color.append(self.coord_index_triangle_to_texture_value_mapping[temp1[i]])
                        
                        temp_new_coord_index = self.select_coord_index_dict.get(temp1[i],None)
                        if temp_new_coord_index == None :
                            self.select_coord_index_dict[temp1[i]] = my_count_select_coord_index
                            temp_new_coord_index = my_count_select_coord_index
                            my_count_select_coord_index += 1
                        temp_tri_new_coord_indices.append(temp_new_coord_index)
                        
                        if i == 2 :
                            self.select_coord_index.append(temp_tri_new_coord_indices)
        
                my_count_texcoordindex = my_count_texcoordindex + 1        


    def garbage_collect(self,):
        del coord_index_to_texcoord_index_mapping, select_coord_index_dict
    def read(self,wrl_fname):
        self.read_Res_dictionary(wrl_fname,os.path.dirname(wrl_fname))
        self.parse_Res_Dictionary()
        self.get_geometry()
        self.get_texture()
        shape = self.coord_Coordinate
        texture = self.coord_index_triangle_to_texture_value_mapping

#         display_texture(self.texture_image)
#         display_face_nose_no_lighting(self.select_color,self.select_coord,
#         self.select_coord_index,self.coord_index_triangle_to_texture_value_mapping,
#         self.coord_Coordinate,self.coordIndex)
        
        return shape,texture


