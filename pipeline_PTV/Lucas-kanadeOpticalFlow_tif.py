import numpy as np
import cv2
import tifffile
#lucas-kanade Optical FLow


# cap = cv2.VideoCapture("cars.gif")

# params for ShiTomasi corner detection
feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )

# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (15,15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Create some random colors
color = np.random.randint(0,255,(100,3))

# Take first frame and find corners in it
tifpath="/Volumes/USB/IBP_data/results/tanitracer"
imgs=tifffile.imread(tifpath+"/220906-E4_Out_marked.tif")
# print(imgs.shape)
num_frames = imgs.shape[0]
first_frame=imgs[0].astype('uint8')
# print(first_frame.shape)
first_frame = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)


# Create a mask image for drawing purposes
mask = np.zeros_like(first_frame)
mask[214:338, 62:243] = 255

p0 = cv2.goodFeaturesToTrack(first_frame, mask=mask, **feature_params)
# mask = np.expand_dims(imgs[0], axis=-1)
# mask = np.repeat(mask, 3, axis=-1)


for i in range(1, num_frames):
    # ret,frame = cap.read()

    
    frameNext = imgs[i].astype('uint8')
    frame_gray = cv2.cvtColor(frameNext, cv2.COLOR_BGR2GRAY)
    # calculate optical flow
    p1, st, err = cv2.calcOpticalFlowPyrLK(first_frame, frame_gray, p0, None, **lk_params)
    # Select good points that are within the specified mask
    mask_points_inside = (p1[:, 0, 1] >= 214) & (p1[:, 0, 1] <= 338) & (p1[:, 0, 0] >= 62) & (p1[:, 0, 0] <= 243)
    good_new = p1[mask_points_inside]
    good_old = p0[mask_points_inside]

    # # Select good points
    # good_new = p1[st==1]
    # print(good_new)
    # good_old = p0[st==1]

    # draw the tracks
    for i,(new,old) in enumerate(zip(good_new,good_old)):
        a,b = new.ravel()
        a,b = int(a), int(b)
        c,d = old.ravel()
        c,d = int(c), int(d)
        mask = cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
        frame = cv2.circle(frameNext,(a,b),5,color[i].tolist(),-1)
    img = cv2.add(frame_gray,mask)

    cv2.imshow('frame',img)
    k = cv2.waitKey(240) & 0xff
    if k == 27:
        break

    # Now update the previous frame and previous points
    first_frame = frame_gray.copy()
    p0 = good_new.reshape(-1,1,2)

cv2.destroyAllWindows()


