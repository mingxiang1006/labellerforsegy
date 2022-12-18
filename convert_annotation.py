import os 
import numpy as np
import segyio
from image_labelling_tool import labelled_image

if __name__ == "__main__":
    path_to_dataset = r''
    path_to_load    = r''
    
    # This one need to edit
    # Select slices to load from annotation files
    
    train_slice = []
    train_segmentation = []
    
    with segyio.open(path_to_dataset) as segyfile:
        # Memory map 
        segyfile.mmap()
        seis_data = segyio.tools.cube(segyfile)
        ilines = segyfile.ilines[:800:100]
        xlines = segyfile.xlines[:800:100]
        slices_to_load = {'inline': [np.where(ilines==i)[0][0] for i in ilines], 'xline': [np.where(xlines==i)[0][0] for i in xlines]}
        
        for key in slices_to_load:
            for slice in slices_to_load[key]:
                data  = segyfile.iline[segyfile.ilines[slice]] if (key=='inline') else segyfile.xline[segyfile.xlines[slice]]
                