import pandas as pd
import plotly.express as px

# 1. データ読み込み
df = pd.read_csv("processed_2023.csv", encoding='utf-8')

# 2. データの前処理
# 'value' 列のカンマを削除し、数値型に変換
df['value'] = df['value'].str.replace(',', '').astype(float)


# 'date' 列を datetime 型に変換
df['date'] = pd.to_datetime(df['date'])

# 3. 年を削除し、月と日のみを持つ新しい列を作成
df['month_day'] = df['date'].dt.strftime('%m-%d')

# 4. 2月29日のデータを除外
df = df[df['month_day'] != '02-29']

# 5. 年の列を作成
df['year'] = df['date'].dt.year

# 6. 1月1日から12月31日までの日付リストを作成
date_list = [f"{i:02d}-{j:02d}" for i in range(1, 13) for j in range(1, 32)]
date_list = [d for d in date_list if d != '02-29']  # 2/29 を除外
date_list = date_list[:365] #リストが365要素になるように調整

# 7. 通し番号を割り当てる関数
def assign_index(month_day):
    try:
        return date_list.index(month_day)
    except ValueError:
        return None  # リストにない場合は None を返す

# 8. 通し番号を割り当てる
df['day_index'] = df['month_day'].apply(assign_index)
df = df.dropna(subset=['day_index'])  # None を含む行を削除
df['day_index'] = df['day_index'].astype(int)  # int型に変換

# プロット（折れ線グラフ）
fig = px.line(df, x="day_index", y="value", color="name", facet_col="store_name",
                 facet_row="year",  # 年でグラフを分ける
                 hover_data=['name', 'store_name', 'date', 'month_day', 'year'],
                 title="Date と Value の推移 (店別、部門別、年別)")

# X軸の目盛りを調整 (ファセットごとに適用)
for annotation in fig['layout']['annotations']:
    annotation['text'] = annotation['text'].split("=")[1]

# 10. X軸の目盛りを調整 (ファセットごとに適用)
for facet in fig.layout.annotations:
    facet_text = facet.text
    # 'year=' のようなテキストを削除
    store_name = facet_text.split('=')[-1]  # store_nameを抽出

    fig.update_xaxes(
        tickmode='array',
        tickvals=list(range(0, len(date_list), 30)),  # 30日ごとに目盛りを表示
        ticktext=[date_list[i] for i in range(0, len(date_list), 30)],  # 対応する日付を表示
        matches=None,  # 軸を共有しないように設定
        title="day_index",  # X軸のタイトルを表示
        # store_name に対応する列を指定。ただし、facet_colの数を超えないようにする
    )


# グローバルなレイアウト設定
fig.update_layout(
    xaxis_title="day_index",  # グローバルなX軸のタイトル
    autosize=True,  # ウィンドウサイズに合わせて自動調整

)

# HTMLファイルとして保存
fig.write_html("interactive_graph.html")

print("HTMLファイルが保存されました。")