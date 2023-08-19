from moviepy.editor import ImageSequenceClip, AudioFileClip
from image_downloader import download_images
import os
from PIL import Image
import gen_voice

api_key = "YOUR_ELEVENLABS_API_KEY"
topic = input("Topic of video: ").lower()
script = open('script.txt', 'r').read()
def img_generator(t, n, image_size):
    download_images(t, n)
    imgs = os.listdir(f"{t}")
    
    # Resize downloaded images to a consistent size
    resized_imgs = []
    for img in imgs:
        img_path = os.path.join(t, img)
        original_img = Image.open(img_path)
        resized_img = original_img.resize(image_size)
        resized_img = resized_img.convert("RGB")  # Convert to RGB mode before saving
        resized_img_path = os.path.join(t, f"resized_{img}")
        resized_img.save(resized_img_path, "JPEG")  # Save as JPEG format
        resized_imgs.append(resized_img_path)
    
    return resized_imgs

def video_maker(images, delay_between_image, fps):
	gen_voice.gen_voice(script, api_key)
	print("AI Voice Generated !")
	audio_file = "output.mp3"
	audio_clip = AudioFileClip(audio_file)
	audio_duration = audio_clip.duration
	video_clip = ImageSequenceClip(images, durations=[delay_between_image] * len(images))
	video_duration = len(images) * delay_between_image
	if audio_duration < video_duration:
		video_duration = audio_duration

	video_clip = video_clip.set_audio(audio_clip)
	output_file = 'output_video.mp4'
	video_clip.subclip(0, video_duration).write_videofile(output_file, fps=fps, codec='libx264')

imgs = img_generator(topic, 15, (553, 311))  # Specify the desired image size (width, height)
video_maker(imgs, 8, 30)