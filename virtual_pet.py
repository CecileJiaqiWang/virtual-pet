import threading
import random

happiness = random.randint(0, 100)
hungry = random.randint(0, 100)
health = random.randint(0, 100)
delta_dict = {"walk": [0, 3, 1],
              "play": [1, 3, 0],
              "feed": [0, -3, 0],
              "seedoctor": [0, 0, 4]}
status_list = ["letalone"]


def boundary():
    global happiness, hungry, health
    happiness = max(0, happiness)
    happiness = min(100, happiness)
    hungry = max(0, hungry)
    hungry = min(100, hungry)
    health = max(0, health)
    health = min(100, health)
    return


def fun_timer():
    global timer, hours, status_list
    global happiness, hungry, health

    command = status_list[0]

    # Too hungry or too full
    if hungry > 80 or hungry < 20:
        health -= 2
        # Boundary check
        boundary()

    # Too sad
    if happiness < 20:
        health -= 1
        # Boundary check
        boundary()

    if status_list[0] == "letalone":
        # Awake
        if hours >= 8:
            hungry += 2
            happiness -= 1
        # Sleeping
        else:
            hungry += 1
        # Boundary check
        boundary()
    else:
        happiness += delta_dict[command][0]
        hungry += delta_dict[command][1]
        health += delta_dict[command][2]
        # Boundary check
        boundary()

    hours += 1

    if hours > 23:
        hours = 0
        # Go to sleep
        status_list[0] = "letalone"

    # Recursive call
    timer = threading.Timer(5.0, fun_timer)
    timer.start()


def main():
    global hours
    global happiness, hungry, health
    global delta_dict
    global status_list
    command_lst = ["walk", "play", "feed", "seedoctor",
                   "letalone", "status", "bye"]

    try:
        file = open("profile.txt", "r")
    except IOError:
        file = open("profile.txt", "w+")

    init_status = file.readline().split(" ")
    # Initial play
    if len(init_status) < 4:
        hours = random.randint(0, 23)
    # Otherwise
    else:
        happiness = int(init_status[0])
        hungry = int(init_status[1])
        health = int(init_status[2])
        hours = int(init_status[3])
    if hours >= 8:
        print("Now is %-2d" % hours)
        print("I'm awake, but bored......")
        print("Happiness: ", happiness)
        print("Hungry: ", hungry)
        print("Health: ", health)
    else:
        print("Now is %-2d" % hours)
        print("I'm sleeping......")
        print("Happiness: ", happiness)
        print("Hungry: ", hungry)
        print("Health: ", health)
    file.close()
    fun_timer()
    while True:
        command = input("Command:")
        if command == "bye":
            print("Bye.....")
            timer.cancel()
            file = open("profile.txt", "w")
            file.write(str(happiness) + " " + str(hungry) + " "
                       + str(health) + " " + str(hours))
            file.close()
            break
        elif command == "status":
            print("Now is %-2d" % hours)
            if status_list[0] == "letalone":
                if hours >= 8:
                    print("I'm awake, but bored......")
                else:
                    print("I'm sleeping......")
            else:
                print(str(status_list[0]) + "......")
            print("Happiness: ", happiness)
            print("Hungry: ", hungry)
            print("Health: ", health)
        elif command == "letalone":
            status_list[0] = "letalone"
            if hours >= 8:
                print("I'm awake, but bored......")
            else:
                print("I'm sleeping......")
        elif command in command_lst:
            status_list[0] = str(command)
            # Sleeping
            if hours < 8:
                decision = input("I'm sleeping. Are you sure that you wanna wake me up?\n"
                                 "(y stands for yes / everything else stands for no)")
                if decision == "y":
                    # Penalty
                    happiness -= 4
                    # Boundary check
                    boundary()
                    print(str(command) + "......")
        else:
            print("I don't understand what you are saying......")

main()