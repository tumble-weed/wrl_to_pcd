#---------------------------------------------
import os,sys
from os.path import dirname,abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from pcd import to_pcd

import new_rendering
from new_rendering import inverse_renderer
# from superface import get_superface_nose_coods
fname = 'andreadm2.wrl'#'subject002.wrl'#
def test_to_pcd():
    inv = inverse_renderer()
    shape,texture =  inv.read(fname)
    to_pcd(shape,texture,fname.split('.')[0] + '.pcd')
    # new_rendering.display_texture(inv.texture_image)
test_to_pcd()
