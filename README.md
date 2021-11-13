# VirtualSurroundSound
Binaural virtual surround sound reproduction and surround sound stereo downmix
---
#### Original Audio
From Soundly 5.0 Surround Sound library: https://getsoundly.com/ \
Content: Garage ambience with water dripping.

#### Virtual Surround
Processing:
1. Get HRIR from database for L, C, R, Ls, Rs.
    - L: Elevation 0 degree, Azimuth -30 degree
    - C: Elevation 0 degree, Azimuth 0 degree
    - R: Elevation 0 degree, Azimuth 30 degree
    - Ls: Elevation 180 degree, Azimuth -60 degree
    - Rs: Elevation 180 degree, Azimuth 60 degree
2. Convolve Each channel with respective HRIR.
    - Left ear signal = Original file * Left Ear HRIR
    - Right ear signal = Original file * Right Ear HRIR
3. Sum 5 left ear channel to one left channel, and 5 right ear channel to one right channel.
4. Combine left and right channel to stereo file.
5. Normalize: Normalize according to change in volume (ratio)
    - ratio: Original signal / Processed signal


#### Stereo Downmix
Processing:
1. Left All: L + (–3 dB × C) + (–3 dB × Ls)
2. Right All: R + (–3 dB × C) + (–3 dB × Rs)
3. Normalize: Normalize according to change in volume (ratio)
    - ratio: Original signal / Processed signal


#### Reference
- HRTF data from CIPIC database by UC Davis: https://www.ece.ucdavis.edu/cipic/spatial-sound/hrtf-data/
- Stereo downmix method reference Dolby website (Lo/Ro - default): https://professionalsupport.dolby.com/s/article/How-do-the-5-1-and-Stereo-downmix-settings-work?language=en_US
