import pandas as pd
import matplotlib.pyplot as plt


# 移動平均のグラフを描きまっす！


# ファイルパス
file_path = './data/merged_data.csv'  # 相対パスを使用

# CSVファイルをShift-JISで読み込む
try:
    df = pd.read_csv(file_path, encoding='shift-jis')
except FileNotFoundError:
    print(f"エラー：ファイル '{file_path}' が見つかりませんでした。")
    exit()
except UnicodeDecodeError:
    print(f"エラー：ファイル '{file_path}' の読み込みに失敗しました。正しいエンコーディングがShift-JISであることを確認してください。")
    exit()

# 必要な列名が存在するか確認
required_columns = ['年月日', '旭川_最高気温(℃)', '札幌_最高気温(℃)']
if not all(col in df.columns for col in required_columns):
    print(f"エラー：必要な列 ({required_columns}) がCSVファイルに含まれていません。")
    print(f"CSVファイルの列名：{df.columns.tolist()}")
    exit()

# 列名の変更
df = df.rename(columns={
    '旭川_最高気温(℃)': 'Asahikawa_Max_Temp',
    '札幌_最高気温(℃)': 'Sapporo_Max_Temp'
})

# '年月日'列をdatetime型に変換
try:
    df['年月日'] = pd.to_datetime(df['年月日'])
except ValueError:
    print("エラー：'年月日'列を日付型に変換できませんでした。日付の形式を確認してください。")
    exit()

# 数値データに変換
numeric_columns = ['Asahikawa_Max_Temp', 'Sapporo_Max_Temp']  # 変更後の列名を使用
for col in numeric_columns:
    try:
        df[col] = pd.to_numeric(df[col])
    except ValueError:
        print(f"エラー：'{col}'列を数値型に変換できませんでした。数値以外の値が含まれていないか確認してください。")
        exit()

# '年月日'列をインデックスに設定
df.set_index('年月日', inplace=True)

# 移動平均の計算 (窓幅7日)
window_size = 25
df['Asahikawa_Max_Temp_MA'] = df['Asahikawa_Max_Temp'].rolling(window=window_size).mean()
df['Sapporo_Max_Temp_MA'] = df['Sapporo_Max_Temp'].rolling(window=window_size).mean()

# プロット
plt.figure(figsize=(12, 6))  # 図のサイズを調整

# # オリジナルのデータをプロット（薄い色で）
# plt.plot(df.index, df['Asahikawa_Max_Temp'], label='Asahikawa_Max_Temp (Original)', alpha=0.5)
# plt.plot(df.index, df['Sapporo_Max_Temp'], label='Sapporo_Max_Temp (Original)', alpha=0.5)

# 移動平均をプロット（濃い色で）
plt.plot(df.index, df['Asahikawa_Max_Temp_MA'], label=f'Asahikawa_Max_Temp (MA {window_size} days)')
plt.plot(df.index, df['Sapporo_Max_Temp_MA'], label=f'Sapporo_Max_Temp (MA {window_size} days)')

plt.xlabel('Date')
plt.ylabel('Maximum Temperature')
plt.title('Maximum Temperatures in Asahikawa and Sapporo (with Moving Average)')
plt.legend()
plt.grid(True)  # グリッド線を表示
plt.xticks(rotation=45)  # X軸のラベルを45度回転
plt.tight_layout()  # ラベルがはみ出さないように調整
plt.show()