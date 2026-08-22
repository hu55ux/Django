import os


class Character:
    def __init__(self, name: str, health: int, attack_power: int):
        self.name = name
        self.health = max(0, health)
        self.attack_power = attack_power

    def take_damage(self, amount: int) -> int:
        damage = max(0, amount)
        self.health = max(0, self.health - damage)
        print(f"{self.name} took {damage} damage. (HP: {self.health})")
        if not self:
            print(f"{self.name} has been defeated.")
        return damage

    def attack(self, target: "Character") -> None:
        if not self:
            print(f"{self.name} is dead and cannot attack.")
            return
        if not target:
            print(f"{target.name} is already dead.")
            return

        print(f"{self.name} attacks {target.name} for {self.attack_power} damage.")
        target.take_damage(self.attack_power)

    def get_info(self) -> str:
        status = "Alive" if self else "Dead"
        return f"[{self.__class__.__name__}] {self.name} | HP: {self.health} | ATK: {self.attack_power} | Status: {status}"

    def __str__(self) -> str:
        return self.get_info()

    def __bool__(self) -> bool:
        return self.health > 0

    def __len__(self) -> int:
        return self.health

    def __lt__(self, other: "Character") -> bool:
        if not isinstance(other, Character):
            return NotImplemented
        return self.health < other.health

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Character):
            return False
        return (
            self.name == other.name
            and self.health == other.health
            and self.attack_power == other.attack_power
        )

    def __add__(self, other) -> "Team":
        if isinstance(other, Character):
            return Team(f"{self.name} & {other.name}", [self, other])
        elif isinstance(other, Team):
            return other + self
        return NotImplemented


class Warrior(Character):
    def __init__(self, name: str, health: int, attack_power: int, armor: int = 5):
        super().__init__(name, health, attack_power)
        self.armor = armor

    def take_damage(self, amount: int) -> int:
        reduced_damage = max(1, amount - self.armor)
        print(f"{self.name}'s armor ({self.armor}) blocked some damage.")
        return super().take_damage(reduced_damage)

    def attack(self, target: Character) -> None:
        if not self or not target:
            return
        total_damage = self.attack_power + 5
        print(f"[Warrior] {self.name} slashes {target.name} for {total_damage} damage.")
        target.take_damage(total_damage)

    def get_info(self) -> str:
        return f"{super().get_info()} | Armor: {self.armor}"


class Mage(Character):
    def __init__(self, name: str, health: int, attack_power: int, mana: int = 30):
        super().__init__(name, health, attack_power)
        self.mana = mana

    def attack(self, target: Character) -> None:
        if not self or not target:
            return

        if self.mana >= 10:
            self.mana -= 10
            damage = self.attack_power * 2
            print(f"[Mage] {self.name} casts Fireball on {target.name} for {damage} damage. (Mana left: {self.mana})")
            target.take_damage(damage)
        else:
            print(f"[Mage] {self.name} has no mana left, uses wand attack for {self.attack_power} damage.")
            target.take_damage(self.attack_power)

    def get_info(self) -> str:
        return f"{super().get_info()} | Mana: {self.mana}"


class Archer(Character):
    def __init__(self, name: str, health: int, attack_power: int, arrows: int = 5):
        super().__init__(name, health, attack_power)
        self.arrows = arrows

    def attack(self, target: Character) -> None:
        if not self or not target:
            return

        if self.arrows > 0:
            self.arrows -= 1
            print(f"[Archer] {self.name} shoots an arrow at {target.name} for {self.attack_power} damage. (Arrows left: {self.arrows})")
            target.take_damage(self.attack_power)
        else:
            print(f"[Archer] {self.name} ran out of arrows, punches {target.name} for 5 damage.")
            target.take_damage(5)

    def get_info(self) -> str:
        return f"{super().get_info()} | Arrows: {self.arrows}"


class Team:
    def __init__(self, name: str, members: list[Character] = None):
        self.name = name
        self.members = members if members is not None else []

    def __add__(self, other) -> "Team":
        if isinstance(other, Character):
            return Team(self.name, self.members + [other])
        elif isinstance(other, Team):
            return Team(f"{self.name} & {other.name}", self.members + other.members)
        return NotImplemented

    def __str__(self) -> str:
        members_str = ", ".join(m.name for m in self.members)
        return f"Team [{self.name}]: ({members_str})"


def clear_screen(header: str = "MAIN MENU") -> None:
    os.system('cls' if os.name == 'nt' else 'clear')
    print("========================================")
    print(f"       GAME ARENA - {header}")
    print("========================================")
    print(" [Type '0' or 'b' at any prompt to go back]")
    print("-" * 40)


def get_user_input(prompt: str) -> str:
    val = input(prompt).strip()
    if val.lower() in ["0", "b", "esc", "back", "cancel"]:
        return "ESC"
    return val


def print_characters(characters: list[Character]) -> None:
    if not characters:
        print("No characters available.")
        return
    for i, c in enumerate(characters, 1):
        print(f"  [{i}] {c}")


def pause() -> None:
    input("\nPress Enter to continue...")


