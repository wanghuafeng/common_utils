#!-*- coding:utf-8 -*-
# image_merge.py
# 图片垂直合并
import os
import Image

def image_resize(img, size=(1500, 1100)):
    """调整图片大小
    """
    try:
        if img.mode not in ('L', 'RGB'):
            img = img.convert('RGB')
        img = img.resize(size)
    except Exception, e:
        pass
    return img

def image_merge(images, output_dir='output', output_name='merge.jpg',
                restriction_max_width=None, restriction_max_height=None):
    """垂直合并多张图片
    images - 要合并的图片路径列表
    ouput_dir - 输出路径
    output_name - 输出文件名
    restriction_max_width - 限制合并后的图片最大宽度，如果超过将等比缩小
    restriction_max_height - 限制合并后的图片最大高度，如果超过将等比缩小
    """
    max_width = 0
    total_height = 0
    # 计算合成后图片的宽度（以最宽的为准）和高度
    for img_path in images:
        if os.path.exists(img_path):
            img = Image.open(img_path)
            width, height = img.size
            if width > max_width:
                max_width = width
            total_height += height

    # 产生一张空白图
    new_img = Image.new('RGB', (max_width, total_height), 255)
    # 合并
    x = y = 0
    for img_path in images:
        if os.path.exists(img_path):
            img = Image.open(img_path)
            width, height = img.size
            new_img.paste(img, (x, y))
            y += height

    if restriction_max_width and max_width >= restriction_max_width:
        # 如果宽带超过限制
        # 等比例缩小
        ratio = restriction_max_height / float(max_width)
        max_width = restriction_max_width
        total_height = int(total_height * ratio)
        new_img = image_resize(new_img, size=(max_width, total_height))

    if restriction_max_height and total_height >= restriction_max_height:
        # 如果高度超过限制
        # 等比例缩小
        ratio = restriction_max_height / float(total_height)
        max_width = int(max_width * ratio)
        total_height = restriction_max_height
        new_img = image_resize(new_img, size=(max_width, total_height))

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    save_path = '%s/%s' % (output_dir, output_name)
    new_img.save(save_path)
    return save_path

if __name__ == '__main__':
    image_merge(images=['900-000-000-0501a_b.jpg', '900-000-000-0501b_b.JPG', '1216005237382a_b.jpg'])



def image_merge(images, output_dir='output', output_name='merge.jpg'):
    max_width = 84
    max_height = 30
    new_img = Image.new('RGB', (max_width, max_height), 255)
    x = y = 0
    for img_path in images:
        if os.path.exists(img_path):
            img = Image.open(img_path)
            width, height = img.size
            new_img.paste(img, (x, y))
            x += width
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    save_path = '%s/%s' % (output_dir, output_name)
    new_img.save(save_path)
    return save_path

if __name__ == '__main__':
    pl = r'D:\py_project\fi\pic\InsuranceDeZhou_left.jpg'
    po = r'D:\py_project\fi\pic\InsuranceDeZhou_operator.jpg'
    pr = r'D:\py_project\fi\pic\InsuranceDeZhou_right.jpg'
    pe = r'D:\py_project\fi\pic\InsuranceDeZhou_equals.jpg'
    image_merge(images=[pl, po, pr, pe], output_dir=r'D:\py_project\fi\pic')