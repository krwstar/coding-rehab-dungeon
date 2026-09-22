import random

from models import (
    Player,
    calculate_max_hp,
    calculate_max_mp,
    calculate_speed,
    calculate_attack_power,
    calculate_magic_power,
    calculate_defense,
    calculate_crit_chance,
)

from data import equipments, items, skills, sans, sans_skill


STAT_REWARDS = {
    "최대 HP": "max_hp",
    "최대 MP": "max_mp",
    "ATK": "attack",
    "MAG": "magic",
    "SPD": "speed",
    "DEF": "defense",
}

BASIC = "Basic"
COMMON = "Common"
RARE = "Rare"
EPIC = "Epic"
LEGENDARY = "Legendary"

FLOOR_RARITY_WEIGHTS = {
    1: {COMMON: 65, RARE: 28, EPIC: 6, LEGENDARY: 1},
    2: {COMMON: 45, RARE: 35, EPIC: 17, LEGENDARY: 3},
    3: {COMMON: 25, RARE: 35, EPIC: 30, LEGENDARY: 10},
}

TREASURE_FLOOR_RARITY_WEIGHTS = {
    1: {COMMON: 45, RARE: 35, EPIC: 17, LEGENDARY: 3},
    2: {COMMON: 30, RARE: 35, EPIC: 28, LEGENDARY: 7},
    3: {COMMON: 15, RARE: 30, EPIC: 40, LEGENDARY: 15},
}

SHOP_FLOOR_RARITY_WEIGHTS = {
    1: {COMMON: 55, RARE: 32, EPIC: 11, LEGENDARY: 2},
    2: {COMMON: 35, RARE: 38, EPIC: 22, LEGENDARY: 5},
    3: {COMMON: 15, RARE: 35, EPIC: 38, LEGENDARY: 12},
}

BOSS_FLOOR_RARITY_WEIGHTS = {
    1: {RARE: 60, EPIC: 35, LEGENDARY: 5},
    2: {RARE: 40, EPIC: 50, LEGENDARY: 10},
    3: {RARE: 20, EPIC: 60, LEGENDARY: 20},
}


def create_player():
    while True:

        name = input("이름을 입력하세요: ")
        if name == "샌즈":
            print(sans)
            print("와!! 샌즈!!!")
        confirm = input(f"이름을 {name}(으)로 하시겠습니까? y/n: ")
        if confirm.lower() == "y" or confirm == "":
            new_player = Player(
                name=name, skills=[], items=[items[0], items[1]]
            )
            if name == "샌즈":
                new_player.skills.append(sans_skill)
            return new_player

def show_status(player):
    while True:
        print()
        print("=" * 45)
        print("                  스테이터스")
        print("=" * 45)
        print(f"이름: {player.name}")
        print(
            f"HP  {player.hp}/{calculate_max_hp(player)}    "
            f"MP  {player.mp}/{calculate_max_mp(player)}"
        )
        print(
            f"ATK {calculate_attack_power(player):2d}    "
            f"MAG {calculate_magic_power(player):2d}"
        )
        print(
            f"SPD {calculate_speed(player):2d}    "
            f"DEF {calculate_defense(player):2d}"
        )
        print(
            f"크리티컬 확률 {int(calculate_crit_chance(player)*100):2d}%"
        )
        print(f"Gold: {player.gold}G")
        print("-" * 45)
        print(f"무기:   [{player.weapon.rarity}] {player.weapon.name}")
        print(f"방어구: [{player.armor.rarity}] {player.armor.name}")
        print(f"반지:   [{player.ring.rarity}] {player.ring.name}")
        print("-" * 45)
        print(f"스킬: {len(player.skills)}/5")
        print(f"아이템: {len(player.items)}개")
        print("-" * 45)
        print("1. 스테이터스 상세")
        print("2. 장비 상세")
        print("3. 스킬 상세")
        print("4. 아이템 상세")
        print("0. 뒤로")
        print("=" * 45)

        choice = input("> ")

        if choice == "0":
            return
        elif choice == "1":
            show_stat_details(player)
        elif choice == "2":
            show_equipment_details(player)
        elif choice == "3":
            show_skill_details(player)
        elif choice == "4":
            show_item_details(player)
        else:
            print("올바르지 않은 입력")

