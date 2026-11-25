#!/usr/bin/env python3
"""ตรวจอักขระต้องห้าม ลำดับสระ วรรณยุกต์ การเว้นวรรค คำสะกดผิด และสำนวน AI"""
import re, sys, unicodedata

def rng(a, b):
    return chr(a) + "-" + chr(b)

ALLOWED = re.compile("[" + chr(9) + chr(10) + chr(13) + rng(0x20, 0x7E) + rng(0x0E01, 0x0E3A)
                     + rng(0x0E3F, 0x0E4D) + rng(0x0E50, 0x0E59) + "]")
C = rng(0x0E01, 0x0E2E)                              # พยัญชนะ
V = chr(0x0E31) + rng(0x0E34, 0x0E3A) + chr(0x0E47)  # สระบน สระล่าง ไม้ไต่คู้
T = rng(0x0E48, 0x0E4C)                              # วรรณยุกต์ และ การันต์
T4 = rng(0x0E48, 0x0E4B)                             # วรรณยุกต์ 4 รูป
TH = rng(0x0E01, 0x0E4D)
AM, NIK, E, YMK = chr(0x0E33), chr(0x0E4D), chr(0x0E40), chr(0x0E46)
LEAD = rng(0x0E40, 0x0E44)                           # สระหน้า

ERRORS = [
    ("สระอำมาก่อนวรรณยุกต์ ต้องพิมพ์วรรณยุกต์ก่อนสระอำ", AM + "[" + T4 + "]"),
    ("ใช้นิคหิต (U+0E4D) ต้องใช้สระอำ U+0E33 ตัวเดียว", NIK),
    ("สระเอสองตัว ต้องใช้สระแอ U+0E41", E + E),
    ("สระหน้าไม่มีพยัญชนะตาม", "[" + LEAD + "](?![" + C + "])"),
    ("วรรณยุกต์มาก่อนสระบนหรือสระล่าง", "[" + T + "][" + V + "]"),
    ("วรรณยุกต์ซ้อน", "[" + T + "]{2,}"),
    ("สระบนหรือสระล่างซ้อน", "[" + V + "]{2,}"),
    ("สระหรือวรรณยุกต์ไม่มีพยัญชนะนำ", "(?<![" + C + V + T + "])[" + V + T + "]"),
    ("สระอำไม่มีพยัญชนะนำ", "(?<![" + C + T4 + "])" + AM),
    ("ใช้อัฒภาคหรืออัศเจรีย์ในภาษาไทย", "[" + TH + r"]\s?[;!]"),
]
WARNS = [
    ("จุลภาคในประโยคไทย ใช้การเว้นวรรคแทน", "[" + TH + r"]\s?,"),
    ("ไม้ยมกต้องเว้นวรรคข้างหน้า", r"\S" + YMK),
    ("ไม้ยมกต้องเว้นวรรคข้างหลัง", YMK + "[" + TH + "A-Za-z0-9]"),
    ("ควรเว้นวรรคก่อนวงเล็บเปิด", "[" + TH + r"]\("),
    ("ควรเว้นวรรคหลังวงเล็บปิด", r"\)[" + TH + "]"),
    ("ควรเว้นวรรคก่อน จำกัด ในชื่อบริษัท", r"(?:บริษัท|ห้างหุ้นส่วน)\s?[^\s]{1,30}จำกัด"),
]
MISSPELL = {
    "อินเตอร์เน็ต": "อินเทอร์เน็ต", "ซอฟท์แวร์": "ซอฟต์แวร์", "เว็ปไซต์": "เว็บไซต์",
    "เวบไซต์": "เว็บไซต์", "เว็บไซท์": "เว็บไซต์", "แอพพลิเคชั่น": "แอปพลิเคชัน",
    "แอปพลิเคชั่น": "แอปพลิเคชัน", "แอพ": "แอป", "ดิจิตอล": "ดิจิทัล",
    "อัพเดท": "อัปเดต", "อัพเดต": "อัปเดต", "อัพโหลด": "อัปโหลด", "แบ็คอัพ": "แบ็กอัป",
    "คลิ๊ก": "คลิก", "อีเมล์": "อีเมล", "เทคโนโลยี่": "เทคโนโลยี", "แพลทฟอร์ม": "แพลตฟอร์ม",
    "เน็ตเวิร์ค": "เน็ตเวิร์ก", "สคริปท์": "สคริปต์", "เทมเพลท": "เทมเพลต",
    "โปรเจค": "โปรเจกต์", "โปรเจ็ค": "โปรเจกต์", "เซิฟเวอร์": "เซิร์ฟเวอร์",
    "ล็อคอิน": "ล็อกอิน", "คอมเม้นท์": "คอมเมนต์", "อนุญาติ": "อนุญาต",
    "ผลลัพท์": "ผลลัพธ์", "กระทันหัน": "กะทันหัน", "โควต้า": "โควตา", "สังเกตุ": "สังเกต",
    "ปฎิบัติ": "ปฏิบัติ", "กฏ": "กฎ", "บุคคลากร": "บุคลากร", "ลายเซ็นต์": "ลายเซ็น",
    "ซอฟแวร์": "ซอฟต์แวร์", "เวอร์ชั่น": "เวอร์ชัน", "ฟังก์ชั่น": "ฟังก์ชัน",
    "เบราเซอร์": "เบราว์เซอร์", "บราวเซอร์": "เบราว์เซอร์",
}
AI_TH = ["ในยุคดิจิทัล", "ในยุคปัจจุบันที่", "ในโลกที่เปลี่ยนแปลง", "ปฏิเสธไม่ได้ว่า",
         "กล่าวโดยสรุป", "โดยสรุปแล้ว", "โดยรวมแล้ว", "ท้ายที่สุดแล้ว", "ไม่เพียงแต่",
         "ทำให้มั่นใจได้ว่า", "มีบทบาทสำคัญ", "ก้าวสำคัญ", "ก้าวไปอีกขั้น", "เป็นสิ่งสำคัญที่",
         "สิ่งสำคัญคือ", "ในการที่จะ", "ได้ถูก", "มันคือ", "ไร้รอยต่อ", "ปลดล็อก", "ขุมพลัง",
         "เหนือระดับ", "พลิกโฉม", "ปฏิวัติวงการ", "ล้ำสมัย", "ตอบโจทย์ทุก", "ภูมิทัศน์",
         "หัวใจสำคัญ", "กุญแจสำคัญ", "จุดเปลี่ยน", "เปรียบเสมือน", "ประตูสู่", "ไม่ว่าจะเป็น",
         "อย่างลึกซึ้ง", "อย่างแท้จริง", "อย่างยิ่งยวด", "การดำเนินการในการ", "ทำการ"]
