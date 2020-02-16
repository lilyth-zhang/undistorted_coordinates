import cv2
import numpy as np

class UndistortVideo(object):
    def __init__(self,realtime_img,K,D,DIM,mode,calibrate_choice,scale=0.8,balance=0.3):
        self.realtime_img = realtime_img
        self.K = K
        self.D = D
        self.DIM = DIM
        self.calibrate_choice = calibrate_choice  #默认方法矫正or可视范围更大的矫正
        self.scale = scale   #dim2变化的比例
        self.balance = balance
        self.video_mode = mode
        
    def mapping_choice(self):
        assert self.video_mode in ["normal", "fisheye"], "No such camera mode！"
        if self.video_mode == "normal":
            h, w = self.realtime_img.shape[:2]
            new_K, roi=cv2.getOptimalNewCameraMatrix(self.K, self.D, (w,h), 1, (w,h))
            map1, map2 = cv2.initUndistortRectifyMap(self.K, self.D, np.eye(3), new_K, (w,h), 5)
            return map1,map2,roi
        
        elif self.video_mode == "fisheye":
            assert self.calibrate_choice in ["default", "custom"], "No such calibrateion choice！"
            roi = (0,0,self.realtime_img.shape[:2][0],self.realtime_img.shape[:2][1])
            if self.calibrate_choice == "default":
                map1, map2 = cv2.fisheye.initUndistortRectifyMap(self.K, self.D, 
                                                                 np.eye(3), self.K,self.DIM,cv2.CV_16SC2)
            elif self.calibrate_choice == "custom" :
                dim1 = self.realtime_img.shape[:2][::-1]
                assert dim1[0]/dim1[1] == self.DIM[0]/self.DIM[1], "Image to undistort needs to have same aspect ratio as the ones used in calibration"
                dim2 = tuple([int(i*self.scale) for i in dim1])  
                scaled_K = self.K * dim1[0] / self.DIM[0]  # The values of K is to scale with image dimension.
                scaled_K[2][2] = 1.0
                new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(scaled_K, 
                            self.D, dim2, np.eye(3), balance=self.balance)
                map1, map2 = cv2.fisheye.initUndistortRectifyMap(scaled_K, self.D, 
                            np.eye(3), new_K, dim1, cv2.CV_16SC2)    
            return map1,map2,roi
        
       
        
    def return_frames(self):
        map1,map2,roi = self.mapping_choice()
        x, y, w, h = roi
        undistorted_img = cv2.remap(self.realtime_img, map1, map2, 
                                    interpolation=cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT) 
        _image = undistorted_img[y:y+h, x:x+w]
        return_image = cv2.resize(_image,self.realtime_img.shape[:2][::-1])
        yield return_image 