print("=========== Activity 1 ============")
print("=======================")
print("Welcome here")
print("My first post!")
print("=======================")

username = "cool_creator"
bio = "Fun Blogger"
followers = 100

print("=========== Activity 2 ============")

print("Username: ", username)
print("Bio: ", bio)
print("Followers: ", followers)

print("=========== Activity 3 ============")
followers = 100
followers +=50

print("Day 1: ", followers)

followers +=20
print("Day 2: ", followers)

followers -=10
print("Day 3: ", followers)

print("=========== Activity 4 ============")
username = input("Enter Username: ")
ageString = input("Enter Age: ")

try:
    age = int(ageString)
except ValueError:
    print("The age you entered is not an integer!")
    exit()

hobby = input("Enter Hobby: ")

print("=========== Activity 5 ============")
print("\nInstagram Profile")
print("===================")
print("Username: ", username)
print("Age: ", age)
print("Hobby: ", hobby)

if age >= 23 and hobby == "Sleeping":
    print("You are boring")