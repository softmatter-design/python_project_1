import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pyrespect_time import ReSpect, ReSpectConfig
import os

def main():
    st.title('試験')
    df = upload_file()

    download()
    return

def upload_file():
    selected_file = st.file_uploader("データファイルをアップロードしてください", type=["txt", "dat", "csv", "xls", "xlsx"])

    if selected_file is not None:
        file_type = selected_file.name.split(".")[-1].lower()
        try:
            if file_type == "csv":
                df = pd.read_csv(selected_file, header=None)
            elif file_type in ["dat", "txt"]:
                df = pd.read_table(selected_file, header=None, encoding="utf-8", sep="\t")
            elif file_type in ["xlsx", "xls"]:
                df = pd.read_excel(selected_file)  
            else:
                st.error("対応していないファイル形式です。")
                st.stop()
        except Exception as e:
            st.error(f"ファイルの読み込みに失敗しました: {e}")
            st.stop()

        if not df.empty:
            df = convert_to_number(df)
            #
            st.success("データプレビュー（数値データ以外を消去済み）")
            st.write(f'データ数: {len(df)}行')
            st.dataframe(df)
        mod_df = modify_df(df)
            
        return mod_df

def convert_to_number(df):
    for col in df:
        # 文字列化
        series_str = df[col].astype(str)
        # 数字・小数点・マイナス以外を削除
        series_str = series_str.str.replace(r"[^0-9.-]", "", regex=True)
        # 空文字は NaN に
        series_str = series_str.replace("", None)
        # 数値変換（失敗時は NaN）
        df[col] = pd.to_numeric(series_str, errors="coerce")
    return df

def modify_df(df):
    selected_df = select_col(df)
    return selected_df

def select_col(df):
    # 列選択（複数選択可）
    selected_columns = st.multiselect(
        "時間列とG(t)を選択してください",
        options=df.columns.tolist(),
        max_selections=2
        )
    
    if len(selected_columns)==2:
        tmp_df = df[selected_columns]
        tmp_df.columns = ['Time', 'G(t)']

        base = st.number_input('測定開始時間の行を入力してください', min_value=0, max_value=100, step=1)
        init_time = tmp_df.iloc[base,0]
        init_g = tmp_df.iloc[base,1]
        st.success(f'初期値は{base}行目：時間は{init_time}で初期弾性率は{init_g}')
        selected_df = show_mod_df(tmp_df, base, init_time, init_g)
        return 
            
    # else:
    #     st.warning("少なくとも1列は選択してください。")
    

def show_mod_df(tmp_df, base, init_time, init_g):
    selected_df = tmp_df.loc[base:]
    selected_df['Mod. Time']=selected_df['Time']-init_time
    selected_df['Norm. G(t)']=selected_df['G(t)']/init_g
    st.subheader(f"選択した列のデータを{base}行目から表示")
    st.dataframe(selected_df)  

    if st.button("これで良ければクリック"):
        time = selected_df['Mod. Time'][1:].to_numpy()
        gt = selected_df['G(t)'][1:].to_numpy()
        ngt = selected_df['Norm. G(t)'][1:].to_numpy()

        plt.plot(time, gt)
        plt.xscale('log')
        plt.yscale('log')
        st.pyplot(plt)

        # Default settings — fit from a data file
        solver = ReSpect()
        solver.fit(time, gt)  # "Gt.dat" file contains data

        # Access results
        print(solver.continuous.H)    # continuous spectrum H(s)
        print(solver.discrete.tau)    # discrete relaxation times
        print(solver.discrete.g)      # discrete mode weights

        solver.save(which="full", path="output/")
        solver.plot(which="full", toFile=True, path="output/")
    return selected_df

def download():
    dir_path = './output'
    files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]

    filename = st.selectbox('ダウンロードする画像を選択', files)
    print(filename)

    with open(os.path.join(dir_path, filename), "rb") as file:
        st.download_button(
            label='ダウンロード',
            data=file,
            file_name=filename
        )

# ===== 使用例 =====
if __name__ == "__main__":
    main()