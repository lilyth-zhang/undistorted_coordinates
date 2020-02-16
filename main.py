import os
import cv2
import numpy as np
import pickle
from config import *
from undis_box import *
from calib_img import *
from write_xml import *
from read_xml import *
from xml.dom.minidom import parse
import xml.dom.minidom




        
def undistorted_video(path,K,D,DIM,mode,calibrate_choice,img_shape):
    frame = cv2.imread(path)
    frame = cv2.resize(frame, (ori_size, ori_size))
    result = UndistortVideo(frame, K, D, DIM, mode, calibrate_choice)
    result_frame = result.return_frames()
    for rf in result_frame:
        rf = cv2.resize(rf, (img_shape, img_shape))
        return rf

def K_D_DIM(sn):
    path = './params/SN%s.json' % sn
    f = open(path, 'rb')
    k_d_dim = pickle.load(f)
    return k_d_dim

    
    
if __name__ == '__main__':
    
    mode = 'normal'
    calibrate_choice = 'nochoice'
    k_d_dim = K_D_DIM('cam')
    K = np.array(k_d_dim['K'])
    D = np.array(k_d_dim['D'])
    DIM = k_d_dim['DIM']
      
    
    for xml_file in xml_total_3f:
        for file in os.listdir(os.path.join(root_dir, xml_file)):
            ann_path = os.path.join(root_dir, xml_file, file)
            img_path = os.path.join(root_dir, xml_file.replace('xml','to_ann'),file.replace('.xml', '.jpg'))
            if ann_path.endswith('.xml'):
                print(ann_path)
                try:
                    img_shape, all_boxes, all_ids = parse_ann(ann_path)   #从xml文件获取要的信息
                    cal_frame = undistorted_video(img_path, K, D, DIM, mode, calibrate_choice, img_shape[0])
                    UB = UndistortedBox(all_boxes, cal_frame, K, D, img_shape[0])
                    vis_frame, res_list = UB.frame_xml()
                    xml_write(img_name = file
                            ,path_dir = './total_3f/xml'
                            ,data_dict = {'label':'head', 'imageHeight':img_shape[0], 'imageWidth':img_shape[1], 'bndbox':res_list})
                    vis_path = os.path.join('./total_3f/vis', file.replace('xml', 'jpg'))
                    cv2.imwrite(vis_path, vis_frame)
                except:
                    print('{} is empty!'.format(ann_path))
