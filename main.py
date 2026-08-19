import os


class Character:
    """
    Base Character Class
    """

    def __init__(self, name: str, health: int, attack_power: int):
        self.name = name
        self.health = max(0, health)
        self.attack_power = attack_power

    def take_damage(self, amount: int) -> int:
        """Character receives damage and updates remaining health."""
        actual_damage = max(0, amount)
        self.health = max(0, self.health - actual_damage)
        print(f"💥 {self.name} took {actual_damage} damage! (Remaining HP: {self.health})")
        if not self:
            print(f"💀 {self.name} has been defeated!")
        return actual_damage

    def attack(self, target: "Character") -> None:
        """Base attack method on another character."""
        if not self:
            print(f"⚠️ {self.name} is defeated and cannot attack!")
            return
        if not target:
            print(f"⚠️ {target.name} is already defeated!")
            return

        print(f"⚔️ {self.name} performs a base attack on {target.name} for {self.attack_power} damage.")
        target.take_damage(self.attack_power)

    def get_info(self) -> str:
        """Returns string representation of character information."""
        status = "Alive" if self else "Defeated"
        return f"[{self.__class__.__name__}] {self.name} | HP: {self.health} | Attack: {self.attack_power} | Status: {status}"

    # --- Magic Methods ---

    def __str__(self) -> str:
        """Returns string info about the character."""
        return self.get_info()

    def __bool__(self) -> bool:
        """Returns True if character is alive, False otherwise."""
        return self.health > 0

    def __len__(self) -> int:
        """Returns numeric characteristic of character (current health)."""
        return self.health

    def __lt__(self, other: "Character") -> bool:
        """Compares health of two characters (<)."""
        if not isinstance(other, Character):
            return NotImplemented
        return self.health < other.health

    def __eq__(self, other: object) -> bool:
        """Checks equality of two characters (==)."""
        if not isinstance(other, Character):
            return False
        return (
            self.name == other.name
            and self.health == other.health
            and self.attack_power == other.attack_power
        )

    def __add__(self, other) -> "Team":
        """Combines characters into a Team (+)."""
        if isinstance(other, Character):
            return Team(f"{self.name} & {other.name} Team", [self, other])
        elif isinstance(other, Team):
            return other + self
        return NotImplemented


class Warrior(Character):
    """
    Warrior Class - Features Armor attribute.
    """

    def __init__(self, name: str, health: int, attack_power: int, armor: int = 5):
        super().__init__(name, health, attack_power)
        self.armor = armor

    def take_damage(self, amount: int) -> int:
        """Warrior reduces incoming damage using armor."""
        reduced_damage = max(1, amount - self.armor)
        print(f"🛡️ {self.name}'s armor ({self.armor}) reduced incoming damage to {reduced_damage}!")
        return super().take_damage(reduced_damage)

    def attack(self, target: Character) -> None:
        """Warrior's special heavy strike."""
        if not self or not target:
            return
        bonus_damage = 5
        total_damage = self.attack_power + bonus_damage
        print(f"🪓 [Warrior] {self.name} performs a heavy axe strike on {target.name} for {total_damage} damage!")
        target.take_damage(total_damage)

    def get_info(self) -> str:
        return f"{super().get_info()} | Armor: {self.armor}"


class Mage(Character):
    """
    Mage Class - Features Mana attribute.
    """

    def __init__(self, name: str, health: int, attack_power: int, mana: int = 30):
        super().__init__(name, health, attack_power)
        self.mana = mana

    def attack(self, target: Character) -> None:
        """Mage's magical spell attack using Mana."""
        if not self or not target:
            return

        if self.mana >= 10:
            self.mana -= 10
            magic_damage = self.attack_power * 2
            print(f"🔮 [Mage] {self.name} casts Fireball on {target.name} for {magic_damage} magic damage! (Remaining Mana: {self.mana})")
            target.take_damage(magic_damage)
        else:
            print(f"🪄 [Mage] {self.name} is out of Mana! Uses basic wand attack for {self.attack_power} damage.")
            target.take_damage(self.attack_power)

    def get_info(self) -> str:
        return f"{super().get_info()} | Mana: {self.mana}"


class Archer(Character):
    """
    Archer Class - Features Arrow count attribute.
    """

    def __init__(self, name: str, health: int, attack_power: int, arrows: int = 5):
        super().__init__(name, health, attack_power)
        self.arrows = arrows

    def attack(self, target: Character) -> None:
        """Archer's ranged attack using arrows."""
        if not self or not target:
            return

        if self.arrows > 0:
            self.arrows -= 1
            print(f"🏹 [Archer] {self.name} fires a precise arrow at {target.name} for {self.attack_power} damage! (Arrows left: {self.arrows})")
            target.take_damage(self.attack_power)
        else:
            print(f"🥊 [Archer] {self.name} is out of arrows! Performs a melee punch for 5 damage.")
            target.take_damage(5)

    def get_info(self) -> str:
        return f"{super().get_info()} | Arrows: {self.arrows}"


