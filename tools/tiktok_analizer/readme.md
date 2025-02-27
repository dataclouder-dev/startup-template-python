this library need some dependencies, eventhoug is in my current project best thing to do practice is isolate dependencies on this project. 

### Isolate environment for video 
conda env create -f conda_config.yml


### Run Jupiter Notebook 


### Activate env terminal or select on jupiter
conda activate video-analysis


### Tiktok video extraction and analisis. 


### Start Extraction (use ! for command in jupiter)
yt-dlp -o "tik1.mp4" "https://www.tiktok.com/t/ZT2UMvso3/"
