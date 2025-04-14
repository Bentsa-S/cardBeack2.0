def calculate_seka_score(cards):
    """Обчислює бали для гри Сека з урахуванням Шанти (7-Hearts)."""
    
    values = [card.split('-')[0] for card in cards]
    suits = [card.split('-')[1] for card in cards]
    
    has_shanta = '7' in values and 'Hearts' in suits  # Перевірка на Шанту

    # Якщо є Шанта, перебираємо всі можливі варіанти
    if has_shanta:
        best_score = 0
        for new_value, new_suit in get_shanta_replacements(values, suits):
            new_values = [new_value if val == '7' and suit == 'Hearts' else val for val, suit in zip(values, suits)]
            new_suits = [new_suit if val == '7' and suit == 'Hearts' else suit for val, suit in zip(values, suits)]
            score = calculate_seka_score_base(new_values, new_suits)
            best_score = max(best_score, score)

        return best_score

    return calculate_seka_score_base(values, suits)


def get_shanta_replacements(values, suits):
    """Генерує найкращі варіанти для заміни Шанти."""
    possible_replacements = []

    suit_counts = {suit: suits.count(suit) for suit in set(suits)}

    # Якщо є дві однакові масті — робимо Шанту третьою
    for suit, count in suit_counts.items():
        if count == 2:
            possible_replacements.append(('A', suit))  # Туз такої ж масті
            possible_replacements.append(('K', suit))  # Король такої ж масті

    # Якщо є хоча б одна карта будь-якої масті — ставимо туза такої ж масті
    for suit in set(suits):
        possible_replacements.append(('A', suit))

    # Додаємо стандартні варіанти (найвищі можливі карти)
    possible_values = ['A', 'K', 'Q', 'J'] + [str(i) for i in range(10, 1, -1)]
    for value in possible_values:
        possible_replacements.append((value, 'Hearts'))  # Як запасний варіант

    return possible_replacements


def calculate_seka_score_base(values, suits):
    """Обчислення балів без Шанти."""

    unique_suits = len(set(suits))
    has_ace = 'A' in values
    ace_count = values.count('A')

    # Три однакові карти (Трійка)
    if len(set(values)) == 1:
        return 40 + int(values[0]) if values[0].isdigit() else 41 + "JQKA".index(values[0])

    if ace_count == 2:
        return 22  # Два тузи

    if unique_suits == 3:
        return 11 if has_ace else 10  # Усі масті різні

    if unique_suits == 2:
        return 21 if has_ace else 20  # Дві однакові масті

    if unique_suits == 1:
        return 31 if has_ace else 30  # Три однакові масті

    return 0  # Не повинно трапитися
