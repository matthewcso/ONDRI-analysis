apptainer exec \
                 --no-home \
                 -B ~/ONDRI-analysis-new/data:/T1 \
                 -B ~/ONDRI-analysis-new/outputs:fastsurfer \

                 ./fastsurfer-gpu.sif \
                 /fastsurfer/run_fastsurfer.sh \
                --seg_only 
