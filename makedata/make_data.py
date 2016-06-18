import sqlite3
import cv2
import numpy

dataset = sqlite3.connect("aflw.sqlite");

cursor = dataset.execute("select name from sqlite_master where type='table'");
table = dataset.cursor();
for item in cursor:
	nows = str(item)
	nows = nows[3:len(nows)-3]
	print nows
	table.execute("PRAGMA table_info("+nows+")");
	print table.fetchall();

imageface = dataset.cursor();
imagerect = dataset.cursor();
imagepoint = dataset.cursor();

cursor.execute("select * from Faces order by face_id");
for item in cursor:
	imageface.execute("select * from FaceImages where file_id='"+item[1]+"'");
	imagerect.execute("select * from FaceRect where face_id="+str(item[0]));
	for imagefile in imageface:
		for rect in imagerect:
			imagepath = "flickr\\"+imagefile[3];
			image = cv2.imread(imagepath);

			x = rect[1];
			y = rect[2];
			w = rect[3];
			h = rect[4];

			cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),5);

			imagepoint.execute("select * from FeatureCoords where face_id="+str(item[0]));
			for point in imagepoint:
				if (point[4]==0):
					cv2.circle(image,(int(point[2]),int(point[3])),4,(0,255,0),4);
				else:
					cv2.circle(image,(int(point[2]),int(point[3])),4,(0,0,255),4);

			cv2.namedWindow("Image");
			cv2.imshow("Image",image);

			img = image[max(y,0):min(y+h,len(image)),max(x,0):min(x+w,len(image[0]))];

			cv2.namedWindow("Img");
			cv2.imshow("Img",img);
			cv2.waitKey(0);

