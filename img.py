import base64
import requests
import json


# OpenAI API Key
api_key = ""

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_paths_user = [
    r"C:\Users\me\Desktop\gpt_img\b1.png",
    r"C:\Users\me\Desktop\gpt_img\b2.png",
    r"C:\Users\me\Desktop\gpt_img\b3.png",
    r"C:\Users\me\Desktop\gpt_img\b4.png",
    r"C:\Users\me\Desktop\gpt_img\b5.png",
    r"C:\Users\me\Desktop\gpt_img\b6.png",
    r"C:\Users\me\Desktop\gpt_img\b7.png",


]

image_annotations_user = [
    "圖片1: 模擬初始設定，左右邊可選擇不同實驗樣品，並可以調節液體密度",
    "圖片2: 比較不同液體密度，相同體積與重量的樣品(A鉛塊)所受浮力(排開液體重量)不同",
    "圖片3: 比較不同形狀，體積以及重量相同的物體(A和B)，在同樣液體密度下所受浮力相同",
    "圖片4: 所有其他條件都相同，比較在不同深度下，物體所受浮力仍然相同",
    "圖片5: 比較下沉體積對浮力的影響，相同物體，左側下沉一半，右側完全沉入水面，右側所受浮力較大",
    "圖片6: 比較相同體積不同重量的物體，右側較輕物體密度小於液體密度，因此浮在水面上，其所受浮力等於其重量",
    "圖片7: 比較重量相同，體積(密度)不同的物體，在相同的液體密度下，左側物體排開液體體積較小，因此浮力無法支撐其重量讓他浮在水面上 ",
]

#image_paths_sys = [
#    r"C:\Users\me\Desktop\gpt_img\1.png",
#    r"C:\Users\me\Desktop\gpt_img\2.png",
#    r"C:\Users\me\Desktop\gpt_img\3.png",
#    r"C:\Users\me\Desktop\gpt_img\4.png"
#]
#
#image_annotations_sys = [
#    "圖片1: 模擬的初始狀態。",
#    "圖片2: 黏土剛開始下沉的變化。",
#    "圖片3: 黏土下沉一段時間的變化。",
#    "圖片4: 黏土下沉的最終狀態。"
#]


text_user = '''模擬說明:
此程式模擬在薄凸透鏡的成像與其光路。模擬中使用者可以選擇三種不同的成像情境，設定透鏡的焦長，與光路呈現的方式。模擬中三條特殊光線的簡易作圖路徑為 (1)平行主軸的光行經薄凸透鏡偏折後，會穿過透鏡另一側的焦點。(2) 射向鏡心的光線，前進方向不變。(3) 穿過同側焦點的光線，行經薄凸透鏡偏折後會平行主軸前進。使用者可以拖動紅色箭頭改變其位置，以觀察光線行經透鏡折射後所成的像的位置，方向與大小的變化。所成的像若為實像則以實線表示，若為虛像則以虛線表示。
成像情境模式:箭頭模式: 畫面中有一個可以拖曳的紅色箭頭的物體，拖曳箭頭後可觀察箭頭上的光線經透鏡折射後的成像位置，此外，畫面中有一隻可拖曳的眼睛，移動眼睛位置以觀察可以看到像的位置與判斷像的虛實。
可調參數: 
f: 薄凸透鏡焦長
單選選框:
可選擇(a)不顯示光路 (b)顯示靜態光路 (c)顯示動態光路
按鈕:
放大視野: 按鈕可放大觀察視野
縮小視野: 按鈕可縮小觀察視野
模擬操作: 
(1)設定成像模式，薄凸透鏡焦長(f)
(2)用滑鼠按壓薄凸透鏡左方的紅色箭頭，拖動箭頭以觀察箭頭的成像。
(3)搭配勾選顯示光路的模式來顯示光路
'''

text_sys='''

'''
# Getting the base64 string
encoded_images_user = [encode_image(path) for path in image_paths_user]
#encoded_images_sys = [encode_image(path) for path in image_paths_sys]

