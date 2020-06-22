# vim: set ft=python:

# see the README at https://gist.github.com/phiresky/4bfcfbbd05b3c2ed8645
# source: https://github.com/mpv-player/mpv/issues/2149
# source: https://github.com/mpv-player/mpv/issues/566
# source: https://github.com/haasn/gentoo-conf/blob/nanodesu/home/nand/.mpv/filters/mvtools.vpy

import vapoursynth

core = vapoursynth.get_core()

ignore_threshold=150 #def 400
scene_change_percentage=25 #def 51

dst_fps = display_fps
while (dst_fps > 60):
    dst_fps /= 2

flag = "video_in" in globals()

if flag:
    clip = video_in
    src_fps_num = int(container_fps * 1e8)
    src_fps_den = int(1e8)
else:
    clip = core.ffms2.Source(source=in_filename)

if not (clip.width > 2600 or clip.fps_num/clip.fps_den > 59):
    try:
        if flag:
            clip = core.std.AssumeFPS(clip, fpsnum = src_fps_num, fpsden = src_fps_den)
        else: 
            dst_fps=float(dst_fps)

        analParams = {
            'overlap': 0,
            'search': 3,
            'truemotion': True,
            #'chrome': True,
            #'blksize': 16,
            #'searchparam': 2
        }
        blockParams = {
            'thscd1': ignore_threshold,
            'thscd2': int(scene_change_percentage*255/100),
            'mask': 2,
        }

        dst_fps_num = int(dst_fps * 1e4)
        dst_fps_den = int(1e4)

        sup  = core.mv.Super(clip, pel=2)
        bvec = core.mv.Analyse(sup, isb=True, **analParams)
        fvec = core.mv.Analyse(sup, isb=False, **analParams)
        clip = core.mv.FlowFPS(clip, sup, bvec, fvec, 
                num=dst_fps_num, den=dst_fps_den, 
                **blockParams)
    except: 
        print('se jodió')

clip.set_output()