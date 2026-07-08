import streamlit as st
import pandas as pd
###
### Main ###
def main():
	st.set_page_config(
		page_title="シンプルアプリ",
		layout="wide"
			)
	st.title('データ選択')
	#
	read_file()
	#
	if 'load_df' in st.session_state:
		st.success(f'Selected File = {st.session_state.filename}')
	return

def read_file():
	selected_file = st.file_uploader("データファイルをアップロードしてください", type=["txt", "dat", "csv", "xls", "xlsx"])

	if selected_file is not None:
		st.session_state.filename = selected_file.name
		file_type = selected_file.name.split(".")[-1].lower()
		try:
			if file_type == "csv":
				load_df = pd.read_csv(selected_file, header=None)
			elif file_type in ["dat", "txt"]:
				load_df = pd.read_table(selected_file, header=None, encoding="utf-8", sep="\t")
			elif file_type in ["xlsx", "xls"]:
				load_df = pd.read_excel(selected_file)  
			else:
				st.error("対応していないファイル形式です。")
				st.stop()
		except Exception as e:
			st.error(f"ファイルの読み込みに失敗しました: {e}")
			st.stop()
		#
		show_data(load_df)

		check_col(load_df)

		if st.button("これで良ければクリック"):
			st.success('このページは終了')

	return

def show_data(load_df):
	if not load_df.empty:
		load_df = convert_to_number(load_df)
		#
		st.success("データプレビュー（数値データ以外を消去済み）")
		st.write(f'データ数: {len(load_df)}行')
		st.dataframe(load_df)
		st.session_state['load_df'] = load_df
	return

def convert_to_number(load_df):
	for col in load_df:
		# 文字列化
		series_str = load_df[col].astype(str)
		# 数字・小数点・マイナス以外を削除
		series_str = series_str.str.replace(r"[^0-9.-]", "", regex=True)
		# 空文字は NaN に
		series_str = series_str.replace("", None)
		# 数値変換（失敗時は NaN）
		load_df[col] = pd.to_numeric(series_str, errors="coerce")
	return load_df

def check_col(load_df):
	if ('時間' in load_df.columns.tolist()) and ('緩和弾性率' in load_df.columns.tolist()):
		sel_df = load_df[['時間', '緩和弾性率']]
		sel_df.columns = ['Time', 'G(t)']
		st.session_state['sel_df'] = sel_df
		return
	else:
		list_col=[]
		for i in range(len(load_df.columns)):
			list_col.append('col_'+str(i))
		load_df.columns = list_col		
		st.session_state['sel_df'] = pd.DataFrame()
	return

###
if __name__ == "__main__":
	main()