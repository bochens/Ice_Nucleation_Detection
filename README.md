# Ice_Nucleation_Detection

## Introduction

The Ice Nucleation Detection code is for automatically detecting freezing event in ice nucleation experiments on cold stage. This code is created and used by Bo Chen and Dr. Sarah D. Brooks group at Texas A&M University.

1. image_deres.py is for resizing the image
2. grayscale_sum.py is for selecting droplet on image and calculating total gray scale value of each droplet on each image. The results are saved in an output file.
3. freeze_finder.py is for detecitng a freezing event from the output of the grayscale_sum.py. When freezing, the gray scale of the droplet drops immediately due to change of refractive index. Such change is detected using a convolution with a step change function.
