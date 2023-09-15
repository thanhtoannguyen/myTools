import re
import clipboard
import time
import os

# Danh sách để lưu trữ các liên kết đã chuyển đổi
converted_links = set()

def extract_link(text):
    # Tìm kiếm link bằng regex
    pattern = r"(https?://\S+)"
    match = re.search(pattern, text)
    if match:
        return match.group(0)
    else:
        return None

def check_clipboard():
    last_copied_text = ""
    while True:
        copied_text = clipboard.paste()
        if copied_text != last_copied_text:
            last_copied_text = copied_text
            link = extract_link(copied_text)
            if link and link not in converted_links:  # Kiểm tra liên kết chưa tồn tại trong danh sách
                clipboard.copy(link)
                print("Link đã được sao chép vào clipboard: ", link)
                converted_links.add(link)  # Thêm liên kết vào danh sách
        time.sleep(1)

if __name__ == "__main__":
    try:
        check_clipboard()
    except KeyboardInterrupt:
        # Ngắt chương trình và tạo tệp txt khi nhấn Ctrl+C
        if converted_links:
            # Tìm tên tệp txt tiếp theo trong dãy: links_part_1.txt, links_part_2.txt, ...
            index = 1
            while True:
                txt_file_name = f"links_part_{index}.txt"
                if not os.path.exists(txt_file_name):
                    break
                index += 1

            # Tạo và ghi danh sách các liên kết vào tệp txt
            with open(txt_file_name, 'w') as txt_file:
                for link in converted_links:
                    txt_file.write(link + '\n')
            print(f"Đã lưu danh sách các liên kết vào tệp txt '{txt_file_name}'")
