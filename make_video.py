import cv2
import os

def make_video(save_folder, output_file):
    img_array = []
    for filename in sorted(os.listdir(save_folder)):
        if not filename.endswith('.jpg'):
            continue
        file_path = os.path.join(save_folder, filename)
        img = cv2.imread(file_path)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
        # os.remove(file_path)
    out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'DIVX'), 5, size) #15
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()


if __name__ == '__main__':
    make_video('outputs/trail_messages_trial_288_SaturnA_TM000008', 'outputs/trail_messages_trial_288_SaturnA_TM000008.avi')
