with open('word5.txt', 'w', encoding='utf-8') as output:
    with open('russian_nouns_with_definition.txt', encoding='utf-8') as file:
        for line in file:
            word = line.split(':', maxsplit=1)[0]
            if len(word.encode('utf-16-le')) // 2 != 5:
                continue
            if sorted(set(word)) != sorted(list(word)):
                continue
            print(line, file=output, end='')
