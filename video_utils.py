import os
import subprocess
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import tempfile

def generate_video_from_text(title, content):
    """Generate simple video with narration from text"""
    try:
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title.replace(" ", "_")
        
        output_dir = "media/videos"
        os.makedirs(output_dir, exist_ok=True)

        audio_path = f"{output_dir}/{safe_title}.mp3"
        video_path = f"{output_dir}/{safe_title}.mp4"
        image_path = f"{output_dir}/{safe_title}.png"

        # Convert text to audio (limit text length for gTTS)
        text_for_audio = content[:2000]  # gTTS has character limits
        print(f"Generating audio for: {title}")
        tts = gTTS(text=text_for_audio, lang='en')
        tts.save(audio_path)

        # Generate image background
        print("Generating background image...")
        img = Image.new("RGB", (1280, 720), color=(20, 30, 60))
        draw = ImageDraw.Draw(img)
        
        # Try to use a larger font if available
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            try:
                font = ImageFont.truetype("Arial", 40)
            except:
                font = ImageFont.load_default()
        
        # Draw title on image
        draw.text((50, 300), title, fill=(255, 255, 255), font=font)
        img.save(image_path)

        # Create video using FFmpeg
        print("Creating video with FFmpeg...")
        command = [
            "ffmpeg",
            "-loop", "1",
            "-i", image_path,
            "-i", audio_path,
            "-c:v", "libx264",
            "-tune", "stillimage",
            "-c:a", "aac",
            "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-shortest",
            video_path,
            "-y"
        ]

        # Run FFmpeg command
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"FFmpeg error: {result.stderr}")
            raise Exception(f"FFmpeg failed: {result.stderr}")

        print(f"Video generated successfully: {video_path}")
        
        # Clean up temporary files (optional)
        # os.remove(audio_path)
        # os.remove(image_path)
        
        return video_path
        
    except Exception as e:
        print(f"Error generating video: {str(e)}")
        raise e