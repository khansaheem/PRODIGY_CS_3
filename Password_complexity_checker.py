import re
import math
import requests
import hashlib
import getpass  

print("\n\n╔═════════════════════════════════════════════════════════════════╗")
print("║        🚀 PASSWORD COMPLEXITY CHECKER BY SAHEEM 🚀              ║")
print("╠═════════════════════════════════════════════════════════════════╣")
print("║       Let's evaluate your password strength like a pro! 💻      ║")
print("╚═════════════════════════════════════════════════════════════════╝\n")



def calculate_entropy(password):
    charset_size = len(set(password))  
    entropy = len(password) * math.log2(charset_size)
    return entropy

def common_patterns(password):
    sequential = "abcdefghijklmnopqrstuvwxyz"
    if any(seq in password.lower() for seq in sequential):
        return "Avoid sequential letters"
    return ""

def check_common_passwords(password):
    with open("D:\prodigy infotech\common_password.txt.txt", "r") as file:
        common_passwords = file.read().splitlines()
    if password in common_passwords:
        return "This password is too common"
    return ""

def check_leaked_passwords(password):
    hashed_password = hashlib.sha1(password.encode()).hexdigest().upper()
    response = requests.get(f"https://api.pwnedpasswords.com/range/{hashed_password[:5]}")
    return "Password found in data breach!" if hashed_password[5:] in response.text else ""


def check_password_strength(password):
    strength = 0
    feedback = []

    
    if len(password) >= 8:
        strength += 1
    else:
        feedback.append("Password is too short")

    if re.search("[A-Z]", password): strength += 1
    if re.search("[a-z]", password): strength += 1
    if re.search("[0-9]", password): strength += 1
    if re.search("[@#$%^&*!]", password): strength += 1
    
    entropy = calculate_entropy(password)
    if entropy < 40:
        feedback.append(f"Low entropy: {entropy} bits")

    pattern_feedback = common_patterns(password)
    if pattern_feedback:
        feedback.append(pattern_feedback)
  
    common_feedback = check_common_passwords(password)
    if common_feedback:
        feedback.append(common_feedback)

    leaked_feedback = check_leaked_passwords(password)
    if leaked_feedback:
        feedback.append(leaked_feedback)

    return {"strength": strength, "feedback": feedback}

password = getpass.getpass("Enter password: ")  
result = check_password_strength(password)

print(f"Password strength: {result['strength']}/5")
print("Feedback: ", result['feedback'])
