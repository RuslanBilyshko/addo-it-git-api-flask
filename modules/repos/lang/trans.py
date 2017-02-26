# Сдесь почему-то не получилось имортировать конкретную локализацию russian.py
# Вообще хотел динамически подгружать локаль но не получилось :(

def trans(label: str, lang="ru"):
    # imp = 'import %s.returns as l' % (lang)
    # exec(imp)

    t = ""

    if lang == "ru":
        t = ru.get(label)

    if t is not None:
        return t
    else:
        return label


ru = {
    "id": "Идентификатор",
    "url": "Ссылка",
    "name": "Имя",
    "full_name": "Полное имя",
    "html_url": "Ссылка на репозиторий",
    "language": "Язик",
    "default_branch": "Branch по-умочанию"
}
