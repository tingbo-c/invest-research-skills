"""
把整个 skill suite 的所有 .md 文件合并成一个文档，方便发给 AI 做方法论审查。
运行方式：python export_for_review.py
输出文件：skill_suite_for_review.md（在同目录下）
"""

import os

# 要包含的目录（按顺序，底座在前）
SKILL_DIRS = [
    "shared-research-context",
    "行业研究skill",
    "stock-fundamental",
    "macro-research",
    "research-review",
]

# 每个目录里优先输出的文件顺序
FILE_PRIORITY = ["SKILL.md", "README.md"]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(BASE_DIR, "skill_suite_for_review.md")


def collect_md_files(skill_dir_path):
    """收集一个 skill 目录下的所有 .md 文件，SKILL.md 和 README.md 优先"""
    all_files = []
    for root, dirs, files in os.walk(skill_dir_path):
        # 跳过隐藏目录
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for f in files:
            if f.endswith('.md'):
                all_files.append(os.path.join(root, f))

    # 排序：优先文件在前，其余按路径排序
    def sort_key(path):
        filename = os.path.basename(path)
        if filename in FILE_PRIORITY:
            return (0, FILE_PRIORITY.index(filename), path)
        return (1, 0, path)

    return sorted(all_files, key=sort_key)


def main():
    output_lines = []
    output_lines.append("# Research Skill Suite - 完整方法论文档")
    output_lines.append("\n> 本文档由 export_for_review.py 自动生成，用于方法论审查。\n")
    output_lines.append("---\n")

    total_files = 0

    for skill_dir_name in SKILL_DIRS:
        skill_dir_path = os.path.join(BASE_DIR, skill_dir_name)
        if not os.path.exists(skill_dir_path):
            print(f"⚠️  目录不存在，跳过：{skill_dir_name}")
            continue

        output_lines.append(f"\n\n# ═══ {skill_dir_name} ═══\n")

        md_files = collect_md_files(skill_dir_path)
        for filepath in md_files:
            relative_path = os.path.relpath(filepath, BASE_DIR)

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
            except Exception as e:
                print(f"⚠️  读取失败：{relative_path} - {e}")
                continue

            output_lines.append(f"\n\n## 📄 {relative_path}\n")
            output_lines.append("```")
            output_lines.append(content)
            output_lines.append("```\n")
            total_files += 1
            print(f"[OK] {relative_path}")

    # 写出合并文件
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))

    file_size_kb = os.path.getsize(OUTPUT_FILE) / 1024
    print(f"\n完成！共合并 {total_files} 个文件")
    print(f"输出文件：{OUTPUT_FILE}")
    print(f"文件大小：{file_size_kb:.1f} KB")


if __name__ == "__main__":
    main()
