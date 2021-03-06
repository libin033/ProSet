#coding:utf-8
import imageio
import os
from PIL import Image, ImageDraw

'''
def Create_GIF():
    inpath = r"G:\ProductAnalysis\python\DATA\Image"
    #
    frames = []
    #
    filels = os.listdir(inpath)
    filels.sort()
    #filels = ["AT_Prof_500.jpg","AT_Prof_700.jpg","AT_Prof_850.jpg","AT_Prof_1000.jpg"]
    #for item in range(32):
    for item in range(101):

        filename = os.path.join(inpath, "%s.png" % item)
        print(filename)
        frames.append(imageio.imread(filename))

    imageio.mimsave(os.path.join(inpath, "AT_V.gif"), frames, "GIF", duration = 0.1)
'''

def Create_GIF(filels, outname, duration=0.1):
    '''
    使用 imageio 生成 GIF
    :param files: 输入需要创建GIF的图片列表
    :param outname: 输出GIF文件名
    :param duration: 时间间隔，控制GIF播放速度
    :return:
    '''
    #print(filels)
    frames = []
    inpath = os.path.dirname(outname)
    if not os.path.isdir(inpath):
        print("%s is not exist, will be create!!" % inpath)
        os.makedirs(inpath)

    if not outname.endswith(".gif") and not outname.endswith(".GIF"):
        outname[-4:-1] = ".gif"

    print("outname:",outname)
    num = 0
    for item in filels:
        if not item.endswith(".jpg") and not item.endswith(".png"):
            print(not item.endswith(".jpg") , not item.endswith(".png"))
            continue

        if not os.path.isfile(item):
            print("%s not exist, will be continue !!!!" % item)
            continue
        num += 1
        print("%d:%s" % (num,item))
        frames.append(imageio.imread(item))

    imageio.mimsave(outname, frames, "GIF", duration = duration)


def analyseImage(path):
    '''
    Pre-process pass over the image to determine the mode (full or additive).
    Necessary as assessing single frames isn't reliable. Need to know the mode
    before processing all frames.
    '''
    im = Image.open(path)
    results = {
        'size': im.size,
        'mode': 'full',
    }
    try:
        while True:
            if im.tile:
                tile = im.tile[0]
                update_region = tile[1]
                update_region_dimensions = update_region[2:]
                if update_region_dimensions != im.size:
                    results['mode'] = 'partial'
                    break
            im.seek(im.tell() + 1)
    except EOFError:
        pass
    return results


def processImage(path):
    '''
    拆解GIF文件，还原成单幅图像
    Iterate the GIF, extracting each frame.
    '''
    mode = analyseImage(path)['mode']

    im = Image.open(path)

    i = 0
    p = im.getpalette()
    last_frame = im.convert('RGBA')

    try:
        while True:
            print("saving %s (%s) frame %d, %s %s" % (path, mode, i, im.size, im.tile))

            '''
            If the GIF uses local colour tables, each frame will have its own palette.
            If not, we need to apply the global palette to the new frame.
            '''
            if not im.getpalette():
                im.putpalette(p)

            new_frame = Image.new('RGBA', im.size)

            '''
            Is this file a "partial"-mode GIF where frames update a region of a different size to the entire image?
            If so, we need to construct the new frame by pasting it on top of the preceding frames.
            '''
            if mode == 'partial':
                new_frame.paste(last_frame)

            new_frame.paste(im, (0,0), im.convert('RGBA'))
            new_frame.save('%s-%d.png' % (''.join(os.path.basename(path).split('.')[:-1]), i), 'PNG')

            i += 1
            last_frame = new_frame
            im.seek(im.tell() + 1)
    except EOFError:
        pass


def get_gif(fils, outname, t=0.1):
    '''
    使用 Image 生成 GIF
    :param files: 输入需要创建GIF的图片列表
    :param outname: 输出GIF文件名
    :param t: 时间间隔，控制GIF播放速度
    :return:
    '''
    imgs = []
    for item in fils:
        print(item)
        if not item.endswith(".jpg") and not item.endswith(".png"):
            print(not item.endswith(".jpg") , not item.endswith(".png"))
            continue

        if not os.path.isfile(item):
            print("%s not exist, will be continue !!!!" % item)
            continue

        temp = Image.open(item)
        imgs.append(temp)

    imgs[0].save(outname, save_all=True, append_images=imgs, duration=t)

    return outname


if __name__ == '__main__':
    pathin = r'F:\trace'
    fils = os.listdir(pathin)
    fils.sort()
    filename = []
    for ifile in fils:
        filename.append(os.path.join(pathin, ifile))

    # 使用 imageio 生成 GIF
    Create_GIF(filename, r"F:\trace\GIF\Trace1.GIF", 0.5)

    # 使用 Image 生成 GIF
    # get_gif(filename, r"F:\trace\GIF\Trace2.GIF", 0.5)
    # get_gif(filename, r"G:\ProductAnalysis\python\GIFProcess\data\get_gif.GIF")
    #processImage("1.gif")

