import os
import sys
import glob
import tqdm
import numpy as np
from tqdm import tqdm
import pandas as pd
import xml.etree.cElementTree as ET

def getXMLFromOpenFaceData(path_folder_openface_data, path_output_xml):
    """
    Generates XML data file from a folder containing the output csv files from OpenFace.

	Usage: If executing in scripts folder,
			1. activate detect_face environment 
			2. Run: python openface_to_xml.py 

    Parameters
    ----------
    path_folder_openface_data : str
    	Path where all the OpenFace outputs(csv files) are stored.

    path_output_xml : str
    	Path where the output will be stores as openface_no_of_folders.xml.

    Returns
    -------
	None
    """
    
    list_csv_files = glob.glob(path_folder_openface_data + '/*.csv')
    
    #Generate XML file.
    root = ET.Element("dataset")
    name = ET.SubElement(root, "name").text = "Labelled faces"
    comment = ET.SubElement(root, "comment").text = "These are labelled images from Bagamoyo"
    images = ET.SubElement(root, "images")

    # Read csv file and populate the XML data.
    for path_csv in tqdm(list_csv_files):
        name_video = os.path.splitext(os.path.basename(path_csv))[0]
        df_data = pd.read_csv(path_csv)
        
        # Iterate over each frame in this video's output
        for index, row in df_data.iterrows():
            #define the image node for which box will be a child.
            frame_num = row.frame
            image_node_file_name = name_video + " " + "%03d"%frame_num + ".jpg"
            image_node=None
            #check if the attribute for frame already exists, create if not.
            for image_elem in images.findall('image'):
                file_name = image_elem.get('file')
                if(file_name == image_node_file_name):
                    image_node = image_elem
                    print("found")
            if(image_node is None):
                image_node = ET.SubElement(images, "image", file=image_node_file_name)
                
            #get box coordinates
            list_x_coord_landmarks = list(row[' x_0':' x_67']) 
            list_y_coord_landmarks = list(row[' y_0':' y_67'])
            left = int(min(list_x_coord_landmarks))
            right = int(max(list_x_coord_landmarks))
            top = int(min(list_y_coord_landmarks))
            bottom = int(max(list_y_coord_landmarks))
            width = right - left
            height = bottom - top
            #add box node
            box = ET.SubElement(image_node, "box", height=str(height), left=str(left), top=str(top), width=str(width))
    
    #save the XML
    tree = ET.ElementTree(root)
    dest_name = path_output_xml + 'openface_{}_folders.xml'.format(len(list_csv_files))
    tree.write(dest_name)
    print("xml written to {}".format(dest_name))  

def main(argv):
	
	#read commandline arguments
	path_folder_openface_data = argv[1]
	path_output_xml = argv[2]

	#run and save XML
	getXMLFromOpenFaceData(path_folder_openface_data, path_output_xml)


if __name__ == '__main__':
	main(sys.argv)