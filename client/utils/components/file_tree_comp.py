import os
import streamlit_antd_components as sac

def build_tree_data(root_dir):
    tree = []

    for root, dirs, files in os.walk(root_dir):
        # Игнорируем скрытые папки
        dirs[:] = [d for d in dirs if not d.startswith(".")]

        # Получаем относительный путь
        rel_root = os.path.relpath(root, root_dir)
        if rel_root == ".":
            rel_root = ""

        # Добавляем файлы
        parquet_files = [f for f in files if f.endswith(".parquet")]
        file_items = [
            {
                "label": f,
                "value": os.path.abspath(os.path.join(root, f))  # ← абсолютный путь
            }
            for f in parquet_files
        ]

        # Вложенные папки
        if rel_root == "":
            tree.extend(file_items)
        else:
            # Найти родительскую ветку
            parent = tree
            parts = rel_root.split(os.sep)
            for part in parts:
                match = next((item for item in parent if item["label"] == part), None)
                if not match:
                    match = {"label": part, "children": []}
                    parent.append(match)
                parent = match.setdefault("children", [])
            parent.extend(file_items)

    return tree


# client/utils/components/file_tree_comp.py

def extract_label_to_path(items):
    label_to_path = {}

    def walk(subitems):
        for item in subitems:
            if "children" in item:
                walk(item["children"])
            elif "label" in item and "value" in item:
                label_to_path[item["label"]] = item["value"]

    walk(items)
    return label_to_path