def show_stat_details(player):
    print()
    print("=" * 45)
    print("               스테이터스 상세")
    print("=" * 45)

    print(
        f"최대 HP: {player.max_hp} "
        f"+ 장비 {calculate_max_hp(player) - player.max_hp} "
        f"= {calculate_max_hp(player)}"
    )
    print(
        f"최대 MP: {player.max_mp} "
        f"+ 장비 {calculate_max_mp(player) - player.max_mp} "
        f"= {calculate_max_mp(player)}"
    )
    print(
        f"ATK: {player.attack} "
        f"+ 장비 {calculate_attack_power(player) - player.attack} "
        f"= {calculate_attack_power(player)}"
    )
    print(
        f"MAG: {player.magic} "
        f"+ 장비 {calculate_magic_power(player) - player.magic} "
        f"= {calculate_magic_power(player)}"
    )
    print(
        f"SPD: {player.speed} "
        f"+ 장비 {calculate_speed(player) - player.speed} "
        f"= {calculate_speed(player)}"
    )
    print(
        f"DEF: {player.defense} "
        f"+ 장비 {calculate_defense(player) - player.defense} "
        f"= {calculate_defense(player)}"
    )

    print("=" * 45)
    input("Enter를 눌러 돌아가기...")

def show_equipment_details(player):
    print()
    print("=" * 45)
    print("                  장비 상세")
    print("=" * 45)

    equipments = [
        ("무기", player.weapon),
        ("방어구", player.armor),
        ("반지", player.ring),
    ]

    for slot_name, equipment in equipments:
        print(f"[{slot_name}] [{equipment.rarity}] {equipment.name}")

        stats = get_equipment_stats(equipment)
        if stats:
            print(f"능력치: {stats}")
        else:
            print("능력치: 없음")

        print(f"{equipment.flavor_text}")
        print("-" * 45)

    input("Enter를 눌러 돌아가기...")

def show_skill_details(player):
    print()
    print("=" * 45)
    print("                  스킬 상세")
    print("=" * 45)

    if not player.skills:
        print("보유한 스킬이 없다.")
    else:
        for i, skill in enumerate(player.skills, start=1):
            print(f"{i}. [{skill.rarity}] {skill.name}")
            print(f"소비 MP: {skill.mp_cost}")
            print(f"{skill.description}")
            print("-" * 45)

    input("Enter를 눌러 돌아가기...")

def show_item_details(player):
    while True:
        print()
        print("=" * 45)
        print("                 아이템 상세")
        print("=" * 45)

        if not player.items:
            print("보유한 아이템이 없다.")
            input("Enter를 눌러 돌아가기...")
            return

        grouped_items = group_items(player.items)
        item_menu = "아이템 목록\n"
        for i, entry in enumerate(grouped_items, start=1):
            item = entry["item"]
            count = entry["count"]
            item_menu += f"{i}. [{item.name}] x{count}\n"
            item_menu += f"    {item.flavor_text}\n"
        item_menu += "0. 뒤로\n"
        print(item_menu)
        
        choice = input("> ")
        if not choice.isdigit():
            print("올바르지 않은 입력")
            continue

        choice = int(choice)
        if choice == 0:
            return
        if choice not in range(1, len(player.items) + 1):
            print("올바르지 않은 입력")
            continue
        
        item = player.items[choice - 1]
        if not item.usable_outside_battle:
            print("전투 중에만 사용할 수 있는 아이템이다.")
            continue
        
        use_item(player, item)
        player.items.remove(item)

        item_uses = player.run_stats["items_used"]
        item_uses[item.name] = item_uses.get(item.name, 0) + 1

def group_items(items):
    grouped = {}

    for item in items:
        if item.name not in grouped:
            grouped[item.name] = {
                "item": item,
                "count": 0,
            }

        grouped[item.name]["count"] += 1

    return list(grouped.values())


def use_item(
    user,
    item,
    target=None,
    enemy_units=None,
    battle_logs=None,
):
    need_print = False

    if battle_logs is None:
        need_print = True
        battle_logs = []

    battle_logs.append(
        f"{user.name}은(는) {item.name}을 사용했다!"
    )

    for effect in item.effects:
        if effect.target_type == "self":
            effect.apply(user, user, battle_logs)

        elif item.target_type == "all_enemies":
            for enemy in enemy_units:
                if enemy.hp > 0:
                    effect.apply(user, enemy, battle_logs)

        else:
            effect.apply(user, target, battle_logs)

    if need_print:
        for log in battle_logs:
            print(log)

    if isinstance(user, Player):
        item_uses = user.run_stats["items_used"]
        item_uses[item.name] = item_uses.get(item.name, 0) + 1


