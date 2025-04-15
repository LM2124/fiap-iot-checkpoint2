# pip install opencv-python pyserial mediapipe

import cv2                          # OpenCV: captura e exibição de vídeo
from drawing import draw_hand_landmarks_on_image
import mediapipe as mp              # MediaPipe: detecção de pose humana
import serial                       # Comunicação com Arduino
import time                         # Pausa para inicializar


class FakeArduino():
    def __init__(self, debug=True):
        self.debug = debug
    def write(self, buffer):
        # print(f"Arduino Write: {buffer}")
        print("Arduino Write")
    def close(self):
        print(f"Arduino Close")

# Conecta com o Arduino (ajuste a porta COM conforme seu sistema)
arduino = FakeArduino()
# arduino = serial.Serial('COM6', 9600, timeout=1); time.sleep(2)  # Espera o Arduino iniciar

# Inicializando parâmetros do modelo
hand_model_path = "./hand_landmarker.task"
handLandmarker = mp.tasks.vision.HandLandmarker
handLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions(
    base_options=mp.tasks.BaseOptions(model_asset_path=hand_model_path),
    running_mode=mp.tasks.vision.RunningMode.VIDEO,
    num_hands=2
)
# Inicializa a tarefa da mão
handTracker = handLandmarker.create_from_options(handLandmarkerOptions)


# Abre o vídeo
# https://docs.opencv.org/4.11.0/d4/d15/group__videoio__flags__base.html#gaeb8dd9c89c10a5c63c139bf7c4f5704d
# cap = cv2.VideoCapture("dedinho.mp4")
cap = cv2.VideoCapture(0)

# Estado
lastNumber = None

# Não podemos usar o timecode do vídeo pelo cv2, pois caso o vídeo
# reiniciar, a timestamp terá reduzido, e o mediapipe dá chilique.
frameTime = 1000 / cap.get(cv2.CAP_PROP_FPS)
frameCount = 0
while True:
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reinicia o vídeo
        continue

    frame = cv2.resize(frame, (500, 500))      # Redimensiona
    frame = cv2.flip(frame, 1)                 # Espelha horizontalmente

    # Calculando a timestamp do vídeo
    timestamp = int(frameCount * frameTime)
    frameCount += 1

    # Processa a imagem para detectar pontos dos dedos
    result = handTracker.detect_for_video(mp.Image(image_format=mp.ImageFormat.SRGB, data=frame), timestamp)

    if result.hand_landmarks:
        # Desenha os marcos de dedo no frame
        frame = draw_hand_landmarks_on_image(frame, result)

        DEDO_ON_THRESH = 0.4
        pontosMao1 = result.hand_landmarks[0]
        dedos1 = [1 if abs(dedo) > DEDO_ON_THRESH else 0 for dedo in [
            pontosMao1[4].x, # Dedão
            1-pontosMao1[8].y, # Index
            1-pontosMao1[12].y, # Middle
            1-pontosMao1[16].y, # Ring
            1-pontosMao1[20].y, # Pinky
        ]]

        dedos2 = []
        if (len(result.hand_landmarks) >= 2):
            pontosMao2 = result.hand_landmarks[1]
            dedos2 = [1 if abs(dedo) > DEDO_ON_THRESH else 0 for dedo in [
                1-pontosMao2[4].x, # Dedão
                1-pontosMao2[8].y, # Index
                1-pontosMao2[12].y, # Middle
                1-pontosMao2[16].y, # Ring
                1-pontosMao2[20].y, # Pinky
        ]]


        total = 0
        all_dedos = dedos1 + dedos2
        # all_dedos = dedos1 # TEMP - Só primeira mão por enquanto

        for dedoIdx in range(len(all_dedos)):
            if (all_dedos[dedoIdx] == 1):
                total += 2**dedoIdx

        if total != lastNumber:
            lastNumber = total
            arduino.write(bytes(total))

        # Exibe string binária criada por cada dedo
        cv2.putText(frame, f"Dedos 1: {''.join([str(dedo) for dedo in dedos1[::-1]])}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        cv2.putText(frame, f"Dedos 2: {''.join([str(dedo) for dedo in dedos2[::-1]])}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # Exibe contador
        cv2.putText(frame, f"Resultado Binario: {total}", (10, 130),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Mostra o vídeo
    cv2.imshow("Conta binaria", frame)

    # Sai com a tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Finaliza
cap.release()
arduino.close()
cv2.destroyAllWindows()
