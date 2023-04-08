import cv2
import numpy as np 
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--webcam', help="True/False", default=False)
parser.add_argument('--play_video', help="True/False", default=False)
parser.add_argument('--video_path', help="Path of video file", default="videos/fire1.mp4")
parser.add_argument('--verbose', help="To print statements", default=True)
args = parser.parse_args()


def load_yolo():
	net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
	classes = []
	with open("obj.names", "r") as f:
		classes = [line.strip() for line in f.readlines()]

	layers_names = net.getLayerNames()
	output_layers = [layers_names[i-1] for i in net.getUnconnectedOutLayers()]
	colors = np.random.uniform(0, 255, size=(len(classes), 3))
	return net, classes, colors, output_layers

def load_image(img_path):
	img = cv2.imread(img_path)
	img = cv2.resize(img, None, fx=0.4, fy=0.4)
	height, width, channels = img.shape
	return img, height, width, channels

def start_webcam():
	cap = cv2.VideoCapture(0)
	return cap

def display_blob(blob):
	for b in blob:
		for n, imgb in enumerate(b):
			cv2.imshow(str(n), imgb)

def detect_objects(img, net, outputLayers):			
	blob = cv2.dnn.blobFromImage(img, scalefactor=0.00392, size=(320, 320), mean=(0, 0, 0), swapRB=True, crop=False)
	net.setInput(blob)
	outputs = net.forward(outputLayers)
	return blob, outputs

def get_box_dimensions(outputs, height, width):
	boxes = []
	confs = []
	class_ids = []
	for output in outputs:
		for detect in output:
			scores = detect[5:]
			class_id = np.argmax(scores)
			conf = scores[class_id]
			if conf > 0.3:
				center_x = int(detect[0] * width)
				center_y = int(detect[1] * height)
				w = int(detect[2] * width)
				h = int(detect[3] * height)
				x = int(center_x - w/2)
				y = int(center_y - h / 2)
				boxes.append([x, y, w, h])
				confs.append(float(conf))
				class_ids.append(class_id)
	return boxes, confs, class_ids
			
def draw_labels(boxes, confs, colors, class_ids, classes, img, weapon_count):
    # Create the crash_frames folder if it doesn't exist
    if not os.path.exists("weapon_frames"):
        os.makedirs("weapon_frames")
    
    indexes = cv2.dnn.NMSBoxes(boxes, confs, 0.5, 0.4)
    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[i % len(colors)]
            cv2.rectangle(img, (x, y), (x+w, y+h), color, 5)
            cv2.putText(img, label, (x, y - 5), font, 2, color, 2)
            if "Gun" in label or "Rifle" in label:
                print("Weapon detected")
                weapon_count += 1
                weapon_frame_path = f"weapon_frames/weapon_{weapon_count:04d}.png"
                cv2.imwrite(weapon_frame_path, img)
                print(f"Weapon frame saved to {weapon_frame_path}")

    img = cv2.resize(img, (800, 600))
    cv2.imshow("Image", img)
    return weapon_count

def webcam_detect():
    model, classes, colors, output_layers = load_yolo()
    cap = start_webcam()
    weapon_count = 0  # Initialize weapon_count outside the loop
    while True:
        _, frame = cap.read()
        height, width, channels = frame.shape
        blob, outputs = detect_objects(frame, model, output_layers)
        boxes, confs, class_ids = get_box_dimensions(outputs, height, width)
        weapon_count = draw_labels(boxes, confs, colors, class_ids, classes, frame, weapon_count)
        key = cv2.waitKey(1)
        if key == 27:
            break
    cap.release()

def start_video(video_path):
    model, classes, colors, output_layers = load_yolo()
    cap = cv2.VideoCapture(video_path)
    weapon_count = 0  # Initialize weapon_count outside the loop
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        height, width, channels = frame.shape
        blob, outputs = detect_objects(frame, model, output_layers)
        boxes, confs, class_ids = get_box_dimensions(outputs, height, width)
        weapon_count = draw_labels(boxes, confs, colors, class_ids, classes, frame, weapon_count)

        key = cv2.waitKey(1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()


if __name__ == '__main__':
	webcam = args.webcam
	video_play = args.play_video
	image = args.image
	if webcam:
		if args.verbose:
			print('---- Starting Web Cam object detection ----')
		webcam_detect()
	if video_play:
		video_path = args.video_path
		if args.verbose:
			print('Opening '+video_path+" .... ")
		start_video(video_path)

	
	cv2.destroyAllWindows()
