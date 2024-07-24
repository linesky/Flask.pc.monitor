
from flask import Flask, render_template, Response
from PIL import Image, ImageDraw
import io
import time
import math
import threading

app = Flask(__name__)

# Inicializar variáveis de animação
frame_rate = 30  # 30 frames por segundo
circle_pos = 100
direction = 1
image_width = 640
image_height = 480
circle_radius = 15

def generate_image():
    global circle_pos, direction
    while True:
        # Criar uma nova imagem
        image = Image.new("RGB", (image_width, image_height), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        
        # Desenhar um círculo
        circle_x = circle_pos
        circle_y = image_height // 2
        draw.ellipse((200-100, 200-100,200+100, 200+100),fill=(255,255,255), outline=(0,0,0))
        
        for i in range(12):
             angle = math.pi / 6 * i
             x_start = 200 + 100 * 0.7 * math.sin(angle)
             y_start = 200 - 100 * 0.8 * math.cos(angle)
             x_end = 200 + 100 * 1 * math.sin(angle)
             y_end = 200 - 100 * 1 * math.cos(angle)
             draw.line((int(x_start),int(y_start),int(x_end),int(y_end)),fill=1)
             
        current_time = time.localtime()
        hours = current_time.tm_hour % 12
        minutes = current_time.tm_min
        seconds = current_time.tm_sec

        hour_angle = math.pi / 6 * hours + math.pi / 360 * minutes
        minute_angle = math.pi / 30 * minutes
        second_angle = math.pi / 30 * seconds
        x_end = 200 + (100 * 0.4) * math.sin(hour_angle)
        y_end = 200 -  (100 * 0.4) * math.cos(hour_angle)
        draw.line((200, 200, int(x_end), int(y_end)),fill=1 )
  
        x_end = 200 + (100 * 0.6) * math.sin(minute_angle)
        y_end = 200 -  (100 * 0.6) * math.cos(minute_angle)
        draw.line((200, 200, int(x_end), int(y_end)),fill=1)
        x_end = 200 + (100 * 0.7) * math.sin(second_angle)
        y_end = 200 -  (100 * 0.7) * math.cos(second_angle)
        draw.line((200, 200, int(x_end), int(y_end)),fill=1)
        
        # Converter a imagem para bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        # Enviar a imagem como stream
        yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + img_byte_arr + b'\r\n')
        
        time.sleep(1 / frame_rate)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_image(), mimetype='multipart/x-mixed-replace; boundary=frame')
print("\x1bc\x1b[47;34m")
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
