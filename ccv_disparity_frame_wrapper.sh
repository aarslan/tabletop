#!/bin/bash

CODE_DIR=/gpfs/home/aarslan/code/tabletop
FRAMES_DIR=/gpfs/data/tserre/Users/aarslan/tabletop_mono/frames_full_def
TARGET_DIR=/gpfs/data/tserre/Users/aarslan/tabletop_mono/features

TEMP_DIR=/gpfs/home/aarslan/joblists

JOB_COUNT=100

data_in=$ANGLES_DIR
data_out=$TARGET_DIR


##Here, we make the big joblist and split them into multiple parts
find $FRAMES_DIR/*/l/ -name "*.png" | awk '{print "python /gpfs/home/aarslan/code/tabletop/process_directory_stereo.py --src_dir "$0 " --target_dir /gpfs/data/tserre/Users/aarslan/tabletop_mono/features"}' >> $TEMP_DIR/biglist.txt
split  $TEMP_DIR/biglist.txt  $TEMP_DIR/part -d -l $JOB_COUNT



for f in part*;
do 
	sbatch ./ccv_disparity_frame_core.sh $TEMP_DIR/$f
	sleep 0.5
done

