import random
import time
import os
import math


class Character:
    def __init__(self, name, health, attack, defense, mana):
        self.name = name
        self.mHealth = health
        self.cHealth = health
        self.power = attack
        self.defense = defense
        self.block = False
        self.shield = 2
        self.shieldScaling = 0.5
        self.mMana = mana
        self.cMana = 0
        self.bleedStacks = 0
        self.bleedDamage = 0
        self.wPoison = 0
        self.poisonStacks = 0
        self.healthPotion = {"Name": "Health", "Desc": "Restore a large portion of Health.", "Quant": 1}
        self.manaPotion = {"Name": "Mana", "Desc": "Start next battle with full Mana.", "Quant": 0}
        self.poisonPotion = {"Name": "Poison", "Desc": "Poison weapon for next battle.", "Quant": 0}
        self.pList = [self.healthPotion, self.manaPotion, self.poisonPotion]
    
    def status(self):
        print(f"{self.name}: {self.cHealth}/{self.mHealth} health, {self.cMana}/{self.mMana} mana")
    def isAlive(self):
        if self.cHealth > 0:
            return True
        else:
            print(f"{self.name} is dead!")

    def strike(self, target):
        damage = self.power
        if target.block == True:
            blockedDamage = damage / target.shield
            damage = math.floor(blockedDamage)
        damage -= target.defense
        if damage < 0:
            damage = 0
        target.cHealth -= damage
        print(f"{self.name} deals {damage} damage to {target.name}!")
        if self.wPoison >= 1:
            target.poisonStacks += self.wPoison
            print(f"{target.name} is poisoned!")
        return damage

    def hRegen(self, amount):
        self.cHealth += amount
        self.cHealth = math.ceil(self.cHealth)
        if self.cHealth > self.mHealth:
            self.cHealth = self.mHealth
    
    def mRegen(self, amount):
        self.cMana += amount
        if self.cMana > self.mMana:
            self.cMana = self.mMana
    
    def defend(self):
        self.block = True
        self.mRegen(2)
        print(f"{self.name} defends!")
    
    def bleed(self):
        if self.bleedStacks > 0:
            self.cHealth -= self.bleedDamage
            self.bleedStacks -= 1
            print(f"{self.name} bleeds for {self.bleedDamage} damage!")
            if self.bleedStacks == 0:
                self.bleedDamage = 0
                print(f"{self.name} stops bleeding!")
    
    def poison(self):
        if self.poisonStacks > 0:
            self.cHealth -= self.poisonStacks
            print(f"{self.name} takes {self.poisonStacks} damage from poison!")
            self.poisonStacks -= 1
            if self.poisonStacks == 0:
                print(f"{self.name} is no longer poisoned!")
            

    def turnStart(self):
        alive = self.isAlive()
        if alive == True:    
            self.mRegen(1)
            self.block = False
            self.bleed()
            self.poison()
            self.status()
            return self.isAlive()
        else:
            return(False)
    def battleWon(self):
        if self.cHealth <= 0:
            self.cHealth = 1
        self.bleedStacks = 0
        self.poisonStacks = 0
        self.wPoison = 0
        

#Player Classes:
class Berserker(Character):
    def __init__(self, name, health, attack, defense, mana):
        super().__init__(name, health, attack, defense, mana)
        self.job = "Berserker"
        self.manaCost = 4
        self.level = 1
    def rend(self, target):
        self.cMana -= self.manaCost
        damage = self.strike(target)
        print(f"{self.name} tears into {target.name}!")
        target.bleedStacks += 2
        target.bleedDamage += math.ceil(damage * 0.6)
        print(f"{target.name} is bleeding!")    
    def action(self, target):
        print("What will you do?: ")
        choice = input(f"1: Attack \n2: Block\n3: Rend (Costs {self.manaCost} Mana)\n1-3: ")
        if choice == "1":
            self.strike(target)
        elif choice == "2":
            self.defend()
        elif choice == "3":
            if self.cMana >= self.manaCost:
                self.rend(target)
            else:
                print(f"{self.name} tried, but didn't have the Mana.")
        else:
            print(f"{self.name} couldn't choose, and wasted the turn.")
    def charsheet(self):
        print(f"{self.name}: Level {self.level} Berserker")
        print(f"Health Points: {self.cHealth}/{self.mHealth}")
        print(f"Max Mana: {self.mMana}")
        print(f"Attack Power: {self.power}")
        print(f"Defense: {self.defense}; Shield: Rank {(self.shield-2)/self.shieldScaling}")
        print(f"Special Attack: \n Rend: Causes the target to bleed for two turns.")

