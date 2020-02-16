项目在Pytho 3.6.8版本, ubantu下运行。

# ss摄像头标注图片+bounding box矫正

### 项目总体介绍

用ss摄像头拍摄并标注的图片存在一定的畸变，标注的bounding box也是在存在畸变的图片上标注的。本项目用测试摄像头训练得到的变换参数来线性变换标注的bounding box，并求外接矩形，生成新的xml文件和可视化结果。

### 项目前提条件

- 需要安装的库见 ```./requirements.txt```
- 全局变量设置见 ```./config.txt```

### 模块功能

- 利用摄像头参数矫正图片  ```calib_img.py```
- 读取原始图片的xml文件，获得bounding box的坐标和图片size  ```read_xml.py```
- 根据bounding box的原始坐标，利用摄像头参数获得在矫正后的坐标系下的新的bounding box的坐标，并在矫正后的图片中画出新的bounding box  ```undis_box.py```
- 将矫正后坐标保存到xml文件   ```write_xml.py```

### 使用方法
- ```example.py```   按实际需要修改config中待矫正的图片xml路径。


