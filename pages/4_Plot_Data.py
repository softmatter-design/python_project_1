import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io
import zipfile
from datetime import datetime
###
def main():
	st.set_page_config(
		page_title="シンプルアプリ",
		layout="wide"
			)
	st.title('データ選択')

	if len(st.session_state.sel_df.columns) != 2:
		st.write('データはまだ選択されていません')
	else:
		st.write('現時点でのデータ形式は以下です')
		st.dataframe(st.session_state.cut_df)

		make_graph(st.session_state.cut_df)
		# plot(st.session_state.cut_df)

	return

# グラフ生成関数
def create_plot(title, x, y):
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_title(title)
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    fig.tight_layout()
    return fig

# ZIP作成関数
def create_zip(figs):
	# CSV出力
	csv_buffer = io.StringIO()
	st.session_state.cut_df.to_csv(csv_buffer, index=False)
	csv_buffer.seek(0)
	#
	zip_buffer = io.BytesIO()
	with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
		for i, fig in enumerate(figs, start=1):
			img_buffer = io.BytesIO()
			fig.savefig(img_buffer, format="png")
			img_buffer.seek(0)
			zip_file.writestr(f"graph_{i}.png", img_buffer.read())
		zip_file.writestr("table.csv", csv_buffer.getvalue())
	zip_buffer.seek(0)
	return zip_buffer

def make_graph(df):
	time = df['Mod. Time'][1:].to_numpy()
	gt = df['G(t)'][1:].to_numpy()
	ngt = df['Norm. G(t)'][1:].to_numpy()
	# グラフ作成
	figs = [
		create_plot("G(t)", time, gt),
		create_plot("Norm. G(t)", time, ngt),
	]

	# 表示
	for fig in figs:
		st.pyplot(fig)
	#
	zip_data = create_zip(figs)

	# ダウンロードボタン
	st.download_button(
		label="📦 ZIPで一括ダウンロード",
		data=zip_data,
		file_name=f"graphs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
		mime="application/zip"
	)

	return










def plot(df):
	time = df['Mod. Time'][1:].to_numpy()
	gt = df['G(t)'][1:].to_numpy()
	ngt = df['Norm. G(t)'][1:].to_numpy()
	#
	g_type = st.selectbox('Select Graph', ['G(t)', 'Norm.G(t)'])
	fig, ax = plt.subplots(figsize=(4, 4)) 
	#
	if 'G(t)' in g_type:
		ax.plot(time, gt)
		ax.set_xlabel('Time')
		ax.set_ylabel('G(t)')
	elif 'Norm.G(t)' in g_type:
		ax.plot(time, ngt)
		ax.set_xlabel('Time')
		ax.set_ylabel('Norm.G(t)')
	#
	ax.set_xscale('log')
	ax.set_yscale('log')
	#
	fn = 'graph.png'
	img = io.BytesIO()
	plt.savefig(img, format='png')

	btn = st.download_button(
	label="Download graph as PNG",
	data=img,
	file_name=fn,
	mime="image/png"
	)
	#
	st.pyplot(fig)

	return

###
if __name__ == "__main__":
	main()