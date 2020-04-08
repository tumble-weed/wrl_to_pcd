from os.path import dirname,abspath,join
import sys
my_dir = dirname(abspath(__file__))
sys.path.append(my_dir)
#from new_rendering import read_3d
import new_rendering
from new_rendering import inverse_renderer
from superface import get_superface_nose_coods
#def test_rendering():
#    fname = "andread/andreadm2.wrl"
#    read_3d(fname)
#    pass
def test_rendering():
    inv = inverse_renderer(select_range=get_superface_nose_coods())
    inv.read("andreadm2.wrl")
    new_rendering.display_texture(inv.texture_image)
    new_rendering.display_face_nose_no_lighting(inv.select_color,inv.select_coord,
        inv.select_coord_index,inv.coord_index_triangle_to_texture_value_mapping,
        inv.coord_Coordinate,inv.coordIndex)
    import pdb;pdb.set_trace()
    pass

test_rendering()
