import time

class Players:

    possible_roles = ['mage', 'demon', 'healer']
    possible_titles = ["Mage Elder", "Demon King", "Healing Wizard"]
    all_weapons = []
    all_chars = []
    all_monsters = []

    def __init__(self, name, role, intro_char=False):
        self.name = name
        self.role = role
        if self.role not in Players.possible_roles:
            print(f"\033[31mFailed! - {self.role} Role Not Possible\033[0m")
        else:
            if not intro_char:
                print(f"\033[32mSuccess! - {self.name} w/ role {self.role} created!\033[0m")
        #Not User Defined
        self.rank = 0
        self.gold = 0
        self.dark_gold = 0
        self.xp = 0
        self.title = "Noob"
        self.xp_list = [100, 200, 400, 700, 1000, 1200, 1500, 2000]
        self.inventory = []
        self.inv_max = 5
        self.hp = 100
        self.monster_slots = []
        Players.all_chars.append(self)
        if self.role == 'healer':
            self.healing = 10
    
    def __repr__(self): # very messy ik :(
        return f"\033[34mName: \033[31m{self.name}\033[0m \033[34mRole:\033[31m \033[31m{self.role}\033[0m \033[34mRank:\033[31m \033[31m{self.rank}\033[0m \033[34mGold:\033[31m \033[31m{self.gold}\033[0m \033[34mDark Gold:\033[31m \033[31m{self.dark_gold}\033[0m\033[0m \033[34mTitle: \033[31m{self.title}\033[0m"

    def rank_change(self, amt):
        self.rank += amt
        return f"\033[32mRank Now: {self.rank}\033[0m"
    
    def level_up(self, xp):
        self.xp += xp
        if not self.xp_list:
            return f"Max Rank: {self.rank} -> XP: {self.xp}"
        while self.xp >= self.xp_list[0]: 
            self.rank += 1
            self.hp += (self.rank * 10)
            if self.role == 'healer':
                self.healing += (self.rank * 10)
            #print("Rank up!", self.rank) # <---- REMOVE COMMENT AFTER
            del self.xp_list[0]
            if not self.xp_list:
                if self.title == 'Noob':
                    self.title = Players.possible_titles[Players.possible_roles.index(self.role)]
                    #print(f"Title Upgraded: {self.title}") # <---- REMOVE COMMENT AFTER
                return f"Max Rank: {self.rank} -> XP: {self.xp}"
        if self.rank >= 5:
            self.title = Players.possible_titles[Players.possible_roles.index(self.role)]
            #print(f"Title Upgraded: {self.title}") # <---- REMOVE COMMENT AFTER
        return f"{xp} XP added! - Total XP: {self.xp} Rank: {self.rank}"
    
    def add_inventory(self, item):
        if item not in Players.all_weapons:
            return f"That item does not exist!"
        elif len(self.inventory) < self.inv_max:
            self.inventory.append(item)
            return f"\033[32mSuccess! - {item.name} added to {self.name}'s inventory!\033[0m"
        else:
            return f"Inventory Full!"
    
    def attack_player(self, enemy, att_type):
        if att_type == 0: # monster
            if len(Players.all_monsters) < 1:
                return f"No Monsters Created"
            elif len(self.monster_slots) < 1:
                return f"No Monster In Monster Slots!"
            else:
                counter2 = 0
                for monster in self.monster_slots:
                    counter2 += 1
                    print(f"{counter2} - {monster.name}")
                monster_picked = int(input("Pick a Monster: "))
                while monster_picked <= 0 or monster_picked > counter2 or type(monster_picked) != int:
                    print(f"Incorrect Choice")
                    monster_picked = int(input("Pick a Monster: "))
                final_monster = self.monster_slots[monster_picked - 1]
                print(f"\033[0;35m{final_monster.name} Chosen!\033[00m")
                
                enemy.hp -= final_monster.dmg
            if enemy.hp <= 0:
                Players.all_chars.remove(enemy)
                if len(Players.all_chars) == 1:
                    self.gold += 1000
                    Players.level_up(self, 500)
                    return f"{enemy.name} is dead and YOURE THE LAST ONE LEFT!"
                self.gold += 100
                print(f"100 Gold Gained - Total Gold: {self.gold}")
                Players.level_up(self, 50)
                return f"{enemy.name} is dead"
            else:
                self.gold += (0.8 * final_monster.dmg)
                return f"{enemy.name} \033[31mHP: {enemy.hp}\033[0m - You did \033[0;31m\033[0;4m{final_monster.dmg} DMG\033[00m\033[00m"
        elif att_type == 1: # weapon
            if len(self.inventory) < 1:
                return f"Sorry! - You have no weapons!"
            else: # picks a weapon from inventory
                choice_num = 1
                chosen_weapon = None
                print("Possible Weapons:")
                for i in self.inventory:
                    print(f"{choice_num} - {i.name}")
                    choice_num += 1
                choice = int(input(f"What Weapon Would You Like To Use? [Enter Num]: "))
                while (choice <= 0 or choice > len(self.inventory)) or choice not in [x for x in range(1, 11)]:
                    print("Failed! - Choose a number from list above")
                    choice = int(input(f"What Weapon Would You Like To Use? [Enter Num]: "))
                chosen_weapon = self.inventory[choice - 1]
                print(f"\033[0;35m{chosen_weapon.name} Chosen!\033[00m")
            

            enemy.hp -= chosen_weapon.dmg
            if enemy.hp <= 0:
                Players.all_chars.remove(enemy)
                if len(Players.all_chars) == 1:
                    self.gold += 1000
                    Players.level_up(self, 500)
                    return f"{enemy.name} is dead and YOU WON!!!"
                self.gold += 100
                print(f"100 Gold Gained - Total Gold: {self.gold}")
                Players.level_up(self, 50)
                return f"{enemy.name} is dead"
            else:
                self.gold += (0.8 * chosen_weapon.dmg)
                return f"{enemy.name} \033[31mHP: {enemy.hp}\033[0m - You did \033[0;31m\033[0;4m{chosen_weapon.dmg} DMG\033[00m\033[00m"
        else:
            return f"Incorrect Attack Type -> (0 or 1)"  




