import numpy as np
import cv2
import math

mask_Size = int(input("Enter mask size value : "))
global Filter,original_Image,padding

def create_FilterMask(mask_Size):
    Filter = np.full((mask_Size,mask_Size),0,np.uint8)
    mask_Range = mask_Size * mask_Size
    mask_Size = (mask_Size,mask_Size)
    list = [0 for i in range(mask_Range)]
    print('Enter',mask_Range,'values')
    for i in range(len(list)):
        mask_Value = int(input('Enter values for Filter : '))
        if mask_Value < 0:
            mask_Value = 256 + mask_Value
        list[i] = mask_Value

    k = 0

    for i in range(Filter.shape[0]):
        for j in range(Filter.shape[1]):
            Filter[i,j] = list[k]
            k += 1

    return Filter

original_Image = cv2.imread('Capture.tif',0)
Lena_Image = cv2.imread('Capture2.PNG',0)

def Add_Padding(mask_Size,original_Image):
    padding = int(mask_Size/2)
    original_Image = cv2.copyMakeBorder(original_Image,padding,padding,padding,padding,cv2.BORDER_CONSTANT,value = 0)
    return original_Image,padding

def Apply_Avg_Filter(original_Image,Filter):
    Filter_Sum = Filter.shape[0]*Filter.shape[1]
    copy_Filter = np.full((Filter.shape[0],Filter.shape[1]),0,np.uint8)

    for i in range(padding,original_Image.shape[0]-padding):
        for j in range(padding,original_Image.shape[1]-padding):
            copy_Filter[:, :] = Filter[:, :]*original_Image[i - padding:i + padding + 1, j - padding:j + padding + 1]
            original_Image[i, j] = round(np.sum(copy_Filter[:,:]) / Filter_Sum)

    return original_Image

def Apply_Median_Filter(original_Image):

    for i in range(padding,original_Image.shape[0]-padding):
        for j in range(padding,original_Image.shape[1]-padding):
            original_Image[i, j] = np.median(original_Image[i-padding:i+padding+1,j-padding:j+padding+1])
    return original_Image

Filter = create_FilterMask(mask_Size)

cv2.imshow('Original Image',original_Image)
cv2.waitKey(0)

original_Image,padding = Add_Padding(mask_Size,original_Image)
Lena_Image,padding = Add_Padding(mask_Size,Lena_Image)

new_Image = Apply_Avg_Filter(original_Image,Filter)
cv2.imshow('Avg Filter',new_Image)
cv2.waitKey(0)

Normalized_Image = new_Image
cv2.normalize(new_Image,Normalized_Image,0,255,cv2.NORM_MINMAX)
cv2.imshow('Normalized',Normalized_Image)
cv2.waitKey(0)

cv2.imshow('Original Image',Lena_Image)
cv2.waitKey(0)

new_Image_Lena = Apply_Median_Filter(Lena_Image)
cv2.imshow('Median Filter',new_Image_Lena)
cv2.waitKey(0)