def add_skill(player, skill):
    if len(player.skills) < 5:
        player.skills.append(skill)
        print(f"{skill.name}을(를) 배웠다.")
        return True
    else:
        while True:
            print("스킬이 너무 많다.")
            print(f"1. 기존 스킬 하나와 교체한다")
            print(f"2. 포기한다")
            choice = input("> ")
            if choice == "1":
                while True:
                    skill_menu = "스킬 목록\n"
                    for i, owned_skill in enumerate(player.skills, start=1):
                        skill_menu += (
                            f"{i}. {owned_skill.name} " f"(MP {owned_skill.mp_cost})\n"
                        )
                    skill_menu += "0. 뒤로"
                    print(skill_menu)

                    choice = input("> ")
                    
                    if not choice.isdigit():
                        print("올바르지 않은 입력")
                        continue
                    choice = int(choice)
                    if choice == 0:
                        break
                    if not choice in range(1, len(player.skills) + 1):
                        print("올바르지 않은 입력")
                        continue
                    old_skill = player.skills.pop(choice - 1)
                    player.skills.append(skill)
                    print(f"{old_skill.name}을 {skill.name}으로 교체했다.")
                    return True
            elif choice == "2":
                print("포기했다.")
                return False
            print("올바르지 않은 입력")


def get_equipment_stats(equipment):
    stats = []
    if equipment.hp != 0:
        stats.append(f"HP {equipment.hp:+d}")
    if equipment.mp != 0:
        stats.append(f"MP {equipment.mp:+d}")
    if equipment.attack != 0:
        stats.append(f"ATK {equipment.attack:+d}")
    if equipment.magic != 0:
        stats.append(f"MAG {equipment.magic:+d}")
    if equipment.speed != 0:
        stats.append(f"SPD {equipment.speed:+d}")
    if equipment.defense != 0:
        stats.append(f"DEF {equipment.defense:+d}")
    if equipment.critical != 0:
        stats.append(f"크리티컬 확률 {int(equipment.critical*100):+d}%")
    return ", ".join(stats)


def equip(player, equipment):
    slot = equipment.slot
    if slot == "weapon":
        current_equipment = player.weapon
    elif slot == "armor":
        current_equipment = player.armor
    elif slot == "ring":
        current_equipment = player.ring
    
    print("-" * 45)
    print(f"현재 장비: {current_equipment.name}")
    stats = get_equipment_stats(current_equipment)
    if stats:
        print(f"  능력치: {stats}")
    else:
        print("  능력치: 없음")
    print(f"  설명: {current_equipment.flavor_text}")
    print()
    print(f"교체할 장비: {equipment.name}")
    stats = get_equipment_stats(equipment)
    if stats:
        print(f"  능력치: {stats}")
    else:
        print("  능력치: 없음")
    print(f"  설명: {equipment.flavor_text}")
    
    print("-" * 45)
    print("장비를 교체하시겠습니까? y/n")
    choice = input("> ")
    
    if not (choice.lower() == "y" or choice == ""):
        return False
    
    if slot == "weapon":
        player.weapon = equipment
    elif slot == "armor":
        player.armor = equipment
    elif slot == "ring":
        player.ring = equipment
    else:
        print("올바르지 않은 장비 슬롯")
        return False
    player.hp = min(player.hp, calculate_max_hp(player))
    player.mp = min(player.mp, calculate_max_mp(player))
    return True


def find_equipment(equipments, name):
    for equipment in equipments:
        if equipment.name == name:
            return equipment
    print(f"[{name}]이란 이름의 장비를 찾을 수 없음")
    return None


def find_skill(skills, name):
    for skill in skills:
        if skill.name == name:
            return skill

    print(f"[{name}]이란 이름의 스킬을 찾을 수 없음")
    return None

