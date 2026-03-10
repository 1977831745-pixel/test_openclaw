#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
模拟 ATM 机
支持查询余额、存款、取款、退出等功能
"""

import json
import os

# 数据存储文件
DATA_FILE = "atm_data.json"

# 初始化数据
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

# 加载数据
def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# 保存数据
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# 注册用户
def register(username, password, initial_balance=0):
    data = load_data()
    if username in data:
        return False, "用户名已存在"
    data[username] = {
        "password": password,
        "balance": initial_balance
    }
    save_data(data)
    return True, "注册成功"

# 登录验证
def login(username, password):
    data = load_data()
    if username not in data:
        return False, "用户不存在"
    if data[username]["password"] != password:
        return False, "密码错误"
    return True, "登录成功"

# 查询余额
def check_balance(username):
    data = load_data()
    return data[username]["balance"]

# 存款
def deposit(username, amount):
    if amount <= 0:
        return False, "存款金额必须大于0"
    data = load_data()
    data[username]["balance"] += amount
    save_data(data)
    return True, f"存款成功，当前余额: {data[username]['balance']}"

# 取款
def withdraw(username, amount):
    if amount <= 0:
        return False, "取款金额必须大于0"
    data = load_data()
    if data[username]["balance"] < amount:
        return False, "余额不足"
    data[username]["balance"] -= amount
    save_data(data)
    return True, f"取款成功，当前余额: {data[username]['balance']}"

# 主菜单
def main_menu(username):
    while True:
        print("\n" + "="*30)
        print(f"欢迎, {username}!")
        print("1. 查询余额")
        print("2. 存款")
        print("3. 取款")
        print("4. 退出")
        print("="*30)

        choice = input("请选择操作 (1-4): ")

        if choice == "1":
            balance = check_balance(username)
            print(f"\n当前余额: {balance}")

        elif choice == "2":
            try:
                amount = float(input("请输入存款金额: "))
                success, message = deposit(username, amount)
                print(f"\n{message}")
            except ValueError:
                print("\n无效的金额!")

        elif choice == "3":
            try:
                amount = float(input("请输入取款金额: "))
                success, message = withdraw(username, amount)
                print(f"\n{message}")
            except ValueError:
                print("\n无效的金额!")

        elif choice == "4":
            print("\n谢谢使用，再见!")
            break

        else:
            print("\n无效的选择，请重新输入!")

# 主程序
def main():
    print("\n" + "="*30)
    print("      模拟 ATM 机")
    print("="*30)

    # 注册/登录选择
    while True:
        print("\n1. 注册")
        print("2. 登录")
        print("3. 退出")

        choice = input("请选择 (1-3): ")

        if choice == "1":
            username = input("请输入用户名: ")
            password = input("请输入密码: ")
            try:
                initial_balance = float(input("请输入初始存款金额 (默认0): ") or "0")
            except ValueError:
                initial_balance = 0

            success, message = register(username, password, initial_balance)
            print(f"\n{message}")

            if success:
                main_menu(username)

        elif choice == "2":
            username = input("请输入用户名: ")
            password = input("请输入密码: ")

            success, message = login(username, password)
            print(f"\n{message}")

            if success:
                main_menu(username)

        elif choice == "3":
            print("\n再见!")
            break

        else:
            print("\n无效的选择!")

if __name__ == "__main__":
    main()