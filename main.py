# tkinter モジュールをインポートし、短縮名を tk として定義
import tkinter as tk
# ttk モジュールをインポート
from tkinter import ttk
# messagebox モジュールをインポート
from tkinter import messagebox
# filedialog モジュールをインポート
from tkinter import filedialog
# datetime モジュールから date クラス、timedelta クラスをインポート
from datetime import date, timedelta
# calendar モジュールをインポート
import calendar
# csv モジュールをインポート
import csv
# tkinter.ttk モジュールから Treeview クラスをインポート
from tkinter.ttk import Treeview

# 指定された日付オブジェクトから、曜日の略称（例：月曜日 -> 月）を取得する関数
def get_weekday(date_obj):
    return calendar.day_name[date_obj.weekday()][:2]

# 学習計画を生成する関数
def generate_study_plan():
    study_plan = []

    # 開始日と終了日を Entry ウィジェットから取得し、date オブジェクトに変換
    start_date = date.fromisoformat(start_date_entry.get())
    end_date = date.fromisoformat(end_date_entry.get())

    # 現在の日付を開始日に設定し、日数カウントと開始ページ数を初期化
    current_date = start_date
    day_count = 0
    start_page = 0

    # 現在の日付が終了日を超えるまで、ループを繰り返す
    while current_date <= end_date:
        # テーブルに表示する行データを表すリストを作成し、日付と曜日を追加
        row_data = [current_date, get_weekday(current_date)]

        # 各カラムの設定を反映して、行データに学習内容を追加していく
        for column_data in columns:
            interval = int(column_data["interval"].get())
            prefix = column_data["prefix"].get()
            suffix = column_data["suffix"].get()
            start_page = int(column_data["start_page"].get())
            max_page = int(column_data["max_page"].get())

            study_count = column_data["study_count"]

            review_interval = int(column_data["review_interval"].get())
            study_weekdays = column_data["weekdays_only_var"].get() == 1
            study_weekends = column_data["weekends_only_var"].get() == 1

            # 平日のみまたは土日祝のみに設定されている場合、学習を実施
            if (study_weekdays and current_date.weekday() < 5) or (study_weekends and current_date.weekday() >= 5):
                # 復習日の場合、"復習" という文字列を追加
                if day_count % review_interval == 0:
                    row_data.append("           復習")
            else:
                # 学習日の場合、指定されたページ数の範囲で学習を実施し、結果を追加
                if study_count == 0:
                    study_count = start_page

                if study_count + interval - 1 > max_page:
                    row_data.append(f"ページ数を超えています (最大: {max_page})")
                else:
                    row_data.append(prefix + str(study_count) + suffix + "-" + prefix + str(study_count + interval - 1) + suffix)
                    study_count += interval
                    column_data["study_count"] = study_count
        else:
            # 平日または土日祝に設定されていない場合、空白という文字列を追加
            row_data.append("(空白)")

    # 行データを学習計画に追加
    study_plan.append(row_data)

    # 現在の日付を1日進め、日数カウントを加算
    current_date += timedelta(days=1)
    day_count += 1

    # 各カラムの開始ページ数を初期化
    for column_data in columns:
        column_data["study_count"] = int(column_data["start_page"].get())

    # 学習計画を表示する Treeview ウィジェットの表示内容をリセット
    study_plan_tree.delete(*study_plan_tree.get_children())

    # 学習計画の内容を Treeview ウィジェットに追加
    for row in study_plan:
        study_plan_tree.insert("", tk.END, values=(row[0], row[1], ", ".join(row[2:])))

    return study_plan

#学習計画を CSV ファイルにエクスポートする関数
def export_study_plan():
# 学習計画を生成
    study_plan = generate_study_plan()
    # 保存先のファイルパスを指定するダイアログを表示
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSVファイル", "*.csv")])

    # ファイルパスが指定されていない場合は処理を終了
    if not file_path:
        return

    # CSV ファイルを開き、学習計画を書き込む
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["日付", "曜日"] + [f"学習計画 {i + 1}" for i in range(len(columns))])
        for row in study_plan:
            writer.writerow(row)

