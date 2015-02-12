import os
import sys
import string
import math
import PIL
import PIL.Image
import lxml
import lxml.etree
import glob
import numpy as np

tile_num_pixels_y = 512
tile_num_pixels_x = 512

original_input_images_path = r'C:\dev\datasets\conn\main_dataset\ac3train\input_images'
output_tile_image_path     = r'C:\dev\datasets\ac3x20\mojo\images\tiles'
output_tile_volume_file    = r'C:\dev\datasets\ac3x20\mojo\images\tiledVolumeDescription.xml'
input_image_extension      = '.tif'
output_image_extension     = '.jpg'
image_resize_filter        = PIL.Image.ANTIALIAS
nimages_to_process         = 20


def mkdir_safe( dir_to_make ):

    if not os.path.exists( dir_to_make ):
        os.makedirs(dir_to_make)
        # execute_string = 'mkdir ' + '"' + dir_to_make + '"'
        # print execute_string
        # print
        # os.system( execute_string )
                
        
files = sorted( glob.glob( original_input_images_path + '\\*' + input_image_extension ) )

tile_index_z = 0

for file in files:

    original_image = PIL.Image.open( file )

    # Note - size returns reverse order to shape
    ( original_image_num_pixels_x, original_image_num_pixels_y ) = original_image.size

    # Enhance contrast to 2% saturation
    saturation_level = 0.02
    pix_sorted = np.sort( np.uint8(original_image).ravel() )
    minval = np.float32( pix_sorted[ len(pix_sorted) * ( saturation_level / 2 ) ] )
    maxval = np.float32( pix_sorted[ len(pix_sorted) * ( 1 - saturation_level / 2 ) ] )

    original_image = original_image = original_image.point(lambda i: (i - minval) * ( 255 / (maxval - minval)))

    current_image_num_pixels_y = original_image_num_pixels_y
    current_image_num_pixels_x = original_image_num_pixels_x
    current_tile_data_space_y  = tile_num_pixels_y
    current_tile_data_space_x  = tile_num_pixels_x
    tile_index_w               = 0

    while current_image_num_pixels_y > tile_num_pixels_y / 2 or current_image_num_pixels_x > tile_num_pixels_x / 2:
    
        current_tile_image_path    = output_tile_image_path     + '\\' + 'w=' + '%08d' % ( tile_index_w ) + '\\' + 'z=' + '%08d' % ( tile_index_z )

        mkdir_safe( current_tile_image_path )

        current_image = original_image.resize( ( current_image_num_pixels_x, current_image_num_pixels_y ), image_resize_filter )
        
        num_tiles_y = int( math.ceil( float( current_image_num_pixels_y ) / tile_num_pixels_y ) )
        num_tiles_x = int( math.ceil( float( current_image_num_pixels_x ) / tile_num_pixels_x ) )

        for tile_index_y in range( num_tiles_y ):
            for tile_index_x in range( num_tiles_x ):

                y = tile_index_y * tile_num_pixels_y
                x = tile_index_x * tile_num_pixels_x

                current_tile_image_name = current_tile_image_path + '\\' + 'y=' + '%08d' % ( tile_index_y ) + ','  + 'x=' + '%08d' % ( tile_index_x ) + output_image_extension

                tile_image = current_image.crop( ( x, y, x + tile_num_pixels_x, y + tile_num_pixels_y ) )     
                tile_image.save( current_tile_image_name )
                print current_tile_image_name
                print
                
        current_image_num_pixels_y = current_image_num_pixels_y / 2
        current_image_num_pixels_x = current_image_num_pixels_x / 2
        current_tile_data_space_y  = current_tile_data_space_y  * 2
        current_tile_data_space_x  = current_tile_data_space_x  * 2
        tile_index_w               = tile_index_w + 1
        
    tile_index_z = tile_index_z + 1

    if tile_index_z >= nimages_to_process:
        break

#Output TiledVolumeDescription xml file
tiledVolumeDescription = lxml.etree.Element( "tiledVolumeDescription",
    fileExtension = output_image_extension[1:],
    numTilesX = str( int( math.ceil( original_image_num_pixels_x / tile_num_pixels_x ) ) + ((original_image_num_pixels_x % tile_num_pixels_x) > 0) ),
    numTilesY = str( int( math.ceil( original_image_num_pixels_y / tile_num_pixels_y ) ) + ((original_image_num_pixels_x % tile_num_pixels_x) > 0) ),
    numTilesZ = str( tile_index_z ),
    numTilesW = str( tile_index_w ),
    numVoxelsPerTileX = str( tile_num_pixels_x ),
    numVoxelsPerTileY = str( tile_num_pixels_y ),
    numVoxelsPerTileZ = str( 1 ),
    numVoxelsX = str( original_image_num_pixels_x ),
    numVoxelsY = str( original_image_num_pixels_y ),
    numVoxelsZ = str( tile_index_z ),
    dxgiFormat = 'R8_UNorm',
    numBytesPerVoxel = str( 1 ),      
    isSigned = str( False ).lower() )
    
with open( output_tile_volume_file, 'w' ) as file:
    file.write( lxml.etree.tostring( tiledVolumeDescription, pretty_print = True ) )