class Assassin(Character):
    def __init__(self, name, health, attack, defense, mana):
        super().__init__(name, health, attack, defense, mana)
        self.job = "Assassin"
        self.manaCost = 3
        self.level = 1
    def pDart(self, target):
        self.strike(target)
        target.poisonStacks += (self.cMana - 1)
        self.cMana = 0
        print(f"{target.name} is poisoned!")  
    def action(self, target):
        print("What will you do?: ")
        choice = input(f"1: Attack \n2: Block\n3: Poison Dart (Costs at least {self.manaCost} Mana)\n1-3: ")
        if choice == "1":
            self.strike(target)
        elif choice == "2":
            self.defend()
        elif choice == "3":
            if self.cMana >= self.manaCost:
                self.pDart(target)
            else:
                print(f"{self.name} tried, but didn't have the Mana.")
        else:
            print(f"{self.name} couldn't choose, and wasted the turn.")
    def charsheet(self):
        print(f"{self.name}: Level {self.level} Assaassin")
        print(f"Health Points: {self.cHealth}/{self.mHealth}")
        print(f"Max Mana: {self.mMana}")
        print(f"Attack Power: {self.power}")
        print(f"Defense: {self.defense}; Shield: Rank {(self.shield-2)/self.shieldScaling}")
        print(f"Special Attack: \n Poison Dart: Afflicts the target with poison relative to Mana spent.")

class Paladin(Character):
    def __init__(self, name, health, attack, defense, mana):
        super().__init__(name, health, attack, defense, mana)
        self.job = "Paladin"        
        self.manaCostA = 2
        self.manaCostB = 7
        self.level = 1
    def smite(self, target):
        damage = self.strike(target)
        holyDamage = (self.cMana * 2) + damage
        target.cHealth -= holyDamage
        print(f"Holy light scorches {target.name} for {holyDamage} damage!")
        self.cMana = 0  
    def healPrayer(self):
        misHealth = (self.mHealth - self.cHealth)
        self.hRegen(misHealth*0.8)
        self.cMana -= self.manaCostB
        self.bleedStacks = 0
        self.poisonStacks = 0
        print(f"{self.name}'s wounds close!")
    def action(self, target):
        print("What will you do?: ")
        choice = input(f"1: Attack \n2: Block\n3: Smite (Costs at least {self.manaCostA} Mana)\n4: Heal Prayer (Costs {self.manaCostB} Mana)\n1-3: ")
        if choice == "1":
            self.strike(target)
        elif choice == "2":
            self.defend()
        elif choice == "3":
            if self.cMana >= self.manaCostA:
                self.smite(target)
            else:
                print(f"{self.name} tried, but didn't have the Mana.")
        elif choice == "4":
            if self.cMana >= self.manaCostB:
                self.healPrayer()
            else:
                print(f"{self.name} tried, but didn't have the Mana.")  
        else:
            print(f"{self.name} couldn't choose, and wasted the turn.")
    def charsheet(self):
        print(f"{self.name}: Level {self.level} Paladin")
        print(f"Health Points: {self.cHealth}/{self.mHealth}")
        print(f"Max Mana: {self.mMana}")
        print(f"Attack Power: {self.power}")
        print(f"Defense: {self.defense}; Shield: Rank {(self.shield-2)/self.shieldScaling}")
        print(f"Special Attack: \n Smite: Scorch the target with holy light, piercing defenses.")
        print(f"Spell: \n Heal Prayer: Restores {self.name}'s health, and cures bleed and poison.")       


