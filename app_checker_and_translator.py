import streamlit as st
from deep_translator import GoogleTranslator
from langdetect import detect, LangDetectException
from nltk.tokenize import wordpunct_tokenize
from spellchecker import SpellChecker
from nltk.tokenize.treebank import TreebankWordDetokenizer
import langcodes

MIN_INPUT_LENGTH = 3

SPELL_LANGS = {
    "en", "es", "fr", "pt", "de",
    "ru", "ar", "eu", "lv", "nl"
}

TARGET_LANGS = {
    "Tiếng Việt": "vi",
    "Tiếng Anh": "en",
    "Tiếng Pháp": "fr",
    "Tiếng Nhật": "ja",
    "Tiếng Trung (Giản thể)": "zh-CN",
    "Tiếng Hàn": "ko",
    "Tiếng Đức": "de"
}

@st.cache_resource(show_spinner = False)

def get_spellchecker(code):
    return SpellChecker(language = code)

def detect_language(raw):
    try:
        return detect(raw)
    except LangDetectException:
        return None
    
def language_name(code):
    return langcodes.Language.get(code).display_name()

def fix_typos(text, code):
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

def run_spellcheck(text):
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

def run_translation(text, target_code):
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
            
 

   
    