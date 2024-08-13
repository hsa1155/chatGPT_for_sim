import json

def remove_entries(data, keys_to_remove):
    """
    遞歸移除 JSON 中值為空字符串的項和特定鍵名的項。
    :param data: 字典或列表形式的 JSON 數據
    :param keys_to_remove: 要移除的鍵名列表
    :return: 移除指定項後的 JSON 數據
    """
    if isinstance(data, dict):
        return {k: remove_entries(v, keys_to_remove) for k, v in data.items() if v != "" and k not in keys_to_remove}
    elif isinstance(data, list):
        return [remove_entries(item, keys_to_remove) for item in data if item != ""]
    return data

def process_json_file(input_file, output_file, keys_to_remove):
    """
    從輸入文件讀取 JSON 數據，移除值為空字符串和特定鍵名的項，並將結果寫入輸出文件。
    :param input_file: 輸入 JSON 文件路徑
    :param output_file: 輸出 JSON 文件路徑
    :param keys_to_remove: 要移除的鍵名列表
    """
    # 從文件中讀取 JSON 數據
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

#移除值為空字符串和特定鍵名的項
    cleaned_data = remove_entries(data, keys_to_remove)

#將結果寫回到另一個 JSON 文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=4)

#使用示例
input_file = r"C:\Users\me\Desktop\gpt_img\buoyancy.json" # 輸入文件的絕對路徑
output_file =r"C:\Users\me\Desktop\gpt_img\output.json"  # 輸出文件的絕對路徑
keys_to_remove = ["imagefile", "attr_imagefile","id","blocklyEditorContent","StepsPerDisplay","numericalMethod","blocklyXML","attr_id","AbsoluteTolerance","fps"]  # 要移除的特定鍵名列表

process_json_file(input_file, output_file, keys_to_remove)