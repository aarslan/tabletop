#!/bin/bash

#SBATCH --time=00:59:00
#SBATCH --mem=64G
##SBATCH -n 8
##SBATCH -N 8-16 
#SBATCH --qos=pri-aarslan ##bibs-tserre-condo
#SBATCH --exclusive
#SBATCH --exclude=smp012,smp013,smp014,smp015

#SBATCH -J disparity_xtract_tabletop
#SBATCH -o /users/aarslan/out/disparity_xtract_%j.out


module unload python
module load enthought
module unload cuda

src_code_dir='/users/aarslan/code/dorsoventral'
joblist='/users/aarslan/joblists/'$1

parallel -j4 -a $joblist

rm $joblist -f
