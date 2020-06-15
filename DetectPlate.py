#scikit-image (a.k.a. skimage) is a collection of algorithms for image processing and computer vision.
from skimage.io import imread #skimage.io- Utilities to read and write images in various formats.
from skimage.filters import threshold_otsu#Return threshold value based on Otsu's method i.e seperates pixels into foreground and background classes
import matplotlib.pyplot as plt#matplotlib.pyplot is a state-based interface to matplotlib. It provides a MATLAB-like way of plotting.

filename = 'C:/Academic Contents/IBM/IBM ICE 2019-20191112T071612Z-001/IBM ICE 2019/CODE/video12.mp4'
import cv2
cap = cv2.VideoCapture(filename)# starts capturing the video
# cap = cv2.VideoCapture(0)
count = 0
while cap.isOpened():   #Returns true if video capturing has been initialized already.
    ret,frame = cap.read()  #starts reading the video frames and returns next frame
    if ret == True:
        cv2.imshow('window-name',frame)
        cv2.imwrite("frame%d.jpg" % count, frame) # starts playing the video 
        count = count + 1
        if cv2.waitKey(10) & 0xFF == ord('q'): #press q to quit
            break
    else:
        break
cap.release()#Closes video file or capturing device.
cv2.destroyAllWindows() #Destroys all of the HighGUI windows.

# car image -> grayscale image -> binary image
import imutils#A series of convenience functions to make basic image processing functions such as translation, rotation, resizing
car_image = imread("frame%d.jpg"%(count-1), as_gray=True)
car_image = imutils.rotate(car_image, 270)
# car_image = imread("car.png", as_gray=True)
# it should be a 2 dimensional array
print(car_image.shape)#gives output as (1080, 1920)

# the next line is not compulsory however, a grey scale pixel
# in skimage ranges between 0 & 1. multiplying it with 255
# will make it range between 0 & 255 (something we can relate better with

gray_car_image = car_image * 255
fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.imshow(gray_car_image, cmap="gray")
threshold_value = threshold_otsu(gray_car_image)
binary_car_image = gray_car_image > threshold_value
# print(binary_car_image)
ax2.imshow(binary_car_image, cmap="gray")
# ax2.imshow(gray_car_image, cmap="gray")
plt.show()

# CCA (Connected component analysis for finding connected regions) of binary image


from skimage import measure#Measurement of image properties, e.g., similarity and contours. 
from skimage.measure import regionprops#regionprops-Measure properties of labeled image regions.
import matplotlib.pyplot as plt#matplotlib.pyplot is a state-based interface to matplotlib. It provides a MATLAB-like way of plotting
import matplotlib.patches as patches#`matplotlib.patches-defines classes for drawing polygons 

# this gets all the connected regions and groups them together
label_image = measure.label(binary_car_image)

# print(label_image.shape[0]) #width of car img

# getting the maximum width, height and minimum width and height that a license plate can be
plate_dimensions = (0.03*label_image.shape[0], 0.08*label_image.shape[0], 0.15*label_image.shape[1], 0.3*label_image.shape[1])
plate_dimensions2 = (0.08*label_image.shape[0], 0.2*label_image.shape[0], 0.15*label_image.shape[1], 0.4*label_image.shape[1])
min_height, max_height, min_width, max_width = plate_dimensions
plate_objects_cordinates = []
plate_like_objects = []

fig, (ax1) = plt.subplots(1)
ax1.imshow(gray_car_image, cmap="gray")
flag =0
# regionprops creates a list of properties of all the labelled regions
for region in regionprops(label_image):
    # print(region)
    if region.area < 50:
        #if the region is so small then it's likely not a license plate
        continue
        # the bounding box coordinates
    min_row, min_col, max_row, max_col = region.bbox
    # print(min_row)
    # print(min_col)
    # print(max_row)
    # print(max_col)

    region_height = max_row - min_row
    region_width = max_col - min_col
    # print(region_height)
    # print(region_width)

    # ensuring that the region identified satisfies the condition of a typical license plate
    if region_height >= min_height and region_height <= max_height and region_width >= min_width and region_width <= max_width and region_width > region_height:
        flag = 1
        plate_like_objects.append(binary_car_image[min_row:max_row,
                                  min_col:max_col])
        plate_objects_cordinates.append((min_row, min_col,
                                         max_row, max_col))
        rectBorder = patches.Rectangle((min_col, min_row), max_col - min_col, max_row - min_row, edgecolor="red",
                                       linewidth=2, fill=False)
        ax1.add_patch(rectBorder)
        # let's draw a red rectangle over those regions
if(flag == 1):
    # print(plate_like_objects[0])
    plt.show()




if(flag==0):
    min_height, max_height, min_width, max_width = plate_dimensions2
    plate_objects_cordinates = []
    plate_like_objects = []

    fig, (ax1) = plt.subplots(1)
    ax1.imshow(gray_car_image, cmap="gray")

    # regionprops creates a list of properties of all the labelled regions
    for region in regionprops(label_image):
        if region.area < 50:
            #if the region is so small then it's likely not a license plate
            continue
            # the bounding box coordinates
        min_row, min_col, max_row, max_col = region.bbox
        # print(min_row)
        # print(min_col)
        # print(max_row)
        # print(max_col)

        region_height = max_row - min_row
        region_width = max_col - min_col
        # print(region_height)
        # print(region_width)

        # ensuring that the region identified satisfies the condition of a typical license plate
        if region_height >= min_height and region_height <= max_height and region_width >= min_width and region_width <= max_width and region_width > region_height:
            # print("hello")
            plate_like_objects.append(binary_car_image[min_row:max_row,
                                      min_col:max_col])
            plate_objects_cordinates.append((min_row, min_col,
                                             max_row, max_col))
            rectBorder = patches.Rectangle((min_col, min_row), max_col - min_col, max_row - min_row, edgecolor="red",
                                           linewidth=2, fill=False)
            ax1.add_patch(rectBorder)
            # let's draw a red rectangle over those regions
    # print(plate_like_objects[0])
    plt.show()