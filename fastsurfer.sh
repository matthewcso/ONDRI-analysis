#!/bin/bash
#SBATCH --account=def-akhademi-ab
#SBATCH --time=48:00:00
#SBATCH --gpus-per-node=1
#SBATCH --mem=4000M

module load apptainer

for file in /home/mso/ONDRI-analysis/data/T1/*
do
    echo $file
    file_basename=$(basename "$file")
    file_basename=${file_basename%.*}
    file_basename=${file_basename%.*}

    apptainer exec --nv \
                 --no-home \
                 -B /home/mso/ONDRI-analysis/data:/T1 \
                 -B /home/mso/scratch:/outputs  \
                 /home/mso/fastsurfer-gpu.sif \
                 /fastsurfer/run_fastsurfer.sh \
                 --t1 $file \
                 --sid $file_basename --sd /outputs \
                 --seg_only 

done