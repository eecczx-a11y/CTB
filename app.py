from flask import Flask, render_template, request, jsonify
import datetime

app = Flask(__name__)
LOG_FILE = "chat_log.txt"

# 关键字库（50+词）
keyword_advice = {
    "学习": "学习时制定计划，每次专注一小段时间效果最好。",
    "考试": "考试前复习重点，保证充足睡眠，轻松应考。",
    "作业": "作业可以先做简单的，再做难题，提高效率。",
    "运动": "运动时注意热身和拉伸，保持规律性。",
    "跑步": "跑步时保持呼吸均匀，循序渐进，避免受伤。",
    "健身": "健身计划要合理安排力量和有氧训练。",
    "工作": "工作时分清轻重缓急，合理安排时间。",
    "职业": "职业发展需要不断学习与积累经验。",
    "健康": "保持健康需要良好的作息和均衡饮食。",
    "饮食": "均衡饮食，多吃蔬菜水果，少吃油炸食品。",
    "压力": "压力大时可以尝试深呼吸、散步或写下感受来放松。",
    "焦虑": "焦虑时可以做冥想或与朋友倾诉，缓解情绪。",
    "心情": "保持好心情有助于身心健康，尝试记录感恩日记。",
    "睡眠": "保持规律作息，保证每天7-8小时睡眠。",
    "烦躁": "烦躁时可以深呼吸或短暂休息，避免冲动。",
    "人际": "与人相处要互相理解，学会倾听。",
    "朋友": "朋友间保持真诚和沟通最重要。",
    "恋爱": "恋爱中沟通与尊重比任何技巧更重要。",
    "家庭": "关心家人，尝试多沟通，营造温暖氛围。",
    "情绪": "情绪波动时记录感受，有助于自我调节。",
    "开心": "开心时多分享快乐，增强幸福感。",
    "悲伤": "悲伤时允许自己感受情绪，也可寻求倾诉。",
    "孤单": "孤单时尝试培养兴趣或与朋友联系。",
    "目标": "设定明确目标，并分阶段执行，更易达成。",
    "计划": "制定计划可以提高效率和自律能力。",
    "拖延": "拖延时先从小任务开始，逐步完成大目标。",
    "金钱": "理财需量入为出，合理规划预算。",
    "理财": "理财时注意风险分散，不盲目投资。",
    "学习英语": "学英语每天积累单词和口语练习效果更好。",
    "考试焦虑": "焦虑时深呼吸，提前做好复习计划。",
    "锻炼": "规律锻炼有助于身心健康，选择自己喜欢的运动。",
    "跑步机": "跑步机上跑步注意速度循序渐进。",
    "减肥": "减肥时结合饮食和运动，循序渐进。",
    "健身房": "健身房训练前做好热身，循序渐进。",
    "饮水": "多喝水保持身体代谢，健康生活习惯。",
    "作息": "规律作息可提升精神状态和效率。",
    "睡眠不足": "睡眠不足时避免过度兴奋，尽量补眠。",
    "压力大": "压力大时运动、休息或写下感受帮助缓解。",
    "焦虑感": "焦虑感强时做深呼吸或短暂休息。",
    "烦恼": "烦恼时尝试找朋友倾诉或写日记。",
    "失眠": "失眠时避免咖啡因，多做放松活动。",
    "抑郁": "抑郁时可以寻求心理咨询或倾诉。",
    "开心事": "开心事多分享给朋友，增强幸福感。",
    "负面情绪": "负面情绪时可通过运动或倾诉缓解。",
    "心烦": "心烦时尝试短暂散步或放松音乐。",
    "压力释放": "压力释放可通过运动、兴趣爱好或聊天。",
    "成长": "成长需要持续学习和反思经验。"
}

# 情绪识别
def detect_emotion(text):
    text = text.lower()
    if any(word in text for word in ["难过", "伤心", "不开心", "焦虑", "悲伤", "抑郁"]):
        return "难过"
    elif any(word in text for word in ["开心", "高兴", "快乐", "兴奋", "开心事"]):
        return "开心"
    elif any(word in text for word in ["生气", "烦", "心烦", "烦躁"]):
        return "生气"
    else:
        return "中性"

# 根据关键字匹配建议
def get_advice(user_input):
    for keyword, advice in keyword_advice.items():
        if keyword in user_input:
            return advice
    return "抱歉，我暂时没有相关建议，可以换一个话题吗？"

# 保存聊天记录
def save_chat(user_input, bot_reply):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] 用户: {user_input}\n")
        f.write(f"[{timestamp}] 机器人: {bot_reply}\n")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form["message"]
    emotion = detect_emotion(user_input)
    bot_reply = get_advice(user_input)
    bot_reply_with_emotion = f"{bot_reply} (情绪: {emotion})"
    save_chat(user_input, bot_reply_with_emotion)
    return jsonify({"reply": bot_reply_with_emotion})

if __name__ == "__main__":
    app.run(debug=True)