#Enemy Types:
class Goblin(Character):
    def __init__(self, name, health, attack, defense, mana, aggro):
        super().__init__(name, health, attack, defense, mana)
        self.aggro = aggro
        self.manaCost = 4
    def rend(self, target):
        self.cMana -= self.manaCost
        damage = self.strike(target)
        print(f"{self.name} tears into {target.name}!")
        target.bleedStacks += 2
        target.bleedDamage += math.ceil(damage * 0.5)
        print(f"{target.name} is bleeding!")
    def poisonWeapon(self):
        if self.wPoison == 0:
            self.wPoison += 2
            print(f"{self.name} poisoned their weapon!")
        else:
            self.wPoison += 1
            print(f"{self.name} added more poison to their weapon!")    
    def actionSelect(self):
        self.choice = random.randint(1, self.aggro)
        if self.choice >= 11:
            print(f"{self.name} is fiddling with something...")
        elif self.choice >= 5:
            print(f"{self.name} takes an aggressive stance.")
        elif self.choice >= 2:
            self.defend()
        else:
            print(f"{self.name} looks lost.")         
    def action(self, target):
        if self.choice >= 11:
            self.cMana -= 1
            self.poisonWeapon()
        elif self.choice >= 8:
            if self.cMana >= self.manaCost:
                self.rend(target)
            else:
                print(f"{self.name} tries to rend {target.name}, but doesn't have the Mana.")
        elif self.choice >= 5:
            self.strike(target)

class Snake(Character):
    def __init__(self, name, health, attack, defense, mana, aggro):
        super().__init__(name, health, attack, defense, mana)
        self.aggro = aggro
        self.manaCost = 3
        self.wPoison = 1
    def pBite(self, target):
        self.strike(target)
        if self.cMana >= 6:
            manaPoison = 6
        else:
            manaPoison = (self.cMana) 
        target.poisonStacks += (manaPoison - 2)
        self.cMana -= manaPoison
        print(f"{self.name}'s fangs inject extra poison into {target.name}!")
    def burninate(self, target):
        fireDamage = (self.cMana * 2)
        if target.block == True:
            fireDamage /= target.shield
            fireDamage = math.ceil(fireDamage)
        target.cHealth -= fireDamage
        print(f"{self.name} burninates {target.name} for {fireDamage} damage!")
        self.cMana = 0      
    def actionSelect(self):
        self.choice = random.randint(1, self.aggro)
        if self.choice >= 11:
            print(f"{self.name} is taking a deep breath...")
        elif self.choice >= 6:
            print(f"{self.name} takes an aggressive stance.")
        elif self.choice >= 2:
            self.defend()
        else:
            print(f"{self.name} slithers in circles.")         
    def action(self, target):
        if self.choice >= 11:
            self.burninate(target)
        elif self.choice >= 8:
            if self.cMana >= self.manaCost:
                self.pBite(target)
            else:
                print(f"{self.name} tries to bite {target.name}, but doesn't have the Mana.")
        elif self.choice >= 6:
            self.strike(target)

class Cultist(Character):
    def __init__(self, name, health, attack, defense, mana, aggro):
        super().__init__(name, health, attack, defense, mana)
        self.aggro = aggro
        self.manaCostA = 4
        self.manaCostB = 3
    def profaneSmite(self, target):
        damage = self.strike(target)
        unholyDamage = (self.cMana * 2) + damage
        target.cHealth -= unholyDamage
        print(f"The Void consumes {target.name} for {unholyDamage} damage!")
        self.cMana = 0  
    def bloodDraw(self, target):
        self.cMana -= self.manaCostB
        damage = self.strike(target)
        if target == self:
            print(f"{self.name} makes a blood sacrifice!")
            self.mMana += 2
            self.mRegen(2)
        else:
            print(f"{self.name} opens up {target.name}!")
            self.mMana += 1
            self.mRegen(1)
        target.bleedStacks += 3
        target.bleedDamage += math.ceil(damage * 0.4)
        print(f"{target.name} is bleeding!")      
    def actionSelect(self):
        self.choice = random.randint(1, self.aggro)
        if self.choice >= 11:
            print(f"{self.name} raises a wicked dagger...")
        elif self.choice >= 6:
            print(f"{self.name} takes an aggressive stance.")
        elif self.choice >= 3:
            self.defend()
        else:
            print(f"{self.name} raises a wicked dagger...")         
    def action(self, target):
        if self.choice >= 11:
            if self.cMana >= self.manaCostB:
                self.bloodDraw(target)
            else:
                print(f"{self.name} doesn't have the mana.")
        elif self.choice >= 8:
            if self.cMana >= self.manaCostA:
                self.profaneSmite(target)
            else:
                print(f"{self.name} tries to smite {target.name}, but doesn't have the Mana.")
        elif self.choice >= 6:
            self.strike(target)
        elif self.choice < 3:
            if self.cHealth <= self.power:
                print(f"Gasping, {self.name} stays their hand.")
            elif self.cMana >= self.manaCostB:
                self.bloodDraw(self)
            else:
                print(f"{self.name} doesn't have the mana.")
        
        
