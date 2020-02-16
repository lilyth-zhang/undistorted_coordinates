import os
import cv2
import numpy as np
from xml.dom.minidom import *
from config import *


class UndistortedBox(object):
    def __init__(self, all_boxes, frame, K, D, img_shape):
        self.all_boxes = all_boxes  
        self.frame = frame
        self.K = K
        self.D = D
        self.img_shape = img_shape
        
    def undistort_box_corr(self, box):
        x_cen = (box[0] + box[2])/2
        y_cen = (box[1] + box[3])/2
        xmin_ori = box[0]/self.img_shape*ori_size
        ymin_ori = box[1]/self.img_shape*ori_size
        xmax_ori = box[2]/self.img_shape*ori_size
        ymax_ori = box[3]/self.img_shape*ori_size
        if (x_cen > self.img_shape/2 and y_cen < self.img_shape/2) or (x_cen < self.img_shape/2 and y_cen > self.img_shape/2):  #左上或右下
            points = [[[xmin_ori, ymax_ori]], [[xmax_ori, ymin_ori]]]
            points = np.array(points, dtype=np.float32)
            undist_points = cv2.undistortPoints(points, self.K, self.D, P=self.K).reshape(1,4).tolist()[0] 
            xmin, ymax, xmax, ymin = undist_points
        else:   #左下或右上
            points = [[[xmin_ori, ymin_ori]], [[xmax_ori, ymax_ori]]]
            points = np.array(points, dtype=np.float32)
            undist_points = cv2.undistortPoints(points, self.K, self.D, P=self.K).reshape(1,4).tolist()[0] 
            xmin, ymin, xmax, ymax = undist_points
        xmin = int(xmin/ori_size*self.img_shape)
        ymax = int(ymax/ori_size*self.img_shape)
        xmax = int(xmax/ori_size*self.img_shape)
        ymin = int(ymin/ori_size*self.img_shape)
        return xmin, ymin, xmax, ymax
    
    
    def rec_area(self, xmin, ymin, xmax, ymax):   #判断是否需要把矩形去掉
        real_xmin = min(max(0, xmin), self.img_shape)
        real_ymin = min(max(0, ymin), self.img_shape)
        real_xmax = min(max(0, xmax), self.img_shape)
        real_ymax = min(max(0, ymax), self.img_shape)        
        
        ideal_area = (xmax - xmin) * (ymax - ymin)
        real_area = (real_xmax - real_xmin) * (real_ymax - real_ymin)
        
        if real_area == 0 or real_area/ideal_area < 0.35:
#             print('面积不够 ', real_xmin, real_ymin, real_xmax, real_ymax)
            return False
        elif real_xmin > real_xmax or real_ymin > real_ymax:
#             print('坐标错位 ', real_xmin, real_ymin, real_xmax, real_ymax)
            return False
        elif real_xmax - real_xmin > self.img_shape/5 or real_ymax - real_ymin > self.img_shape/5:   
#             print('人头太大 ', real_xmin, real_ymin, real_xmax, real_ymax )
            return False
        else:
            return real_xmin, real_ymin, real_xmax, real_ymax
        
        
        
    
    def frame_xml(self):
        res_list = []
        for box in self.all_boxes:
            xmin, ymin, xmax, ymax = self.undistort_box_corr(box)
            if self.rec_area(xmin, ymin, xmax, ymax):
                xmin, ymin, xmax, ymax = self.rec_area(xmin, ymin, xmax, ymax)
                self.frame = cv2.rectangle(self.frame, (xmin, ymin), (xmax, ymax), (54,243,75), 10)    
                res_list.append([xmin, ymin, xmax, ymax])
        return self.frame, res_list
                
    