def select_job(player):
    while True:
        print("=" * 45)
        print("직업을 고르세요.")
        print()
        # print("0. 디버거")
        print("1. 전사")
        print("   활용 스탯/자원: ATK / HP")
        print("   특징: 강력한 단타와 출혈, 흡혈을 활용해 적과 정면으로 맞섭니다.")
        print()
        print("2. 마법사")
        print("   활용 스탯/자원: MAG / MP")
        print("   특징: 마력을 순환시키며 순수 마력, 화염, 냉기 마법을 사용합니다.")
        print()
        print("3. 도적")
        print("   활용 스탯/자원: SPD / 독")
        print("   특징: 빠른 다단 공격과 독을 활용하며, 행동 템포와 회피로 전투를 주도합니다.")
        print()
        print("4. 수호자")
        print("   활용 스탯/자원: DEF / 방어도")
        print("   특징: 방어도를 높게 쌓아 공격을 막고, 공격과 반격에 활용합니다.")
        print()
        print("5. 검객")
        print("   활용 스탯/자원: ATK / SPD")
        print("   특징: 적과 나의 행동 순서를 조절하고, 패링으로 공격을 받아치는 고인물용 직업입니다.")
        choice = input("> ")
        if choice == "1":
            player.weapon = find_equipment(equipments, "철 검")
            player.armor = find_equipment(equipments, "가죽 갑옷")
            player.ring = find_equipment(equipments, "전사의 반지")
            player.skills.append(find_skill(skills, "강타"))
            player.skills.append(find_skill(skills, "휩쓸기"))
            break
        elif choice == "2":
            player.weapon = find_equipment(equipments, "마법봉")
            player.armor = find_equipment(equipments, "로브")
            player.ring = find_equipment(equipments, "마력의 반지")
            player.skills.append(find_skill(skills, "마력탄"))
            player.skills.append(find_skill(skills, "화염살"))
            player.skills.append(find_skill(skills, "냉기탄"))
            break
        elif choice == "3":
            player.weapon = find_equipment(equipments, "단검")
            player.armor = find_equipment(equipments, "경량복")
            player.ring = find_equipment(equipments, "독침의 반지")
            player.skills.append(find_skill(skills, "독 플라스크"))
            player.skills.append(find_skill(skills, "회피 기동"))
            player.skills.append(find_skill(skills, "연막"))
            break
        elif choice == "4":
            player.weapon = find_equipment(equipments, "철제 방패")
            player.armor = find_equipment(equipments, "중갑")
            player.ring = find_equipment(equipments, "견고한 의지의 반지")
            player.skills.append(find_skill(skills, "방패 강타"))
            player.skills.append(find_skill(skills, "철벽 태세"))
            break
        elif choice == "5":
            player.weapon = find_equipment(equipments, "연습용 도")
            player.armor = find_equipment(equipments, "검객의 외투")
            player.ring = find_equipment(equipments, "도전자의 반지")
            player.skills.append(find_skill(skills,"패링"))
            player.skills.append(find_skill(skills,"도발"))
            break
        # elif choice == "0":
        #     player.weapon = find_equipment(equipments, "연습용 도")
        #     player.armor = find_equipment(equipments, "성채의 갑주")
        #     player.ring = find_equipment(equipments, "도전자의 반지")
        #     player.skills.append(find_skill(skills,"납도"))
        #     player.skills.append(find_skill(skills,"히코보시"))
        #     player.skills.append(find_skill(skills,"최후의 성벽"))
        #     player.skills.append(find_skill(skills,"난공불락"))
        #     player.items.extend(items)
        #     player.max_hp += 1000
        #     player.max_mp += 1000
        #     player.attack += 150
        #     player.magic += 15
        #     player.defense += 15
        #     player.speed += 15
        #     break
        else:
            print("올바르지 않은 입력")
    player.hp = calculate_max_hp(player)
    player.mp = calculate_max_mp(player)


def increase_stat(player, stat_name):
    amount = random.randint(1, 3)
    attr_name = STAT_REWARDS[stat_name]
    
    if stat_name == "최대 HP":
        amount += 2
    elif stat_name == "최대 MP":
        amount += 1
    
    setattr(
        player, attr_name,
        getattr(player, attr_name) + amount
    )
    
    if stat_name == "최대 HP":
        player.hp += amount
    elif stat_name == "최대 MP":
        player.mp += amount

    print(f"{stat_name} +{amount}")