class Team:
    """
    Team Class representing combined characters.
    """

    def __init__(self, name: str, members: list[Character] = None):
        self.name = name
        self.members = members if members is not None else []

    def __add__(self, other) -> "Team":
        if isinstance(other, Character):
            new_members = self.members + [other]
            return Team(self.name, new_members)
        elif isinstance(other, Team):
            new_members = self.members + other.members
            return Team(f"{self.name} & {other.name}", new_members)
        return NotImplemented

    def __str__(self) -> str:
        member_names = ", ".join([m.name for m in self.members])
        return f"🏆 [{self.name}] Members: ({member_names})"


# ==========================================
# INTERACTIVE CLI APPLICATION WITH NAVIGATION
# ==========================================

def clear_screen(title: str = "MAIN MENU") -> None:
    """Clears the console screen and prints a consistent header."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("==================================================")
    print("      🎮 CHARACTER BATTLE ARENA SYSTEM 🎮       ")
    print("==================================================")
    print(f" 📌 CURRENT SECTION: {title.upper()}")
    print(" 💡 [Tip: Enter '0', 'b', or 'esc' at any prompt to return]")
    print("--------------------------------------------------")


def get_user_input(prompt: str) -> str:
    """
    Helper function to get input.
    Returns 'ESC' if user types '0', 'b', 'esc', 'back', or 'cancel'.
    """
    val = input(prompt).strip()
    if val.lower() in ["0", "b", "esc", "back", "cancel"]:
        return "ESC"
    return val


def display_character_list(characters: list[Character]) -> None:
    """Displays formatted list of characters."""
    if not characters:
        print("⚠️ No characters available. Create or load sample characters first!")
        return
    print("📋 Current Characters:")
    for idx, char in enumerate(characters, 1):
        print(f"  [{idx}] {char}")


def pause_prompt() -> None:
    """Pauses execution so user can review screen content."""
    input("\nPress Enter to return to Main Menu...")


def main_interactive():
    characters: list[Character] = []
    teams: list[Team] = []

    while True:
        clear_screen("MAIN MENU")
        print("1. ➕ Create New Character")
        print("2. 📜 Display All Characters & Magic Methods")
        print("3. ⚔️ Perform Attack (Polymorphism Demo)")
        print("4. 🛡️ Combine Characters into Team (__add__)")
        print("5. 🔍 Compare Two Characters (__lt__ / __eq__)")
        print("6. 📦 Load Sample Characters")
        print("0. ❌ Exit Program (or type 'esc')")
        print("--------------------------------------------------")

        choice = get_user_input("Enter choice (0-6 or 'esc'): ")

        if choice in ["0", "ESC", "7"]:
            clear_screen("EXIT SYSTEM")
            print("👋 Thank you for using Character Battle Arena! Goodbye!")
            break

        elif choice == "1":
            clear_screen("CREATE NEW CHARACTER")
            print("Select Character Class (or '0' to Go Back):")
            print("  1. Warrior (High Defense & Armor)")
            print("  2. Mage (High Damage & Mana)")
            print("  3. Archer (Ranged & Arrow Count)")
            print("  4. Base Character")
            type_choice = get_user_input("\nChoice (1-4, or '0' to Back): ")
            if type_choice == "ESC":
                print("↩️ Returned to Main Menu.")
                continue

            name = get_user_input("Enter character name [Default: Hero]: ")
            if name == "ESC":
                continue
            if not name:
                name = "Hero"

            hp_val = get_user_input("Enter HP (Health Points) [Default 100]: ")
            if hp_val == "ESC":
                continue
            try:
                hp = int(hp_val) if hp_val else 100
            except ValueError:
                hp = 100

            atk_val = get_user_input("Enter Attack Power [Default 20]: ")
            if atk_val == "ESC":
                continue
            try:
                atk = int(atk_val) if atk_val else 20
            except ValueError:
                atk = 20

            if type_choice == "1":
                armor_val = get_user_input("Enter Armor value [Default 5]: ")
                if armor_val == "ESC":
                    continue
                try:
                    armor = int(armor_val) if armor_val else 5
                except ValueError:
                    armor = 5
                char = Warrior(name, hp, atk, armor)

            elif type_choice == "2":
                mana_val = get_user_input("Enter Mana value [Default 30]: ")
                if mana_val == "ESC":
                    continue
                try:
                    mana = int(mana_val) if mana_val else 30
                except ValueError:
                    mana = 30
                char = Mage(name, hp, atk, mana)

            elif type_choice == "3":
                arrow_val = get_user_input("Enter Arrow count [Default 5]: ")
                if arrow_val == "ESC":
                    continue
                try:
                    arrows = int(arrow_val) if arrow_val else 5
                except ValueError:
                    arrows = 5
                char = Archer(name, hp, atk, arrows)

            else:
                char = Character(name, hp, atk)

            characters.append(char)
            print(f"\n✅ Character successfully created:\n   {char}")
            pause_prompt()

        elif choice == "2":
            clear_screen("DISPLAY CHARACTERS & MAGIC METHODS")
            display_character_list(characters)

            if characters:
                print("\n🔍 Dunder / Magic Method Inspection:")
                for char in characters:
                    print(f"  • __str__: {str(char)}")
                    print(f"  • __bool__ (Is Alive?): {bool(char)}")
                    print(f"  • __len__ (Current HP): {len(char)}")

            if teams:
                print("\n🏆 Formed Teams (__add__):")
                for team in teams:
                    print(f"  • {team}")

            pause_prompt()

        elif choice == "3":
            clear_screen("PERFORM ATTACK (POLYMORPHISM DEMO)")
            if len(characters) < 2:
                print("⚠️ You need at least 2 characters to perform an attack!")
                pause_prompt()
                continue

            display_character_list(characters)
            
            att_str = get_user_input("\nSelect ATTACKER index (or '0' to Back): ")
            if att_str == "ESC":
                continue

            tar_str = get_user_input("Select TARGET index (or '0' to Back): ")
            if tar_str == "ESC":
                continue

            try:
                attacker_idx = int(att_str) - 1
                target_idx = int(tar_str) - 1

                if 0 <= attacker_idx < len(characters) and 0 <= target_idx < len(characters):
                    if attacker_idx == target_idx:
                        print("⚠️ A character cannot attack themselves!")
                    else:
                        print("\n--- Attack Result ---")
                        characters[attacker_idx].attack(characters[target_idx])
                else:
                    print("❌ Invalid index selection!")
            except ValueError:
                print("❌ Please enter valid integer indices!")

            pause_prompt()

        elif choice == "4":
            clear_screen("COMBINE CHARACTERS INTO TEAM (__ADD__)")
            if len(characters) < 2:
                print("⚠️ You need at least 2 characters to form a team!")
                pause_prompt()
                continue

            display_character_list(characters)
            
            c1_str = get_user_input("\nSelect FIRST character index (or '0' to Back): ")
            if c1_str == "ESC":
                continue

            c2_str = get_user_input("Select SECOND character index (or '0' to Back): ")
            if c2_str == "ESC":
                continue

            try:
                c1_idx = int(c1_str) - 1
                c2_idx = int(c2_str) - 1

                if 0 <= c1_idx < len(characters) and 0 <= c2_idx < len(characters) and c1_idx != c2_idx:
                    c1 = characters[c1_idx]
                    c2 = characters[c2_idx]
                    new_team = c1 + c2
                    teams.append(new_team)
                    print(f"\n🎉 Team created successfully using __add__ operator!\n   {new_team}")
                else:
                    print("❌ Invalid selection!")
            except ValueError:
                print("❌ Please enter valid integer indices!")

            pause_prompt()

        elif choice == "5":
            clear_screen("COMPARE CHARACTERS (__LT__ / __EQ__)")
            if len(characters) < 2:
                print("⚠️ You need at least 2 characters to compare!")
                pause_prompt()
                continue

            display_character_list(characters)
            
            c1_str = get_user_input("\nSelect FIRST character index (or '0' to Back): ")
            if c1_str == "ESC":
                continue

            c2_str = get_user_input("Select SECOND character index (or '0' to Back): ")
            if c2_str == "ESC":
                continue

            try:
                c1_idx = int(c1_str) - 1
                c2_idx = int(c2_str) - 1

                if 0 <= c1_idx < len(characters) and 0 <= c2_idx < len(characters):
                    c1 = characters[c1_idx]
                    c2 = characters[c2_idx]

                    print("\n--- Comparison Results ---")
                    print(f"👉 Are {c1.name} and {c2.name} equal? (__eq__): {c1 == c2}")
                    if c1 < c2:
                        print(f"👉 {c1.name} has LESS HP than {c2.name} (__lt__)")
                    elif c2 < c1:
                        print(f"👉 {c2.name} has LESS HP than {c1.name} (__lt__)")
                    else:
                        print(f"👉 Both characters have equal HP!")
                else:
                    print("❌ Invalid selection!")
            except ValueError:
                print("❌ Please enter valid integer indices!")

            pause_prompt()

        elif choice == "6":
            clear_screen("LOAD SAMPLE CHARACTERS")
            w = Warrior("Thor", 120, 22, 6)
            m = Mage("Gandalf", 85, 25, 30)
            a = Archer("Legolas", 90, 18, 3)
            dummy = Character("Goblin", 60, 12)
            characters.extend([w, m, a, dummy])
            print("✅ Loaded sample characters:")
            print("  • Thor (Warrior)")
            print("  • Gandalf (Mage)")
            print("  • Legolas (Archer)")
            print("  • Goblin (Base Character)")
            pause_prompt()

        else:
            print("❌ Invalid choice. Please enter a number between 0 and 6.")
            pause_prompt()


if __name__ == "__main__":
    main_interactive()