class Weapons:

    possible_w_types = ["bleed", "freeze", "burn", "slice", "blunt"]

    def __init__(self, name, dmg, strength, w_type, shop_weapon=False, intro_items=False):
        self.name = name
        self.dmg = dmg
        self.strength = strength
        self.w_type = w_type
        if self.w_type not in Weapons.possible_w_types:
            print(f"\033[31mFailed! - {self.w_type} Weapon Type Not Possible\033[0m")
        else:
            if not intro_items:
                print(f"\033[32mSuccess! - {self.name} created!\033[0m")
        if not shop_weapon:
            Players.all_weapons.append(self)
        
    
    def __repr__(self):
        return f"{self.w_type} Weapon - {self.name} with {self.dmg} Damage and {self.strength} Strength"


# class Monsters <-- Monsters (pets) to help Players
class Monsters:

    possible_breeds = ["phoenix", "griffin", "dementor", "cerberus"]

    def __init__(self, name, breed, dmg, shop_item=False):
        self.name = name
        self.dmg = dmg
        self.breed = breed
        if self.breed not in Monsters.possible_breeds:
            print(f"{self.breed} is not a possible breed - has to be one of these:")
            for i in Monsters.possible_breeds:
                print("-", i)
        else:
            print(f"Successful! - {self.name} ({self.breed}) Created!")
        if not shop_item:
            Players.all_monsters.append(self)


# "\033[0;31mOK this is red\033[00m"


p1 = Players("Miran", "mage", intro_char=True)
p2 = Players("Ayaan", "demon", intro_char=True)
p3 = Players("Secret_Character", "healer", intro_char=True)

w1 = Weapons("Blood Blade", 120, 12, "bleed", intro_items=True)
w2 = Weapons("Wooden Sword", 20, 2, "blunt", intro_items=True)


# Game Loop

logo = '''
███████╗ ██████╗ ██████╗ ████████╗██╗   ██╗███╗   ██╗███████╗
██╔════╝██╔═══██╗██╔══██╗╚══██╔══╝██║   ██║████╗  ██║██╔════╝
█████╗  ██║   ██║██████╔╝   ██║   ██║   ██║██╔██╗ ██║█████╗  
██╔══╝  ██║   ██║██╔══██╗   ██║   ██║   ██║██║╚██╗██║██╔══╝  
██║     ╚██████╔╝██║  ██║   ██║   ╚██████╔╝██║ ╚████║███████╗
╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═══╝╚══════╝                                              
'''

print('##############################################################')
print(logo)
print('##############################################################')