user_content = [
    {"type": "text", "text": text_user}
]
#sys_content = [
#    {"type": "text", "text": text_sys}
#]

for encoded_image, annotation in zip(encoded_images_user, image_annotations_user):
    #user_content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}})
    user_content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}})
    user_content.append({"type": "text", "text": annotation})

#for encoded_image, annotation in zip(encoded_images_sys, image_annotations_sys):
#    sys_content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}})
#    sys_content.append({"type": "text", "text": annotation})


json_file_path=r"C:\Users\me\Desktop\gpt_img\output.json"

with open(json_file_path, 'r',encoding='utf-8') as file:
        json_data = json.load(file)
        json_data=json.dumps(json_data)





payload = {
    "model": "gpt-4o",
    "messages": [
        {
           "role":"system",
           "content":'''
           你是一個可以根據模擬說明文字以及圖片，以及該模擬程式資料的json檔案生成該模擬的教學文件的助手
           你必須參考以下範例的風格，用最詳細的方式描述此模擬的場景以及細節。你的回覆只能使用繁體中文。
           你的回覆會參考圖片，但是產生回覆時禁止提到圖片x，只能提到在狀況描述中 狀況一，狀況二...等等的內容
           你的回覆遵照 #模擬情境描述 #模擬操作 #參考流程 #相關數據 #狀況描述 #教育目標 #觀察到什麼 的格式
           你的回覆內容沒有字數限制，字數越多越詳細越好
           在模擬情境描述中，你必須介紹此模擬的情境，並描述模擬執行過程中，會發生什麼樣的變化，你也必須列出此模擬中有哪些重要的物件，針對這些物件介紹，以及根據圖片精確地描述這些物件的外觀及作用;若是描述中有提及的話，也要列出實驗目標。
           在模擬操作中，你必須介紹學生可以進行那些操作，並且要說明這些操作會造成什麼相應的變化，你必須提出實驗過程中可能發生的所有情況
           在教育目標中，寫出此模擬中對於國高中生的教育意義，此模擬中的哪個特色可以讓學生從中學習到什麼概念，將所有可學到的概念列出 
           在狀況描述中，描述此模擬有哪些關鍵狀況，可以參考圖片描述其狀況，以 狀況一:... 狀況二... 描述，並且對於每一張圖片至少產生一個狀況描述，禁止提到如圖片x所示...的說法，直接產生該狀況描述即可，除了圖片之外有其他導致模擬結果有變化的關鍵狀況也要列出
           在觀察到什麼中，寫出此模擬中哪些變化會導致什麼其他變化的實例。例如:x的值越大，y便開始移動，或是某個z導致a顯著變化等等
           在參考流程，提出一個幫助實驗進行的參考流程，讓學生可以參考此流程學習到此實驗的教育目標或達成實驗目標
           在相關數據中，列出此模擬使用到跟物理現象有關的重要變數(忽略只跟模擬程式及座標有關的變數)，並解釋變數的意義，若是此變數應該由學生推論(用於觀察的變數)，則註記該變數為觀察目標。若是此變數由學生操控(學生可調整的變數)，則註記為調整變數，若是此變數只出現在json中而不存在於模擬說明以及圖片中，且此變數與此模擬有物理意義的關係，則註記為隱藏變數(學生無法直接觀測到)。

           範例:
#模擬情境描述
此模擬描述了一個不受外力作用的船上載著一個人，當人以等速 V 移動向船緣移動時，觀察人與船的運動狀況。船與水面間無磨擦力，因此可忽略摩擦力的影響。在模擬過程中，人以等速向船的左或右端點移動，並觀察船與人之間的相對運動。模擬的
目的是通過觀察質心位置和速度的變化，理解動量守恆和質心運動的概念。

模擬中的物件包括：
1. **人**：質量為50公斤的角色，位於船上，可以左右移動。
2. **船**：質量為 Mb 公斤，初始位置在畫面中央。
3. **黃色圓點**：表示系統質心的位置。
4. **藍色箭頭**：表示人的移動速度。
5. **橘色箭頭**：表示船的移動速度。
6. **粉紅色線段**：表示船身全長20公尺。

#模擬操作
學生可以進行下列操作：
1. **設置參數**: 使用滑動條設定船的質量Mb和人的移動速度Va，範圍在25公斤至1500公斤和-200公分/秒至200公分/秒之間。
2. **執行模擬**: 點擊「執行」按鈕後，觀察人在船上行走過程中，船和人的運動變化。
3. **重置模擬**: 點擊「重置」按鈕，恢復初始狀態，以便重新設置和運行模擬。

操作效果：
- 當設定好參數並執行模擬後，船上的人將以設定的速度向某一方向移動，船會因為人移動的反作用力向反方向移動。
- 當人移動至船的邊緣時，將以相同速度反向移動，這過程中船也會反方向移動，以保持系統質心位置不變。

#教育目標
此模擬主要教育以下概念：
1. **動量守恆**：了解在一個封閉系統中綜合動量保持不變。
2. **質心運動**：理解質心是如何在系統內物體相對運動下保持不變的。
3. **牛頓第三定律**：學習作用力與反作用力的概念。
4. **反作用原理**：探討人和船的相對運動所帶來的現象。

#狀況描述
- **狀況一**：初始狀態，船和人都位於畫面中央，人的速度為0，船的速度為0。
- **狀況二**：人開始向右行走，藍色箭頭表示人的速度，橘色箭頭表示船的反向速度，質心位置保持不變。
- **狀況三**：人行走至船的右邊緣，船向左移動較多，系統質心位置依然保持不變。
- **狀況四**：人停止向右行走並反向向左行走，此時船開始向右移動，保持質心位置不變。
- **狀況五**：人向左行走至船的左邊緣，船向右移動更多，系統質心位置保持不變。

#參考流程
1. **準備工作**：檢查模擬畫面人、船和質心的位置，確保滑桿設定正確。
2. **設定參數**：使用滑桿設定船的重量 (Mb) 和人的移動速度 (Va)。
3. **執行模擬**：點擊「執行」按鈕開始模擬，觀察人和船的運動。
4. **記錄數據**：定期記錄時間 (t)，人和船的質心位置 (Xa, Xb)，以及人和船的速度 (Va, Vb)。
5. **觀察對比**：觀察人在船上移動時，船的反向運動情況，以及系統質心的位置如何保持不變。
6. **完成模擬**：點擊「重置」按鈕，完成一次完整的模擬。

#相關數據
1. **t (時間)**：以秒為單位 (調整變數)。
2. **Ma (人的重量)**：50公斤 (固定變數)。
3. **Va (人的移動速度)**：以公分/秒為單位 (調整變數)。
4. **Mb (船的重量)**：以公斤為單位 (調整變數)。
5. **Xa (人的質心位置)**：以公分為單位 (觀察目標)。
6. **Xb (船的質心位置)**：以公分為單位 (觀察目標)。
7. **Vb (船的移動速度)**：以公分/秒為單位 (觀察目標)。
8. **Xc (系統的質心位置)**：以公分為單位 (隱藏變數)。

#觀察到什麼
- 當人向某一方向移動時，船會向反方向運動以保持整個系統的動量不變。
- 人和船的質心位置在整個過程中會互相對應但相反移動，系統的總質心位置不變。
- 藍色箭頭表示人的移動速度，橘色箭頭表示船的移動速度，兩者的長度與方向揭示了系統動量守恆現象。
'''
        },

        {
            "role": "user",
            "content": user_content
        },
         {
            "role": "user",
            "content": json_data
         }
    ],
    "n": 3  
}
#print(payload)

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

responses = response.json()
for i, choice in enumerate(responses['choices']):
    print(f"Response {i+1}: {choice['message']['content']}\n")



    