from collections import OrderedDict
import numpy as np
import skimage

def rgb_to_24bit(r,g,b):
    # from https://github.com/dimatura/pypcd/blob/20b032bfc729dec853ac810bceeb360f78bdc1d6/pypcd/numpy_pc2.py
    # 'merge_rgb_fields'
    
    word = np.array((r << 16) | (g << 8) | (b << 0) , dtype=np.uint32)
    word.dtype = np.float32
    return word

def write_list(l):
    s = ' '.join([str(el) for el in l])
    return s
    pass

def write_points(p):
    l_s = list(map(write_list,p))
    return '\n'.join(l_s)

def make_pcd_points(shape,texture):
    texture_np = np.array(texture)
    texture_np = skimage.img_as_ubyte(texture_np)
    shape_np = np.array(shape)
    
    rgb_as_24bit_words = rgb_to_24bit(texture_np[:,0],texture_np[:,1],texture_np[:,2])
    
    pcd_point_list = []
    
    for s,rgb_ in zip(shape.tolist(),rgb_as_24bit_words):
        pcd_point_list.append(list(s) + [rgb_])
    # import pdb;pdb.set_trace()
    return pcd_point_list
def get_pcd_row(data,key):
    if key == 'VERSION':
        return 'VERSION' +' ' + str(data[key])
    if key == 'FIELDS':
        return 'FIELDS' +' ' + ' '.join(data[key])
    if key == 'SIZE':
        return 'SIZE' +' ' + ' '.join(list(map(str,data[key])))
    if key == 'TYPE':
        return 'TYPE' +' ' + ' '.join(data[key])
    if key == 'COUNT':
        return 'COUNT' +' ' + ' '.join(list(map(str,data[key])))
    if key == 'WIDTH':
        return 'WIDTH' +' ' + str(data[key])
    if key == 'HEIGHT':
        return 'HEIGHT' +' ' + str(data[key])
    if key == 'VIEWPOINT':
        return 'VIEWPOINT' +' ' + ' '.join(list(map(str,data[key])))
    if key == 'POINTS':
        return 'POINTS' +' ' + str(data[key])
    if key == 'DATA':
        return 'DATA ascii'
        pass   
    
def get_data_rows(pcd_data):
    data = pcd_data['DATA']
    rows = []
    
    for p in data:
        rows.append(' '.join(list(map(str,p))))
    return rows

def write_pcd(pcd_data : OrderedDict,
fname: str):
    
    with open(fname,'w') as f:
        for k in pcd_data:
            # if k is 'DATA':
            #     continue
            row = get_pcd_row(pcd_data,k)
            f.write(row+'\n')
        data_rows = get_data_rows(pcd_data)
        for r in data_rows:
            f.write(r+'\n')
    
    
def to_pcd(shape,texture,pcd_fname):

    item_order = ['VERSION','FIELDS','SIZE','TYPE',
    'COUNT','WIDTH','HEIGHT','VIEWPOINT','POINTS','DATA']
    
    shape_np = np.array(shape)
    texture_np = np.array(texture)
    texture_np = skimage.img_as_ubyte(texture_np)
    
    pcd_points = make_pcd_points(shape,texture)
    
    POINTS = shape_np.shape[0]
    pcd_data = OrderedDict({})
    pcd_data['VERSION'] = 0.7
    pcd_data['FIELDS'] = ['x','y','z','rgb']
    pcd_data['SIZE'] = [4,4,4,4] #https://github.com/PointCloudLibrary/pcl/blob/master/test/bunny.pcd
    pcd_data['TYPE'] = ['F','F','F','F']
    pcd_data['COUNT'] = [1,1,1,1]
    pcd_data['WIDTH'] = POINTS
    pcd_data['HEIGHT'] = 1
    pcd_data['VIEWPOINT'] = [0,0,0,1,0,0,0]
    pcd_data['POINTS'] = POINTS
    pcd_data['DATA'] = pcd_points
    
    write_pcd(pcd_data,pcd_fname)

pass