while True:
    time.sleep(0.5)
    print('''
    1 - Make A Character
    2 - Make A Weapon
    3 - Attack A Player
    4 - Add Item To Inventory
    5 - Check Bank
    6 - Check Stats
    7 - Check Inventory
    8 - Make A Monster
    9 - Add Monster To Slot
    10 - Check Monster Slots
    11 - Heal A Player
    12 - Shop
    q - Exit
    ''')
    option = input("Enter an Option: ")
    if option == 'q' or option == 'Q':
        print("Exit!")
        break
    
    if option == '1': # make a character -> add help tips like char roles
        char_name = input("Enter Name: ")
        char_role = input("Enter Role: ")
        char_name = Players(char_name, char_role)
    
    if option == '2': # make a weapon -> add help tips like w types
        w_name = input("Enter Weapon Name: ")
        w_dmg = int(input("Enter Weapon Damage: "))
        w_strength = int(input("Enter Weapon Strength: "))
        w_type = input("Enter Weapon Type: ")
        final_weapon = Weapons(w_name, w_dmg, w_strength, w_type)
    
    if option == '3': # attack player
        
        if len(Players.all_chars) < 2: # Section lets you pick your char
            print("There needs to be at least 2 players to Attack!")
            break
        counter = 0
        for char in Players.all_chars:
            counter += 1
            print(f"{counter} - {char.name}")
        p1 = int(input("Who Are You:"))
        while p1 <= 0 or p1 > counter or type(p1) != int:
            print("Incorrect Choice!")
            p1 = int(input("Who Are You:"))
        

        counter2 = 0
        chars2 = [i for i in Players.all_chars if i != Players.all_chars[p1-1]]
        for char in chars2:
            counter2 += 1
            print(f"{counter2} - {char.name}")
        p2 = int(input("Who Do You Want To Attack:"))
        while p2 <= 0 or p2 > counter2 or type(p2) != int:
            print("Incorrect Choice!")
            p2 = int(input("Who Do You Want To Attack:"))

        attack_type = int(input("Type 0 to attack with Monster, 1 for Weapon: "))
        while attack_type not in [0, 1]:
            print(f"Incorrect Type")
            attack_type = int(input("Type 0 to attack with Monster, 1 for Weapon: "))

        print(Players.attack_player(Players.all_chars[p1-1], chars2[p2-1], attack_type))
        

    if option == '4': # add to inventory
        
        if len(Players.all_chars) < 1: # Section lets you pick your char
            print("There needs to be at least 1 player")
            break
        counter = 0
        for char in Players.all_chars:
            counter += 1
            print(f"{counter} - {char.name}")
        p1 = int(input("Who Are You:"))
        while p1 <= 0 or p1 > counter or type(p1) != int:
            print("Incorrect Choice!")
            p1 = int(input("Who Are You:"))
        you = Players.all_chars[p1-1]

        if len(you.inventory) == you.inv_max:
            print(f"Inventory Full!")
        else:
            if len(Players.all_weapons) < 1: # Section lets you pick your weapon
                print("There needs to be at least 1 item")
                break
            counter2 = 0
            for weapon in Players.all_weapons:
                counter2 += 1
                print(f"{counter2} - {weapon.name}")
            weapon1 = int(input("Pick A Weapon:"))
            while weapon1 <= 0 or weapon1 > counter2 or type(weapon1) != int:
                print("Incorrect Choice!")
                weapon1 = int(input("Pick A Weapon:"))
            weapon_chosen = Players.all_weapons[weapon1-1]

            print(Players.add_inventory(you, weapon_chosen))
    
    if option == '5':
        if len(Players.all_chars) < 1: # Section lets you pick your char
            print("There needs to be at least 1 player")
            break
        counter = 0
        for char in Players.all_chars:
            counter += 1
            print(f"{counter} - {char.name}")
        p1 = int(input("Who Are You:"))
        while p1 <= 0 or p1 > counter or type(p1) != int:
            print("Incorrect Choice!")
            p1 = int(input("Who Are You:"))
        you = Players.all_chars[p1-1]

        print(f"Gold: {you.gold}, Dark Gold: {you.dark_gold}")
    
    if option == '6':
        if len(Players.all_chars) < 1: # Section lets you pick your char
            print("There needs to be at least 1 player")
            break
        counter = 0
        for char in Players.all_chars:
            counter += 1
            print(f"{counter} - {char.name}")
        p1 = int(input("Who Are You:"))
        while p1 <= 0 or p1 > counter or type(p1) != int:
            print("Incorrect Choice!")
            p1 = int(input("Who Are You:"))
        you = Players.all_chars[p1-1]

        print(you)
    
    if option == '7':
        if len(Players.all_chars) < 1: # Section lets you pick your char
            print("There needs to be at least 1 player")
            break
        counter = 0
        for char in Players.all_chars:
            counter += 1
            print(f"{counter} - {char.name}")
        print('---------------------')
        p1 = int(input("Who Are You:"))
        while p1 <= 0 or p1 > counter or type(p1) != int:
            print("Incorrect Choice!")
            p1 = int(input("Who Are You:"))
        you = Players.all_chars[p1-1]

        if len(you.inventory) < 1:
            print("Inventory Empty!")
        else:
            counter2 = 0
            for item in you.inventory:
                counter2 += 1
                print(f"{counter2} - {item.name}")
        
    if option == '8':
        m_name = input("Enter Monster Name: ")
        m_breed = input("Enter Monster Breed: ")
        m_dmg = int(input("Enter Monster Damage: "))
        final_monster = Monsters(m_name, m_breed, m_dmg)
    
    if option == '9':
        if len(Players.all_chars) < 1: # Section lets you pick your char
            print("There needs to be at least 1 player")
            break
        counter = 0
        for char in Players.all_chars:
            counter += 1
            print(f"{counter} - {char.name}")
        print('---------------------')
        p1 = int(input("Who Are You:"))
        while p1 <= 0 or p1 > counter or type(p1) != int:
            print("Incorrect Choice!")
            p1 = int(input("Who Are You:"))
        you = Players.all_chars[p1-1]

        if len(Players.all_monsters) < 1:
            print(f"No Monsters Created!")
        else:
            counter2 = 0
            for monster in Players.all_monsters:
                counter2 += 1
                print(f"{counter2} - {monster.name}")
            monster_picked = int(input("Pick a Monster: "))
            while monster_picked <= 0 or monster_picked > counter2 or type(monster_picked) != int:
                print(f"Incorrect Choice")
                monster_picked = int(input("Pick a Monster: "))
            final_monster = Players.all_monsters[monster_picked - 1]
            you.monster_slots.append(final_monster)
            print(f"Successful! - {final_monster.name} added to {you.name}'s inventory!")
    
    if option == '10':
        if len(Players.all_chars) < 1: # Section lets you pick your char
            print("There needs to be at least 1 player")
            break
        counter = 0
        for char in Players.all_chars:
            counter += 1
            print(f"{counter} - {char.name}")
        print('---------------------')
        p1 = int(input("Who Are You:"))
        while p1 <= 0 or p1 > counter or type(p1) != int:
            print("Incorrect Choice!")
            p1 = int(input("Who Are You:"))
        you = Players.all_chars[p1-1]

        if len(you.monster_slots) < 1:
            print(f"Monster Slots Empty")
        else:
            counter2 = 0
            for monster in you.monster_slots:
                counter2 += 1
                print(f"{counter2} - {monster.name}")
    
    if option == '11': # healing
        if len([i for i in Players.all_chars if i.role == 'healer']) < 1:
            print(f"No Healers")
        else:
            counter = 0
            for char in [i for i in Players.all_chars if i.role == 'healer']:
                counter += 1
                print(f"{counter} - {char.name}")
            p1 = int(input("Who Are You:"))
            while p1 <= 0 or p1 > counter or type(p1) != int:
                print("Incorrect Choice!")
                p1 = int(input("Who Are You:"))
            you = [i for i in Players.all_chars if i.role == 'healer'][p1-1]

            counter2 = 0
            for char in Players.all_chars:
                counter2 += 1
                print(f"{counter2} - {char.name}")
            p2 = int(input("Who Do You Want To Heal: "))
            while p2 <= 0 or p2 > counter2 or type(p2) != int:
                print("Incorrect Choice!")
                p2 = int(input("Who Do You Want To Heal: "))
            to_heal = Players.all_chars[p2-1]

            to_heal.hp += you.healing
            print(f"{to_heal.name} + {you.healing} HP -> (healed by {you.name})")


    if option == '12': # shop feature

        counter = 0
        for char in Players.all_chars:
            counter += 1
            print(f"{counter} - {char.name}")
        print('---------------------')
        p1 = int(input("Who Are You:"))
        while p1 <= 0 or p1 > counter or type(p1) != int:
            print("Incorrect Choice!")
            p1 = int(input("Who Are You:"))
        you = Players.all_chars[p1-1]

        shop = '''+----------------------+----------------------+----------------------+
| \033[0;4mWeapons\033[00m              | \033[0;4mItems\033[00m                | \033[0;4mMonsters\033[00m             |
+----------------------+----------------------+----------------------+
| Demon Slayer (200G)  | Health Potion (50G)  | Serpent (500G)       |
+----------------------+----------------------+----------------------+
| Cloud Blade (250G)   | DMG Potion (60G)     | Lion (600G)          |
+----------------------+----------------------+----------------------+
| Venom Scythe (450G)  | Healer Potion (50G)  | Demogorgan (900G)    |
+----------------------+----------------------+----------------------+
| Flame Sickle (100DG) | Shield Potion (100G) | Velociraptor (1200G) |
+----------------------+----------------------+----------------------+'''

        print(shop)
        shop_dict = {1: 'weapons', 2: 'items', 3: 'monsters'}
        shop_items = {'weapons': [(Weapons("Demon Slayer", 200, 150, 'bleed', shop_weapon=True), 200), (Weapons("Cloud Blade", 250, 170, 'burn', shop_weapon=True), 250), (Weapons("Venom Scythe", 400, 300, 'slice', shop_weapon=True), 450), (Weapons("Flame Sickle", 600, 450, 'blunt', shop_weapon=True), 1000)], 'items': [], 'monsters': [(Monsters("Serpent", "griffin", 700), 555)]}
        print('''
        1 - Weapons
        2 - Items
        3 - Monsters
        ''')
        choice = int(input("What Do You Want To Buy?: "))
        while choice not in [1, 2, 3]:
            print("Incorrect Choice!")
            choice = int(input("What Do You Want To Buy?: "))

        shop_category = shop_items[shop_dict[choice]]
        if choice in [1, 2]: # weapons, items
            if len(you.inventory) == you.inv_max:
                print(f"Inventory Full")
            else:
                counter = 0
                for tupl in shop_category:
                    counter += 1
                    print(f"{counter} - {tupl[0].name} -> Price: {tupl[1]} Gold")
                choice2 = int(input("What Do You Want To Buy?: "))
                while choice2 not in [_ for _ in range(1, counter+1)]:
                    print("Incorrect Choice!")
                    choice2 = int(input("What Do You Want To Buy?: "))

                acc_item = shop_category[choice2 - 1][0]
                item_name = shop_category[choice2 - 1][0].name
                item_price = shop_category[choice2 - 1][1]

                if you.gold < item_price:
                    print(f"Sorry - You're Broke! HAHAHAH")
                else:
                    confirm = (input(f"Confirm Purchase Of {item_name} (y/n)"))
                    while confirm not in ['y', 'Y', 'n', 'N']:
                        print("Incorrect Choice!")
                        confirm = (input(f"Confirm Purchase Of {item_name} (y/n)"))
                    if confirm in ['Y', 'y']:
                        you.gold -= item_price
                        you.inventory.append(acc_item)
                        print(f"\033[32m{item_name} Successfully added to {you.name}'s inventory!\033[0m")
                    elif confirm in ['n', 'N']:
                        print(f"Purchase Cancelled!")
        elif choice in [3]: # monsters
            counter = 0
            for tupl in shop_category:
                counter += 1
                print(f"{counter} - {tupl[0].name} -> Price: {tupl[1]} Gold")
            choice2 = int(input("What Do You Want To Buy?: "))
            while choice2 not in [_ for _ in range(1, counter+1)]:
                print("Incorrect Choice!")
                choice2 = int(input("What Do You Want To Buy?: "))
            
            acc_item = shop_category[choice2 - 1][0]
            item_name = shop_category[choice2 - 1][0].name
            item_price = shop_category[choice2 - 1][1]

            if you.gold < item_price:
                print(f"Sorry - You're Broke! HAHAHAH")
            else:
                confirm = (input(f"Confirm Purchase Of {item_name} (y/n)"))
                while confirm not in ['y', 'Y', 'n', 'N']:
                    print("Incorrect Choice!")
                    confirm = (input(f"Confirm Purchase Of {item_name} (y/n)"))
                if confirm in ['Y', 'y']:
                    you.gold -= item_price
                    you.monster_slots.append(acc_item)
                    print(f"\033[32m{item_name} Successfully added to {you.name}'s Monster Slots!\033[0m")
                elif confirm in ['n', 'N']:
                    print(f"Purchase Cancelled!")

                
            





# TODO FEATURES:
    # - Finish Monsters shop and items shop
    # - Add use_item option to allow you to use item from inv
    # - Add color to listing of players (higher rank, better colour)
    # - Add color to listing of weapons (colour based on w type)
    # - Add clans
    # - POTENTIAL (remove weapon from global list if someone adds to inv)