import json
import os
import csv

DATA_FILE = "students.json"
SUBJECTS = ["বাংলা", "ইংরেজি", "গণিত", "বিজ্ঞান", "সামাজিক বিজ্ঞান", "ধর্ম"]

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_data(students):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(students, f, ensure_ascii=False, indent=2)

def get_grade(avg):
    if avg >= 80: return "A+"
    elif avg >= 70: return "A"
    elif avg >= 60: return "B"
    elif avg >= 50: return "C"
    else: return "F"

def get_total(s): return sum(s["marks"].values())
def get_avg(s): return get_total(s) / len(s["marks"])
def is_passed(s): return all(m >= 33 for m in s["marks"].values())

def get_ranked(students):
    return sorted(students, key=lambda s: get_avg(s), reverse=True)

# ১. ছাত্র যোগ করো
def add_student(students):
    print("\n--- নতুন ছাত্র যোগ ---")
    name = input("নাম: ").strip()
    roll = input("Roll নম্বর: ").strip()

    if any(s["roll"] == roll for s in students):
        print("❌ এই Roll আগেই আছে!")
        return

    marks = {}
    for sub in SUBJECTS:
        while True:
            try:
                m = int(input(f"  {sub}: "))
                if 0 <= m <= 100:
                    marks[sub] = m
                    break
                else:
                    print("  ⚠️ 0-100 এর মধ্যে দাও!")
            except ValueError:
                print("  ⚠️ সংখ্যা দাও!")

    students.append({"name": name, "roll": roll, "marks": marks})
    save_data(students)
    print(f"✅ {name} এর ফলাফল সংরক্ষণ হয়েছে!")

# ২. Class Rank দেখো
def view_class_rank(students):
    if not students:
        print("\n❌ কোনো ছাত্রের তথ্য নেই!")
        return

    ranked = get_ranked(students)
    medals = {0: "🥇", 1: "🥈", 2: "🥉"}

    print("\n" + "="*70)
    print(f"{'Rank':<6} {'নাম':<20} {'Roll':<8} {'মোট':<8} {'গড়':<8} {'গ্রেড':<6} {'ফলাফল'}")
    print("="*70)

    for i, s in enumerate(ranked):
        medal = medals.get(i, f"  #{i+1}")
        total = get_total(s)
        avg = get_avg(s)
        grade = get_grade(avg)
        result = "পাস ✅" if is_passed(s) else "ফেল ❌"
        print(f"{medal:<6} {s['name']:<20} {s['roll']:<8} {total:<8} {avg:<8.1f} {grade:<6} {result}")

    print("="*70)

    avgs = [get_avg(s) for s in students]
    passed_count = sum(1 for s in students if is_passed(s))
    print(f"\n📊 ক্লাস গড়   : {sum(avgs)/len(avgs):.1f}")
    print(f"🏆 সর্বোচ্চ গড় : {max(avgs):.1f} ({ranked[0]['name']})")
    print(f"✅ পাস: {passed_count} | ❌ ফেল: {len(students)-passed_count}")

# ৩. Marks Edit করো
def edit_marks(students):
    if not students:
        print("\n❌ কোনো ছাত্রের তথ্য নেই!")
        return

    print("\n--- Marks Edit ---")
    query = input("নাম বা Roll দাও: ").strip().lower()

    found = [s for s in students
             if query in s["name"].lower() or query == s["roll"]]

    if not found:
        print("❌ পাওয়া যায়নি!")
        return

    if len(found) > 1:
        print("একাধিক ছাত্র পাওয়া গেছে:")
        for i, s in enumerate(found):
            print(f"  {i+1}. {s['name']} (Roll: {s['roll']})")
        try:
            choice = int(input("কোনজন? (নম্বর দাও): ")) - 1
            student = found[choice]
        except (ValueError, IndexError):
            print("❌ ভুল selection!")
            return
    else:
        student = found[0]

    print(f"\n{student['name']} (Roll: {student['roll']}) এর বর্তমান নম্বর:")
    for sub, mark in student["marks"].items():
        print(f"  {sub}: {mark}")

    print("\nনতুন নম্বর দাও (পরিবর্তন না করলে Enter চাপো):")
    for sub in SUBJECTS:
        current = student["marks"].get(sub, 0)
        val = input(f"  {sub} [{current}]: ").strip()
        if val:
            try:
                new_mark = int(val)
                if 0 <= new_mark <= 100:
                    student["marks"][sub] = new_mark
                else:
                    print("  ⚠️ 0-100 এর মধ্যে হতে হবে, পরিবর্তন হয়নি।")
            except ValueError:
                print("  ⚠️ ভুল input, পরিবর্তন হয়নি।")

    save_data(students)
    print(f"\n✅ {student['name']} এর নম্বর আপডেট হয়েছে!")

