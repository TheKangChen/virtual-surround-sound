# VirtualSurroundSound
Binaural virtual surround sound reproduction and surround sound stereo downmix.
---
#### Updated Nov, 20, 2021:
Now able to take 7.1.4 Audio files as input for virtual surround.
- 7.1.4 layout: L, R, C, LFE, LS, RS, RLS, RRS, FLU, FRU, RLU, RRU
- HRIRs from database:
    - L: Elevation 0 degree, Azimuth -65 degree
    - R: Elevation 0 degree, Azimuth 65 degree
    - C: Elevation 0 degree, Azimuth 0 degree
    - LFE: N/A
    - LS: Elevation 180 degree, Azimuth -20 degree
    - RS: Elevation 180 degree, Azimuth 20 degree
    - RLS: Elevation 180 degree, Azimuth -55 degree
    - RRS: Elevation 180 degree, Azimuth 55 degree
    - FLU: Elevation 45 degree, Azimuth -30 degree
    - FRU: Elevation 45 degree, Azimuth 30 degree
    - RLU: Elevation 135 degree, Azimuth -30 degree
    - RRU: Elevation 135 degree, Azimuth 30 degree

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

---
#### Reference
- HRTF data from CIPIC database by UC Davis: https://www.ece.ucdavis.edu/cipic/spatial-sound/hrtf-data/
- Stereo downmix method reference Dolby website (Lo/Ro - default): https://professionalsupport.dolby.com/s/article/How-do-the-5-1-and-Stereo-downmix-settings-work?language=en_US
