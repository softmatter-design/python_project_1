import streamlit as st
import sys

if st.button(label='click me!'):
    st.write('Thank you')

# ダウンロードするデータ
text_data = "これはサンプルのテキストデータです。\t aaa \n aaa\tbbb\n"

# ダウンロードボタンを作成
st.download_button(
label="ダウンロード",
data=text_data,
file_name="sample.txt",
mime="text/plain"
)

if st.button("アプリを終了"):
    st.write("終了します...")
    sys.exit(0)  # プロセスを終了