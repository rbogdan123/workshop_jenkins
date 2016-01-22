#! /usr/local/bin/python3.4
import random

chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'

def get_string():
	return ''.join(random.choice(chars) for x in range(50))

if __name__ == "__main__":
    print(get_string())
