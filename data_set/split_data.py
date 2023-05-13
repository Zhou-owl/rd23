import os
from shutil import copy
import random

def mkfile(file):
    if not os.path.exists(file):
        os.makedirs(file)
        
# 获取 flower_photos 文件夹下除 .txt 文件以外所有文件夹名（即5种花的类名）
file_path = 'data_set/flower_data/flower_photos'
print(os.getcwd())
flower_class = [cla for cla in os.listdir(file_path) if ".txt" not in cla] 

# 创建 训练集train 文件夹，并由5种类名在其目录下创建5个子目录
mkfile('data_set/flower_data/train')
for cla in flower_class:
    mkfile('data_set/flower_data/train/'+cla+'/'+flower_class[0])
    mkfile('data_set/flower_data/train/'+cla+'/'+flower_class[1])
    mkfile('data_set/flower_data/train/'+cla+'/'+flower_class[2])
    mkfile('data_set/flower_data/train/'+cla+'/'+flower_class[3])
    mkfile('data_set/flower_data/train/'+cla+'/'+flower_class[4])

    
# 创建 验证集val 文件夹，并由5种类名在其目录下创建5个子目录
mkfile('data_set/flower_data/val')
for cla in flower_class:
    mkfile('data_set/flower_data/val/'+cla+'/'+cla)

# 划分比例，训练集 : 验证集 = 9 : 1
train_test_rate = 0.1
error_rate = 0.04 # *4
# 遍历5种花的全部图像并按比例分成训练集和验证集
for count, cla in enumerate(flower_class):
    cla_path = file_path + '/' + cla + '/'  # 某一类别花的子目录
    images = os.listdir(cla_path)		    # iamges 列表存储了该目录下所有图像的名称
    num = len(images)
    val_images = random.sample(images, k=int(num*train_test_rate)) # 从images列表中随机抽取 k 个图像名称
    train_images = [x for x in images if x not in val_images]
    
    print("start processing gt <{}>, total <{}>, val <{}>, train <{}>".format(cla, len(images),len(val_images),len(train_images)))
    with open("output.txt", "a") as f:
        print("start processing gt <{}>, total <{}>, val <{}>, train <{}>".format(cla, len(images),len(val_images),len(train_images)), file=f)

    for valimg in val_images:
    	# eval_index 中保存验证集val的图像名称
					
            image_path = cla_path + valimg
            new_path = os.path.join('data_set/flower_data/val/',cla,cla,valimg)
            copy(image_path, new_path)  # 将选中的图像复制到新路径

            print("val img: " + new_path)


        # 其余的图像保存在训练集train中

    num = len(train_images)
    err_1 = random.sample(train_images, k=int(error_rate*num))
    train_images = [x for x in train_images if x not in err_1]
    err_2 = random.sample(train_images, k=int(error_rate*num))
    train_images = [x for x in train_images if x not in err_2]
    err_3 = random.sample(train_images, k=int(error_rate*num))
    train_images = [x for x in train_images if x not in err_3]
    err_4 = random.sample(train_images, k=int(error_rate*num))
    train_images = [x for x in train_images if x not in err_4]

    error_set = [err_1,err_2,err_3,err_4]



    for trueimg in train_images:
        image_path = cla_path + trueimg
        new_path = os.path.join('data_set/flower_data/train/',cla,cla,trueimg)
        copy(image_path, new_path)
        print("train img (true label): " + new_path)


    for err_x in error_set:
        for x, errimg in enumerate(err_x):
            err_cla = flower_class[(count+x+1) % 5]
            image_path = cla_path + errimg
            new_path = os.path.join('data_set/flower_data/train/',err_cla,cla,errimg)
            copy(image_path, new_path)

            print("train img (gt [{}] label as [{}]): {}".format(cla, err_cla, new_path))  # processing bar
            with open("output.txt", "a") as f:
                print("train img (gt [{}] label as [{}]): {}".format(cla, err_cla, new_path),file=f)  # processing bar


    print("class: " + cla)
    print("total train num: ", num)
    print("image with true label: ", len(train_images))
    print("error rate = ", (num-len(train_images))/num)
    with open("output.txt", "a") as f:
        print("class: " + cla,file=f)
        print("total train num: ", num, file=f)
        print("image with true label: ", len(train_images),file=f)
        print("error rate = ", (num-len(train_images))/num,file=f)

print("processing done!")
with open("output.txt", "a") as f:
    print("processing done!",file=f)