def add_column():
# カラムの設定を表す辞書を作成
    column_data = {
    "title": ttk.Label(column_frame, text=f"学習計画 {len(columns) + 1}"),
    "interval": ttk.Entry(column_frame),
    "prefix": ttk.Entry(column_frame),
    "suffix": ttk.Entry(column_frame),
    "start_page": ttk.Entry(column_frame),
    "max_page": ttk.Entry(column_frame),
    "review_interval": ttk.Entry(column_frame),
    "weekdays_only_var": tk.IntVar(),
    "weekends_only_var": tk.IntVar(),
    "study_count": 0
    }
    # カラムのタイトルを表示するラベルをカラムフレームに配置
    column_data["title"].grid(row=0, column=len(columns) * 7, padx=5, pady=5)

    # カラムの設定項目をラベルとエントリーで表示する
    ttk.Label(column_frame, text="間隔:").grid(row=1, column=len(columns) * 7, padx=5, pady=5)
    column_data["interval"].grid(row=1, column=len(columns) * 7 + 1, padx=5, pady=5)

    ttk.Label(column_frame, text="接頭辞:").grid(row=2, column=len(columns) * 7, padx=5, pady=5)
    column_data["prefix"].grid(row=2, column=len(columns) * 7 + 1, padx=5, pady=5)

    ttk.Label(column_frame, text="接尾語:").grid(row=3, column=len(columns) * 7, padx=5, pady=5)
    column_data["suffix"].grid(row=3, column=len(columns) * 7 + 1, padx=5, pady=5)

    ttk.Label(column_frame, text="開始ページ:").grid(row=4, column=len(columns) * 7, padx=5, pady=5)
    column_data["start_page"].grid(row=4, column=len(columns) * 7 + 1, padx=5, pady=5)

    ttk.Label(column_frame, text="最大ページ:").grid(row=5, column=len(columns) * 7, padx=5, pady=5)
    column_data["max_page"].grid(row=5, column=len(columns) * 7 + 1, padx=5, pady=5)

    ttk.Label(column_frame, text="復習間隔:").grid(row=6, column=len(columns) * 7, padx=5, pady=5)
    column_data["review_interval"].grid(row=6, column=len(columns) * 7 + 1, padx=5, pady=5)

    # 平日のみと土日祝のみのチェックボックスを表示する
    ttk.Checkbutton(column_frame, text="平日のみ", variable=column_data["weekdays_only_var"]).grid(row=7, column=len(columns) * 7, padx=5, pady=5)
    ttk.Checkbutton(column_frame, text="土日祝のみ", variable=column_data["weekends_only_var"]).grid(row=7, column=len(columns) * 7 + 1, padx=5, pady=5)

    # 各設定項目の初期値を設定
    column_data["interval"].insert(0, "2")
    column_data["prefix"].insert(0, "第")
    column_data["suffix"].insert(0, "ページ")
    column_data["start_page"].insert(0, "1")
    column_data["max_page"].insert(0, "100")
    column_data["review_interval"].insert(0, "7")

    # カラムデータをリストに追加
    columns.append(column_data)
root = tk.Tk()
root.title("学習計画ジェネレーター")
main_frame = ttk.Frame(root, padding=10)
main_frame.grid(row=0, column=0)
date_frame = ttk.Frame(main_frame)
date_frame.grid(row=0, column=0)
column_frame = ttk.Frame(main_frame)
column_frame.grid(row=1, column=0)
treeview_frame = ttk.Frame(main_frame)
treeview_frame.grid(row=2, column=0)
button_frame = ttk.Frame(main_frame)
button_frame.grid(row=3, column=0)
ttk.Label(date_frame, text="開始日:").grid(row=0, column=0, padx=5, pady=5)
start_date_entry = ttk.Entry(date_frame)
start_date_entry.grid(row=0, column=1, padx=5, pady=5)
start_date_entry.insert(0, date.today().isoformat())

ttk.Label(date_frame, text="終了日:").grid(row=0, column=2, padx=5, pady=5)
end_date_entry = ttk.Entry(date_frame)
end_date_entry.grid(row=0, column=3, padx=5, pady=5)
end_date_entry.insert(0, (date.today() + timedelta(days=30)).isoformat())

columns = []

#最初のカラムを追加
add_column()

#カラム追加ボタンを作成してカラムフレームに配置
add_column_button = ttk.Button(column_frame, text="追加", command=add_column)
add_column_button.grid(row=8, column=0, padx=5, pady=5)

#学習計画を表示するツリービューを作成してフレームに配置
study_plan_tree = Treeview(treeview_frame, columns=("日付", "曜日", "学習計画"), show="headings")
study_plan_tree.column("日付", width=100, anchor=tk.CENTER)
study_plan_tree.column("曜日", width=50, anchor=tk.CENTER)
study_plan_tree.column("学習計画", width=400, anchor=tk.W)
study_plan_tree.heading("日付", text="日付")
study_plan_tree.heading("曜日", text="曜日")
study_plan_tree.heading("学習計画", text="学習計画")
study_plan_tree.grid(row=0, column=0, padx=5, pady=5)

#生成とエクスポートのボタンを作成してフレームに配置
generate_button = ttk.Button(button_frame, text="生成", command=generate_study_plan)
generate_button.grid(row=0, column=0, padx=5, pady=5)

export_button = ttk.Button(button_frame, text="エクスポート", command=export_study_plan)
export_button.grid(row=0, column=1, padx=5, pady=5)

root.mainloop()
