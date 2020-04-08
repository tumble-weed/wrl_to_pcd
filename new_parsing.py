# coding: utf-8
# Your code here!
# ===========Sec-1==================================================================
#
# libraries to be imported 
#

#import tensorflow as tf
import matplotlib.pyplot as plt 
import matplotlib.image as img
#import numpy as np
#import png
#import itertools
#import operator
#import urllib.request
import re
def max_min_coord(data):
    arr = np.array(data)
    max_list = np.amax(arr, axis = 0)
    min_list = np.amin(arr, axis = 0)
    return max_list,min_list




class VRML():
    def __init__(self):
        # initializations 
        
#        self.header_found = False
#        self.navigation_done = False
#        self.transform_done = False
        self.coordinates = []
        self.xy = []
        self.navigation_dict_type = []
        self.transform_scale_list = [] 
        self.transform_translation_list = [] 
        self.navigation_dict = {}
        self.Res_Dictionary = {}
        self.transform_dict = {}
        self.transform_children_dict = {}
        self.transform_children_shape_dict = {}
        self.transform_children_shape_geometry_dict = {}
        self.transform_children_shape_appearance_dict = {}
        self.transform_children_shape_geometry_diffuseColor = []
        self.transform_children_shape_geometry_specularColor = []
        
        pass
    def read_image(self,imname):
        self.image = img.imread(imname)  # image is now numpy array
        
        
    def next_line(self):
        line = str(next(self.vrml))
        line = line.replace("b'","")
        line = line.replace("\\","")
        line = line.replace("n'","")
        if len(line.strip()) == 0 :
            line = self.next_line()
        return line 
    

    def get_string_between_two_similar_substring(self,line,str_val):
        a = line.find(str_val)
        t = line[a+1:]
        b = t.find(str_val)
        return line[a+1:b+a+1]
    

    def check_for_header(self,line):
        if "#VRML V2.0 utf8" in line :
            return True 
        else :
            return False 


    def check_for_navigation(self,line):
        if "NavigationInfo" in line :
            return True 
        else :
            return False 
    

    def check_for_transform(self,line):
        if "Transform" in line :
            return True 
        else :
            return False 
    
    

    def find_navigation_type(self,line):
        type_res = (line[line.find("[")+1:line.find("]")].split(","))
        for each_item in type_res :
            temp = self.get_string_between_two_similar_substring(each_item,'"')
            #temp = each_item[each_item.find('"')+1:each_item.find('"')]
            self.navigation_dict_type.append(temp)
        return self.navigation_dict_type
    

    def get_navigation_params(self,line):
        if "{" in line :
            if (line[line.find("{")+1:].strip()) == "" : 
                line = str(next(self.vrml))
    ## we can make multiple functions for different navigations configs 
            if "type" in line :
                navigation_dict_type = self.find_navigation_type(line)
                self.navigation_dict["type"] = navigation_dict_type
                line = str(next(self.vrml))
            # we can make multiple functions for different navigations configs 
        if not "}" in line :
            print ("some issue with navigation parsing") 
        self.Res_Dictionary["NavigationInfo"] = self.navigation_dict
    

    def find_transform_scale(self,line):
        line = line.split("\\")[0]
        points = line[line.find("scale")+6:].split(" ")
        for each in points :
            each = each.strip()
            self.transform_scale_list.append(int(each))
        return self.transform_scale_list
    

    def find_transform_translation(self,line):
        line = line.split("\\")[0]
        points = line[line.find("translation")+12:].split(" ")
        for each in points :
            each = each.strip()
            self.transform_translation_list.append(int(each))
        return self.transform_translation_list
    
    def find_transform_children_shape_geometry_crease(self,line):
        temp = float(line.split(" ")[-1])
        return (temp)
    
    def find_transform_children_shape_geometry_solid (self,line):
        return line.split(" ")[-1]
    


    def pick_the_data(self,line):
        coordinates = []
        line = line.replace("point","")
        line = line.strip()
        if line == "":
            line = self.next_line()
        if "[" in line :
            line = self.next_line()
            while not "]" in line :
                row = line.split(",")
                #xyz = []
                for each_val in row :
                    data_vals = each_val.split(" ")
                    while("" in data_vals) : 
                        data_vals.remove("") 
                    if not len(data_vals) == 0 :
                        data_vals = [float(i) for i in data_vals] 
                        coordinates.append(data_vals)
                line = self.next_line()
        if "]" in line :
            return coordinates 
    


    def pick_the_data_tex_coordinates(self,line):
        coordinates = []
        line = line.replace("point","")
        line = line.strip()
        if line == "":
            line = self.next_line()
        if "[" in line :
            line = self.next_line()
            temp = []
            while not "]" in line :
                row = line.split(" ")
                for i in row :
                    if len(i) > 0 :
                        temp.append(i)
                line = self.next_line()
        xy = []
        zz = []
        for i in range(0,len(temp),2): 
            xy.append(temp[i])
            xy.append(temp[i+1])
            zz.append(xy)
            xy = []
        coordinates.append(zz)
        if "]" in line :
            return coordinates 
        return coordinates 
    

    def pick_the_data_coord_index1 (self,line):
        coordinates = []
        line = self.next_line()
        if "[" in line :
            line = self.next_line()
            temp = []
            while not "]" in line :
                row = line.split(" ")
                for i in row :
                    if len(i) > 0 :
                        temp.append(i)
                line = self.next_line()
        xy = []
        zz = []
        for i in temp:
            if not i == "-1" :
                xy.append(i)
            else :
                xy = [int(i) for i in xy] 
                zz.append(xy)
                xy = []
        coordinates.append(zz)
        if "]" in line :
            return coordinates 
    

    def pick_the_data_coord_index2 (self,line):
        coordinates = []
        line = self.next_line()
        if "[" in line :
            line = self.next_line()
            temp = []
            while not "]" in line :
                row = line.split(" ")
                for i in row :
                    if len(i) > 0 :
                        temp.append(i)
                line = self.next_line()
        xy = []
        zz = []
        for i in temp:
            lastcharcomma = re.match(".*,$",i)
            list_ind = i.split(",")
            if lastcharcomma :
                list_ind = list_ind[:-2]
            else :
                list_ind = list_ind[:-1]
            xy = [int(i) for i in list_ind] 
            zz.append(xy)
            xy = []
        coordinates.append(zz)
        if "]" in line :
            return coordinates 
    
    
    def find_transform_children_shape_geometry_coord(self,line):
        temp = line.split(" ")[-1]
        temp = "coord_" + temp
        line = self.next_line()
        if "{" in line :
            if (line[line.find("{")+1:].strip()) == "" : 
                line = self.next_line()
            if "point" in line :
                matrix = self.pick_the_data(line)
                line = self.next_line()
        return matrix,temp,line
    
    def find_transform_children_shape_geometry_texcoord (self,line):
        temp = line.split(" ")[-1]
        temp = "texcoord_" + temp
        line = self.next_line()
        if "{" in line :
            if (line[line.find("{")+1:].strip()) == "" : 
                line = self.next_line()
            if "point" in line :
                matrix = self.pick_the_data_tex_coordinates(line)
                line = self.next_line()
        return matrix,temp
    
    def find_transform_children_shape_geometry(self,line):
        line = line.replace("geometry","")
        line = line.strip()
        geo_type = "geometry_" + line 
        line = self.next_line()
        if "{" in line :
            if (line[line.find("{")+1:].strip()) == "" : 
                line = self.next_line()
    ## we can make multiple functions for different geometry configs 
            if "creaseAngle" in line :
                self.transform_children_shape_geometry_dict["creaseAngle"] = self.find_transform_children_shape_geometry_crease(line)
                line = self.next_line()
            if "solid" in line :
                self.transform_children_shape_geometry_dict["solid"] = self.find_transform_children_shape_geometry_solid(line)
                line = self.next_line()
            if "coord" in line :
                a,b,line = self.find_transform_children_shape_geometry_coord(line)
                self.transform_children_shape_geometry_dict[b] = a 
                line = self.next_line()
            if "texCoord" in line :
                a,b = self.find_transform_children_shape_geometry_texcoord(line)
                self.transform_children_shape_geometry_dict[b] = a 
                line = self.next_line()
            if "texCoordIndex" in line :
                self.transform_children_shape_geometry_dict["texCoordIndex"] = self.pick_the_data_coord_index1(line)
                line = self.next_line()
            if "coordIndex" in line :
                self.transform_children_shape_geometry_dict["coordIndex"] = self.pick_the_data_coord_index2(line)
                line = self.next_line()
        if not "}" in line :
            print ("some issue with transform_children_shape_geometry parsing") 
        return self.transform_children_shape_geometry_dict,geo_type
    


    def find_transform_children_shape_geometry_ambientIntensity(self,line):
        temp = float(line.split(" ")[-1])
        return (temp)
    
    def find_transform_children_shape_geometry_shininess(self,line):
        temp = float(line.split(" ")[-1])
        return (temp)

    def find_transform_children_shape_geometry_specularColor(self,line):
        points = line[line.find("specularColor")+14:].split(" ")
        for each in points :
            each = each.strip()
            self.transform_children_shape_geometry_specularColor.append(float(each))
        return self.transform_children_shape_geometry_specularColor    

    def find_transform_children_shape_geometry_diffuseColor(self,line):
        points = line[line.find("diffuseColor")+13:].split(" ")
        for each in points :
            each = each.strip()
            self.transform_children_shape_geometry_diffuseColor.append(float(each))
        return self.transform_children_shape_geometry_diffuseColor    
    
    def find_transform_children_shape_appearance_material(self,line):
        line = line.replace("material","")
        line = line.strip()
        #geo_type = "material_" + line 
        line = self.next_line()
        if "{" in line :
            if (line[line.find("{")+1:].strip()) == "" : 
                line = self.next_line()
    ## we can make multiple functions for different appearance configs 
            if "ambientIntensity" in line :
                self.transform_children_shape_appearance_dict["ambientIntensity"] = self.find_transform_children_shape_geometry_ambientIntensity(line)
                line = self.next_line()
            if "diffuseColor" in line :
                self.transform_children_shape_appearance_dict["diffuseColor"] = self.find_transform_children_shape_geometry_diffuseColor(line)
                line = self.next_line()
            if "specularColor" in line :
                self.transform_children_shape_appearance_dict["specularColor"] = self.find_transform_children_shape_geometry_specularColor(line)
                line = self.next_line()
            if "shininess" in line :
                self.transform_children_shape_appearance_dict["shininess"] = self.find_transform_children_shape_geometry_shininess(line)
                line = self.next_line()
        if not "}" in line :
            print ("some issue with transform_children_shape_appearance parsing") 
        return self.transform_children_shape_appearance_dict
    
   
    def find_transform_children_shape_appearance_texture(self,line):
        line = line.split(" ")
        while("" in line) : 
            line.remove("") 
        return line[1],line[-2]
    
    def find_transform_children_shape_appearance(self,line):
        line = line.replace("appearance","")
        line = line.strip()
        appearance_type = "appearance_" + line 
        line = self.next_line()
        if "{" in line :
            if (line[line.find("{")+1:].strip()) == "" : 
                line = self.next_line()
    ## we can make multiple functions for different appearance configs 
            if "material" in line :
                self.transform_children_shape_appearance_dict["material"] = self.find_transform_children_shape_appearance_material(line)
                line = self.next_line()
            if "texture" in line : 
                self.transform_children_shape_appearance_dict["texture"] = self.find_transform_children_shape_appearance_texture(line)
                line = self.next_line()
        if not "}" in line :
            print ("some issue with transform_children_shape_appearance parsing") 
        return self.transform_children_shape_appearance_dict,appearance_type
    
    def find_transform_children(self,line):
        line = line.replace("children","")
        line = line.strip()
        if line == "":
            line = self.next_line()
        if "[" in line :
            if (line[line.find("[")+1:].strip()) == "" : 
                line = self.next_line()
    ## we can make multiple functions for different children configs 
            if "Shape" in line :
                transform_children_shape_dict = self.find_transform_children_shape(line)
                self.transform_children_dict["shape"] = transform_children_shape_dict
                line = self.next_line()
                
        if not "]" in line :
            print ("some issue with transform_children parsing") 
        return self.transform_children_dict    
    def find_transform_children_shape(self,line):
        line = line.replace("Shape","")
        line = line.strip()
        #print (line)
        if line == "":
            line = self.next_line()
        if "{" in line :
            if (line[line.find("{")+1:].strip()) == "" : 
                line = self.next_line()
    ## we can make multiple functions for different shape configs 
            if "geometry" in line :
                #print (line)
                transform_children_shape_geometry_dict,geo_type = self.find_transform_children_shape_geometry(line)
                self.transform_children_shape_dict[geo_type] = transform_children_shape_geometry_dict
                line = self.next_line()
            if "appearance" in line : 
                transform_children_shape_appearance_dict,appearance_type = self.find_transform_children_shape_appearance(line)
                self.transform_children_shape_dict[appearance_type] = transform_children_shape_appearance_dict
                line = self.next_line()
        if not "}" in line :
            print ("some issue with transform_children_shape parsing") 
        return self.transform_children_shape_dict        
    
    def get_transform_params(self,line):
        if "{" in line :
            if (line[line.find("{")+1:].strip()) == "" : 
                line = self.next_line()
    ## we can make multiple functions for different transform configs 
            if "scale" in line :
                self.transform_dict["scale"] = self.find_transform_scale(line)
                line = self.next_line()
            if "translation" in line : 
                self.transform_dict["translation"] = self.find_transform_translation(line)
                line = self.next_line()
            if "children" in line :
                transform_dict_children = self.find_transform_children(line)
                self.transform_dict["children"] = transform_dict_children
                line = self.next_line()
        if not "}" in line :
            print ("some issue with transform parsing") 
        self.Res_Dictionary["TransformInfo"] = self.transform_dict
    
    def read(self,wrl_name):
        # -------------------------- Code is starting here ---------------------------------------------------
        header_found = False
        navigation_done = False
        transform_done = False

        with open(wrl_name, "rb") as vrml:
            self.vrml = vrml
            for line in self.vrml :
                line = line.decode('UTF-8') # decode the line in UTF8 format
                if header_found == False :
                    if self.check_for_header(line) == True :
                        #print ("Header is #VRML V2.0 utf8 ")
                        header = "#VRML V2.0 utf8"
                        header_found = True 
                        self.Res_Dictionary["Header"] = header
                        continue 
                else :
                    if navigation_done == False :
                        if self.check_for_navigation(line) == True :
                            #print ("NavigationInfo found")
                            self.get_navigation_params(line)
                            navigation_done = True 
                            continue
                    if transform_done == False :
                        if self.check_for_transform(line) == True :
                            #print ("Transform found")
                            self.get_transform_params(line)
                            transform_done = True 
                            continue
            
            pass
    def display_image(self,):
        #Display input 2D image
        plt.title("2d image of face")
        plt.imshow(self.image, interpolation='nearest') 
        plt.show()
        
        #Display input 2D image - nose
        plt.title("2d image of nose from face")
        plt.imshow(self.image[265:282,310:345,:], interpolation='nearest') 
        plt.show()
#-----------------------------------

