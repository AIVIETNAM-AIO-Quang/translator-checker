# Translator and Spell Checker

Đây là ứng dụng Streamlit cơ bản đầu tiên trong quá trình học AIO. Ứng dụng cung cấp hai chức năng xử lí ngôn ngữ tự nhiên cơ bản: dịch văn bản và kiểm tra lỗi chính tả.

## Chức năng chính

- Tự động nhận diện ngôn ngữ đầu vào.
- Dịch văn bản sang ngôn ngữ được chọn.
- Kiểm tra và sửa lỗi chính tả đối với các ngôn ngữ được hỗ trợ.
- Cung cấp giao diện web đơn giản bằng Streamlit.

## Ngôn ngữ và thư viện được sử dụng

- Python
- Streamlit
- deep-translator
- langdetect
- nltk
- pyspellchecker
- langcodes

## Cấu trúc project

```text
translator-checker/
│
├── app_checker_and_translator.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Cách chạy trên máy cá nhân

Clone repository:

```bash
git clone https://github.com/AIVIETNAM-AIO-Quang/translator-checker.git
cd translator-checker
```

Cài đặt thư viện cần thiết:

```bash
pip install -r requirements.txt
```

Chạy ứng dụng Streamlit:

```bash
streamlit run app_checker_and_translator.py
```

## Deploy

Ứng dụng có thể được deploy bằng Streamlit Community Cloud.

Thiết lập deploy:

```text
Repository: AIVIETNAM-AIO-Quang/translator-checker
Branch: main
Main file path: app_checker_and_translator.py
```

## Ghi chú

Project này được xây dựng với mục tiêu luyện tập các thao tác NLP cơ bản như nhận diện ngôn ngữ, dịch văn bản và sửa lỗi chính tả. Đây là một ứng dụng đơn giản, phù hợp cho người mới bắt đầu làm quen với Streamlit và xử lý ngôn ngữ tự nhiên.
