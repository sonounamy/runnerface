TRANSLATION_MAP = {
    "CONFUSED": "混乱",
    "DISGUSTED": "嫌悪",
    "SAD": "悲しみ",
    "FEAR": "恐怖",
    "ANGRY": "怒り",
    "CALM": "落ち着き",
    "SURPRISED": "驚き",
    "HAPPY": "喜び",
}


def translate_emotions(emotion_raw_list):
    translated_emotion_list = []
    for emotions in emotion_raw_list:
        translated_dict = {}
        for emotion in emotions:
            translated_dict[TRANSLATION_MAP[emotion["Type"]]] = f"{round(emotion['Confidence'], 3)}%"
        sorted_data = sorted(translated_dict.items(), key=lambda x: float(x[1].strip('%')), reverse=True)
        translated_emotion_list.append(sorted_data)

    return translated_emotion_list
