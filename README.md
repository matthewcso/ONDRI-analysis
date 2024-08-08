DOWNLOADS:
1. Download this repo. 
2. Create folder `data/summary`, `outputs`. Download `ONDO1_FLAIR_Summary.xlsx` and `OND01_T1_Summary.xlsx` and place into folder.
3. run `download_ondri.py`. Required: `client_secrets.json`. Open the link and it will create a `credentials.txt`, and a `data/summary/ONDRI_summary.csv`. It will also populate the `data` folder.

IMAGE REGISTRATION (FLAIR-atlas based):
4. If necessary, run `create_atlases.ipynb` to create `mni_icbm152_nlin_sym_09c_t2_csfnull.nii.gz`.
5. For healthy controls, use [HD-BET](https://github.com/MIC-DKFZ/HD-BET) to extract brainmasks and save to `data/hdbet_mask`.
6. Run `registration.ipynb` to create atlas-based segmentations. Saves to `outputs/registration_images`.

T1 
7. Moved T1 images to compute cluster for FastSurfer analysis. Downloaded `download_ondri.py` on cluster and ran it.  ~`rsync -avz data/T1 mso@graham.computecanada.ca:/home/mso/scratch/T1`~ 
8. On cluster, `cd $SCRATCH`, `mkdir outputs`, `singularity build fastsurfer-gpu.sif docker://deepmi/fastsurfer:latest`
9. On cluster, `sbatch fastsurfer.sh`. The file outputs are strangely scattered across `/scratch` in this case, but it shouldn't matter.
10. Get the results back: `rsync -avz -L --exclude 'fastsurfer-gpu.sif' mso@graham.computecanada.ca:/home/mso/scratch outputs/fastsurfer`