def choose_stat_reward(player):
    stat_names = list(STAT_REWARDS.keys())
    
    while True:
        print()
        print("성장할 스테이터스를 선택하세요.")
        print()
        
        for i, stat_name in enumerate(stat_names, start=1):
            print(f"{i}. {stat_name}")
        choice = input("> ")
        
        if not choice.isdigit():
            print("올바르지 않은 입력")
            continue
        
        choice = int(choice)
        
        if choice not in range(1, len(stat_names)+1):
            print("올바르지 않은 입력")
            continue
        
        increase_stat(player, stat_names[choice-1])
        return


def choose_random_stat_reward(player):
    stat_names = random.sample(list(STAT_REWARDS.keys()), 3)
    
    while True:
        print()
        print("성장할 스테이터스를 선택하세요.")
        print()
        
        for i, stat_name in enumerate(stat_names, start=1):
            print(f"{i}. {stat_name}")
        choice = input("> ")
        
        if not choice.isdigit():
            print("올바르지 않은 입력")
            continue
        
        choice = int(choice)
        
        if choice not in range(1, 4):
            print("올바르지 않은 입력")
            continue
        
        increase_stat(player, stat_names[choice-1])
        return


def make_rewards(reward_pool, rarity_weights, count=5):
    rewards = []

    while len(rewards) < count:
        reward = get_random_reward_by_rarity(
            reward_pool,
            rarity_weights,
        )

        if reward is not None and reward not in rewards:
            rewards.append(reward)

    return rewards


def choose_equipment_or_skill(player, event=None, floor=1):
    if random.random() > 0.5:
        reward_pool = equipments
        reward_type = "equipment"
    else:
        reward_pool = skills
        reward_type = "skill"

    if event == "treasure":
        rarity_weights = TREASURE_FLOOR_RARITY_WEIGHTS[floor]
    elif event == "boss":
        rarity_weights = BOSS_FLOOR_RARITY_WEIGHTS[floor]
    else:
        rarity_weights = FLOOR_RARITY_WEIGHTS[floor]

    rewards = make_rewards(reward_pool, rarity_weights, count=5)
    rerolled = False

    while len(rewards) < 5:
        reward = get_random_reward_by_rarity(
            reward_pool,
            rarity_weights,
        )

        if reward is not None and reward not in rewards:
            rewards.append(reward)

    while True:
        print()
        
        if reward_type == "equipment":
            print("장비를 선택하세요.")
        else:
            print("스킬을 선택하세요.")
        print()
        for i, reward in enumerate(rewards, start=1):
            if reward_type == "equipment":
                stats = get_equipment_stats(reward)

                print(
                    f"{i}. [{reward.rarity}] {reward.name}"
                    f" - {stats}"
                )
                print(f"{reward.flavor_text}")
                print()

            else:
                print(
                    f"{i}. [{reward.rarity}] {reward.name}"
                    f" - MP {reward.mp_cost}"
                )
                print(f"{reward.description}")
                print()
                
        reroll_index = len(rewards) + 1
        if not rerolled:
            print(f"{reroll_index}. 리롤 (50G)")
        print("0. 넘기기")

        choice = input("> ")
        
        if not choice.isdigit():
            print("올바르지 않은 입력")
            continue

        choice = int(choice)

        if choice == 0:
            print("보상을 포기했다.")
            return False

        if not rerolled and choice == reroll_index:
            if player.gold < 50:
                print("골드가 부족하다.")
                continue
            player.gold -= 50
            player.run_stats["gold_spent"] += 50
            rewards = make_rewards(reward_pool, rarity_weights,)
            rerolled = True
            print("보상을 다시 뽑았다.")
            continue

        if choice not in range(1, len(rewards)+1):
            print("올바르지 않은 입력")
            continue

        reward = rewards[choice - 1]

        if reward in equipments:
            equiped = equip(player, reward)
            if not equiped:
                continue

            print(f"{reward.name}을(를) 획득했다.")
            return True

        if add_skill(player, reward):
            return True


def get_random_reward_by_rarity(reward_pool, rarity_weights):
    rarity = random.choices(
        population=list(rarity_weights.keys()),
        weights=list(rarity_weights.values()),
        k=1,
    )[0]

    candidates = [
        reward for reward in reward_pool
        if reward.rarity == rarity
    ]

    if not candidates:
        return None

    return random.choice(candidates)