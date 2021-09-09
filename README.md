# OpenCV x Python 練習 — 醫學影像檢測

這個小練習應用 OpenCV 與 Python ，將食道癌 MRI 醫學影像中的癌細胞標記出來。

## 特徵

在做癌細胞 MRI 影像檢測前患者會接受注射顯影劑。在顯影劑的作用下，癌細胞會在 MRI 影像中變成相當亮的白色光點 ( R, G, B 大約都在 150 以上)。

## 方法

乘上所述，要知道癌細胞在 MRI 影像上的位置只要查看 RGB(150, 150, 150) 以上的像素點就行了。 
分為三個步驟：

1. 讀取影像並圈選出有興趣的區域（ region of interest, ROI ）
   做這一步中不但可以減少電腦要處理的資訊量、還能有效的過濾掉我們沒興趣的資訊
1. 過濾出癌細胞影像位置
1. 根據癌細胞位置畫記

## 實作

1. 讀取影像及選取 ROI ：
   cv2.imread 函式將影像讀入為 shape 為 (n, m, 3) 的 numpy.ndarray ，色彩通道順序為 B → G → R
   cv2.selectROI 函式會開啟互動式介面讓我們方便選取，選下來的資料結構為 tuple(x, y, width, height), 其中 x, y, width, height 都是整數
   拿到 ROI 後利用 numpy.ndarray 取值的特性裁切圖片，這裡要注意的是 numpy.ndarray 的第一個維度是 y （垂直座標）、第二個維度是 x （水平座標），跟直覺相反。而第三個維度是色彩通道
1. 過濾出癌細胞位置：
   我們可以看到整張圖片的藍色相當少、而癌細胞是純白的，也就是說整張圖片僅有癌細胞有較高的藍色數值。我們可以利用這一點過濾出癌細胞  
   由於我們下一步要用 cv2.findContours 函式找出癌細胞群集的輪廓，我們必須將圖像轉換成它可以接受的純黑、純白二元圖像  
   很性用的是 cv2.threshold 函式帶上 cv2.THRESH_BINARY 這個模式參數不但可以過濾出癌細胞（利用上述藍色通道亮度），還可以將圖片馬上轉換成癌細胞純白、其他純黑的二元圖片  
1. 在癌細胞位置上畫記：  
   cv2.findContours 接受我們畫好的二元圖片後，會吐出癌細胞群集的邊界像素座標  
   cv2.drawContours 能接受 cv2.findContours 的輸出，幫我們畫好服貼於癌細胞群集邊界的輪廓線  
   也可以像我在這裡的作法——找出每個群集的最左上角、最右下角——然後畫方框

## 備註

過濾出癌細胞這步，如果邏輯是「我要找純白又亮的值！」會變成對於每個顏色通道都過濾「大於某個數字，然而各彩色的數值均一」這件事情。  
一樣拿接下來要用 cv2.findContours 這個函式只吃純黑、純白的圖片來說，程式稿會變成：

```python
crop = img[roi[1]:roi[1]+roi[3], roi[0]:roi[0]+roi[2]]
B, G, R = cv2.split(crop)
a = np.zeros((crop.shape[0], crop.shape[1]))
b = np.zeros((crop.shape[0], crop.shape[1]))
c = np.zeros((crop.shape[0], crop.shape[1]))
for i in range(crop.shape[0]):
    for j in range(crop.shape[1]):
        if G[i][j] == B[i][j] and B[i][j] == R[i][j] and R[i][j] > 20:
            a[i][j] = 255
            b[i][j] = 255
            c[i][j] = 255
        else:
            a[i][j] = 0
            b[i][j] = 0
            c[i][j] = 0
mono = cv2.merge([a, b, c])
```

此時 mono 就是過濾癌細胞出來，cv2.findContours 可接受的影像。

也或者找尋各顏色都大於 145 的點也可行。
