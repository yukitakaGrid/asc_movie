from pytube import YouTube
import cv2
import os

def get_youtube_frame(video_url):
    # ダウンロード先のフォルダ
    download_folder = "downloads"
    if not(os.path.isdir(download_folder)):
       os.mkdir(download_folder)
    frame_folder = "frame"
    if not(os.path.isdir(frame_folder)):
       os.mkdir(frame_folder)

    # YouTube動画をダウンロード
    yt = YouTube(video_url)
    ys = yt.streams.get_lowest_resolution()
    ys.download(download_folder)
    print("youtubeの動画をダウンロードしました")

    # ダウンロードした動画を読み込み
    video_path = os.path.join(download_folder, ys.title + ".mp4")
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    frame_exist = True
    i=0

    while(1):
        # フレームを1つ読み込む
        frame_exist, frame = cap.read()

        if(frame_exist==False):
            break
        
        cv2.imwrite(f"frame/frame{i}.jpg", frame)
        
        i+=1

    # リソースを解放
    cap.release()
    print("動画をフレームに変換しました")

    return i ,fps
