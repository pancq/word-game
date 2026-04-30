import pygame
import sys
import json
import os
import random
import subprocess
import platform
import logging

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")

# 初始化 pygame
pygame.init()
pygame.mixer.init()  # 初始化音频模块

# 常量
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 界面文字翻译
UI_TEXT = {
    "中文": {
        "title": "儿童识字游戏",
        "language": "语言",
        "difficulty": "难度",
        "theme": "主题",
        "back": "返回",
        "correct": "✓ 正确！",
        "wrong": "✗ 错误",
        "great": "太棒了！继续加油！",
        "correct_answer": "正确答案是",
        "ok": "确定",
        "easy": "简单",
        "medium": "中等",
        "hard": "困难",
        "modes": "游戏模式",
        "mode_learn": "学习模式",
        "mode_quiz": "测验模式",
        "mode_spell": "组词游戏",
        "mode_match": "连连看",
        "mode_whack": "打地鼠",
        "mode_memory": "记忆翻牌",
        "mode_chain": "听音选字",
        "mode_time": "计时挑战",
    },
    "English": {
        "title": "Kids Word Game",
        "language": "Language",
        "difficulty": "Difficulty",
        "theme": "Theme",
        "back": "Back",
        "correct": "✓ Correct!",
        "wrong": "✗ Wrong",
        "great": "Great job! Keep going!",
        "correct_answer": "Correct answer is",
        "ok": "OK",
        "easy": "Easy",
        "medium": "Medium",
        "hard": "Hard",
        "modes": "Game Modes",
        "mode_learn": "Learn",
        "mode_quiz": "Quiz",
        "mode_spell": "Word Match",
        "mode_match": "Match",
        "mode_whack": "Whack",
        "mode_memory": "Memory",
        "mode_chain": "Listen",
        "mode_time": "Time",
    }
}

# 数据库 - 适合幼升小（5-7岁）儿童学习
CHINESE_DATABASE = {
    "简单": [
        # 数字 (10个)
        {"word": "一", "pinyin": "yī", "meaning": "数字一"},
        {"word": "二", "pinyin": "èr", "meaning": "数字二"},
        {"word": "三", "pinyin": "sān", "meaning": "数字三"},
        {"word": "四", "pinyin": "sì", "meaning": "数字四"},
        {"word": "五", "pinyin": "wǔ", "meaning": "数字五"},
        {"word": "六", "pinyin": "liù", "meaning": "数字六"},
        {"word": "七", "pinyin": "qī", "meaning": "数字七"},
        {"word": "八", "pinyin": "bā", "meaning": "数字八"},
        {"word": "九", "pinyin": "jiǔ", "meaning": "数字九"},
        {"word": "十", "pinyin": "shí", "meaning": "数字十"},
        # 基础字 (20个)
        {"word": "人", "pinyin": "rén", "meaning": "人类"},
        {"word": "口", "pinyin": "kǒu", "meaning": "嘴巴"},
        {"word": "手", "pinyin": "shǒu", "meaning": "手掌"},
        {"word": "足", "pinyin": "zú", "meaning": "脚"},
        {"word": "目", "pinyin": "mù", "meaning": "眼睛"},
        {"word": "耳", "pinyin": "ěr", "meaning": "耳朵"},
        {"word": "大", "pinyin": "dà", "meaning": "很大的"},
        {"word": "小", "pinyin": "xiǎo", "meaning": "很小的"},
        {"word": "上", "pinyin": "shàng", "meaning": "在上面"},
        {"word": "下", "pinyin": "xià", "meaning": "在下面"},
        {"word": "左", "pinyin": "zuǒ", "meaning": "在左边"},
        {"word": "右", "pinyin": "yòu", "meaning": "在右边"},
        {"word": "天", "pinyin": "tiān", "meaning": "天空"},
        {"word": "地", "pinyin": "dì", "meaning": "地面"},
        {"word": "日", "pinyin": "rì", "meaning": "太阳"},
        {"word": "月", "pinyin": "yuè", "meaning": "月亮"},
        {"word": "水", "pinyin": "shuǐ", "meaning": "喝的水"},
        {"word": "火", "pinyin": "huǒ", "meaning": "火焰"},
        {"word": "山", "pinyin": "shān", "meaning": "高高的山"},
        {"word": "石", "pinyin": "shí", "meaning": "石头"},
    ],
    "中等": [
        # 家庭成员 (10个)
        {"word": "爸", "pinyin": "bà", "meaning": "爸爸"},
        {"word": "妈", "pinyin": "mā", "meaning": "妈妈"},
        {"word": "哥", "pinyin": "gē", "meaning": "哥哥"},
        {"word": "姐", "pinyin": "jiě", "meaning": "姐姐"},
        {"word": "弟", "pinyin": "dì", "meaning": "弟弟"},
        {"word": "妹", "pinyin": "mèi", "meaning": "妹妹"},
        {"word": "爷", "pinyin": "yé", "meaning": "爷爷"},
        {"word": "奶", "pinyin": "nǎi", "meaning": "奶奶"},
        {"word": "叔", "pinyin": "shū", "meaning": "叔叔"},
        {"word": "姨", "pinyin": "yí", "meaning": "阿姨"},
        # 日常用品 (15个)
        {"word": "家", "pinyin": "jiā", "meaning": "我们住的家"},
        {"word": "门", "pinyin": "mén", "meaning": "进出的门"},
        {"word": "窗", "pinyin": "chuāng", "meaning": "窗户"},
        {"word": "床", "pinyin": "chuáng", "meaning": "睡觉的床"},
        {"word": "桌", "pinyin": "zhuō", "meaning": "桌子"},
        {"word": "椅", "pinyin": "yǐ", "meaning": "椅子"},
        {"word": "灯", "pinyin": "dēng", "meaning": "照明的灯"},
        {"word": "书", "pinyin": "shū", "meaning": "看的书"},
        {"word": "笔", "pinyin": "bǐ", "meaning": "写字的笔"},
        {"word": "纸", "pinyin": "zhǐ", "meaning": "写字的纸"},
        {"word": "包", "pinyin": "bāo", "meaning": "背的书包"},
        {"word": "衣", "pinyin": "yī", "meaning": "穿的衣服"},
        {"word": "鞋", "pinyin": "xié", "meaning": "穿的鞋子"},
        {"word": "帽", "pinyin": "mào", "meaning": "戴的帽子"},
        {"word": "伞", "pinyin": "sǎn", "meaning": "遮雨的伞"},
    ],
    "困难": [
        # 动物 (15个)
        {"word": "鼠", "pinyin": "shǔ", "meaning": "小老鼠"},
        {"word": "牛", "pinyin": "niú", "meaning": "大黄牛"},
        {"word": "虎", "pinyin": "hǔ", "meaning": "大老虎"},
        {"word": "兔", "pinyin": "tù", "meaning": "小兔子"},
        {"word": "龙", "pinyin": "lóng", "meaning": "神话中的龙"},
        {"word": "蛇", "pinyin": "shé", "meaning": "长长的蛇"},
        {"word": "马", "pinyin": "mǎ", "meaning": "跑得快的马"},
        {"word": "羊", "pinyin": "yáng", "meaning": "温顺的羊"},
        {"word": "猴", "pinyin": "hóu", "meaning": "爱吃香蕉的猴子"},
        {"word": "鸡", "pinyin": "jī", "meaning": "会打鸣的鸡"},
        {"word": "狗", "pinyin": "gǒu", "meaning": "看家的狗"},
        {"word": "猪", "pinyin": "zhū", "meaning": "胖胖的猪"},
        {"word": "猫", "pinyin": "māo", "meaning": "会抓老鼠的猫"},
        {"word": "鱼", "pinyin": "yú", "meaning": "水里游的鱼"},
        {"word": "鸟", "pinyin": "niǎo", "meaning": "天上飞的鸟"},
        # 食物和动作 (10个)
        {"word": "饭", "pinyin": "fàn", "meaning": "吃的米饭"},
        {"word": "菜", "pinyin": "cài", "meaning": "吃的蔬菜"},
        {"word": "肉", "pinyin": "ròu", "meaning": "吃的肉"},
        {"word": "果", "pinyin": "guǒ", "meaning": "吃的水果"},
        {"word": "茶", "pinyin": "chá", "meaning": "喝的茶"},
        {"word": "吃", "pinyin": "chī", "meaning": "吃东西"},
        {"word": "喝", "pinyin": "hē", "meaning": "喝水"},
        {"word": "走", "pinyin": "zǒu", "meaning": "走路"},
        {"word": "跑", "pinyin": "pǎo", "meaning": "跑步"},
        {"word": "跳", "pinyin": "tiào", "meaning": "跳起来"},
    ]
}