# ৪. CSV Export করো
def export_csv(students):
    if not students:
        print("\n❌ কোনো ছাত্রের তথ্য নেই!")
        return

    filename = input("\nCSV ফাইলের নাম (default: results.csv): ").strip()
    if not filename:
        filename = "results.csv"
    if not filename.endswith(".csv"):
        filename += ".csv"

    ranked = get_ranked(students)

    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)

        # Header
        writer.writerow([
            "Rank", "Roll", "নাম",
            *SUBJECTS,
            "মোট নম্বর", "গড়", "গ্রেড", "ফলাফল"
        ])

        # Data rows
        for i, s in enumerate(ranked):
            total = get_total(s)
            avg = get_avg(s)
            grade = get_grade(avg)
            result = "পাস" if is_passed(s) else "ফেল"
            writer.writerow([
                i + 1,
                s["roll"],
                s["name"],
                *[s["marks"].get(sub, 0) for sub in SUBJECTS],
                total,
                f"{avg:.1f}",
                grade,
                result
            ])

    print(f"✅ '{filename}' ফাইলে export হয়েছে! ({len(students)} জন ছাত্র)")

# ৫. ছাত্র খোঁজো (বিস্তারিত)
def search_student(students):
    print("\n--- ছাত্র খোঁজো ---")
    query = input("নাম বা Roll দাও: ").strip().lower()
    ranked = get_ranked(students)

    found = [s for s in students
             if query in s["name"].lower() or query == s["roll"]]

    if not found:
        print("❌ পাওয়া যায়নি!")
        return

    for s in found:
        rank = next(i+1 for i, r in enumerate(ranked) if r["roll"] == s["roll"])
        total = get_total(s)
        avg = get_avg(s)
        grade = get_grade(avg)

        print(f"\n{'='*42}")
        print(f"  নাম       : {s['name']}")
        print(f"  Roll      : {s['roll']}")
        print(f"  Class Rank: #{rank} / {len(students)}")
        print(f"{'='*42}")
        for sub in SUBJECTS:
            m = s["marks"].get(sub, 0)
            status = "✅" if m >= 33 else "❌"
            print(f"  {sub:<20}: {m:>3}  {status}")
        print(f"{'='*42}")
        print(f"  মোট নম্বর : {total} / {len(SUBJECTS)*100}")
        print(f"  গড় নম্বর  : {avg:.1f}")
        print(f"  গ্রেড      : {grade}")
        print(f"  ফলাফল     : {'পাস ✅' if is_passed(s) else 'ফেল ❌'}")
        print(f"{'='*42}")

# Main Menu
def main():
    students = load_data()

    while True:
        print("\n" + "="*38)
        print("   📚 Student Result System v2.0")
        print("="*38)
        print("  1. নতুন ছাত্র যোগ করো")
        print("  2. Class Rank দেখো 🏆")
        print("  3. Marks Edit করো ✏️")
        print("  4. CSV Export করো 📄")
        print("  5. ছাত্র খোঁজো 🔍")
        print("  6. বের হও")
        print("="*38)

        choice = input("অপশন বেছে নাও (1-6): ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            view_class_rank(students)
        elif choice == "3":
            edit_marks(students)
        elif choice == "4":
            export_csv(students)
        elif choice == "5":
            search_student(students)
        elif choice == "6":
            print("বিদায়! 👋")
            break
        else:
            print("⚠️ 1-6 এর মধ্যে বেছে নাও!")

main()