#Inventory
def showInv(player):
    print("Potion Types:")
    for item in player.pList:
        print(f"{item["Name"]}: {item["Quant"]} owned.")
        print(f"-{item["Desc"]}")

def useItem(player):
    showInv(player)
    choice = str.capitalize(input("Which potion do you want to use? Type the name of the potion, or hit enter to skip: "))
    for item in player.pList:
        if choice == item["Name"]:
            if item["Quant"] > 0:
                item["Quant"] -= 1
                if choice == "Health":
                    player.hRegen(player.mHealth/2)
                    print(f"{player.name} regained Health!")
                if choice == "Mana":
                    player.mRegen(player.mMana)
                    print(f"{player.name}'s Mana was maxed out!")
                if choice == "Poison":
                    if player.wPoison == 0:
                        player.wPoison += 2
                        print(f"{player.name} poisoned their weapon!")
                    else:
                        player.wPoison += 1
                        print(f"{player.name} added more poison to their weapon.")
            else:
                print(f"{player.name} doesn't have any of those.")


def Loot(player):
    loot = random.randint(1, 10)
    if loot >= 6:
        potion = random.choice(player.pList)
        potion["Quant"] += 1
        print(f"{player.name} found a {potion["Name"]} Potion!")
    elif loot >= 5:
        player.defense += 1
        print(f"{player.name} found an armor upgrade! Defense +1!")
    elif loot >= 3:
        player.shield += player.shieldScaling
        print(f"{player.name} found a shield upgrade! Shield Rank +1!")
    else:
        player.mMana += 1
        print(f"{player.name} found a Mana enchantment! Max Mana +1!")

#Leveling

def LevelUp(player):
    player.level += 1
    print(f"{player.name} reached level {player.level}")
    valid = 0
    while valid == 0:
        valid = 1
        choice = input("What do you want to upgrade?\n 1: +5 Health\n 2: +1 Attack Power\n 3: +1 Mana\n 1-3: ")
        if choice == "1":
            player.mHealth += 5
            player.cHealth += 5
            print("Health upgraded.")
        elif choice == "2":
            player.power += 1
            print("Power upgraded.")
        elif choice == "3":
            player.mMana += 1
            print("Mana upgraded.")
        else:
            valid = 0
            print("Please type 1, 2, or 3 to select one of the given options.")
    

#Combat

def spawnEnemy(tier, difficulty, group):
    if group == 1:
        names = ["Goblin", "Bob Goblin", "Gobert the Terrible"]
        name = names[tier]
        healths = [30, 50, 70, 90]
        if difficulty < 20:
            health = healths[tier]
        else:
            health = healths[tier + 1]
        pows = [6, 7, 8]
        power = pows[tier]
        defs = [2, 3, 4]
        defense = defs[tier]
        manas = [4, 7, 9]
        mana = manas[tier]
        aggros = [8, 10, 12]
        aggro = aggros[tier]
        enemy = Goblin(name, health, power, defense, mana, aggro)
    elif group == 2:
        names = ["Snake", "Weird Snake Joe", "Trogdor the Burninator"]
        name = names[tier]
        healths = [20, 40, 60, 80]
        if difficulty < 20:
            health = healths[tier]
        else:
            health = healths[tier + 1]
        pows = [3, 4, 5]
        power = pows[tier]
        defs = [0, 1, 2]
        defense = defs[tier]
        manas = [7, 11, 15]
        mana = manas[tier]
        aggros = [8, 10, 12]
        aggro = aggros[tier]
        enemy = Snake(name, health, power, defense, mana, aggro)
    elif group == 3:
        names = ["Cultist", "Cultist Cain", "Jim the Voidpriest"]
        name = names[tier]
        healths = [40, 60, 80, 100]
        if difficulty < 20:
            health = healths[tier]
        else:
            health = healths[tier + 1]
        pows = [5, 6, 7]
        power = pows[tier]
        defs = [1, 2, 3]
        defense = defs[tier]
        manas = [4, 6, 8]
        mana = manas[tier]
        aggros = [8, 10, 12]
        aggro = aggros[tier]
        enemy = Cultist(name, health, power, defense, mana, aggro)
    if difficulty >= 30:
       pScaling = (difficulty - 27) / 3
       enemy.power += math.ceil(pScaling)
    if difficulty >= 30:
        hScaling = ((difficulty - 28) * 0.1) + 1
        enemy.mHealth = math.ceil(enemy.mHealth * hScaling)
        enemy.cHealth = math.ceil(enemy.cHealth * hScaling)
    return enemy
    


