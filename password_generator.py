import string
import secrets
import hashlib

def generate_password(length=12, use_uppercase=True, use_digits=True, use_special=True):

    characters = string.ascii_lowercase
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_special:
        characters += string.punctuation

    if not characters:
        raise ValueError("Трябва да изберете поне един тип символи за паролата.")

    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def check_password_strength(password):

    length = len(password)
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)

    score = 0
    if length >= 8:
        score += 1
    if length >= 12:
        score += 1
    if has_lower:
        score += 1
    if has_upper:
        score += 1
    if has_digit:
        score += 1
    if has_special:
        score += 1

    if score <= 2:
        return "Слаба"
    elif score <= 4:
        return "Средна"
    else:
        return "Силна"

def hash_password(password):

    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    return sha256.hexdigest()

def save_password(site, password, password_hash, filename="passwords.txt"):

    with open(filename, mode='a', encoding='utf-8') as file:
        file.write(f"Сайт: {site} *** Парола: {password} *** Хеш: {password_hash}\n")

def main():
    print("### Генератор на сигурни пароли ###")
    
    try:
        length = int(input("Въведете дължина на паролата (минимум 8): "))
        if length < 8:
            print("Дължината трябва да е поне 8 символа.")
            return
    except ValueError:
        print("Моля, въведете валидно число за дължината.")
        return

    use_uppercase = input("Включва главни букви? (y/n): ").strip().lower() == 'y'
    use_digits = input("Включва цифри? (y/n): ").strip().lower() == 'y'
    use_special = input("Включва специални символи? (y/n): ").strip().lower() == 'y'

    try:
        password = generate_password(length, use_uppercase, use_digits, use_special)
        strength = check_password_strength(password)
        password_hash = hash_password(password)
        print(f"\nГенерирана парола: {password}")
        print(f"Сила на паролата: {strength}")
        print(f"Хеш на паролата: {password_hash}\n")

        site = input("Въведете името на сайта за който е паролата: ").strip()
        if site:
            save = input("Искате ли да запазите паролата и хеша във файл? (y/n): ").strip().lower()
            if save == 'y':
                save_password(site, password, password_hash)
                print(f"Паролата за {site} е запазена във файла 'passwords.txt'.")
        else:
            print("Името на сайта не е въведено. Паролата не е запазена.")
    except ValueError as ve:
        print(f"Грешка: {ve}")

main()