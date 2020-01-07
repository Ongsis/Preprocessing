input_path = '/Volumes/Seagate/Boneage/Session1_Sort/Normal/Female'                                                     
output_path = '/Volumes/Seagate/Boneage/Session1_Sort/Normal_Resampled/Female'                                          
                                                                                                                        
list_dcm = os.listdir(input_path)                                                                                       
                                                                                                                        
for img_name in list_dcm:                                                                                               
#for i in range(0, 2):                                                                                                  
    img_dcm = dcm.read_file(os.path.join(input_path, img_name))                                                         
    img_dcm.decompress()                                                                                                
    image = img_dcm.pixel_array                                                                                         
                                                                                                                        
    target_spacing = 0.2                                                                                                
                                                                                                                        
    # Determine current pixel spacing                                                                                   
    if 'PixelSpacing' in img_dcm:                                                                                       
        origin_spacing = img_dcm.PixelSpacing                                                                           
    elif 'ImagerPixelSpacing' in img_dcm:                                                                               
        origin_spacing = img_dcm.ImagerPixelSpacing                                                                     
    #print("pixel_spacing: {}".format(origin_spacing))                                                                  
                                                                                                                        
    #print("original: {}\t new: {}".format(image.shape,iso_image.shape))                                                
                                                                                                                        
    new_spacing = [target_spacing, target_spacing]  # set target spacing value                                          
    # ----------------- Resampling ----------------- #                                                                  
    origin_spacing = np.array([float(origin_spacing[0]), float(origin_spacing[1])])  # modify the format of spacing     
    resize_factor = origin_spacing / new_spacing                                                                        
    new_real_shape = image.shape * resize_factor                                                                        
    new_shape = np.round(new_real_shape)                                                                                
    real_resize_factor = new_shape / image.shape                                                                        
    new_spacing = origin_spacing / real_resize_factor                                                                   
                                                                                                                        
    iso_image = ndimage.interpolation.zoom(image, real_resize_factor)  # modified pixel array                           
                                                                                                                        
    # ----------------- Modify the metadata as resampling ----------------- #                                           
    img_dcm.Rows, img_dcm.Columns = iso_image.shape  # change the size of image                                         
    #print(iso_image.shape)                                                                                             
    print("{}\t original: {}\t new: {}".format(img_name, image.shape, iso_image.shape))                                 
    if 'PixelSpacing' in img_dcm: # change the pixel spacing                                                            
     img_dcm.PixelSpacing[0] = target_spacing                                                                           
     img_dcm.PixelSpacing[1] = target_spacing                                                                           
    elif 'ImagerPixelSpacing' in img_dcm:                                                                               
     img_dcm.ImagerPixelSpacing[0] = target_spacing                                                                     
     img_dcm.ImagerPixelSpacing[1] = target_spacing                                                                     
                                                                                                                        
    img_dcm.PixelData = iso_image.tobytes()  # convert the pixel array to byte                                          
    img_dcm.save_as(os.path.join(output_path, img_name.split('.')[0] + '_2.dcm'))  # save the result dicom file         
                                                                                                                        
    # plt.imshow(iso_image, cmap=plt.cm.bone)                                                                           
    # plt.title('new spacing')                                                                                          
    # plt.show()                                                                                                        
    # -----------------------                                                                                           