LIMITED = ["ทั้งนี้", "นอกจากนี้", "อย่างไรก็ตาม", "ดังนั้น", "ยิ่งไปกว่านั้น", "บูรณาการ",
           "ยกระดับ", "ขับเคลื่อน", "ครอบคลุม", "อย่างมีประสิทธิภาพ", "อย่างยั่งยืน",
           "ครบวงจร", "ศักยภาพ", "นวัตกรรม"]
AI_EN = ["delve", "tapestry", "testament", "leverage", "harness", "unlock", "unleash",
         "elevate", "empower", "robust", "seamless", "cutting-edge", "game-changer",
         "transformative", "revolutionize", "pivotal", "paramount", "holistic", "synergy",
         "streamline", "foster", "embark", "meticulous", "multifaceted", "ever-evolving",
         "vibrant", "showcase", "underscore", "spearhead", "bolster", "plethora", "myriad",
         "utilize", "it's important to note", "it's worth noting", "dive in",
         "in today's fast-paced", "in the digital age", "plays a crucial role",
         "i hope this email finds you well", "look no further", "moreover", "furthermore"]

def loc(text, i):
    line = text.count("\n", 0, i) + 1
    return line, i - (text.rfind("\n", 0, i) + 1) + 1

def ctx(text, s, e):
    return text[max(0, s - 10):e + 10].replace("\n", " ")

def main(path):
    t = open(path, encoding="utf-8-sig").read()  # BOM ที่หัวไฟล์เป็นส่วนของรูปแบบไฟล์ ไม่นับเป็นอักขระต้องห้าม
    err = warn = 0
    for i, ch in enumerate(t):
        if not ALLOWED.match(ch):
            l, c = loc(t, i)
            name = unicodedata.name(ch, "UNKNOWN")
            print(f"ERROR {l}:{c} อักขระต้องห้าม U+{ord(ch):04X} {name} | {ctx(t, i, i + 1)!r}")
            err += 1
    for msg, pat in ERRORS:
        for m in re.finditer(pat, t):
            l, c = loc(t, m.start())
            print(f"ERROR {l}:{c} {msg} | {ctx(t, m.start(), m.end())!r}")
            err += 1
    for msg, pat in WARNS:
        for m in re.finditer(pat, t):
            l, c = loc(t, m.start())
            print(f"WARN  {l}:{c} {msg} | {ctx(t, m.start(), m.end())!r}")
            warn += 1
    for bad, good in MISSPELL.items():
        for m in re.finditer(re.escape(bad), t):
            l, c = loc(t, m.start())
            print(f"WARN  {l}:{c} สะกด {bad} ควรเป็น {good}")
            warn += 1
    for p in AI_TH:
        n = t.count(p)
        if n:
            print(f"WARN  สำนวน AI '{p}' พบ {n} ครั้ง")
            warn += 1
    low = t.lower()
    for p in AI_EN:
        n = len(re.findall(r"\b" + re.escape(p) + r"\b", low))
        if n:
            print(f"WARN  English AI word '{p}' x{n}")
            warn += 1
    pages = max(1, len(t) // 1800)
    for p in LIMITED:
        n = t.count(p)
        if n > pages:
            print(f"WARN  '{p}' ใช้ {n} ครั้ง (ไม่ควรเกิน {pages} ครั้งสำหรับความยาวนี้)")
            warn += 1
    abbr = {}
    for m in re.finditer(r"\(([" + C + r"\.]{2,15})\)", t):
        a = m.group(1)
        if "." in a or len(re.findall("[" + C + "]", a)) >= 3:
            abbr.setdefault(a, []).append(m.start())
    for a, pos in abbr.items():
        if len(pos) > 1:
            l, c = loc(t, pos[1])
            print(f"WARN  {l}:{c} ชื่อเต็มพร้อมตัวย่อ ({a}) ซ้ำ {len(pos)} ครั้ง หลังครั้งแรกให้ใช้ {a} อย่างเดียว")
            warn += 1
    if re.search("[" + rng(0x0E50, 0x0E59) + "]", t) and re.search(r"[0-9]", t):
        print("WARN  มีทั้งเลขไทยและเลขอารบิกในไฟล์เดียว")
        warn += 1
    em = len(re.findall(r"[A-Za-z]!", t))
    words = max(1, len(re.findall(r"[A-Za-z]+", t)))
    if em > max(1, words // 1000):
        print(f"WARN  English exclamation marks x{em}")
        warn += 1
    print(f"สรุป: ERROR {err} / WARN {warn}")
    return 1 if err else 0

if __name__ == "__main__":
    sys.exit(max(main(p) for p in sys.argv[1:]))