ENGLISH_DATABASE = {
    "简单": [
        # Numbers (10)
        {"word": "one", "pinyin": "/wʌn/", "meaning": "数字一"},
        {"word": "two", "pinyin": "/tuː/", "meaning": "数字二"},
        {"word": "three", "pinyin": "/θriː/", "meaning": "数字三"},
        {"word": "four", "pinyin": "/fɔːr/", "meaning": "数字四"},
        {"word": "five", "pinyin": "/faɪv/", "meaning": "数字五"},
        {"word": "six", "pinyin": "/sɪks/", "meaning": "数字六"},
        {"word": "seven", "pinyin": "/ˈsevən/", "meaning": "数字七"},
        {"word": "eight", "pinyin": "/eɪt/", "meaning": "数字八"},
        {"word": "nine", "pinyin": "/naɪn/", "meaning": "数字九"},
        {"word": "ten", "pinyin": "/ten/", "meaning": "数字十"},
        # Basic words (20)
        {"word": "man", "pinyin": "/mæn/", "meaning": "男人"},
        {"word": "mouth", "pinyin": "/maʊθ/", "meaning": "嘴巴"},
        {"word": "hand", "pinyin": "/hænd/", "meaning": "手掌"},
        {"word": "foot", "pinyin": "/fʊt/", "meaning": "脚"},
        {"word": "eye", "pinyin": "/aɪ/", "meaning": "眼睛"},
        {"word": "ear", "pinyin": "/ɪr/", "meaning": "耳朵"},
        {"word": "big", "pinyin": "/bɪɡ/", "meaning": "很大的"},
        {"word": "small", "pinyin": "/smɔːl/", "meaning": "很小的"},
        {"word": "up", "pinyin": "/ʌp/", "meaning": "在上面"},
        {"word": "down", "pinyin": "/daʊn/", "meaning": "在下面"},
        {"word": "left", "pinyin": "/left/", "meaning": "在左边"},
        {"word": "right", "pinyin": "/raɪt/", "meaning": "在右边"},
        {"word": "sky", "pinyin": "/skaɪ/", "meaning": "天空"},
        {"word": "ground", "pinyin": "/ɡraʊnd/", "meaning": "地面"},
        {"word": "sun", "pinyin": "/sʌn/", "meaning": "太阳"},
        {"word": "moon", "pinyin": "/muːn/", "meaning": "月亮"},
        {"word": "water", "pinyin": "/ˈwɔːtər/", "meaning": "喝的水"},
        {"word": "fire", "pinyin": "/ˈfaɪər/", "meaning": "火焰"},
        {"word": "hill", "pinyin": "/hɪl/", "meaning": "小山"},
        {"word": "rock", "pinyin": "/rɑːk/", "meaning": "石头"},
    ],
    "中等": [
        # Family (10)
        {"word": "dad", "pinyin": "/dæd/", "meaning": "爸爸"},
        {"word": "mom", "pinyin": "/mɑːm/", "meaning": "妈妈"},
        {"word": "brother", "pinyin": "/ˈbrʌðər/", "meaning": "哥哥或弟弟"},
        {"word": "sister", "pinyin": "/ˈsɪstər/", "meaning": "姐姐或妹妹"},
        {"word": "boy", "pinyin": "/bɔɪ/", "meaning": "男孩"},
        {"word": "girl", "pinyin": "/ɡɜːrl/", "meaning": "女孩"},
        {"word": "grandpa", "pinyin": "/ˈɡrænpɑː/", "meaning": "爷爷"},
        {"word": "grandma", "pinyin": "/ˈɡrænmɑː/", "meaning": "奶奶"},
        {"word": "uncle", "pinyin": "/ˈʌŋkl/", "meaning": "叔叔"},
        {"word": "aunt", "pinyin": "/ænt/", "meaning": "阿姨"},
        # Daily items (15)
        {"word": "home", "pinyin": "/hoʊm/", "meaning": "我们住的家"},
        {"word": "door", "pinyin": "/dɔːr/", "meaning": "进出的门"},
        {"word": "window", "pinyin": "/ˈwɪndoʊ/", "meaning": "窗户"},
        {"word": "bed", "pinyin": "/bed/", "meaning": "睡觉的床"},
        {"word": "table", "pinyin": "/ˈteɪbl/", "meaning": "桌子"},
        {"word": "chair", "pinyin": "/tʃer/", "meaning": "椅子"},
        {"word": "lamp", "pinyin": "/læmp/", "meaning": "照明的灯"},
        {"word": "book", "pinyin": "/bʊk/", "meaning": "看的书"},
        {"word": "pen", "pinyin": "/pen/", "meaning": "写字的笔"},
        {"word": "paper", "pinyin": "/ˈpeɪpər/", "meaning": "写字的纸"},
        {"word": "bag", "pinyin": "/bæɡ/", "meaning": "背的书包"},
        {"word": "shirt", "pinyin": "/ʃɜːrt/", "meaning": "穿的衣服"},
        {"word": "shoe", "pinyin": "/ʃuː/", "meaning": "穿的鞋子"},
        {"word": "hat", "pinyin": "/hæt/", "meaning": "戴的帽子"},
        {"word": "umbrella", "pinyin": "/ʌmˈbrelə/", "meaning": "遮雨的伞"},
    ],
    "困难": [
        # Animals (15)
        {"word": "mouse", "pinyin": "/maʊs/", "meaning": "小老鼠"},
        {"word": "ox", "pinyin": "/ɑːks/", "meaning": "大黄牛"},
        {"word": "tiger", "pinyin": "/ˈtaɪɡər/", "meaning": "大老虎"},
        {"word": "rabbit", "pinyin": "/ˈræbɪt/", "meaning": "小兔子"},
        {"word": "dragon", "pinyin": "/ˈdræɡən/", "meaning": "神话中的龙"},
        {"word": "snake", "pinyin": "/sneɪk/", "meaning": "长长的蛇"},
        {"word": "horse", "pinyin": "/hɔːrs/", "meaning": "跑得快的马"},
        {"word": "sheep", "pinyin": "/ʃiːp/", "meaning": "温顺的羊"},
        {"word": "monkey", "pinyin": "/ˈmʌŋki/", "meaning": "爱吃香蕉的猴子"},
        {"word": "chicken", "pinyin": "/ˈtʃɪkɪn/", "meaning": "会打鸣的鸡"},
        {"word": "dog", "pinyin": "/dɔːɡ/", "meaning": "看家的狗"},
        {"word": "pig", "pinyin": "/pɪɡ/", "meaning": "胖胖的猪"},
        {"word": "cat", "pinyin": "/kæt/", "meaning": "会抓老鼠的猫"},
        {"word": "fish", "pinyin": "/fɪʃ/", "meaning": "水里游的鱼"},
        {"word": "bird", "pinyin": "/bɜːrd/", "meaning": "天上飞的鸟"},
        # Food & Actions (10)
        {"word": "rice", "pinyin": "/raɪs/", "meaning": "吃的米饭"},
        {"word": "vegetable", "pinyin": "/ˈvedʒtəbl/", "meaning": "吃的蔬菜"},
        {"word": "meat", "pinyin": "/miːt/", "meaning": "吃的肉"},
        {"word": "fruit", "pinyin": "/fruːt/", "meaning": "吃的水果"},
        {"word": "tea", "pinyin": "/tiː/", "meaning": "喝的茶"},
        {"word": "eat", "pinyin": "/iːt/", "meaning": "吃东西"},
        {"word": "drink", "pinyin": "/drɪŋk/", "meaning": "喝水"},
        {"word": "walk", "pinyin": "/wɔːk/", "meaning": "走路"},
        {"word": "run", "pinyin": "/rʌn/", "meaning": "跑步"},
        {"word": "jump", "pinyin": "/dʒʌmp/", "meaning": "跳起来"},
    ]
}

THEMES = {
    "粉红梦幻": {"bg": (255, 200, 220), "text_color": (200, 50, 100)},
    "蓝天白云": {"bg": (200, 230, 255), "text_color": (0, 100, 200)},
    "绿色森林": {"bg": (200, 255, 200), "text_color": (0, 150, 0)},
    "紫色魔法": {"bg": (230, 200, 255), "text_color": (150, 0, 150)},
    "彩虹缤纷": {"bg": (255, 240, 200), "text_color": (200, 100, 0)},
}

# 组词游戏数据库 - 常用双字词语
WORD_COMBINATIONS = {
    "简单": [
        {"chars": ["大", "人"], "word": "大人", "meaning": "成年人"},
        {"chars": ["小", "孩"], "word": "小孩", "meaning": "小朋友"},
        {"chars": ["上", "下"], "word": "上下", "meaning": "上面和下面"},
        {"chars": ["左", "右"], "word": "左右", "meaning": "左边和右边"},
        {"chars": ["天", "上"], "word": "天上", "meaning": "天空中"},
        {"chars": ["地", "下"], "word": "地下", "meaning": "地面下"},
        {"chars": ["日", "月"], "word": "日月", "meaning": "太阳和月亮"},
        {"chars": ["水", "火"], "word": "水火", "meaning": "水和火"},
        {"chars": ["山", "水"], "word": "山水", "meaning": "山和水"},
        {"chars": ["大", "小"], "word": "大小", "meaning": "大和小"},
    ],
    "中等": [
        {"chars": ["爸", "爸"], "word": "爸爸", "meaning": "父亲"},
        {"chars": ["妈", "妈"], "word": "妈妈", "meaning": "母亲"},
        {"chars": ["哥", "哥"], "word": "哥哥", "meaning": "兄长"},
        {"chars": ["姐", "姐"], "word": "姐姐", "meaning": "姊姊"},
        {"chars": ["弟", "弟"], "word": "弟弟", "meaning": "弟弟"},
        {"chars": ["妹", "妹"], "word": "妹妹", "meaning": "妹妹"},
        {"chars": ["爷", "爷"], "word": "爷爷", "meaning": "祖父"},
        {"chars": ["奶", "奶"], "word": "奶奶", "meaning": "祖母"},
        {"chars": ["书", "包"], "word": "书包", "meaning": "装书的包"},
        {"chars": ["桌", "椅"], "word": "桌椅", "meaning": "桌子和椅子"},
        {"chars": ["门", "窗"], "word": "门窗", "meaning": "门和窗户"},
        {"chars": ["衣", "服"], "word": "衣服", "meaning": "穿的衣物"},
    ],
    "困难": [
        {"chars": ["学", "校"], "word": "学校", "meaning": "上学的地方"},
        {"chars": ["老", "师"], "word": "老师", "meaning": "教书的人"},
        {"chars": ["同", "学"], "word": "同学", "meaning": "一起学习的人"},
        {"chars": ["朋", "友"], "word": "朋友", "meaning": "好伙伴"},
        {"chars": ["家", "人"], "word": "家人", "meaning": "家里的人"},
        {"chars": ["动", "物"], "word": "动物", "meaning": "会动的生物"},
        {"chars": ["植", "物"], "word": "植物", "meaning": "花草树木"},
        {"chars": ["太", "阳"], "word": "太阳", "meaning": "天上的太阳"},
        {"chars": ["月", "亮"], "word": "月亮", "meaning": "夜晚的月亮"},
        {"chars": ["星", "星"], "word": "星星", "meaning": "天上的星星"},
    ]
}

class WordGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("儿童识字游戏")
        self.clock = pygame.time.Clock()
        
        # 创建简单的音效
        self.init_sounds()
        
        # 使用统一的字体 - Arial Unicode支持中文、英文和音标
        unified_font_path = None
        
        # 优先使用Arial Unicode，它支持所有字符
        font_candidates = [
            # macOS
            "/Library/Fonts/Arial Unicode.ttf",
            "/System/Library/Fonts/STHeiti Medium.ttc",
            "/System/Library/Fonts/Supplemental/Songti.ttc",
            # Windows
            "C:/Windows/Fonts/msyh.ttc",       # 微软雅黑
            "C:/Windows/Fonts/simsun.ttc",      # 宋体
            "C:/Windows/Fonts/simhei.ttf",      # 黑体
            # Linux
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
            "/usr/share/fonts/truetype/arphic/uming.ttc",
        ]
        
        for path in font_candidates:
            if os.path.exists(path):
                unified_font_path = path
                break
        
        if unified_font_path:
            self.font_large = pygame.font.Font(unified_font_path, 48)
            self.font_medium = pygame.font.Font(unified_font_path, 32)
            self.font_small = pygame.font.Font(unified_font_path, 24)
            self.font_tiny = pygame.font.Font(unified_font_path, 18)
        else:
            self.font_large = pygame.font.Font(None, 48)
            self.font_medium = pygame.font.Font(None, 32)
            self.font_small = pygame.font.Font(None, 24)
            self.font_tiny = pygame.font.Font(None, 18)
        
        self.mode = "menu"
        self.language = "中文"
        self.difficulty = "简单"
        self.theme = "粉红梦幻"
        self.current_question = None
        self.options = []
        self.learn_page = 0  # 学习模式的页码
        
        # 打地鼠游戏状态
        self.whack_score = 0
        self.whack_time = 30  # 30秒倒计时
        self.whack_start_time = 0
        self.whack_moles = []  # 地鼠列表
        self.whack_target_word = None
        
        # 记忆翻牌游戏状态
        self.memory_cards = []
        self.memory_flipped = []
        self.memory_matched = []
        self.memory_first_card = None
        self.memory_second_card = None
        self.memory_lock = False
        self.memory_lock_time = 0
        
        # 拼字游戏状态
        self.spell_target = None
        self.spell_score = 0
        
        # 点击效果状态
        self.clicked_card = None
        self.click_time = 0
        
        # 连连看游戏状态
        self.match_cards = []
        self.match_selected = []
        self.match_matched = []
        self.match_score = 0
        self.match_flip_time = 0   # 答错后延迟清除选择的时间戳
        
        # 听音选字游戏状态
        self.chain_words = []
        self.chain_current_index = 0
        self.chain_current_word = None
        self.chain_options = []
        self.chain_score = 0
        self.chain_audio_played = False  # 是否已播放语音
        self.chain_selected_index = -1  # 选中的选项索引
        self.chain_wrong_index = -1  # 错误的选项索引
        self.chain_correct_index = -1  # 正确的选项索引
        self.chain_effect_time = 0  # 效果显示时间
        
        # 计时挑战游戏状态
        self.time_challenge_start = 0
        self.time_challenge_duration = 60  # 60秒
        self.time_challenge_score = 0
        self.time_challenge_question = None
        self.time_challenge_options = []
        
        self.load_progress()
    
    def init_sounds(self):
        """初始化音效（预留接口，当前未启用）"""
        self.click_sound = None
        self.correct_sound = None
        self.wrong_sound = None
    
    def play_sound(self, sound_type):
        """播放音效"""
        try:
            if sound_type == "click" and self.click_sound:
                self.click_sound.play()
            elif sound_type == "correct" and self.correct_sound:
                self.correct_sound.play()
            elif sound_type == "wrong" and self.wrong_sound:
                self.wrong_sound.play()
        except Exception as e:
            logging.warning("play_sound 失败: %s", e)
    
    def speak_word(self, word, rate=200, wait=False, force_chinese=False):
        """朗读单词（使用系统TTS）"""
        try:
            system = platform.system()
            if system == "Darwin":  # macOS
                if force_chinese or self.language == "中文":
                    voice = "Mei-Jia"
                else:
                    voice = "Samantha"
                cmd = ["say", "-v", voice, "-r", str(rate), word]
                if wait:
                    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                else:
                    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            elif system == "Windows":
                # Windows 使用 PowerShell SAPI，隐藏控制台窗口
                ps_script = (
                    f"Add-Type -AssemblyName System.Speech; "
                    f"$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
                    f"$s.Rate = {max(-10, min(10, (rate - 200) // 20))}; "
                    f"$s.Speak('{word}')"
                )
                cmd = ["powershell", "-WindowStyle", "Hidden", "-Command", ps_script]
                si = subprocess.STARTUPINFO()
                si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                si.wShowWindow = 0  # SW_HIDE
                if wait:
                    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                   startupinfo=si)
                else:
                    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                     startupinfo=si)
            elif system == "Linux":
                # Linux 使用 espeak（需安装）
                cmd = ["espeak", "-s", str(rate), word]
                if wait:
                    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                else:
                    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            logging.warning("speak_word 失败: %s", e)
    
    def load_progress(self):
        try:
            if os.path.exists("word_game_progress.json"):
                with open("word_game_progress.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.language = data.get("language", "中文")
                    self.difficulty = data.get("difficulty", "简单")
                    self.theme = data.get("theme", "粉红梦幻")
        except Exception as e:
            logging.warning("load_progress 失败: %s", e)
    
    def save_progress(self):
        try:
            data = {
                "language": self.language,
                "difficulty": self.difficulty,
                "theme": self.theme
            }
            with open("word_game_progress.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logging.warning("save_progress 失败: %s", e)
    
    def get_current_database(self):
        if self.language == "中文":
            return CHINESE_DATABASE
        else:
            return ENGLISH_DATABASE
    
    def get_ui_text(self, key):
        """获取界面文字"""
        return UI_TEXT[self.language].get(key, key)
    
    def get_difficulty_text(self):
        """获取难度文字"""
        difficulty_map = {
            "简单": self.get_ui_text("easy"),
            "中等": self.get_ui_text("medium"),
            "困难": self.get_ui_text("hard")
        }
        return difficulty_map.get(self.difficulty, self.difficulty)
    
    def draw_menu(self):
        theme_data = THEMES[self.theme]
        self.screen.fill(theme_data["bg"])
        
        # 标题 - 简洁版
        title_text = self.get_ui_text("title")
        title = self.font_large.render(title_text, True, theme_data["text_color"])
        self.screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 30))
        
        # 设置区域
        y_offset = 110
        
        # 语言选择
        lang_text = "中文" if self.language == "中文" else "English"
        pygame.draw.rect(self.screen, WHITE, (60, y_offset, 250, 45), border_radius=8)
        pygame.draw.rect(self.screen, theme_data["text_color"], (60, y_offset, 250, 45), 3, border_radius=8)
        lang = self.font_small.render(f"{self.get_ui_text('language')}: {lang_text}", True, theme_data["text_color"])
        self.screen.blit(lang, (80, y_offset + 12))
        
        # 难度选择
        diff_text = self.get_difficulty_text()
        pygame.draw.rect(self.screen, WHITE, (330, y_offset, 250, 45), border_radius=8)
        pygame.draw.rect(self.screen, theme_data["text_color"], (330, y_offset, 250, 45), 3, border_radius=8)
        diff = self.font_small.render(f"{self.get_ui_text('difficulty')}: {diff_text}", True, theme_data["text_color"])
        self.screen.blit(diff, (350, y_offset + 12))
        
        # 主题选择
        pygame.draw.rect(self.screen, WHITE, (600, y_offset, 240, 45), border_radius=8)
        pygame.draw.rect(self.screen, theme_data["text_color"], (600, y_offset, 240, 45), 3, border_radius=8)
        # 颜色预览小圆点
        pygame.draw.circle(self.screen, theme_data["text_color"], (625, y_offset + 22), 8)
        theme = self.font_small.render(f"{self.get_ui_text('theme')}: {self.theme[:4]}", True, theme_data["text_color"])
        self.screen.blit(theme, (645, y_offset + 12))
        
        # 游戏模式标题
        modes_title = self.font_medium.render(self.get_ui_text("modes"), True, theme_data["text_color"])
        self.screen.blit(modes_title, (WINDOW_WIDTH // 2 - modes_title.get_width() // 2, 180))
        
        # 8个游戏模式按钮 (4行2列)
        modes = [
            "mode_learn", "mode_quiz", "mode_spell", "mode_match",
            "mode_whack", "mode_memory", "mode_chain", "mode_time"
        ]
        
        for i, mode_key in enumerate(modes):
            x = 80 + (i % 2) * 380
            y = 230 + (i // 2) * 100
            
            # 按钮
            pygame.draw.rect(self.screen, theme_data["text_color"], (x, y, 340, 70), border_radius=15)
            
            mode_text = self.font_medium.render(self.get_ui_text(mode_key), True, WHITE)
            self.screen.blit(mode_text, (x + 170 - mode_text.get_width() // 2, y + 22))
    
    def draw_learn_mode(self):
        theme_data = THEMES[self.theme]
        self.screen.fill(theme_data["bg"])
        
        # 标题
        title_text = self.get_ui_text("mode_learn")
        title = self.font_medium.render(title_text, True, theme_data["text_color"])
        self.screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 20))
        
        database = self.get_current_database()
        words = database[self.difficulty]
        
        # 每页显示8个单词（2行4列）
        words_per_page = 8
        total_pages = (len(words) + words_per_page - 1) // words_per_page
        start_idx = self.learn_page * words_per_page
        end_idx = min(start_idx + words_per_page, len(words))
        page_words = words[start_idx:end_idx]
        
        # 显示页码
        page_text = f"{self.learn_page + 1} / {total_pages}"
        page_info = self.font_small.render(page_text, True, theme_data["text_color"])
        self.screen.blit(page_info, (WINDOW_WIDTH // 2 - page_info.get_width() // 2, 60))
        
        # 检查点击效果是否过期
        current_time = pygame.time.get_ticks()
        if self.clicked_card is not None and current_time - self.click_time > 200:
            self.clicked_card = None
        
        # 显示单词卡片（2行4列）
        for i, word_data in enumerate(page_words):
            x = 50 + (i % 4) * 210
            y = 110 + (i // 4) * 220
            
            # 检查是否是被点击的卡片
            is_clicked = (self.clicked_card == i and current_time - self.click_time < 200)
            
            # 如果被点击，添加高亮效果
            if is_clicked:
                # 绘制发光效果
                glow_rect = pygame.Rect(x - 5, y - 5, 200, 190)
                pygame.draw.rect(self.screen, (255, 255, 100), glow_rect, border_radius=12)
                
                # 卡片稍微缩小
                card_x, card_y = x + 3, y + 3
                card_w, card_h = 184, 174
            else:
                card_x, card_y = x, y
                card_w, card_h = 190, 180
            
            # 卡片背景
            pygame.draw.rect(self.screen, WHITE, (card_x, card_y, card_w, card_h), border_radius=10)
            # 卡片边框
            pygame.draw.rect(self.screen, theme_data["text_color"], (card_x, card_y, card_w, card_h), 3, border_radius=10)
            
            # 单词 - 根据长度调整字体大小
            word_text = word_data["word"]
            if len(word_text) > 7:
                word_font = self.font_medium
            else:
                word_font = self.font_large
            word = word_font.render(word_text, True, theme_data["text_color"])
            
            # 如果单词太宽，缩小字体
            if word.get_width() > 170:
                word_font = self.font_small
                word = word_font.render(word_text, True, theme_data["text_color"])
            
            word_x = card_x + card_w // 2 - word.get_width() // 2
            self.screen.blit(word, (word_x, card_y + 30))
            
            # 拼音
            pinyin_text = word_data["pinyin"]
            pinyin = self.font_small.render(pinyin_text, True, (100, 100, 150))
            
            if pinyin.get_width() > 170:
                pinyin = self.font_tiny.render(pinyin_text, True, (100, 100, 150))
            
            pinyin_x = card_x + card_w // 2 - pinyin.get_width() // 2
            self.screen.blit(pinyin, (pinyin_x, card_y + 90))
            
            # 意思
            meaning_text = word_data["meaning"]
            meaning = self.font_small.render(meaning_text, True, (80, 80, 80))
            
            if meaning.get_width() > 170:
                meaning = self.font_tiny.render(meaning_text, True, (80, 80, 80))
            
            meaning_x = card_x + card_w // 2 - meaning.get_width() // 2
            self.screen.blit(meaning, (meaning_x, card_y + 135))
        
        # 底部按钮区域
        # 上一页按钮
        if self.learn_page > 0:
            pygame.draw.rect(self.screen, theme_data["text_color"], (60, 600, 120, 60), border_radius=10)
            prev_text = self.font_small.render("< " + ("上页" if self.language == "中文" else "Prev"), True, WHITE)
            self.screen.blit(prev_text, (120 - prev_text.get_width() // 2, 615))
        
        # 返回按钮
        pygame.draw.rect(self.screen, theme_data["text_color"], (390, 600, 120, 60), border_radius=10)
        back = self.font_small.render(self.get_ui_text("back"), True, WHITE)
        self.screen.blit(back, (450 - back.get_width() // 2, 615))
        
        # 下一页按钮
        if self.learn_page < total_pages - 1:
            pygame.draw.rect(self.screen, theme_data["text_color"], (720, 600, 120, 60), border_radius=10)
            next_text = self.font_small.render(("下页" if self.language == "中文" else "Next") + " >", True, WHITE)
            self.screen.blit(next_text, (780 - next_text.get_width() // 2, 615))
    
    def draw_quiz_mode(self):
        theme_data = THEMES[self.theme]
        self.screen.fill(theme_data["bg"])
        
        # 标题
        title = self.font_medium.render(self.get_ui_text("mode_quiz"), True, theme_data["text_color"])
        self.screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 15))
        
        if not self.current_question:
            self.generate_question()
        
        # 显示问题
        if self.language == "中文":
            question_text = f"请选择拼音为 '{self.current_question['pinyin']}' 的字"
        else:
            question_text = f"Select word with pronunciation '{self.current_question['pinyin']}'"
        
        question = self.font_small.render(question_text, True, theme_data["text_color"])
        self.screen.blit(question, (WINDOW_WIDTH // 2 - question.get_width() // 2, 90))
        
        # 显示选项
        for i, option in enumerate(self.options):
            x = 120 + (i % 2) * 380
            y = 170 + (i // 2) * 150
            
            pygame.draw.rect(self.screen, WHITE, (x, y, 340, 120), border_radius=10)
            pygame.draw.rect(self.screen, theme_data["text_color"], (x, y, 340, 120), 3, border_radius=10)
            
            word = self.font_large.render(option["word"], True, theme_data["text_color"])
            self.screen.blit(word, (x + 170 - word.get_width() // 2, y + 40))
        
        # 返回按钮
        pygame.draw.rect(self.screen, theme_data["text_color"], (60, 600, 150, 60), border_radius=10)
        back = self.font_medium.render(self.get_ui_text("back"), True, WHITE)
        self.screen.blit(back, (135 - back.get_width() // 2, 615))
    
    def draw_coming_soon(self, mode_name):
        """显示即将推出的模式"""
        theme_data = THEMES[self.theme]
        self.screen.fill(theme_data["bg"])
        
        # 标题
        title = self.font_medium.render(self.get_ui_text(mode_name), True, theme_data["text_color"])
        self.screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 120))
        
        # 即将推出
        coming_text = "即将推出..." if self.language == "中文" else "Coming Soon..."
        coming = self.font_large.render(coming_text, True, theme_data["text_color"])
        self.screen.blit(coming, (WINDOW_WIDTH // 2 - coming.get_width() // 2, 220))
        
        # 提示信息
        if self.language == "中文":
            hint_lines = [
                "这个游戏正在开发中",
                "敬请期待更多精彩内容！",
                "",
                "目前可以玩：",
                "• 学习模式 - 认识汉字",
                "• 测验模式 - 测试学习",
                "• 拼字游戏 - 看字学拼音",
                "• 打地鼠 - 快速反应",
                "• 记忆翻牌 - 记忆力训练"
            ]
        else:
            hint_lines = [
                "This game is under development",
                "Stay tuned for more content!",
                "",
                "Available now:",
                "• Learn - Learn characters",
                "• Quiz - Test your knowledge",
                "• Spell - Learn pronunciation",
                "• Whack - Quick reaction",
                "• Memory - Memory training"
            ]
        
        y_offset = 320
        for line in hint_lines:
            if line:
                hint = self.font_small.render(line, True, theme_data["text_color"])
                self.screen.blit(hint, (WINDOW_WIDTH // 2 - hint.get_width() // 2, y_offset))
            y_offset += 35
        
        # 返回按钮
        pygame.draw.rect(self.screen, theme_data["text_color"], (325, 580, 250, 70), border_radius=10)
        back = self.font_medium.render(self.get_ui_text("back"), True, WHITE)
        self.screen.blit(back, (450 - back.get_width() // 2, 600))
    
    def init_whack_game(self):
        """初始化打地鼠游戏"""
        self.whack_score = 0
        self.whack_start_time = pygame.time.get_ticks()
        self.whack_moles = []
        database = self.get_current_database()
        words = database[self.difficulty]
        self.whack_target_word = random.choice(words)
        
        # 生成地鼠（包含正确和错误的字）
        for i in range(9):
            if random.random() < 0.3:  # 30%概率出现正确的字
                word = self.whack_target_word
            else:
                word = random.choice(words)
            
            self.whack_moles.append({
                "word": word,
                "x": 80 + (i % 3) * 270,
                "y": 150 + (i // 3) * 150,
                "visible": random.random() < 0.5,
                "last_change": pygame.time.get_ticks()
            })
    
    def draw_whack_game(self):
        """绘制打地鼠游戏"""
        theme_data = THEMES[self.theme]
        self.screen.fill(theme_data["bg"])
        
        # 计算剩余时间
        elapsed = (pygame.time.get_ticks() - self.whack_start_time) / 1000
        remaining = max(0, self.whack_time - int(elapsed))
        
        # 标题和信息
        title = self.font_medium.render(self.get_ui_text("mode_whack"), True, theme_data["text_color"])
        self.screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 15))
        
        # 目标字
        target_text = f"{'找' if self.language == '中文' else 'Find'}: {self.whack_target_word['word']}"
        target = self.font_small.render(target_text, True, theme_data["text_color"])
        self.screen.blit(target, (100, 60))
        
        # 分数和时间
        score_text = f"{'分数' if self.language == '中文' else 'Score'}: {self.whack_score}"
        score = self.font_small.render(score_text, True, theme_data["text_color"])
        self.screen.blit(score, (400, 60))
        
        time_text = f"{'时间' if self.language == '中文' else 'Time'}: {remaining}s"
        time_display = self.font_small.render(time_text, True, theme_data["text_color"])
        self.screen.blit(time_display, (650, 60))
        
        # 游戏结束
        if remaining == 0:
            result = self.font_large.render(f"{'游戏结束！得分' if self.language == '中文' else 'Game Over! Score'}: {self.whack_score}", 
                                           True, theme_data["text_color"])
            self.screen.blit(result, (WINDOW_WIDTH // 2 - result.get_width() // 2, 300))
            
            pygame.draw.rect(self.screen, theme_data["text_color"], (325, 400, 250, 70), border_radius=10)
            again_text = "再玩一次" if self.language == "中文" else "Play Again"
            again = self.font_medium.render(again_text, True, WHITE)
            self.screen.blit(again, (450 - again.get_width() // 2, 420))
        else:
            # 更新地鼠状态
            current_time = pygame.time.get_ticks()
            for mole in self.whack_moles:
                if current_time - mole["last_change"] > 800:  # 每0.8秒切换
                    mole["visible"] = random.random() < 0.6
                    mole["last_change"] = current_time
                    # 随机更换字
                    if random.random() < 0.3:
                        mole["word"] = self.whack_target_word
                    else:
                        database = self.get_current_database()
                        words = database[self.difficulty]
                        mole["word"] = random.choice(words)
                
                # 绘制地鼠洞
                pygame.draw.rect(self.screen, (139, 90, 43), 
                               (mole["x"], mole["y"], 240, 120), border_radius=10)
                
                # 绘制地鼠（如果可见）
                if mole["visible"]:
                    is_correct = mole["word"]["word"] == self.whack_target_word["word"]
                    color = (100, 200, 100) if is_correct else (200, 100, 100)
                    pygame.draw.rect(self.screen, color, 
                                   (mole["x"] + 20, mole["y"] + 20, 200, 80), border_radius=10)
                    
                    word = self.font_large.render(mole["word"]["word"], True, WHITE)
                    self.screen.blit(word, (mole["x"] + 120 - word.get_width() // 2, mole["y"] + 45))
        
        # 返回按钮
        pygame.draw.rect(self.screen, theme_data["text_color"], (60, 600, 150, 60), border_radius=10)
        back = self.font_small.render(self.get_ui_text("back"), True, WHITE)
        self.screen.blit(back, (135 - back.get_width() // 2, 615))
    
    def init_memory_game(self):
        """初始化记忆翻牌游戏"""
        database = self.get_current_database()
        words = database[self.difficulty]
        
        # 选择6个不同的字，每个字2张牌
        selected_words = random.sample(words, 6)
        self.memory_cards = []
        
        for i, word in enumerate(selected_words):
            self.memory_cards.append({"word": word, "pair_id": i})
            self.memory_cards.append({"word": word, "pair_id": i})
        
        random.shuffle(self.memory_cards)
        self.memory_flipped = []
        self.memory_matched = []
        self.memory_first_card = None
        self.memory_second_card = None
        self.memory_lock = False
    
    def draw_memory_game(self):
        """绘制记忆翻牌游戏"""
        theme_data = THEMES[self.theme]
        self.screen.fill(theme_data["bg"])
        
        # 标题
        title = self.font_medium.render(self.get_ui_text("mode_memory"), True, theme_data["text_color"])
        self.screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 15))
        
        # 配对数
        matched_pairs = len(self.memory_matched) // 2
        pairs_text = f"{'配对' if self.language == '中文' else 'Pairs'}: {matched_pairs}/6"
        pairs = self.font_small.render(pairs_text, True, theme_data["text_color"])
        self.screen.blit(pairs, (WINDOW_WIDTH // 2 - pairs.get_width() // 2, 55))
        
        # 检查是否需要翻回卡片
        if self.memory_lock and pygame.time.get_ticks() - self.memory_lock_time > 1000:
            self.memory_flipped.remove(self.memory_first_card)
            self.memory_flipped.remove(self.memory_second_card)
            self.memory_first_card = None
            self.memory_second_card = None
            self.memory_lock = False
        
        # 绘制卡片（4行3列）
        for i, card in enumerate(self.memory_cards):
            x = 120 + (i % 4) * 180
            y = 100 + (i // 4) * 160
            
            is_flipped = i in self.memory_flipped or i in self.memory_matched
            
            if is_flipped:
                # 显示字
                pygame.draw.rect(self.screen, WHITE, (x, y, 160, 140), border_radius=10)
                pygame.draw.rect(self.screen, theme_data["text_color"], (x, y, 160, 140), 3, border_radius=10)
                
                word = self.font_large.render(card["word"]["word"], True, theme_data["text_color"])
                self.screen.blit(word, (x + 80 - word.get_width() // 2, y + 50))
            else:
                # 显示背面
                pygame.draw.rect(self.screen, theme_data["text_color"], (x, y, 160, 140), border_radius=10)
                question = self.font_large.render("?", True, WHITE)
                self.screen.blit(question, (x + 80 - question.get_width() // 2, y + 50))
        
        # 游戏完成
        if len(self.memory_matched) == 12:
            congrats_text = "完成！" if self.language == "中文" else "Complete!"
            congrats = self.font_large.render(congrats_text, True, theme_data["text_color"])
            self.screen.blit(congrats, (WINDOW_WIDTH // 2 - congrats.get_width() // 2, 550))
        
        # 返回按钮
        pygame.draw.rect(self.screen, theme_data["text_color"], (60, 600, 150, 60), border_radius=10)
        back = self.font_small.render(self.get_ui_text("back"), True, WHITE)
        self.screen.blit(back, (135 - back.get_width() // 2, 615))
    
    def init_spell_game(self):
        """初始化组词游戏"""
        # 根据难度选择词语
        if self.language == "中文":
            words = WORD_COMBINATIONS[self.difficulty]
        else:
            # 英文模式暂时使用中文词语
            words = WORD_COMBINATIONS[self.difficulty]
        
        self.spell_target = random.choice(words)
        self.spell_selected = []  # 已选择的字
        self.spell_score = 0
        
        # 准备可选择的字（包含正确的字和干扰字）
        chars = self.spell_target["chars"].copy()
        
        # 添加一些干扰字
        database = self.get_current_database()
        all_words = database[self.difficulty]
        distractor_chars = []
        for _ in range(2):  # 添加2个干扰字
            random_word = random.choice(all_words)
            distractor_chars.append(random_word["word"])
        
        self.spell_options = chars + distractor_chars
        random.shuffle(self.spell_options)
    
    def init_match_game(self):
        """初始化连连看游戏"""
        database = self.get_current_database()
        words = database[self.difficulty]
        
        # 选择8个不同的字，每个字2张牌
        selected_words = random.sample(words, 8)
        self.match_cards = []
        
        for i, word in enumerate(selected_words):
            self.match_cards.append({"word": word, "pair_id": i, "type": "word"})
            self.match_cards.append({"word": word, "pair_id": i, "type": "meaning"})
        
        random.shuffle(self.match_cards)
        self.match_selected = []
        self.match_matched = []
        self.match_score = 0
    
    def init_chain_game(self):
        """初始化听音选字游戏"""
        database = self.get_current_database()
        words = database[self.difficulty]
        
        # 获取所有字并打乱顺序
        self.chain_words = words.copy()
        random.shuffle(self.chain_words)
        
        # 从第一个字开始
        self.chain_current_index = 0
        self.chain_score = 0
        
        # 生成第一题
        self.generate_chain_question()
    
    def generate_chain_question(self):
        """生成听音选字的问题"""
        if self.chain_current_index >= len(self.chain_words):
            # 所有题目完成，重新开始
            self.chain_current_index = 0
            random.shuffle(self.chain_words)
        
        # 当前要学习的字
        self.chain_current_word = self.chain_words[self.chain_current_index]
        
        # 生成4个选项（包含正确答案）
        self.chain_options = [self.chain_current_word]
        
        # 添加3个干扰项
        other_words = [w for w in self.chain_words if w != self.chain_current_word]
        self.chain_options.extend(random.sample(other_words, 3))
        
        # 打乱选项顺序
        random.shuffle(self.chain_options)
        
        # 标记为未播放语音
        self.chain_audio_played = False
        
        # 重置选中效果
        self.chain_selected_index = -1
        self.chain_wrong_index = -1
        self.chain_correct_index = -1
        self.chain_effect_time = 0
    
    def init_time_challenge(self):
        """初始化计时挑战游戏"""
        self.time_challenge_start = pygame.time.get_ticks()
        self.time_challenge_score = 0
        self.generate_time_question()
    
    def generate_time_question(self):
        """生成计时挑战的问题"""
        database = self.get_current_database()
        words = database[self.difficulty]
        
        self.time_challenge_question = random.choice(words)
        self.time_challenge_options = [self.time_challenge_question]
        
        while len(self.time_challenge_options) < 4:
            option = random.choice(words)
            if option not in self.time_challenge_options:
                self.time_challenge_options.append(option)
        
        random.shuffle(self.time_challenge_options)
    
    def draw_spell_game(self):
        """绘制组词游戏"""
        theme_data = THEMES[self.theme]
        self.screen.fill(theme_data["bg"])
        
        # 标题
        title = self.font_medium.render(self.get_ui_text("mode_spell"), True, theme_data["text_color"])
        self.screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 30))
        
        # 提示：组成词语
        hint_text = "点击汉字组成词语" if self.language == "中文" else "Click to form a word"
        hint = self.font_small.render(hint_text, True, theme_data["text_color"])
        self.screen.blit(hint, (WINDOW_WIDTH // 2 - hint.get_width() // 2, 80))
        
        # 显示意思提示
        meaning_text = f"提示：{self.spell_target['meaning']}"
        meaning = self.font_medium.render(meaning_text, True, (100, 100, 150))
        self.screen.blit(meaning, (WINDOW_WIDTH // 2 - meaning.get_width() // 2, 130))
        
        # 显示已选择的字（答案区域）
        answer_y = 200
        answer_text = "".join(self.spell_selected) if self.spell_selected else "？？"
        
        # 答案框
        answer_box_width = 300
        answer_box_x = (WINDOW_WIDTH - answer_box_width) // 2
        pygame.draw.rect(self.screen, WHITE, (answer_box_x, answer_y, answer_box_width, 100), border_radius=15)
        pygame.draw.rect(self.screen, theme_data["text_color"], (answer_box_x, answer_y, answer_box_width, 100), 4, border_radius=15)
        
        answer = self.font_large.render(answer_text, True, theme_data["text_color"])
        self.screen.blit(answer, (WINDOW_WIDTH // 2 - answer.get_width() // 2, answer_y + 30))
        
        # 显示可选择的字
        chars_y = 350
        
        # 绘制字卡片（一行显示）
        total_width = len(self.spell_options) * 120
        start_x = (WINDOW_WIDTH - total_width) // 2
        
        for i, char in enumerate(self.spell_options):
            x = start_x + i * 120
            
            # 检查是否已被选择
            is_selected = char in self.spell_selected
            
            if is_selected:
                # 已选择的字 - 灰色
                pygame.draw.rect(self.screen, (220, 220, 220), (x, chars_y, 100, 100), border_radius=10)
                pygame.draw.rect(self.screen, (150, 150, 150), (x, chars_y, 100, 100), 3, border_radius=10)
                char_color = (150, 150, 150)
            else:
                # 未选择的字 - 白色
                pygame.draw.rect(self.screen, WHITE, (x, chars_y, 100, 100), border_radius=10)
                pygame.draw.rect(self.screen, theme_data["text_color"], (x, chars_y, 100, 100), 3, border_radius=10)
                char_color = theme_data["text_color"]
            
            char_text = self.font_large.render(char, True, char_color)
            self.screen.blit(char_text, (x + 50 - char_text.get_width() // 2, chars_y + 50 - char_text.get_height() // 2))
        
        # 检查答案按钮
        check_btn_y = 500
        pygame.draw.rect(self.screen, (100, 200, 100), (250, check_btn_y, 180, 60), border_radius=10)
        check_text = self.font_medium.render("检查答案" if self.language == "中文" else "Check", True, WHITE)
        self.screen.blit(check_text, (340 - check_text.get_width() // 2, check_btn_y + 15))
        
        # 清空按钮
        pygame.draw.rect(self.screen, (255, 150, 100), (470, check_btn_y, 180, 60), border_radius=10)
        clear_text = self.font_medium.render("清空重选" if self.language == "中文" else "Clear", True, WHITE)
        self.screen.blit(clear_text, (560 - clear_text.get_width() // 2, check_btn_y + 15))
        
        # 返回按钮
        pygame.draw.rect(self.screen, theme_data["text_color"], (60, 600, 150, 60), border_radius=10)
        back = self.font_small.render(self.get_ui_text("back"), True, WHITE)
        self.screen.blit(back, (135 - back.get_width() // 2, 615))
    
    def draw_match_game(self):
        """绘制连连看游戏"""
        theme_data = THEMES[self.theme]
        self.screen.fill(theme_data["bg"])
        
        # 标题
        title = self.font_medium.render(self.get_ui_text("mode_match"), True, theme_data["text_color"])
        self.screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 15))
        
        # 分数
        score_text = f"{'分数' if self.language == '中文' else 'Score'}: {self.match_score}"
        score = self.font_small.render(score_text, True, theme_data["text_color"])
        self.screen.blit(score, (WINDOW_WIDTH // 2 - score.get_width() // 2, 55))
        
        # 提示
        hint_text = "找出汉字和意思的配对" if self.language == "中文" else "Match words with meanings"
        hint = self.font_tiny.render(hint_text, True, theme_data["text_color"])
        self.screen.blit(hint, (WINDOW_WIDTH // 2 - hint.get_width() // 2, 85))
        
        # 绘制卡片（4行4列）
        for i, card in enumerate(self.match_cards):
            x = 80 + (i % 4) * 200
            y = 120 + (i // 4) * 130
            
            is_selected = i in self.match_selected
            is_matched = i in self.match_matched
            
            if is_matched:
                # 已配对的卡片 - 淡绿色背景，表示成功
                pygame.draw.rect(self.screen, (200, 255, 200), (x, y, 180, 110), border_radius=10)
                pygame.draw.rect(self.screen, (100, 200, 100), (x, y, 180, 110), 3, border_radius=10)
                # 文字颜色改为深绿色
                text_color = (0, 150, 0)
            elif is_selected:
                # 选中的卡片 - 黄色高亮
                pygame.draw.rect(self.screen, (255, 255, 150), (x, y, 180, 110), border_radius=10)
                pygame.draw.rect(self.screen, (255, 200, 0), (x, y, 180, 110), 4, border_radius=10)
                text_color = theme_data["text_color"]
            else:
                # 未选中的卡片 - 白色
                pygame.draw.rect(self.screen, WHITE, (x, y, 180, 110), border_radius=10)
                pygame.draw.rect(self.screen, theme_data["text_color"], (x, y, 180, 110), 3, border_radius=10)
                text_color = theme_data["text_color"]
            
            # 显示内容
            if card["type"] == "word":
                text = self.font_large.render(card["word"]["word"], True, text_color)
            else:
                text = self.font_small.render(card["word"]["meaning"], True, text_color)
            
            self.screen.blit(text, (x + 90 - text.get_width() // 2, y + 55 - text.get_height() // 2))
        
        # 游戏完成
        if len(self.match_matched) == 16:
            congrats_text = "完成！" if self.language == "中文" else "Complete!"
            congrats = self.font_large.render(congrats_text, True, theme_data["text_color"])
            self.screen.blit(congrats, (WINDOW_WIDTH // 2 - congrats.get_width() // 2, 600))
        
        # 返回按钮
        pygame.draw.rect(self.screen, theme_data["text_color"], (60, 600, 150, 60), border_radius=10)
        back = self.font_small.render(self.get_ui_text("back"), True, WHITE)
        self.screen.blit(back, (135 - back.get_width() // 2, 615))
    
    def draw_chain_game(self):
        """绘制听音选字游戏"""
        theme_data = THEMES[self.theme]
        self.screen.fill(theme_data["bg"])
        
        # 自动播放语音（只播放一次）
        if not self.chain_audio_played:
            self.speak_word(self.chain_current_word["word"], rate=160, wait=False)
            self.chain_audio_played = True
        
        # 检查效果是否过期
        current_time = pygame.time.get_ticks()
        if self.chain_effect_time > 0 and current_time - self.chain_effect_time > 800:
            # 效果显示0.8秒后消失
            if self.chain_correct_index >= 0:
                # 正确效果过期后进入下一题
                self.chain_correct_index = -1
                self.chain_effect_time = 0
                self.chain_current_index += 1
                
                # 检查是否完成所有题目
                if self.chain_current_index >= len(self.chain_words):
                    if self.language == "中文":
                        self.show_message("恭喜完成！", f"你完成了所有{len(self.chain_words)}个字！得分：{self.chain_score}", (0, 200, 0))
                    else:
                        self.show_message("Congratulations!", f"You completed all {len(self.chain_words)} words! Score: {self.chain_score}", (0, 200, 0))
                    self.chain_current_index = 0
                    random.shuffle(self.chain_words)
                
                self.generate_chain_question()
            elif self.chain_wrong_index >= 0:
                # 错误效果过期
                self.chain_wrong_index = -1
                self.chain_effect_time = 0
        
        # 标题
        title = self.font_medium.render(self.get_ui_text("mode_chain"), True, theme_data["text_color"])
        self.screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 15))
        
        # 进度和分数
        progress_text = f"{'进度' if self.language == '中文' else 'Progress'}: {self.chain_current_index + 1}/{len(self.chain_words)}"
        progress = self.font_small.render(progress_text, True, theme_data["text_color"])
        self.screen.blit(progress, (100, 55))
        
        score_text = f"{'分数' if self.language == '中文' else 'Score'}: {self.chain_score}"
        score = self.font_small.render(score_text, True, theme_data["text_color"])
        self.screen.blit(score, (650, 55))
        
        # 提示信息
        if self.language == "中文":
            hint_text = "听语音，选择正确的字"
        else:
            hint_text = "Listen and select the correct word"
        
        hint = self.font_medium.render(hint_text, True, theme_data["text_color"])
        self.screen.blit(hint, (WINDOW_WIDTH // 2 - hint.get_width() // 2, 100))
        
        # 大喇叭图标（用文字表示）
        speaker = self.font_large.render("♪", True, theme_data["text_color"])
        self.screen.blit(speaker, (WINDOW_WIDTH // 2 - speaker.get_width() // 2, 150))
        
        # 重新播放按钮
        replay_btn_x = WINDOW_WIDTH // 2 - 100
        replay_btn_y = 220
        pygame.draw.rect(self.screen, (100, 150, 255), (replay_btn_x, replay_btn_y, 200, 50), border_radius=10)
        replay_text = "再听一次" if self.language == "中文" else "Play Again"
        replay = self.font_small.render(replay_text, True, WHITE)
        self.screen.blit(replay, (replay_btn_x + 100 - replay.get_width() // 2, replay_btn_y + 15))
        
        # 显示选项（4个）- 只显示汉字/单词，不显示拼音和意思
        for i, option in enumerate(self.chain_options):
            x = 120 + (i % 2) * 380
            y = 320 + (i // 2) * 150
            
            # 判断是否是错误或正确选项
            is_wrong = (i == self.chain_wrong_index)
            is_correct = (i == self.chain_correct_index)
            
            if is_correct:
                # 正确选项 - 绿色背景和边框
                pygame.draw.rect(self.screen, (200, 255, 200), (x, y, 340, 120), border_radius=10)
                pygame.draw.rect(self.screen, (0, 200, 0), (x, y, 340, 120), 5, border_radius=10)
                word = self.font_large.render(option["word"], True, (0, 150, 0))
            elif is_wrong:
                # 错误选项 - 红色背景和边框
                pygame.draw.rect(self.screen, (255, 200, 200), (x, y, 340, 120), border_radius=10)
                pygame.draw.rect(self.screen, (255, 0, 0), (x, y, 340, 120), 5, border_radius=10)
                word = self.font_large.render(option["word"], True, (255, 0, 0))
            else:
                # 正常选项
                pygame.draw.rect(self.screen, WHITE, (x, y, 340, 120), border_radius=10)
                pygame.draw.rect(self.screen, theme_data["text_color"], (x, y, 340, 120), 3, border_radius=10)
                word = self.font_large.render(option["word"], True, theme_data["text_color"])
            
            self.screen.blit(word, (x + 170 - word.get_width() // 2, y + 60 - word.get_height() // 2))
        
        # 返回按钮
        pygame.draw.rect(self.screen, theme_data["text_color"], (60, 600, 150, 60), border_radius=10)
        back = self.font_small.render(self.get_ui_text("back"), True, WHITE)
        self.screen.blit(back, (135 - back.get_width() // 2, 615))
        self.screen.blit(back, (135 - back.get_width() // 2, 615))
    
    def draw_time_challenge(self):
        """绘制计时挑战游戏"""
        theme_data = THEMES[self.theme]
        self.screen.fill(theme_data["bg"])
        
        # 计算剩余时间
        elapsed = (pygame.time.get_ticks() - self.time_challenge_start) / 1000
        remaining = max(0, self.time_challenge_duration - int(elapsed))
        
        # 标题
        title = self.font_medium.render(self.get_ui_text("mode_time"), True, theme_data["text_color"])
        self.screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 15))
        
        # 分数和时间
        score_text = f"{'分数' if self.language == '中文' else 'Score'}: {self.time_challenge_score}"
        score = self.font_small.render(score_text, True, theme_data["text_color"])
        self.screen.blit(score, (100, 60))
        
        time_text = f"{'时间' if self.language == '中文' else 'Time'}: {remaining}s"
        time_display = self.font_small.render(time_text, True, (255, 0, 0) if remaining < 10 else theme_data["text_color"])
        self.screen.blit(time_display, (650, 60))
        
        # 游戏结束
        if remaining == 0:
            result = self.font_large.render(f"{'游戏结束！得分' if self.language == '中文' else 'Game Over! Score'}: {self.time_challenge_score}", 
                                           True, theme_data["text_color"])
            self.screen.blit(result, (WINDOW_WIDTH // 2 - result.get_width() // 2, 250))
            
            pygame.draw.rect(self.screen, theme_data["text_color"], (325, 400, 250, 70), border_radius=10)
            again_text = "再玩一次" if self.language == "中文" else "Play Again"
            again = self.font_medium.render(again_text, True, WHITE)
            self.screen.blit(again, (450 - again.get_width() // 2, 420))
        else:
            # 显示问题
            if self.language == "中文":
                question_text = f"请选择拼音为 '{self.time_challenge_question['pinyin']}' 的字"
            else:
                question_text = f"Select word with pronunciation '{self.time_challenge_question['pinyin']}'"
            
            question = self.font_small.render(question_text, True, theme_data["text_color"])
            self.screen.blit(question, (WINDOW_WIDTH // 2 - question.get_width() // 2, 110))
            
            # 显示选项
            for i, option in enumerate(self.time_challenge_options):
                x = 120 + (i % 2) * 380
                y = 180 + (i // 2) * 150
                
                pygame.draw.rect(self.screen, WHITE, (x, y, 340, 120), border_radius=10)
                pygame.draw.rect(self.screen, theme_data["text_color"], (x, y, 340, 120), 3, border_radius=10)
                
                word = self.font_large.render(option["word"], True, theme_data["text_color"])
                self.screen.blit(word, (x + 170 - word.get_width() // 2, y + 40))
        
        # 返回按钮
        pygame.draw.rect(self.screen, theme_data["text_color"], (60, 600, 150, 60), border_radius=10)
        back = self.font_small.render(self.get_ui_text("back"), True, WHITE)
        self.screen.blit(back, (135 - back.get_width() // 2, 615))
    
    def generate_question(self):
        database = self.get_current_database()
        words = database[self.difficulty]
        
        self.current_question = random.choice(words)
        self.options = [self.current_question]
        
        while len(self.options) < 4:
            option = random.choice(words)
            if option not in self.options:
                self.options.append(option)
        
        random.shuffle(self.options)
    
    def show_word_detail(self, word_data):
        """显示单词详细信息弹窗"""
        theme_data = THEMES[self.theme]
        
        # 等待点击
        waiting = True
        while waiting:
            # 控制帧率
            self.clock.tick(FPS)
            
            # 重新绘制背景和弹窗
            self.screen.fill(theme_data["bg"])
            
            # 创建完全不透明的遮罩层
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.fill((40, 40, 50))  # 深灰色背景
            self.screen.blit(overlay, (0, 0))
            
            # 详情框
            box_width, box_height = 650, 450
            box_x = (WINDOW_WIDTH - box_width) // 2
            box_y = (WINDOW_HEIGHT - box_height) // 2
            
            pygame.draw.rect(self.screen, WHITE, (box_x, box_y, box_width, box_height), border_radius=20)
            pygame.draw.rect(self.screen, theme_data["text_color"], (box_x, box_y, box_width, box_height), 5, border_radius=20)
            
            # 大字显示
            try:
                # 使用统一字体路径
                font_path = "/Library/Fonts/Arial Unicode.ttf"
                if os.path.exists(font_path):
                    word_font = pygame.font.Font(font_path, 80)
                else:
                    word_font = self.font_large
            except:
                word_font = self.font_large
            
            word_text = word_font.render(word_data["word"], True, theme_data["text_color"])
            self.screen.blit(word_text, (WINDOW_WIDTH // 2 - word_text.get_width() // 2, box_y + 50))
            
            # 拼音
            pinyin_text = self.font_large.render(word_data["pinyin"], True, (100, 100, 150))
            self.screen.blit(pinyin_text, (WINDOW_WIDTH // 2 - pinyin_text.get_width() // 2, box_y + 160))
            
            # 意思
            meaning_text = self.font_medium.render(word_data["meaning"], True, (80, 80, 80))
            self.screen.blit(meaning_text, (WINDOW_WIDTH // 2 - meaning_text.get_width() // 2, box_y + 230))
            
            # 提示文字
            if self.language == "中文":
                hint_text = "点击下方按钮听发音和解释"
            else:
                hint_text = "Click buttons to hear pronunciation"
            hint = self.font_small.render(hint_text, True, (120, 120, 120))
            self.screen.blit(hint, (WINDOW_WIDTH // 2 - hint.get_width() // 2, box_y + 280))
            
            # 三个按钮：听发音、听解释、关闭
            btn_width, btn_height = 180, 55
            btn_y = box_y + box_height - 90
            
            # 听发音按钮
            btn1_x = box_x + 50
            pygame.draw.rect(self.screen, (100, 150, 255), (btn1_x, btn_y, btn_width, btn_height), border_radius=10)
            speak_text = self.font_small.render("听发音" if self.language == "中文" else "Speak", True, WHITE)
            self.screen.blit(speak_text, (btn1_x + btn_width // 2 - speak_text.get_width() // 2, btn_y + 18))
            
            # 听解释按钮
            btn2_x = box_x + 235
            pygame.draw.rect(self.screen, (255, 150, 100), (btn2_x, btn_y, btn_width, btn_height), border_radius=10)
            explain_text = self.font_small.render("听解释" if self.language == "中文" else "Explain", True, WHITE)
            self.screen.blit(explain_text, (btn2_x + btn_width // 2 - explain_text.get_width() // 2, btn_y + 18))
            
            # 关闭按钮
            btn3_x = box_x + 420
            pygame.draw.rect(self.screen, theme_data["text_color"], (btn3_x, btn_y, btn_width, btn_height), border_radius=10)
            close_text = self.font_small.render("关闭" if self.language == "中文" else "Close", True, WHITE)
            self.screen.blit(close_text, (btn3_x + btn_width // 2 - close_text.get_width() // 2, btn_y + 18))
            
            pygame.display.flip()
            
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    
                    # 听发音按钮
                    if btn1_x <= x <= btn1_x + btn_width and btn_y <= y <= btn_y + btn_height:
                        self.speak_word(word_data["word"], rate=160, wait=True)
                    
                    # 听解释按钮
                    elif btn2_x <= x <= btn2_x + btn_width and btn_y <= y <= btn_y + btn_height:
                        if self.language == "中文":
                            explanation = f"{word_data['word']}，读音是 {word_data['pinyin']}，意思是 {word_data['meaning']}"
                            self.speak_word(explanation, rate=180, wait=True, force_chinese=False)
                        else:
                            # 英文模式：用中文朗读解释
                            explanation = f"{word_data['word']}，读音是 {word_data['pinyin']}，意思是 {word_data['meaning']}"
                            self.speak_word(explanation, rate=180, wait=True, force_chinese=True)
                    
                    # 关闭按钮
                    elif btn3_x <= x <= btn3_x + btn_width and btn_y <= y <= btn_y + btn_height:
                        waiting = False
    
    def show_message(self, title, message, color):
        """显示消息弹窗"""
        theme_data = THEMES[self.theme]
        
        # 创建完全不透明的遮罩层
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill((40, 40, 50))  # 深灰色背景
        self.screen.blit(overlay, (0, 0))
        
        # 消息框
        box_width, box_height = 500, 300
        box_x = (WINDOW_WIDTH - box_width) // 2
        box_y = (WINDOW_HEIGHT - box_height) // 2
        
        pygame.draw.rect(self.screen, WHITE, (box_x, box_y, box_width, box_height), border_radius=20)
        pygame.draw.rect(self.screen, color, (box_x, box_y, box_width, box_height), 5, border_radius=20)
        
        # 标题
        title_text = self.font_large.render(title, True, color)
        self.screen.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, box_y + 60))
        
        # 消息
        message_text = self.font_medium.render(message, True, (80, 80, 80))
        self.screen.blit(message_text, (WINDOW_WIDTH // 2 - message_text.get_width() // 2, box_y + 140))
        
        # 确定按钮
        btn_width, btn_height = 200, 60
        btn_x = (WINDOW_WIDTH - btn_width) // 2
        btn_y = box_y + box_height - 90
        
        pygame.draw.rect(self.screen, color, (btn_x, btn_y, btn_width, btn_height), border_radius=10)
        ok_text = self.font_medium.render(self.get_ui_text("ok"), True, WHITE)
        self.screen.blit(ok_text, (WINDOW_WIDTH // 2 - ok_text.get_width() // 2, btn_y + 15))
        
        pygame.display.flip()
        
        # 等待点击
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if btn_x <= x <= btn_x + btn_width and btn_y <= y <= btn_y + btn_height:
                        waiting = False
    
    def run(self):
        running = True
        
        while running:
            self.clock.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    
                    if self.mode == "menu":
                        # 语言切换
                        if 60 <= x <= 310 and 90 <= y <= 135:
                            self.play_sound("click")
                            self.language = "English" if self.language == "中文" else "中文"
                            self.save_progress()
                        
                        # 难度切换
                        elif 330 <= x <= 580 and 90 <= y <= 135:
                            self.play_sound("click")
                            difficulties = ["简单", "中等", "困难"]
                            idx = difficulties.index(self.difficulty)
                            self.difficulty = difficulties[(idx + 1) % 3]
                            self.save_progress()
                        
                        # 主题切换
                        elif 600 <= x <= 840 and 90 <= y <= 135:
                            self.play_sound("click")
                            themes = list(THEMES.keys())
                            idx = themes.index(self.theme)
                            self.theme = themes[(idx + 1) % len(themes)]
                            self.save_progress()
                        
                        # 8个游戏模式按钮
                        else:
                            for i in range(8):
                                btn_x = 80 + (i % 2) * 380
                                btn_y = 220 + (i // 2) * 100
                                
                                if btn_x <= x <= btn_x + 340 and btn_y <= y <= btn_y + 70:
                                    self.play_sound("click")
                                    if i == 0:  # 学习模式
                                        self.mode = "learn"
                                    elif i == 1:  # 测验模式
                                        self.mode = "quiz"
                                        self.current_question = None
                                    elif i == 2:  # 拼字游戏
                                        self.mode = "spell"
                                        self.init_spell_game()
                                    elif i == 3:  # 连连看
                                        self.mode = "match"
                                        self.init_match_game()
                                    elif i == 4:  # 打地鼠
                                        self.mode = "whack"
                                        self.init_whack_game()
                                    elif i == 5:  # 记忆翻牌
                                        self.mode = "memory"
                                        self.init_memory_game()
                                    elif i == 6:  # 汉字接龙
                                        self.mode = "chain"
                                        self.init_chain_game()
                                    elif i == 7:  # 计时挑战
                                        self.mode = "time"
                                        self.init_time_challenge()
                                    else:  # 其他模式
                                        self.mode = f"coming_soon_{i}"
                                    break
                    
                    elif self.mode == "learn":
                        # 上一页按钮
                        if 60 <= x <= 180 and 600 <= y <= 660:
                            if self.learn_page > 0:
                                self.play_sound("click")
                                self.learn_page -= 1
                        
                        # 返回按钮
                        elif 390 <= x <= 510 and 600 <= y <= 660:
                            self.play_sound("click")
                            self.mode = "menu"
                            self.learn_page = 0
                        
                        # 下一页按钮
                        elif 720 <= x <= 840 and 600 <= y <= 660:
                            database = self.get_current_database()
                            words = database[self.difficulty]
                            total_pages = (len(words) + 7) // 8
                            if self.learn_page < total_pages - 1:
                                self.play_sound("click")
                                self.learn_page += 1
                        
                        # 点击单词卡片 - 朗读
                        else:
                            database = self.get_current_database()
                            words = database[self.difficulty]
                            words_per_page = 8
                            start_idx = self.learn_page * words_per_page
                            end_idx = min(start_idx + words_per_page, len(words))
                            page_words = words[start_idx:end_idx]
                            
                            for i, word_data in enumerate(page_words):
                                card_x = 50 + (i % 4) * 210
                                card_y = 100 + (i // 4) * 220
                                
                                if card_x <= x <= card_x + 190 and card_y <= y <= card_y + 180:
                                    self.play_sound("click")
                                    # 记录点击效果
                                    self.clicked_card = i
                                    self.click_time = pygame.time.get_ticks()
                                    # 显示详细信息弹窗
                                    self.show_word_detail(word_data)
                                    break
                    
                    elif self.mode == "quiz":
                        # 返回按钮
                        if 60 <= x <= 210 and 600 <= y <= 660:
                            self.play_sound("click")
                            self.mode = "menu"
                            self.current_question = None
                        
                        # 检查选项点击
                        else:
                            for i in range(4):
                                opt_x = 120 + (i % 2) * 380
                                opt_y = 170 + (i // 2) * 150
                                
                                if opt_x <= x <= opt_x + 340 and opt_y <= y <= opt_y + 120:
                                    if self.options[i]["word"] == self.current_question["word"]:
                                        self.play_sound("correct")
                                        # 先朗读正确答案（等待播放完成）
                                        self.speak_word(self.current_question["word"], rate=180, wait=True)
                                        # 播放鼓励语音（更快更活泼）
                                        if self.language == "中文":
                                            encouragements = [
                                                "太棒了！你真聪明！",
                                                "答对啦！继续加油！",
                                                "真厉害！你是最棒的！",
                                                "好棒啊！再接再厉！"
                                            ]
                                            import random
                                            self.speak_word(random.choice(encouragements), rate=220, wait=False)
                                        else:
                                            encouragements = [
                                                "Great job! You're so smart!",
                                                "Correct! Keep it up!",
                                                "Awesome! You're the best!",
                                                "Well done! Keep going!"
                                            ]
                                            import random
                                            self.speak_word(random.choice(encouragements), rate=220, wait=False)
                                        self.show_message(self.get_ui_text("correct"), self.get_ui_text("great"), (0, 200, 0))
                                    else:
                                        self.play_sound("wrong")
                                        # 播放错误提示语音（等待播放完成）
                                        if self.language == "中文":
                                            wrong_phrases = [
                                                "哎呀，答错了！再想想吧！",
                                                "不对哦，再试一次！",
                                                "差一点点，加油！"
                                            ]
                                            import random
                                            self.speak_word(random.choice(wrong_phrases), rate=200, wait=True)
                                        else:
                                            wrong_phrases = [
                                                "Oops! Try again!",
                                                "Not quite! Think again!",
                                                "Almost! Keep trying!"
                                            ]
                                            import random
                                            self.speak_word(random.choice(wrong_phrases), rate=200, wait=True)
                                        # 说正确答案
                                        if self.language == "中文":
                                            self.speak_word(f"正确答案是 {self.current_question['word']}", rate=180, wait=False)
                                        else:
                                            self.speak_word(f"The correct answer is {self.current_question['word']}", rate=180, wait=False)
                                        wrong_msg = f"{self.get_ui_text('correct_answer')}: {self.current_question['word']}"
                                        self.show_message(self.get_ui_text("wrong"), wrong_msg, (200, 0, 0))
                                    self.current_question = None
                                    break
                    
                    elif self.mode.startswith("coming_soon"):
                        # 返回按钮
                        if 325 <= x <= 575 and 450 <= y <= 520:
                            self.mode = "menu"
                    
                    elif self.mode == "whack":
                        # 返回按钮
                        if 60 <= x <= 210 and 600 <= y <= 660:
                            self.mode = "menu"
                        
                        # 再玩一次按钮
                        elif 325 <= x <= 575 and 400 <= y <= 470:
                            elapsed = (pygame.time.get_ticks() - self.whack_start_time) / 1000
                            if elapsed >= self.whack_time:
                                self.init_whack_game()
                        
                        # 点击地鼠
                        else:
                            elapsed = (pygame.time.get_ticks() - self.whack_start_time) / 1000
                            if elapsed < self.whack_time:
                                for mole in self.whack_moles:
                                    if mole["visible"]:
                                        if mole["x"] + 20 <= x <= mole["x"] + 220 and mole["y"] + 20 <= y <= mole["y"] + 100:
                                            if mole["word"]["word"] == self.whack_target_word["word"]:
                                                self.whack_score += 10
                                                mole["visible"] = False
                                            else:
                                                self.whack_score = max(0, self.whack_score - 5)
                                            break
                    
                    elif self.mode == "memory":
                        # 返回按钮
                        if 60 <= x <= 210 and 600 <= y <= 660:
                            self.mode = "menu"
                        
                        # 点击卡片
                        elif not self.memory_lock:
                            for i, card in enumerate(self.memory_cards):
                                card_x = 120 + (i % 4) * 180
                                card_y = 100 + (i // 4) * 160
                                
                                if card_x <= x <= card_x + 160 and card_y <= y <= card_y + 140:
                                    if i not in self.memory_flipped and i not in self.memory_matched:
                                        self.memory_flipped.append(i)
                                        
                                        if self.memory_first_card is None:
                                            self.memory_first_card = i
                                        elif self.memory_second_card is None:
                                            self.memory_second_card = i
                                            
                                            # 检查是否配对
                                            if self.memory_cards[self.memory_first_card]["pair_id"] == self.memory_cards[self.memory_second_card]["pair_id"]:
                                                self.memory_matched.append(self.memory_first_card)
                                                self.memory_matched.append(self.memory_second_card)
                                                self.memory_first_card = None
                                                self.memory_second_card = None
                                            else:
                                                self.memory_lock = True
                                                self.memory_lock_time = pygame.time.get_ticks()
                                    break
                    
                    elif self.mode == "spell":
                        # 返回按钮
                        if 60 <= x <= 210 and 600 <= y <= 660:
                            self.mode = "menu"
                        
                        # 检查答案按钮
                        elif 250 <= x <= 430 and 500 <= y <= 560:
                            if len(self.spell_selected) > 0:
                                answer = "".join(self.spell_selected)
                                if answer == self.spell_target["word"]:
                                    # 答对了
                                    self.play_sound("correct")
                                    self.spell_score += 10
                                    if self.language == "中文":
                                        self.speak_word(f"太棒了！{self.spell_target['word']}，{self.spell_target['meaning']}", rate=200, wait=False)
                                        self.show_message("正确！", f"'{self.spell_target['word']}'组词正确！", (0, 200, 0))
                                    else:
                                        self.speak_word(f"Great! {self.spell_target['word']}", rate=200, wait=False)
                                        self.show_message("Correct!", f"'{self.spell_target['word']}' is correct!", (0, 200, 0))
                                    self.init_spell_game()
                                else:
                                    # 答错了
                                    self.play_sound("wrong")
                                    if self.language == "中文":
                                        self.show_message("再试试", f"正确答案是：{self.spell_target['word']}", (200, 100, 0))
                                    else:
                                        self.show_message("Try again", f"Correct answer: {self.spell_target['word']}", (200, 100, 0))
                        
                        # 清空按钮
                        elif 470 <= x <= 650 and 500 <= y <= 560:
                            self.spell_selected = []
                        
                        # 点击字卡片
                        else:
                            total_width = len(self.spell_options) * 120
                            start_x = (WINDOW_WIDTH - total_width) // 2
                            chars_y = 350
                            
                            for i, char in enumerate(self.spell_options):
                                char_x = start_x + i * 120
                                
                                if char_x <= x <= char_x + 100 and chars_y <= y <= chars_y + 100:
                                    if char not in self.spell_selected:
                                        self.spell_selected.append(char)
                                        self.play_sound("click")
                                    break
                    
                    elif self.mode == "match":
                        # 返回按钮
                        if 60 <= x <= 210 and 600 <= y <= 660:
                            self.mode = "menu"
                        
                        # 点击卡片
                        else:
                            for i, card in enumerate(self.match_cards):
                                card_x = 80 + (i % 4) * 200
                                card_y = 120 + (i // 4) * 130
                                
                                if card_x <= x <= card_x + 180 and card_y <= y <= card_y + 110:
                                    if i not in self.match_selected and i not in self.match_matched:
                                        self.match_selected.append(i)
                                        
                                        if len(self.match_selected) == 2:
                                            # 检查是否配对
                                            idx1, idx2 = self.match_selected
                                            if self.match_cards[idx1]["pair_id"] == self.match_cards[idx2]["pair_id"]:
                                                self.match_matched.append(idx1)
                                                self.match_matched.append(idx2)
                                                self.match_score += 10
                                                self.play_sound("correct")
                                                self.match_selected = []
                                            else:
                                                self.play_sound("wrong")
                                                # 记录时间戳，在主循环中非阻塞延迟清除
                                                self.match_flip_time = pygame.time.get_ticks()
                                    break
                    
                    elif self.mode == "chain":
                        # 返回按钮
                        if 60 <= x <= 210 and 600 <= y <= 660:
                            self.mode = "menu"
                        
                        # 重新播放按钮
                        elif WINDOW_WIDTH // 2 - 100 <= x <= WINDOW_WIDTH // 2 + 100 and 220 <= y <= 270:
                            self.speak_word(self.chain_current_word["word"], rate=160, wait=False)
                        
                        # 检查选项点击
                        else:
                            for i in range(len(self.chain_options)):
                                opt_x = 120 + (i % 2) * 380
                                opt_y = 320 + (i // 2) * 150
                                
                                if opt_x <= x <= opt_x + 340 and opt_y <= y <= opt_y + 120:
                                    # 检查答案是否正确
                                    if self.chain_options[i]["word"] == self.chain_current_word["word"]:
                                        # 答对了，显示绿色效果
                                        self.chain_score += 10
                                        self.play_sound("correct")
                                        
                                        # 记录正确选项索引和时间
                                        self.chain_correct_index = i
                                        self.chain_effect_time = pygame.time.get_ticks()
                                        
                                        # 注意：不在这里进入下一题，而是在绘制函数中检测效果过期后自动进入
                                    else:
                                        # 答错了，显示红色效果
                                        self.play_sound("wrong")
                                        
                                        # 记录错误选项索引和时间
                                        self.chain_wrong_index = i
                                        self.chain_effect_time = pygame.time.get_ticks()
                                        
                                        # 播放正确答案的语音
                                        self.speak_word(self.chain_current_word["word"], rate=160, wait=False)
                                    break
                    
                    elif self.mode == "time":
                        # 返回按钮
                        if 60 <= x <= 210 and 600 <= y <= 660:
                            self.mode = "menu"
                        
                        # 再玩一次按钮
                        elif 325 <= x <= 575 and 400 <= y <= 470:
                            elapsed = (pygame.time.get_ticks() - self.time_challenge_start) / 1000
                            if elapsed >= self.time_challenge_duration:
                                self.init_time_challenge()
                        
                        # 检查选项点击
                        else:
                            elapsed = (pygame.time.get_ticks() - self.time_challenge_start) / 1000
                            if elapsed < self.time_challenge_duration:
                                for i in range(4):
                                    opt_x = 120 + (i % 2) * 380
                                    opt_y = 180 + (i // 2) * 150
                                    
                                    if opt_x <= x <= opt_x + 340 and opt_y <= y <= opt_y + 120:
                                        if self.time_challenge_options[i]["word"] == self.time_challenge_question["word"]:
                                            self.time_challenge_score += 10
                                            self.play_sound("correct")
                                        else:
                                            self.time_challenge_score = max(0, self.time_challenge_score - 5)
                                            self.play_sound("wrong")
                                        self.generate_time_question()
                                        break
            
            # 非阻塞：连连看答错后延迟500ms清除选中
            if self.match_flip_time and pygame.time.get_ticks() - self.match_flip_time >= 500:
                self.match_selected = []
                self.match_flip_time = 0

            # 绘制（字典分发，便于扩展）
            draw_funcs = {
                "menu":   self.draw_menu,
                "learn":  self.draw_learn_mode,
                "quiz":   self.draw_quiz_mode,
                "whack":  self.draw_whack_game,
                "memory": self.draw_memory_game,
                "spell":  self.draw_spell_game,
                "match":  self.draw_match_game,
                "chain":  self.draw_chain_game,
                "time":   self.draw_time_challenge,
            }
            if self.mode in draw_funcs:
                draw_funcs[self.mode]()
            elif self.mode.startswith("coming_soon"):
                try:
                    mode_idx = int(self.mode.split("_")[-1])
                    mode_names = ["mode_learn", "mode_quiz", "mode_spell", "mode_match",
                                 "mode_whack", "mode_memory", "mode_chain", "mode_time"]
                    self.draw_coming_soon(mode_names[mode_idx])
                except (IndexError, ValueError) as e:
                    logging.warning("coming_soon 模式索引错误: %s", e)
                    self.mode = "menu"
            
            pygame.display.flip()
        
        self.save_progress()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = WordGame()
    game.run()
