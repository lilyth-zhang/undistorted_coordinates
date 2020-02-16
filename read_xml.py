import os
import cv2
import numpy as np
from xml.dom.minidom import *

def xml_read(xml_name):   #从xml里面提取要的信息
    xml_dict = {}

    xml_dict["folder"] = xml_name.split(os.path.sep)[-2]
    # 使用minidom解析器打开 XML 文档
    DOMTree = xml.dom.minidom.parse(xml_name)
    collection = DOMTree.documentElement

    filename = collection.getElementsByTagName("filename")[0]
    xml_dict["filename"] = filename.childNodes[0].data.split(".")[0]

    width = collection.getElementsByTagName("width")[0]
    xml_dict["width"] = width.childNodes[0].data

    height = collection.getElementsByTagName("height")[0]
    xml_dict["height"] = height.childNodes[0].data

    objs = collection.getElementsByTagName("object")
    for num, obj in enumerate(objs):
        obj_num = "obj_" + str(num+1)
        xml_dict[obj_num] = {}
        fields = ['name', 'xmin', 'xmax', 'ymin', 'ymax']
        for f_name in fields:
            f_node = obj.getElementsByTagName(f_name)[0]
            xml_dict[obj_num][f_name] = f_node.childNodes[0].data
    return xml_dict


def parse_ann(xml_path):   #把xml里面的东西弄出来
    xml_dict = xml_read(xml_path)
    img_shape = (int(xml_dict['height']), int(xml_dict['width']), 3)
    all_ids = []
    all_boxes = []
    for k, v in xml_dict.items():
        if k.startswith('obj'):
            all_ids.append(0)
            all_boxes.append([  int(v['xmin'])
                              , int(v['ymin'])
                              , int(v['xmax'])
                              , int(v['ymax'])] )
    return img_shape, np.asarray(all_boxes), np.asarray(all_ids)