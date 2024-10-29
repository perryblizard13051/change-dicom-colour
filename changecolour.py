import os
import pydicom 
from pydicom import encaps
import numpy
from numpy import asarray
from PIL import Image



#set source path for dicoms##
src_path = r'/DICOM_alteration/test_dicom'

save_path = r'/DICOM_alteration/colour_change'

ds = pydicom.dcmread(src_path+ '/' +'FILENAME')

pixel_data = ds.pixel_array
#pull one from to test the pixel function on
snap_shot = pixel_data[1]
#turn array into image
img = Image.fromarray(snap_shot, 'RGB')
#change colour of top 10% of pixels
for x in range(800):
    for y in range(60):
        img.putpixel((x,y),(210,210,210)) 
img = numpy.array(img)    
#convert back to bytes and overwrite pixel data
ds.PixelData = img.tobytes()
ds.save_as(save_path +'/'+ 'output.dcm' , write_like_original= True)





##trying to implement the above into a loop so that all frames are saved back to the DICOM image



import os
import pydicom 
from pydicom import encaps
import numpy
from numpy import asarray
from PIL import Image

#set source path for dicoms##
src_path = r'/DICOM_alteration/test_dicom'

save_path = r'/DICOM_alteration/colour_change'

ds = pydicom.dcmread(src_path+ '/' +'FILENAME')

#pull pixel data from DICOM
pixel_data = ds.pixel_array

frames,height,width, channels = pixel_data.shape
#need a non int value to use enumerate
ind = [pixel_data.shape[0]]

#create empty numpy array
list = numpy.zeros((pixel_data.shape[0],600,800,3))
#try to loop through DICOM slices and change pixels before adding to above array
for index,i in enumerate(ind):
    dicom_slice = pixel_data[i ,:,:,:]
    img = Image.fromarray(dicom_slice, 'RGB')
    for x in range(800):
        for y in range(60):
            img.putpixel((x,y),(210,210,210)) 
    img = numpy.array(img)
    #numpy.append((list,img.reshape(1,600,800,3))) 
    numpy.insert(list,img.reshape(1,600,800,3))

ds.PixelData = encaps.encapsulate(list.tobytes())          

ds.save_as(save_path +'/'+ 'output.dcm' , write_like_original= True)
