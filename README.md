# Softlake Claude Plugins

Marketplace ของ Claude Code สำหรับงานของ Softlake

| Plugin | ใช้ทำอะไร |
|---|---|
| na-bob-style | เขียนเอกสารภาษาไทยและอังกฤษแบบน้า Bob ไม่ให้ดูออกว่า AI เขียน พร้อมสคริปต์ตรวจลำดับสระวรรณยุกต์ อักขระต้องห้าม และสร้าง Word |

## ติดตั้งใน Claude Code

```bash
claude plugin marketplace add softlake-co-th/claude-plugins
claude plugin install na-bob-style@softlake-plugins
```

หรือพิมพ์ใน Claude Code:

```
/plugin marketplace add softlake-co-th/claude-plugins
/plugin install na-bob-style@softlake-plugins
```

Claude Code เวอร์ชัน 2.1.275 ขึ้นไปติดตั้งได้ในบรรทัดเดียว:

```
/plugin install na-bob-style --marketplace softlake-co-th/claude-plugins
```

ถ้า repo เป็น private เครื่องที่ติดตั้งต้อง login GitHub แล้ว (`gh auth login`)

## อัปเดต

```bash
claude plugin marketplace update softlake-plugins
```

เมื่อแก้ plugin ให้เพิ่มเลข `version` ทั้งใน `plugins/na-bob-style/.claude-plugin/plugin.json` และ `.claude-plugin/marketplace.json` ก่อน push

## ติดตั้งแบบ skill ส่วนตัว (ไม่ผ่าน marketplace)

```bash
git clone https://github.com/softlake-co-th/claude-plugins.git
./claude-plugins/install-skill.sh
```

## ใช้งาน

สั่งให้เขียน ร่าง หรือเรียบเรียงเอกสาร Claude จะโหลด skill เอง หรือเรียกตรงด้วย `/na-bob-style`

ตรวจไฟล์ด้วยมือ:

```bash
python3 plugins/na-bob-style/skills/na-bob-style/scripts/check_thai.py เอกสาร.md
```

## โครงสร้าง

```
.claude-plugin/marketplace.json
plugins/na-bob-style/
  .claude-plugin/plugin.json
  README.md
  skills/na-bob-style/
    SKILL.md
    scripts/check_thai.py
    scripts/make_thai_ref.py
install-skill.sh
```