def main():
    characters: list[Character] = []
    teams: list[Team] = []

    while True:
        clear_screen("MAIN MENU")
        print("1. Create Character")
        print("2. View Characters & Status")
        print("3. Attack")
        print("4. Create Team")
        print("5. Compare Characters")
        print("6. Load Preset Characters")
        print("0. Exit")
        print("-" * 40)

        choice = get_user_input("Select option (0-6): ")

        if choice in ["0", "ESC"]:
            clear_screen("EXIT")
            print("Goodbye!")
            break

        elif choice == "1":
            clear_screen("CREATE CHARACTER")
            print("Select Class:")
            print("  1. Warrior")
            print("  2. Mage")
            print("  3. Archer")
            print("  4. Basic Character")
            cls_choice = get_user_input("\nChoice (1-4): ")
            if cls_choice == "ESC":
                continue

            name = get_user_input("Character Name [Hero]: ")
            if name == "ESC":
                continue
            name = name or "Hero"

            hp_in = get_user_input("Health [100]: ")
            if hp_in == "ESC":
                continue
            hp = int(hp_in) if hp_in.isdigit() else 100

            atk_in = get_user_input("Attack Power [20]: ")
            if atk_in == "ESC":
                continue
            atk = int(atk_in) if atk_in.isdigit() else 20

            if cls_choice == "1":
                arm_in = get_user_input("Armor [5]: ")
                if arm_in == "ESC":
                    continue
                armor = int(arm_in) if arm_in.isdigit() else 5
                char = Warrior(name, hp, atk, armor)
            elif cls_choice == "2":
                mn_in = get_user_input("Mana [30]: ")
                if mn_in == "ESC":
                    continue
                mana = int(mn_in) if mn_in.isdigit() else 30
                char = Mage(name, hp, atk, mana)
            elif cls_choice == "3":
                ar_in = get_user_input("Arrows [5]: ")
                if ar_in == "ESC":
                    continue
                arrows = int(ar_in) if ar_in.isdigit() else 5
                char = Archer(name, hp, atk, arrows)
            else:
                char = Character(name, hp, atk)

            characters.append(char)
            print(f"\nCreated: {char}")
            pause()

        elif choice == "2":
            clear_screen("CHARACTER LIST")
            print_characters(characters)

            if characters:
                print("\nInternal Values:")
                for c in characters:
                    print(f"  • {c.name} -> __str__: '{str(c)}' | Alive (__bool__): {bool(c)} | HP (__len__): {len(c)}")

            if teams:
                print("\nTeams:")
                for t in teams:
                    print(f"  • {t}")

            pause()

        elif choice == "3":
            clear_screen("ATTACK")
            if len(characters) < 2:
                print("Need at least 2 characters.")
                pause()
                continue

            print_characters(characters)
            att_s = get_user_input("\nAttacker index: ")
            if att_s == "ESC":
                continue

            tar_s = get_user_input("Target index: ")
            if tar_s == "ESC":
                continue

            if att_s.isdigit() and tar_s.isdigit():
                i1, i2 = int(att_s) - 1, int(tar_s) - 1
                if 0 <= i1 < len(characters) and 0 <= i2 < len(characters):
                    if i1 == i2:
                        print("Cannot attack self.")
                    else:
                        print("\nOutcome:")
                        characters[i1].attack(characters[i2])
                else:
                    print("Invalid character selection.")
            else:
                print("Invalid input.")

            pause()

        elif choice == "4":
            clear_screen("CREATE TEAM")
            if len(characters) < 2:
                print("Need at least 2 characters.")
                pause()
                continue

            print_characters(characters)
            c1_s = get_user_input("\nFirst character index: ")
            if c1_s == "ESC":
                continue

            c2_s = get_user_input("Second character index: ")
            if c2_s == "ESC":
                continue

            if c1_s.isdigit() and c2_s.isdigit():
                i1, i2 = int(c1_s) - 1, int(c2_s) - 1
                if 0 <= i1 < len(characters) and 0 <= i2 < len(characters) and i1 != i2:
                    team = characters[i1] + characters[i2]
                    teams.append(team)
                    print(f"\nFormed: {team}")
                else:
                    print("Invalid selection.")
            else:
                print("Invalid input.")

            pause()

        elif choice == "5":
            clear_screen("COMPARE")
            if len(characters) < 2:
                print("Need at least 2 characters.")
                pause()
                continue

            print_characters(characters)
            c1_s = get_user_input("\nFirst character index: ")
            if c1_s == "ESC":
                continue

            c2_s = get_user_input("Second character index: ")
            if c2_s == "ESC":
                continue

            if c1_s.isdigit() and c2_s.isdigit():
                i1, i2 = int(c1_s) - 1, int(c2_s) - 1
                if 0 <= i1 < len(characters) and 0 <= i2 < len(characters):
                    c1, c2 = characters[i1], characters[i2]
                    print(f"\nEqual (__eq__): {c1 == c2}")
                    if c1 < c2:
                        print(f"{c1.name} has less HP than {c2.name} (__lt__)")
                    elif c2 < c1:
                        print(f"{c2.name} has less HP than {c1.name} (__lt__)")
                    else:
                        print("Both characters have equal HP.")
                else:
                    print("Invalid selection.")
            else:
                print("Invalid input.")

            pause()

        elif choice == "6":
            clear_screen("LOAD PRESETS")
            characters.extend([
                Warrior("Arthur", 120, 20, 5),
                Mage("Gandalf", 80, 25, 30),
                Archer("Legolas", 90, 18, 5),
                Character("Goblin", 50, 10)
            ])
            print("Loaded Arthur (Warrior), Gandalf (Mage), Legolas (Archer), Goblin (Base).")
            pause()

        else:
            print("Invalid choice.")
            pause()


if __name__ == "__main__":
    main()

