import os
import segyio
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageEnhance

def normalize(slice_data):
    slice_data /= max(np.abs(slice_data.min()), np.abs(slice_data.max()))
    slice_data = slice_data / 2 + 0.5
    return slice_data

def save_image(slice_data):
    image = color_map(data)[:,:,:3]
    image = Image.fromarray(np.uint8(image*255))
    image = ImageEnhance.Contrast(image).enhance(1.2)
    resized_image = image.resize((500,500))
    if key == 'inline':
        resized_image.save(os.path.join(path_to_save, key + '_'+ str(ilines[slice])+'.png'))
    else: 
        resized_image.save(os.path.join(path_to_save, key + '_'+ str(xlines[slice])+'.png'))
    return resized_image

def plt_verticalslice(seis_data, key):
    vm = np.percentile(seis_data,95)
    plt.imshow(data.T, cmap='gray', aspect='auto', vmin=-vm, vmax=vm)

    plt.xlabel('{}_indx'.format(key))
    plt.ylabel('TIME_indx')
    plt.show()
    
if __name__ == "__main__":
    path_to_dataset =  os.path.join('..','faultSeg','data','prediction','Poseidon','psdn11_TbsdmF_full_w_AGC_Nov11_8bit_cropped.segy')
    path_to_save    =  os.path.join('images')
    
    if not os.path.isdir(path_to_save):
        os.makedirs(path_to_save)
    
    # Define the colormap for the saved images
    color_map = plt.cm.seismic
    
    with segyio.open(path_to_dataset) as segyfile:
        # Memory map file for faster reading (especially if file is big)s
        segyfile.mmap()
        seis_data = segyio.tools.cube(segyfile)
        print(seis_data.shape)
        
        # This one  you need to edit
        # Select slices to convert (loop with interval)
        ilines = segyfile.ilines[:800:100]
        xlines = segyfile.xlines[:800:100]
        slices_to_save = {'inline': [np.where(ilines==i)[0][0] for i in ilines], 'xline': [np.where(xlines==i)[0][0] for i in xlines]}
        
        for key in slices_to_save:
            for slice in slices_to_save[key]:
                data = segyfile.iline[segyfile.ilines[slice]] if (key=='inline') else segyfile.xline[segyfile.xlines[slice]]
                # plt_verticalslice(data, key)
                data = normalize(data.T)
                resized_image = save_image(data) 

                image = np.array(resized_image)
                print(image.shape)
                # print(image)