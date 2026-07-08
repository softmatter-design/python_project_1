import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pyrespect_time import ReSpect, ReSpectConfig
###
def main():
    st.set_page_config(
        page_title="シンプルアプリ",
        layout="wide"
            )
    st.title('ReSpectでデータ処理')


    if 'download_files' not in st.session_state:
        st.write('データはまだ選択されていません')
    else:
        st.dataframe(st.session_state.cut_df)
        if st.button('データ処理しますか？'):
            st.success('処理中です')
            run_respect(st.session_state.cut_df)
    return

def run_respect(df):
    st.dataframe(df) 
    time = df['Mod. Time'][1:].to_numpy()
    gt = df['G(t)'][1:].to_numpy()

    # Default settings — fit from a data file
    solver = ReSpect()
    solver.fit(time, gt)  # "Gt.dat" file contains data

    # Access results
    print(solver.continuous.H)    # continuous spectrum H(s)
    print(solver.discrete.tau)    # discrete relaxation times
    print(solver.discrete.g)      # discrete mode weights

    solver.save(which="full", path="output/")
    solver.plot(which="full", toFile=True, path="output/")
    return

###
if __name__ == "__main__":
	main()