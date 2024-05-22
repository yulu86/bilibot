import io
import re
import time
import wave
import requests
import simpleaudio as sa
import ollama

<<<<<<< HEAD

=======
# 主题
>>>>>>> 43640737cc8c8e7dcf17aefc7199c7abf3069a31
SUBJECT = ''

# 是否使用OLLMA
USE_OLLAMA = True
<<<<<<< HEAD
# OLLMA模型
OLLMA_MODEL = 'qwen:32b-chat-v1.5-q4_0_stable_weibo'
# safetensors模型
SAFETENSORS_MODEL = 'Qwen1.5-32B-Chat-4Bit'
=======

# OLLMA模型
OLLMA_MODEL1 = 'qwen:32b-chat-v1.5-q4_0_zhihu'
USER1 = 'zhihu'
OLLMA_MODEL2 = 'qwen:32b-chat-v1.5-q4_0_bilibot'
USER2 = 'bilibili'
>>>>>>> 43640737cc8c8e7dcf17aefc7199c7abf3069a31

def generate_speech(text, port):
    time_ckpt = time.time()
    data={
        "text": text,
        "text_language": "zh"
    }
    response = requests.post("http://127.0.0.1:{}".format(port), json=data)
    if response.status_code == 400:
        raise Exception(f"GPT-SoVITS ERROR: {response.message}")
    audio_data = io.BytesIO(response.content)
    with wave.open(audio_data, 'rb') as wave_read:
        audio_frames = wave_read.readframes(wave_read.getnframes())
        audio_wave_obj = sa.WaveObject(audio_frames, wave_read.getnchannels(), wave_read.getsampwidth(), wave_read.getframerate())
    play_obj = audio_wave_obj.play()
    play_obj.wait_done()
    print("Audio Generation Time: %d ms\n" % ((time.time() - time_ckpt) * 1000))

def split_text(text):
    sentence_endings = ['！', '。', '？']
    for punctuation in sentence_endings:
        text = text.replace(punctuation, punctuation + '\n')
    pattern = r'\[.*?\]'
    text = re.sub(pattern, '', text)
    return text

<<<<<<< HEAD
def generate_by_ollama(question):
    response = ollama.chat(model=OLLMA_MODEL, messages=[
=======
def generate_by_ollama(question, amodel):
    response = ollama.chat(model=amodel, messages=[
>>>>>>> 43640737cc8c8e7dcf17aefc7199c7abf3069a31
          {
            'role': 'user',
            'content': question,
          },
        ],
        stream=False
    )    
    return response['message']['content']

<<<<<<< HEAD
if __name__ == "__main__":    
    

    template = ''    

    while True:        
        print("%s: %s" % ("问题", question))
        question = split_text(question)
        generate_speech(question, 9880)        

        time_ckpt = time.time()           
        response = generate_by_ollama(question)    

        print("%s: %s (Time %d ms)\n" % ("哔友", response, (time.time() - time_ckpt) * 1000))
=======
if __name__ == "__main__": 
    question = SUBJECT

    print("%s: %s" % (USER1, question))
    question = split_text(question)
    generate_speech(question, 9881)

    while True:        
        time_ckpt = time.time()           
        response = generate_by_ollama(question, OLLMA_MODEL2)    

        question = response

        print("%s: %s (Time %d ms)\n" % (USER2, response, (time.time() - time_ckpt) * 1000))
        response = split_text(response)
        generate_speech(response, 9881)

        response = generate_by_ollama(question, OLLMA_MODEL1)    
        
        question = response

        print("%s: %s (Time %d ms)\n" % (USER1, response, (time.time() - time_ckpt) * 1000))
>>>>>>> 43640737cc8c8e7dcf17aefc7199c7abf3069a31
        response = split_text(response)
        generate_speech(response, 9881)