import computation as comp, models as mod, params_ali
import matplotlib as mlp
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import os
import argparse
import time
#from hmax.models.dorsal import get_c1, prepare_cuda_kernels, pyramid_vid

def process_frame(src_dir, vid_type, this_fr, target_dir):
	target_stereo_dir = os.path.join(target_dir, vid_type)

	par = params_ali.ventral_absolute_disparity_tabletop()
	#import ipdb; ipdb.set_trace()

	start_time = time.time()
	imleft = os.path.join(src_dir, vid_type, 'l', this_fr);
	imright = os.path.join(src_dir, vid_type, 'r', this_fr);
	print 'loading '+imright
	print 'loading '+imleft
	im = []; im.append(imleft); im.append(imright);
	features = mod.absolute_disparity(par, im)
	
	av_features = np.mean(np.mean(features, axis = 0),axis=1)
	D = np.argmax(av_features, axis=0);
	mD = np.squeeze(np.max(av_features, axis=0, keepdims=True));
	res = sp.array(D*(mD>0.9)/1, dtype='uint8')
	#plt.matshow(res)
	#plt.show()
	#import ipdb; ipdb.set_trace()
	mat_name = os.path.join(target_stereo_dir, this_fr[0:-4])
	if not os.path.exists(target_stereo_dir):
		os.makedirs(target_stereo_dir)
	#sp.io.savemat(mat_name, {'fr': res})
	sp.io.savemat(mat_name, {'fr': np.array(np.mean(features,axis=2),dtype='Float32')})
	elapsed_time = time.time()-start_time
	print elapsed_time

#plt.imshow(res)
#plt.show()


def main():
	parser = argparse.ArgumentParser(description=""" """)
	parser.add_argument('--src_dir', type=str, default='/home/aarslan/prj/data/tabletop/frames_full_def/')
	parser.add_argument('--vid_type', type=str, default='none')
	parser.add_argument('--this_fr', type=int, default=-999)
	parser.add_argument('--target_dir', type=str, default='/home/aarslan/prj/data/tabletop/features_depth/frames_full_def/')
	
	args = parser.parse_args()
	src_dir = args.src_dir
	vid_type = args.vid_type
	this_fr = args.this_fr
	target_dir = args.target_dir
	
	if this_fr == -999:
		path_parts = src_dir.split('/')
		this_fr = path_parts[-1]
		vid_type = path_parts[-3]
		src_dir = os.path.split(os.path.split(os.path.split(src_dir)[0])[0])[0]
	import ipdb; ipdb.set_trace()
	target_dir = args.target_dir
	process_frame(src_dir, vid_type, this_fr, target_dir)

if __name__=="__main__":
	main()
    