def combat(player, tier, difficulty, group):
    #Combat Initiation:
    enemy = spawnEnemy(tier, difficulty, group)
    print(f"{player.name} is attacked by {enemy.name}!")
    time.sleep(1)
    #Combat Loop:
    battleEnd = 0
    while battleEnd == 0:
        eAlive = enemy.turnStart()
        if eAlive == True:
            enemy.actionSelect()
            time.sleep(2)
            pAlive = player.turnStart()
            if pAlive == True:
                player.action(enemy)
                time.sleep(1)
                enemy.action(player)
            else: battleEnd = 2
        else: 
            battleEnd = 1
    time.sleep(2)
    if battleEnd == 1: 
        print("Victory!")
        time.sleep(2)
        player.battleWon()
        for count in range(tier+1):
            Loot(player)
        for count in range(tier+1):
            LevelUp(player)
        player.cMana = 0
        return(0)
    if battleEnd == 2:
        print("Game Over!")
        return(1)
        
#Save and Load
def saveGame(player):
    with open(os.path.expanduser("~/Desktop/IansDungeonPlayerData.txt"), "w") as x:
        x.write(f"{player.name};{player.job};{player.mHealth};{player.cHealth};{player.power};{player.defense};{player.shield};{player.mMana};{player.cMana};{player.pList[0]["Quant"]};{player.pList[1]["Quant"]};{player.pList[2]["Quant"]};{player.level}")
def loadGame(player):
    with open(os.path.expanduser("~/Desktop/IansDungeonPlayerData.txt"), "r") as x:
        for line in x:
            stats = line.split(";")
            if stats[1] == "Berserker":
                player = Berserker(stats[0],int(stats[2]),int(stats[4]),int(stats[5]),int(stats[7]))
            elif stats[1] == "Assassin":
                player = Assassin(stats[0],int(stats[2]),int(stats[4]),int(stats[5]),int(stats[7]))
            elif stats[1] == "Paladin":
                player = Paladin(stats[0],int(stats[2]),int(stats[4]),int(stats[5]),int(stats[7]))
            player.cHealth = int(stats[3])
            player.shield = float(stats[6])
            player.cMana = int(stats[8])
            player.level = int(stats[12])
            for type in player.pList:
                type["Quant"] = int(stats[9 + player.pList.index(type)])
        return player



#Character Creation:
realjob = 0
while realjob == 0:
    realjob = 1
    job = input("Choose your class:\n 1. Berserker\n 2. Assassin\n 3. Paladin\n 1-3: ")
    if job == "1":
        player = Berserker(input("Name your Character: "), 50, 8, 0, 7)
    elif job == "2":
        player = Assassin(input("Name your Character: "), 40, 10, 0, 6)
    elif job == "3":
        player = Paladin(input("Name your Character: "), 50, 7, 2, 7)
    else:
        print("Please choose a number from the list.")
        realjob = 0

#Main Menu:
quit = 0
while quit == 0:
    print("Options: \n " +
          "1. View Character \n " +
          "2. Explore Dungeon \n " + 
          "3. View Inventory \n " +
          "4. Save Game \n " + 
          "5. Load Game \n " +
          "6. Exit")
    choice = input("What will you do? 1-6: ")
    if choice == "1":
        player.charsheet()
    elif choice == "2":
        group = random.randint(1, 3)
        difficulty = 6 + player.level
        event = random.randint(1, difficulty)
        if event >= 15:
            quit = combat(player, 2, difficulty, group)
        elif event >= 10:
            quit = combat(player, 1, difficulty, group)
        elif event >= 6:
            print(f"{player.name} discovered a treasure chest! ")
            Loot(player)
        else:    
            quit = combat(player, 0, difficulty, group)
    elif choice == "3":
        useItem(player)
    elif choice == "4":
        saveGame(player)
    elif choice == "5":
        player = loadGame(player)
    else:
        confirm = str.lower(input("Are you sure you want to quit? y/n: "))
        if confirm == "y":
            quit = 1
