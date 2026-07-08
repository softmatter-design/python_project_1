import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
###
def main():
	st.set_page_config(
		page_title="シンプルアプリ",
		layout="wide"
			)
	st.title('データ選択')

	if 'load_df' not in st.session_state:
		st.write('データはまだ選択されていません')
	elif len(st.session_state.sel_df.columns) < 2:
		st.write('カラム名の自動選択ができていません')
		st.dataframe(st.session_state.load_df)
		modify_df(st.session_state.load_df)
	else:
		st.success("カラム名の自動選択がうまくいきました")
		st.success("このページでやることはないので、次のページへ")
		st.dataframe(st.session_state.sel_df)
	
	return

def modify_df(df):
	# 列選択
	selected_columns = []
	for col in ['時間', '弾性率']:
		selected_columns.append(
			st.selectbox(
			col+"に対応する列を選択してください",
			options=df.columns.tolist(),
				)
		)
	
	if len(selected_columns)==2 and selected_columns != ['col_0', 'col_0']:
	# 	print(selected_columns)
		tmp_df = df[selected_columns]
		tmp_df.columns = ['Time', 'G(t)']
		st.write('今選択されているカラムです')
		st.dataframe(tmp_df)
		#
		if st.button("これで良ければクリック"):
			st.session_state['sel_df'] = tmp_df
			st.success('このページは終了')

	return
	
###
if __name__ == "__main__":
	main()