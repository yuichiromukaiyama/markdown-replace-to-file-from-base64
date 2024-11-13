import base64
import os
import re

# 入力となるMarkdownファイルと出力先フォルダの設定
input_md_file = "input.md"
output_md_file = "output.md"
output_image_folder = "images"

# 出力フォルダが存在しない場合は作成
if not os.path.exists(output_image_folder):
    os.makedirs(output_image_folder)

# Markdownファイルの読み込み
with open(input_md_file, "r", encoding="utf-8") as file:
    markdown_content = file.read()

# Base64形式の画像を検出する正規表現パターン
base64_pattern = r"!\[.*?\]\(data:image/(png|jpeg|jpg|gif);base64,(.*?)\)"

# すべてのBase64画像データを検出
matches = re.findall(base64_pattern, markdown_content)

# 検出されたBase64データを画像ファイルとして保存し、Markdown内の文字列を置換
for index, (img_type, base64_str) in enumerate(matches):
    # Base64データをデコードしてバイナリ形式に変換
    img_data = base64.b64decode(base64_str)

    # ファイル名を生成し、指定フォルダに保存
    img_filename = f"image_{index + 1}.{img_type}"
    img_filepath = os.path.join(output_image_folder, img_filename)

    with open(img_filepath, "wb") as img_file:
        img_file.write(img_data)

    # Markdown内のBase64文字列部分を画像ファイルパスに置換
    markdown_content = markdown_content.replace(
        f"data:image/{img_type};base64,{base64_str}", img_filepath
    )

# 変更後のMarkdown内容を新しいファイルに書き込み
with open(output_md_file, "w", encoding="utf-8") as file:
    file.write(markdown_content)

print(
    f"処理完了。画像は {output_image_folder} に保存され、Markdownは {output_md_file} に出力されました。"
)
