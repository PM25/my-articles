from code import update_index, update_list, update_meta

print("=[Update Index]=")
new_files, modified_files = update_index.update_all(article_folder="articles")

if len(new_files) + len(modified_files) > 0:
    print("\n=[Update List]=")
    update_list.update_all()

    print("\n=[Update Meta]=")
    update_meta.update_all()
