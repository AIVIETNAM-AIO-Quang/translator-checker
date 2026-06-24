import streamlit as st
from deep_translator import GoogleTranslator
from langdetect import detect, LangDetectException 
from nltk.tokenize import wordpunct_tokenize
from spellchecker import SpellChecker
from nltk.tokenize.treebank import TreebankWordDetokenizer #nhớ import thêm cái này vì slide không có
import langcodes #nhớ import thêm cái này vì slide không có

MIN_INPUT_LENGTH = 3 #độ dài tối thiểu cho một câu. một câu cũng cần có chủ ngữ vị ngữ nên không thể quá ngắn nếu không tính câu đặc biệt. 

#em chưa hiểu vì sao lại dùng cái dict này:))
SPELL_LANGS = {
    "en", "es", "fr", "pt", "de",
    "ru", "ar", "eu", "lv", "nl"
}

#dict chứa ngôn ngữ cùng code của chúng để app có thể nhanh chóng nhận diện và biết được cần dịch sang ngôn ngữ nào
TARGET_LANGS = {
    "Tiếng Việt": "vi",
    "Tiếng Anh": "en",
    "Tiếng Pháp": "fr",
    "Tiếng Nhật": "ja",
    "Tiếng Trung (Giản thể)": "zh-CN",
    "Tiếng Hàn": "ko",
    "Tiếng Đức": "de"
}

@st.cache_resource(show_spinner = False) #khởi tạo tài nguyên một lần duy nhất giúp cho app không cần phải khởi tạo sau mỗi lần rerun mà có thể dùng ngay lập tức. show spinner = false có nghĩa là cái vòng xoay khi đang load dữ liệu sẽ bị ẩn đi

def get_spellchecker(code):
    return SpellChecker(language = code) #chuẩn bị chương trình get_spellchecker 

def detect_language(raw): #hàm detect language dùng để phát hiện ngôn ngữ dùng cho việc kiểm tra ngôn ngữ cho việc dịch và sửa lỗi
    try:
        return detect(raw) 
    except LangDetectException:
        return None
    
def language_name(code): 
    return langcodes.Language.get(code).display_name() #lấy và in ra tên ngôn ngữ

def fix_typos(text, code): #hàm fix typo có tác dụng tokenize và detokenize câu
    spell = get_spellchecker(code)
    tokens = wordpunct_tokenize(text)
    fixed = []

    for token in tokens:
        if token.isalpha() and len(token) > 1:
            suggestion = spell.correction(token.lower()) or token
            suggestion = suggestion.title() if token.istitle() else suggestion
            suggestion = suggestion.upper() if token.isupper() else suggestion
            fixed.append(suggestion)
        else:
            fixed.append(token)
    return TreebankWordDetokenizer().detokenize(fixed), fixed != tokens

def run_spellcheck(text): #hàm run spellcheck giúp sửa lỗi chính tả
    raw = text.strip()
    if len(raw) < MIN_INPUT_LENGTH:
        return {"ok": False, "error": f"Nhập tối thiểu {MIN_INPUT_LENGTH} ký tự."}
    code = detect_language(raw)
    if code is None: 
        return {"ok": False, "error": "Không nhận diện được ngôn ngữ."}
    if code not in SPELL_LANGS:
        return {"ok": False, "error": f"pyspell chưa hỗ trợ {language_name(code)}"}
    fixed, changed = fix_typos(raw, code)
    return {"ok": True, "language": language_name(code), "fixed": fixed, "changed": changed}

def run_translation(text, target_code): #hàm dịch ngôn ngữ
    raw = text.strip()
    if len(raw) < MIN_INPUT_LENGTH:
        return {"ok": False, "error": f"Nhập tối thiểu {MIN_INPUT_LENGTH} ký tự."}
    source = detect_language(raw)
    if source is None:
        return {"ok": False, "error": "Không nhận diện được ngôn ngữ."}
    if source == target_code:
        return {"ok": True, "source": language_name(source), "target": language_name(target_code), "translated": raw, "note": "Câu ở trên không cần dịch vì đã ở ngôn ngữ đích."}
    
    try:
        translated = GoogleTranslator(source = source, target = target_code).translate(raw)
    except Exception as e:
        return {"ok": False, "error": f"Lỗi dịch: {e}"}
    return {"ok": True, "source": language_name(source), "target": language_name(target_code), "translated": translated}

#sử dụng các widget input để thể hiện UI, chạy hàm và lấy dữ liệu từ người dùng
st.set_page_config(page_title="App Translator and Checker", layout="centered")
st.title("App Translator and Checker")
st.caption("Hai ứng dụng: Dịch văn bản · Sửa lỗi chính tả")
tab_t, tab_s = st.tabs(["Dịch văn bản", "Sửa lỗi chính tả"])

with tab_t:

    text = st.text_area("Nhập đoạn văn cần dịch")

    target = st.selectbox(
        "Ngôn ngữ muốn dịch",
        list(TARGET_LANGS.keys())
        )
    
    target_code = TARGET_LANGS[target]
    
    if st.button("Chạy chương trình dịch văn bản"):
         result = run_translation(text, target_code)
         if result["ok"] == True: 
             st.write(result["translated"])
         else:
             st.write(result["error"])

with tab_s:

    text = st.text_area("Nhập đoạn văn cần chỉnh sửa")

    if st.button("Chạy chương trình chỉnh sửa văn bản"):
         result = run_spellcheck(text)
         if result["ok"] == True: 
             st.write(result["fixed"])
         else:
             st.write(result["error"])
            
 

   
    