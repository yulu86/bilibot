import io
import re
import time
import wave
import requests
import simpleaudio as sa
import ollama

# 主题
SUBJECT = '你喜欢看什么动漫'

# 是否使用OLLMA
USE_OLLAMA = True

# OLLMA模型
OLLMA_MODEL1 = 'qwen:32b-chat-v1.5-q4_0_weibo'
USER1 = 'weibo'
OLLMA_MODEL2 = 'qwen:32b-chat-v1.5-q4_0_bilibot'
USER2 = 'bilibili'

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

def generate_by_ollama(question, amodel):
    response = ollama.chat(model=amodel, messages=[
          {
            'role': 'user',
            'content': question,
          },
        ],
        stream=False
    )    
    return response['message']['content']

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
        response = split_text(response)
        generate_speech(response, 9881)