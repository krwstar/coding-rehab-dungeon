import random
import time
import sys

from copy import deepcopy
from combat import battle
from run_log import save_run_log
from player_utils import (
    add_skill,
    choose_random_stat_reward,
    equip,
    get_equipment_stats,
    calculate_max_hp,
    calculate_max_mp,
    choose_stat_reward,
    choose_equipment_or_skill,
    COMMON,
    RARE,
    EPIC,
    LEGENDARY,
    FLOOR_RARITY_WEIGHTS,
)
from models import (
    Enemy,
    Action,
    DamageEffect,
    BlockEffect,
    AddStatusEffect,
    CounterStatus,
    Weapon,
    Armor,
    Ring,
    roll_dice,
    take_damage,
)
from data import (
    equipments,
    skills,
    items,
    
    enemies_second_floor
)


def treasure(player, floor):
    print()
    print("=" * 45)
    print("          보물 상자를 발견했다!")
    print("=" * 45)
    
    gold = random.randint(30, 70)
    
    player.gold += gold
    player.run_stats["gold_earned"] += gold
    
    print(f"{gold}G를 획득했다!")
    
    choose_equipment_or_skill(player, "treasure", floor=floor)


def rest(player):
    print()
    print("=" * 45)
    print("                  휴식")
    print("=" * 45)
    
    while True:
        print(
            f"HP {player.hp}/{calculate_max_hp(player)}  "
            f"MP {player.mp}/{calculate_max_mp(player)}"
        )
        
        print()
        print("이 앞은 강적이 기다리고 있는 것 같다.")
        print("1. 휴식한다.")
        print("   최대 HP와 MP의 50%를 회복한다.")
        print("2. 수련한다.")
        print("   원하는 스테이터스를 성장시킨다.")
        choice = input("> ")
        
        if choice == "1":
            old_hp = player.hp
            old_mp = player.mp
            
            hp_recovery = calculate_max_hp(player) // 2
            mp_recovery = calculate_max_mp(player) // 2
            
            player.hp = min(
                player.hp + hp_recovery,
                calculate_max_hp(player)
            )
            player.mp = min(
                player.mp + mp_recovery,
                calculate_max_mp(player)
            )
            
            print()
            print(f"HP +{player.hp - old_hp}")
            print(f"MP +{player.mp - old_mp}")
            return

        if choice == "2":
            choose_stat_reward(player)
            return
            
def event_spring(player):
    while True:
        print(
            "신비한 샘을 발견했다. 어떻게 할까?\n"
            "1. 물을 마신다 (HP +15)\n"
            "2. 몸을 담근다 (최대 HP +5)\n"
            "3. 물을 병에 담는다 (하급 체력 포션 획득)"
        )
        choice = input("> ")
        if choice == "1":
            old_hp = player.hp
            player.hp = min(player.hp + 15, calculate_max_hp(player))
            print("샘의 물을 마시자, 당신의 몸에 생기가 돌아온다.")
            print(f"HP + {player.hp - old_hp}")
            return
        if choice == "2":
            player.max_hp += 5
            player.hp += 5
            print("샘에 몸을 담그니, 생기가 당신의 몸으로 흘러들어온다.")
            print("최대 HP + 5")
            return
        if choice == "3":
            potion = next(
                item for item in items
                if item.name == "하급 체력 포션"
            )
            player.items.append(potion)
            print("샘의 물을 병에 담아가기로 했다.")
            print("하급 체력 포션 획득")
            return
            
        print("올바르지 않은 입력")


def event_altar(player):
    while True:
        print(
            "수상한 제단을 발견했다. 어떻게 할까?\n"
            "1. 힘을 원하며 기도한다 (ATK +7, 최대 HP -5)\n"
            "2. 마력을 원하며 기도한다 (MAG +7, 최대 MP -5)\n"
            "3. 제단에 공물을 바친다. (Gold -150, 전 스탯 +2)\n"
            "4. 제단 위의 공물을 챙긴다. (Gold +200, 전 스탯 -2)\n"
            "5. 떠난다"
        )
        choice = input("> ")
        if choice == "1":
            player.attack += 7
            player.max_hp = max(0, player.max_hp - 5)
            player.hp = min(player.hp, calculate_max_hp(player))
            print("수상한 제단에 기도하자, 모독적인 축복이 내려졌다.")
            print("ATK +7, 최대 HP -5")
            return
        if choice == "2":
            player.magic += 7
            player.max_mp = max(0, player.max_mp - 5)
            player.mp = min(player.mp, calculate_max_mp(player))
            print("수상한 제단에 기도하자, 모독적인 축복이 내려졌다.")
            print("MAG +7, 최대 MP -5")
            return
        if choice == "3":
            if player.gold < 150:
                print("골드가 부족하다.")
                continue
            player.gold -= 150
            player.attack += 2
            player.magic += 2
            player.defense += 2
            player.speed += 2
            print("제단에 공물을 바쳤다.")
            print("제단에서 약간의 힘이 흘러들어오는 느낌이 든다.")
            print("Gold -150, 전 스탯 +2")
            return
        if choice == "4":
            player.gold += 200
            player.attack -= 2
            player.magic -= 2
            player.defense -= 2
            player.speed -= 2
            print("제단 위의 공물을 챙겼다.")
            print("그와 동시에 몸에서 힘이 빠져나가는 느낌이 든다...")
            print("Gold +200, 전 스탯 -2")
            return
        if choice == "5":
            print("때로는 신중한 것이 미덕일 때도 있는 법이다.")
            return
        print("올바르지 않은 입력")


def event_vending_machine(player):
    while True:
        print(
            "벽 한가운데, 있을 리 없는 자판기가 놓여 있다.\n"
            "1. 30G를 넣는다 (랜덤 아이템 획득)\n"
            "2. 자판기를 걷어찬다 (무슨 일이 일어날지 모른다)\n"
            "3. 그냥 지나간다\n"
        )
        choice = input("> ")
        if choice == "1":
            if player.gold < 30:
                print("골드가 부족하다.")
                continue
            item = random.choice(items)
            player.items.append(item)
            player.gold -= 30
            player.run_stats["gold_spent"] += 30
            print(f"골드를 넣자, 자판기에서 {item.name}이(가) 나왔다.")
            return
        if choice == "2":
            rand = random.random()
            if rand < 0.25:
                item = random.choice(items)
                player.items.append(item)
                print(f"자판기를 발로 찼더니, 자판기에서 {item.name}이(가) 나왔다.")
                return
            elif rand < 0.5:
                gold = random.randint(50, 80)
                player.gold += gold
                print("자판기를 발로 찼더니, 자판기에서 골드가 떨어졌다")
                print(f"{gold}G 획득!")
                return
            elif rand < 0.7:
                print("자판기를 발로 찼더니 발이 아프다!")
                print("HP -8")
                take_damage(player, 8)
                if player.hp == 0:
                    print("악! 이건 너무 아프다!")
                    print("Game Over")
                    print("다음장...")
                    save_run_log(player, "패배 - 자판기를 걷어차다 사망")
                    input()
                    exit()
                return
            else:
                print("자판기를 발로 찼더니, 자판기가 변신했다!")
                time.sleep(1)
                vending_machine_mimic = Enemy(
                    name="자판기 미믹",
                    max_hp=37,
                    speed=12,
                    attack=7,
                    defense=7,
                    gold=50,
                    action_pool=[
                        Action(
                            name="음료수 발사",
                            effects=[DamageEffect()],
                            mp_cost=0,
                            flavor_text="자판기 미믹은 당신에게 음료수 병을 발사한다!",
                        ),
                        Action(
                            name="",
                            effects=[BlockEffect()],
                            mp_cost=0,
                            flavor_text="자판기 미믹은 음료수 병을 세워 방어한다!",
                        ),
                    ],
                )
                battle(player, [vending_machine_mimic])
                print()
                print(f"{vending_machine_mimic.name}와(과)의 전투를 마쳤다.")
                print()
                print("전투로부터 경험을 얻었다.")
                choose_random_stat_reward(player)
                if random.random() < 0.2:
                    print("적이 특별한 보상을 드랍했다!")
                    choose_equipment_or_skill(player, floor=1)
                return
        if choice == "3":
            print("당신은 수상한 자판기를 무시하고 지나갔다.")
            return
        print("올바르지 않은 입력")


def event_mirror(player):
    while True:
        print(
            "검은 거울에 당신의 모습이 비친다.\n"
            "거울 속의 당신은 훨씬 부드럽게 움직이고 있다.\n"
            "프레임이 최소 두 배는 높아 보인다.\n"
            "\n"
            "1. 해상도를 낮춘다 (SPD +4, 최대 HP -4)\n"
            "2. 이펙트 품질을 낮춘다 (ATK +4, MAG -3)\n"
            "3. 광원 효과를 낮춘다 (MAG +4, DEF -3)\n"
            "4. 타협하지 않는다 (50% 전 스탯 +2 / 50% HP -10)"
        )
        choice = input("> ")
        if choice == "1":
            player.speed += 4
            player.max_hp -= 4
            player.hp = min(player.hp, calculate_max_hp(player))
            print("당신은 해상도를 낮췄다.")
            print("화면은 조금 흐릿해졌지만, 움직임은 눈에 띄게 부드러워졌다.")
            print("SPD +4, 최대 HP -4")
            return
        if choice == "2":
            player.attack += 4
            player.magic -= 3
            print("당신은 이펙트 품질을 낮췄다.")
            print("화려한 연출은 사라졌지만, 공격 타이밍은 훨씬 선명하게 보인다.")
            print("ATK +4, MAG -3")
            return
        if choice == "3":
            player.magic += 4
            player.defense -= 3
            print("당신은 광원 효과를 낮췄다.")
            print("빛은 칙칙해졌지만, 이상하게도 마력의 흐름은 더 또렷하게 느껴진다.")
            print("MAG +4, DEF -3")
            return
        if choice == "4":
            print("당신은 그래픽 옵션과 타협하지 않았다...")
            time.sleep(1)
            if random.random() < 0.5:
                player.attack += 2
                player.magic += 2
                player.speed += 2
                player.defense += 2
                print("거울은 잠시 침묵하더니, 당신의 무모함을 용기라 판단했다.")
                print("ATK, MAG, SPD, DEF +2")
            else:
                take_damage(player, 10)
                print("심한 프레임 드랍으로 인해 정신적 피해를 입었다!")
                print("HP -10")
                if player.hp == 0:
                    print("악! 이건 너무 아프다!")
                    print("Game Over")
                    print("다음장...")
                    save_run_log(player, "패배 - 프레임 드랍을 견디지 못하고 사망")
                    input()
                    exit()
            return
        print("올바르지 않은 입력")


def event_campfire(player):
    while True:
        print(
            "누군가 피워놓은 모닥불을 발견했다.\n"
            "불씨는 아직 따뜻하다. 어떻게 할까?\n"
            "1. 잠시 휴식한다 (HP/MP 회복)\n"
            "2. 재를 뒤져본다 (무언가 발견할 수도 있다)\n"
            "3. 그냥 지나간다"
        )
        choice = input("> ")

        if choice == "1":
            old_hp = player.hp
            old_mp = player.mp

            player.hp = min(player.hp + 10, calculate_max_hp(player))
            player.mp = min(player.mp + 10, calculate_max_mp(player))

            print("모닥불 앞에서 잠시 몸을 녹였다.")
            print(f"HP +{player.hp - old_hp}, MP +{player.mp - old_mp}")
            return

        if choice == "2":
            rand = random.random()
            if rand < 0.5:
                item = random.choice(items)
                player.items.append(item)
                print(f"재 속에서 {item.name}을(를) 발견했다.")

            elif rand < 0.8:
                gold = random.randint(30, 60)
                player.gold += gold
                print(f"타다 남은 주머니에서 {gold}G를 발견했다.")

            else:
                print("재를 한참 뒤져봤지만 쓸 만한 것은 없었다.")
            return

        if choice == "3":
            print("당신은 모닥불을 뒤로하고 계속 나아갔다.")
            return

        print("올바르지 않은 입력")


def event_suspicious_merchant(player):
    while True:
        print(
            "얼굴을 깊이 가린 수상한 상인이 길을 막아섰다.\n"
            '"돈... 또는 다른 것을 받지요."\n'
            "1. 장비를 보여달라고 한다\n"
            "2. 스킬을 보여달라고 한다\n"
            "3. 50G를 넘긴다 (전 스탯 +1)\n"
            "4. 거래하지 않는다"
        )

        choice = input("> ")

        if choice == "1":
            equipment = random.choice(equipments)

            print()
            print("상인은 말없이 천을 걷어 장비 하나를 보여주었다.")
            print(
                f"[{equipment.rarity}] {equipment.name}\n"
                f"{get_equipment_stats(equipment)}"
            )
            print()
            print("1. 최대 HP 5를 대가로 받는다")
            print("2. 거래하지 않는다")

            while True:
                sub_choice = input("> ")

                if sub_choice == "1":
                    if player.max_hp <= 5:
                        print("더 이상 생명력을 대가로 내놓을 수 없다.")
                        return

                    if not equip(player, equipment):
                        print('"마음이 바뀌었나 보군요."')
                        return

                    player.max_hp -= 5
                    player.hp = min(
                        player.hp,
                        calculate_max_hp(player)
                    )

                    print()
                    print("상인은 당신의 생명력을 조금 떼어갔다.")
                    print(f"{equipment.name}을(를) 받았다.")
                    print("최대 HP -5")
                    return

                if sub_choice == "2":
                    print('"필요 없습니까. 그럼 다음 기회에."')
                    return

                print("올바르지 않은 입력")

        if choice == "2":
            skill = random.choice(skills)

            print()
            print("상인은 낮은 목소리로 한 기술에 대해 설명하기 시작했다.")
            print(
                f"[{skill.rarity}] {skill.name}\n"
                f"MP {skill.mp_cost}\n"
                f"{skill.description}"
            )
            print()
            print("1. 최대 MP 5를 대가로 배운다")
            print("2. 거래하지 않는다")

            while True:
                sub_choice = input("> ")

                if sub_choice == "1":
                    if player.max_mp <= 5:
                        print("더 이상 마력을 대가로 내놓을 수 없다.")
                        return

                    if not add_skill(player, skill):
                        print('"마음이 바뀌었나 보군요."')
                        return

                    player.max_mp -= 5
                    player.mp = min(
                        player.mp,
                        calculate_max_mp(player)
                    )

                    print()
                    print("상인이 당신의 마력을 조금 떼어갔다.")
                    print(f"{skill.name}을(를) 배웠다.")
                    print("최대 MP -5")
                    return

                if sub_choice == "2":
                    print('"필요 없습니까. 그럼 다음 기회에."')
                    return

                print("올바르지 않은 입력")

        if choice == "3":
            if player.gold < 50:
                print("골드가 부족하다.")
                continue

            player.gold -= 50
            player.run_stats["gold_spent"] += 50

            player.attack += 1
            player.magic += 1
            player.defense += 1
            player.speed += 1

            print()
            print("당신은 상인에게 50G를 건넸다.")
            print("상인은 만족한 듯 고개를 끄덕였다.")
            print("ATK, MAG, SPD, DEF +1")
            return

        if choice == "4":
            print('"현명한 선택일 수도, 아닐 수도 있지요."')
            print("상인은 웃으며 어둠 속으로 사라졌다.")
            return

        print("올바르지 않은 입력")


def event_training_ground(player):
    while True:
        print(
            "오랫동안 버려진 훈련장을 발견했다.\n"
            "낡았지만 훈련 도구들은 아직 사용할 수 있을 것 같다.\n"
            "1. 허수아비를 공격한다 (ATK 증가)\n"
            "2. 마법진을 연구한다 (MAG 증가)\n"
            "3. 장애물 코스를 달린다 (SPD 증가)\n"
            "4. 방패 훈련을 한다 (DEF 증가)\n"
            "5. 떠난다"
        )

        choice = input("> ")

        if choice == "5":
            print("당신은 훈련장을 뒤로하고 떠났다.")
            return

        stat_map = {
            "1": ("attack", "ATK"),
            "2": ("magic", "MAG"),
            "3": ("speed", "SPD"),
            "4": ("defense", "DEF"),
        }

        if choice not in stat_map:
            print("올바르지 않은 입력")
            continue

        stat, stat_name = stat_map[choice]

        while True:
            print()
            print("어느 정도로 훈련할까?")
            print(f"1. 가볍게 훈련한다. ({stat_name} +2)")
            print(f"2. 혹독하게 훈련한다. ({stat_name} +4, HP -10)")
            print(f"3. 한계까지 몰아붙인다. ({stat_name} +6, HP -20)")
            print("4. 그만둔다")

            intensity = input("> ")

            if intensity == "1":
                setattr(player, stat, getattr(player, stat) + 2)

                print("무리하지 않는 선에서 훈련을 마쳤다.")
                print(f"{stat_name} +2")
                return

            if intensity == "2":
                if player.hp <= 10:
                    print("지금 상태로는 혹독한 훈련을 버틸 수 없을 것 같다.")
                    continue

                setattr(player, stat, getattr(player, stat) + 4)
                player.hp -= 10

                print("몸이 비명을 지를 때까지 훈련을 계속했다.")
                print(f"{stat_name} +4, HP -10")
                return

            if intensity == "3":
                if player.hp <= 20:
                    print("지금 상태로는 한계까지 몰아붙였다간 쓰러질 것 같다.")
                    continue

                setattr(player, stat, getattr(player, stat) + 6)
                player.hp -= 20

                print("몇 번이나 쓰러질 뻔했지만 끝까지 훈련을 마쳤다.")
                print(f"{stat_name} +6, HP -20")
                return

            if intensity == "4":
                print("훈련을 그만두기로 했다.")
                return

            print("올바르지 않은 입력")


def event_locked_chest(player):
    while True:
        print(
            "방 한가운데 놓인 잠긴 보물 상자를 발견했다.\n"
            "표면에는 수많은 칼자국과 발자국이 남아 있다.\n"
            "1. 억지로 연다 (60% 대량의 골드 / 40% HP -10~20)\n"
            "2. 조심스럽게 자물쇠를 만진다 (50% 소량의 골드 / 50% 랜덤 아이템)\n"
            "3. 포기한다"
        )
        choice = input("> ")

        if choice == "1":
            if random.random() < 0.6:
                gold = random.randint(120, 200)
                player.gold += gold
                player.run_stats["gold_earned"] += gold

                print("당신은 힘으로 상자를 뜯어냈다!")
                print(f"상자 안에서 {gold}G를 발견했다.")
            else:
                damage = random.randint(10, 20)
                take_damage(player, damage)

                print("상자를 열려던 순간 숨겨진 화살이 발사되었다!")
                print(f"HP -{damage}")

                if player.hp == 0:
                    print("악! 이건 너무 아프다!")
                    print("Game Over")
                    print("다음장...")
                    save_run_log(player, "패배 - 수상한 상자를 힘으로 열려다 사망")
                    input()
                    exit()
            return

        if choice == "2":
            result = random.random()

            if result < 0.5:
                gold = random.randint(40, 70)
                player.gold += gold
                player.run_stats["gold_earned"] += gold

                print("자물쇠를 조심스럽게 움직이자 상자가 열렸다.")
                print(f"{gold}G를 획득했다.")
            else:
                item = random.choice(items)
                player.items.append(item)

                print("상자 안쪽의 작은 비밀 칸을 발견했다.")
                print(f"{item.name}을(를) 획득했다.")
            return

        if choice == "3":
            print("상자는 분명 함정이다. 아마도. 틀림없이.")
            print("당신은 스스로를 납득시키며 떠났다.")
            return

        print("올바르지 않은 입력")


def event_mushroom(player):
    while True:
        print(
            "형형색색으로 빛나는 버섯 군락을 발견했다.\n"
            "먹어도 되는지는 모르겠지만, 향은 의외로 괜찮다.\n"
            "1. 버섯을 먹는다 (무슨 일이 일어날지 모른다)\n"
            "2. 버섯 군락을 뒤진다 (60% 아이템 / 20% 골드 / 20% 아무것도 없음)\n"
            "3. 건드리지 않는다"
        )
        choice = input("> ")

        if choice == "1":
            result = random.randint(1, 7)

            if result == 1:
                player.max_hp += 6
                player.hp += 6
                print("몸에서 생명력이 넘쳐흐르는 기분이 든다.")
                print("최대 HP +6")

            elif result == 2:
                player.max_mp += 6
                player.mp += 6
                print("머릿속에서 알 수 없는 지식이 속삭인다.")
                print("최대 MP +6")

            elif result == 3:
                player.attack += 4
                print("갑자기 모든 것이 부술 수 있을 것처럼 보인다.")
                print("ATK +4")

            elif result == 4:
                player.magic += 4
                print("손끝에서 작은 불꽃이 피어올랐다.")
                print("MAG +4")

            elif result == 5:
                player.speed += 4
                print("세상이 조금 느리게 움직이는 것 같다.")
                print("SPD +4")

            elif result == 6:
                player.defense += 4
                print("피부가 잠시 버섯처럼 단단해졌다. 좋은 건가?")
                print("DEF +4")

            else:
                damage = roll_dice(4, 10)
                take_damage(player, damage)

                print("입에 넣자마자 치명적인 판단 착오였음을 깨달았다.")
                print(f"HP -4d10 > {damage}")

                if player.hp == 0:
                    print("악! 이건 너무 아프다!")
                    print("Game Over")
                    print("다음장...")
                    save_run_log(player, "패배 - 독버섯을 먹고 4d10 데미지를 받아 사망")
                    input()
                    exit()
            return

        if choice == "2":
            print("당신은 버섯 군락 속을 뒤졌다.")
            
            rand = random.random()
            
            if rand < 0.6:
                item = random.choice(items)
                player.items.append(item)
                print(f"군락 안에서 {item.name}을(를) 획득했다.")
                return
            elif rand < 0.8:
                gold = random.randint(30, 60)
                player.gold += gold
                print(f"군락 안에서 {gold}G를 획득했다.")
                return
            else:
                print("한참 동안 버섯 군락을 뒤졌지만 아무것도 발견하지 못했다...")
                return

        if choice == "3":
            print("모르는 버섯은 먹지 않는 것이 상식이다.")
            print("다행히도, 당신의 안에는 상식이 아직 살아 있었다.")
            return

        print("올바르지 않은 입력")


def event_broken_gpu(player):
    while True:
        print(
            "먼지투성이 받침대 위에 고장 난 그래픽카드가 놓여 있다.\n"
            "팬은 돌지 않지만, 기판에서는 미약한 빛이 새어나온다.\n"
            "1. 50G를 들여 수리한다. (원하는 스탯 +3)\n"
            "2. 쓸 만한 부품을 뜯는다. (Gold 획득, HP 감소)\n"
            "3. 일단 장착해본다. (무슨 일이 일어날지 모른다)\n"
            "4. 건드리지 않는다"
        )

        choice = input("> ")

        if choice == "1":
            if player.gold < 50:
                print("수리 부품을 살 골드가 부족하다.")
                continue

            while True:
                print(
                    "그래픽카드를 어떤 용도로 최적화할까?\n"
                    "1. 물리 연산을 강화한다. (ATK +3)\n"
                    "2. 마법 연산을 강화한다. (MAG +3)\n"
                    "3. 프레임 처리를 강화한다. (SPD +3)\n"
                    "4. 방어 연산을 강화한다. (DEF +3)\n"
                    "5. 수리를 그만둔다"
                )

                sub_choice = input("> ")

                stat_map = {
                    "1": ("attack", "ATK"),
                    "2": ("magic", "MAG"),
                    "3": ("speed", "SPD"),
                    "4": ("defense", "DEF"),
                }

                if sub_choice == "5":
                    break

                if sub_choice not in stat_map:
                    print("올바르지 않은 입력")
                    continue

                stat, stat_name = stat_map[sub_choice]

                player.gold -= 50
                player.run_stats["gold_spent"] += 50
                setattr(
                    player,
                    stat,
                    getattr(player, stat) + 3
                )

                print("수리에 성공했다.")
                print("그래픽카드가 지정된 연산을 보조하기 시작했다.")
                print(f"Gold -50, {stat_name} +3")
                return

            continue

        if choice == "2":
            gold = random.randint(40, 80)
            damage = random.randint(5, 10)

            player.gold += gold
            player.run_stats["gold_earned"] += gold

            hp_damage, blocked_damage = take_damage(
                player,
                damage
            )

            player.run_stats["damage_taken"] += hp_damage
            player.run_stats["damage_blocked"] += blocked_damage

            print("기판에서 값나가 보이는 부품을 뜯어냈다.")
            print(f"부품을 {gold}G에 팔 수 있을 것 같다.")
            print(f"하지만 감전으로 HP에 {hp_damage} 피해를 받았다.")

            if player.hp == 0:
                print("악! 이건 너무 아프다!")
                print("Game Over")
                print("다음장...")
                save_run_log(player, "패배 - 그래픽카드에 목숨을 잃었다. 시대에 걸맞은 최후다.")
                input()
                exit()

            return

        if choice == "3":
            result = random.randint(1, 3)

            if result == 1:
                player.speed += 3
                print("고장 난 그래픽카드를 그대로 장착했다.")
                print("화면 곳곳에 그래픽 오류가 일어나기 시작했다.")
                print("...그런데 프레임만큼은 이상할 정도로 잘 나온다.")
                print("SPD +3")
                return

            elif result == 2:
                player.attack += 4
                player.magic += 4
                player.max_hp = max(1, player.max_hp - 4)
                player.hp = min(player.hp, calculate_max_hp(player))

                print("고장 난 그래픽카드를 그대로 장착했다.")
                print("잠시 후, 그래픽카드가 무시무시한 열을 내뿜기 시작했다.")
                print("몸은 뜨겁게 달아올랐지만, 이상하게도 힘이 넘쳐흐른다.")
                print("ATK +4, MAG +4, 최대 HP -4")
                return

            else:
                print("고장 난 그래픽카드를 그대로 장착했다.")
                print("화면이 몇 번 깜빡이더니 오류 메시지가 떠올랐다.")
                print()
                print("「지원되지 않는 그래픽 장치입니다.」")
                print()
                print("드라이버가 호환되지 않는다.")
                print("아무 일도 일어나지 않았다.")
                return

        if choice == "4":
            print("당신은 그래픽카드를 내려놓았다.")
            print("언젠가는 더 좋은 그래픽카드를 찾을 수 있을 것이다.")
            return

        print("올바르지 않은 입력")


unknown_events_first_floor = [
    event_spring,
    event_altar,
    event_vending_machine,
    event_mirror,
    event_campfire,
    event_suspicious_merchant,
    event_training_ground,
    event_locked_chest,
    event_mushroom,
    event_broken_gpu,
    treasure,
]


def event_alchemist_table(player):
    while True:
        print(
            "먼지가 쌓인 작업대 위에 붉은 약과 푸른 약이 놓여 있다.\n"
            "친절하게도 병에는 각각 「체력 증강제」, 「마력 증강제」라고 적혀 있다.\n"
            "그 아래, 작은 글씨가 보인다.\n"
            "「※ 부작용 있음. 혼용 금지.」\n"
            "1. 빨간 약을 먹는다 (최대 HP +7, 최대 MP -4)\n"
            "2. 파란 약을 먹는다 (최대 MP +7, 최대 HP -4)\n"
            "3. 둘 다 먹는다 (무슨 일이 일어날지 모른다)\n"
            "4. 건드리지 않는다\n"
        )
        choice = input("> ")
        
        if choice == "1":
            player.max_hp += 7
            player.hp += 7
            player.max_mp = max(0, player.max_mp - 4)
            player.mp = min(player.mp, calculate_max_mp(player))
            print("붉은 약을 단숨에 들이켰다.\n 온몸에 힘이 넘쳐흐른다. 대신 머리가 조금 멍해진 것 같다.")
            print("최대 HP +7, 최대 MP -4.")
            break
        
        elif choice == "2":
            player.max_mp += 7
            player.mp += 7
            player.max_hp = max(1, player.max_hp - 4)
            player.hp = min(player.hp, calculate_max_hp(player))
            print("푸른 약을 마시자 머리가 맑아지고 마력이 솟구친다.\n 대신 몸에서 힘이 쭉 빠져나가는 기분이다.")
            print("최대 MP +7, 최대 HP -4.")
            break
        
        elif choice == "3":
            result = random.random()
            
            if result < 0.5:
                player.max_hp += 7
                player.hp += 7
                player.max_mp += 7
                player.mp += 7
                print("「혼용 금지」라고 쓰여 있긴 한데…… 그래서 더 궁금하다.\n두 약을 한꺼번에 들이켰다.\n\n잠시 후, 몸 안에서 엄청난 힘이 솟구친다!")
                print("최대 HP +7, 최대 MP +7.")
                break
            
            elif result < 0.75:
                player.max_hp = max(1, player.max_hp - 4)
                player.max_mp = max(0, player.max_mp - 4)
                player.hp = min(player.hp, calculate_max_hp(player))
                player.mp = min(player.mp, calculate_max_mp(player))
                print("두 약을 한꺼번에 들이켰다.\n......\n서로의 약효가 완벽하게 상쇄된 모양이다.\n아니, 상쇄된 것보다 조금 더 나빠진 것 같다.")
                print("최대 HP -4, 최대 MP -4.")
                break
            
            else:
                damage = roll_dice(2, 10)
                take_damage(player, damage)
                print("두 약을 한꺼번에 들이켰다.\n배 속에서 뭔가가 격렬하게 반응하기 시작한다.\n약병에 쓰인 「혼용 금지」가 이런 뜻이었나?")
                print(f"{damage}의 데미지를 입었다!")
                if player.hp == 0:
                    print("악! 이건 너무 아프다!")
                    print("Game Over")
                    print("다음장...")
                    save_run_log(player, "패배 - 빨간 약과 파란 약을 둘 다 먹어서 사망")
                    input()
                    exit()
                break
                    
        elif choice == "4":
            print("「혼용 금지」라고 친절하게 경고까지 해놨다.\n이런 걸 굳이 먹을 이유는 없을 것이다...")
            break
        
        print("올바르지 않은 입력")


def event_eternal_brazier(player):
    rarity_order = [
        COMMON,
        RARE,
        EPIC,
        LEGENDARY,
    ]

    while True:
        print(
            "방 한가운데 거대한 화로가 놓여 있다.\n"
            "장작도, 석탄도 보이지 않지만 불길은 맹렬하게 타오르고 있다.\n"
            "화로의 가장자리에는 희미한 글씨가 새겨져 있다.\n"
            "\n"
            "「불꽃은 대가 없이 타오르지 않는다.」\n"
            "\n"
            "1. 무기를 불길에 넣는다\n"
            "  (무기 1개를 한 단계 높은 희귀도의 무기 2개 중 하나로 변경)\n"
            "2. 방어구를 불길에 넣는다\n"
            "  (방어구 1개를 한 단계 높은 희귀도의 방어구 2개 중 하나로 변경)\n"
            "3. 반지를 불길에 넣는다\n"
            "  (반지 1개를 한 단계 높은 희귀도의 반지 2개 중 하나로 변경)\n"
            "4. 지나간다"
        )

        choice = input("> ")

        if choice == "4":
            print(
                "대가 없이 타오르지 않는다니.\n"
                "그렇다면 대가를 주지 않으면 그만이다.\n"
                "\n"
                "화로를 뒤로하고 자리를 떠났다."
            )
            return

        equipment_map = {
            "1": player.weapon,
            "2": player.armor,
            "3": player.ring,
        }

        if choice not in equipment_map:
            print("올바르지 않은 입력")
            continue

        current_equipment = equipment_map[choice]

        if current_equipment is None:
            print("불길에 넣을 장비가 없다.")
            continue

        current_rarity = current_equipment.rarity

        if current_rarity not in rarity_order:
            print(
                "장비를 불길 가까이 가져갔지만,\n"
                "화로는 아무런 반응도 보이지 않았다."
            )
            continue

        current_rarity_index = rarity_order.index(current_rarity)

        if current_rarity != LEGENDARY:
            target_rarity = rarity_order[current_rarity_index + 1]

        else:
            target_rarity = LEGENDARY

        candidates = [
            equipment
            for equipment in equipments
            if equipment.slot == current_equipment.slot
            and equipment.rarity == target_rarity
            and equipment is not current_equipment
        ]

        if not candidates:
            print(
                "장비를 불길 속에 넣었지만,\n"
                "불꽃은 잠시 흔들릴 뿐 아무런 변화도 일으키지 않았다.\n"
                "\n"
                "재련할 수 있는 장비가 없는 것 같다."
            )
            continue

        candidate_count = min(2, len(candidates))
        rewards = random.sample(
            candidates,
            candidate_count,
        )

        print()
        print(
            f"[{current_equipment.rarity}] "
            f"{current_equipment.name}을(를) 불길 속에 집어넣었다."
        )
        print()
        print(
            "불길이 장비를 집어삼키자 형태가 녹아내리기 시작한다.\n"
            "잠시 후, 불꽃 속에서 새로운 형태들이 모습을 드러냈다."
        )
        print()

        for i, equipment in enumerate(rewards, start=1):
            print(
                f"{i}. [{equipment.rarity}] {equipment.name}\n"
                f"   {get_equipment_stats(equipment)}"
            )

        print(f"{len(rewards) + 1}. 재련하지 않는다")

        while True:
            sub_choice = input("> ")

            if not sub_choice.isdigit():
                print("올바르지 않은 입력")
                continue

            sub_choice = int(sub_choice)

            if sub_choice == len(rewards) + 1:
                print(
                    "당신은 장비를 불길에서 황급히 꺼냈다.\n"
                    "다행히 아직 원래 모습이 남아 있다."
                )
                return

            if not 1 <= sub_choice <= len(rewards):
                print("올바르지 않은 입력")
                continue

            new_equipment = rewards[sub_choice - 1]

            if new_equipment.slot == "weapon":
                player.weapon = new_equipment

            elif new_equipment.slot == "armor":
                player.armor = new_equipment

            elif new_equipment.slot == "ring":
                player.ring = new_equipment

            player.hp = min(player.hp, calculate_max_hp(player))
            player.mp = min(player.mp, calculate_max_mp(player))

            print()
            print(
                f"{current_equipment.name}의 형태가 완전히 녹아 사라졌다."
            )
            print(
                "그 자리에 불꽃으로 단련된 새로운 장비가 남았다."
            )
            print()
            print(
                f"[{current_equipment.rarity}] "
                f"{current_equipment.name}"
            )
            print("↓")
            print(
                f"[{new_equipment.rarity}] "
                f"{new_equipment.name}"
            )

            return


def event_vampire_coffin(player):
    vampire_inside = random.random() < 0.5

    while True:
        print(
            "방 한가운데, 검붉은 나무로 만들어진 관 하나가 놓여 있다.\n"
            "관 뚜껑에는 은으로 된 문양이 새겨져 있고,\n"
            "틈새에서는 희미하게 붉은 빛이 새어나온다.\n"
            "\n"
            "……누가 봐도 열면 안 될 것처럼 생겼다.\n"
            "\n"
            "1. 관을 연다 (무슨 일이 일어날지 모른다)\n"
            "2. 관에 말뚝을 박는다 (무슨 일이 일어날지 모른다)\n"
            "3. 그냥 지나간다"
        )

        choice = input("> ")

        if choice == "1":
            print(
                "조심스럽게 관 뚜껑을 밀어 올렸다.\n"
                "\n"
                "끼이이익..."
            )

            if not vampire_inside:
                gold = random.randint(100, 200)

                player.gold += gold
                player.run_stats["gold_earned"] += gold

                print(
                    "관 안에는 시체 대신 금화가 가득 들어 있었다.\n"
                    "\n"
                    "……흡혈귀는 어디 갔지?\n"
                    f"\nGold +{gold}."
                )
                return

            print(
                "관 뚜껑을 열자 붉은 눈이 하나, 둘, 셋 떠올랐다.\n"
                "......잠깐.\n"
                "생각보다 많은데?"
            )

            time.sleep(1)

            vampires = [deepcopy(next(
                    enemy
                    for enemy in enemies_second_floor
                    if enemy.name == "흡혈귀"
                )) for _ in range(3)
            ]

            battle(player, vampires)

            print()
            print("흡혈귀들과의 전투를 마쳤다.")
            print()
            print("전투로부터 경험을 얻었다.")

            choose_random_stat_reward(player)

            print()
            print("흡혈귀의 관 안에서 전리품을 발견했다!")
            choose_equipment_or_skill(
                player,
                floor=2
            )

            return

        if choice == "2":
            print(
                "어디선가 적당한 말뚝을 찾아\n"
                "관 한가운데에 힘껏 박아 넣었다.\n"
                "\n"
                "쾅!"
            )

            time.sleep(1)

            if vampire_inside:
                gold = random.randint(50, 150)

                player.gold += gold
                player.run_stats["gold_earned"] += gold

                print(
                    "\n관 안쪽에서 끔찍한 비명이 터져 나왔다.\n"
                    "\n"
                    "잠시 후, 관 안은 조용해졌다.\n"
                    "조심스럽게 뚜껑을 열어보니\n"
                    "검은 재와 함께 금화가 흩어져 있다.\n"
                    "\n"
                    f"Gold +{gold}."
                )
                return

            print(
                "\n…….\n"
                "\n"
                "아무 일도 일어나지 않는다.\n"
                "\n"
                "조심스럽게 관을 열어보니 안은 텅 비어 있다.\n"
                "괜히 멀쩡한 관에 말뚝만 박은 것 같다."
            )
            return

        if choice == "3":
            print(
                "누가 봐도 수상한 관이다.\n"
                "굳이 열어서 안에 뭐가 들었는지 확인할 필요는 없다.\n"
                "\n"
                "호기심보다 목숨이 중요하다."
            )
            return

        print("올바르지 않은 입력")


def event_dud_bomb(player):
    while True:
        print(
            "복도 한가운데, 시커멓게 그을린 폭탄 하나가 굴러다니고 있다.\n"
            "도화선은 타다 말았고, 몸체에서는 희미하게 연기가 피어오른다.\n"
            "\n"
            "……아마도 불발탄인 것 같다.\n"
            "\n"
            "1. 조심스럽게 해체한다 (고블린 폭탄 획득)\n"
            "2. 걷어찬다 (무슨 일이 일어날지 모른다)\n"
            "3. 그냥 지나간다"
        )

        choice = input("> ")

        if choice == "1":
            bomb = next(
                item for item in items
                if item.name == "고블린 폭탄"
            )

            player.items.append(bomb)

            print(
                "조심스럽게 도화선을 제거하고 폭탄을 분해했다.\n"
                "다행히 폭발하지 않았다.\n"
                "\n"
                "……이 정도면 다시 써먹을 수 있을 것 같다.\n"
                "\n"
                "고블린 폭탄을 획득했다."
            )
            break

        elif choice == "2":
            print(
                "일단 걷어찼다.\n"
                "\n"
                "깡!"
            )

            result = random.random()

            if result <= 0.5:
                print(
                    "폭탄은 복도 저편까지 데굴데굴 굴러갔다.\n"
                    "\n"
                    "……아무 일도 일어나지 않았다."
                )

            elif result <= 0.7:
                damage = roll_dice(4, 10) + 5
                take_damage(player, damage)

                print(
                    "잠시 뒤.\n"
                    "\n"
                    "콰아앙!!\n"
                    "\n"
                    "역시 불발탄이라고 해서 영원히 불발인 것은 아니었다.\n"
                    "\n"
                    f"HP -4d10+5 > {damage}."
                )

                if player.hp == 0:
                    print("악! 이건 너무 아프다!")
                    print("Game Over")
                    print("다음장...")
                    save_run_log(
                        player,
                        "패배 - 불발탄을 걷어찼다가 폭사"
                    )
                    input()
                    exit()

            else:
                gold = random.randint(250, 400)
                player.gold += gold

                print(
                    "폭탄이 벽에 부딪히며 폭발했다.\n"
                    "\n"
                    "콰아앙!!\n"
                    "\n"
                    "폭발한 벽 안쪽에서 숨겨져 있던 금화가 쏟아져 나왔다.\n"
                    "\n"
                    "……이게 왜 되지?\n"
                    f"\nGold +{gold}."
                )

            break

        elif choice == "3":
            print(
                "불발탄이라지만 굳이 가까이 갈 이유는 없다.\n"
                "\n"
                "폭탄을 피해 조심스럽게 지나갔다."
            )
            break

        print("올바르지 않은 입력")


def event_cursed_armory(player):
    rarity_cost = {
        RARE: 4,
        EPIC: 7,
        LEGENDARY: 10,
    }

    available_equipments = [
        equipment
        for equipment in equipments
        if equipment.rarity in rarity_cost
    ]

    equipment = random.choice(available_equipments)
    hp_cost = rarity_cost[equipment.rarity]

    while True:
        print(
            "녹슨 철문 너머로 오래된 무기고가 모습을 드러냈다.\n"
            "대부분의 장비는 썩거나 부서져 있지만,\n"
            "그중 하나만은 이상할 정도로 깨끗한 상태를 유지하고 있다.\n"
            "\n"
            f"[{equipment.rarity}] {equipment.name}\n"
            f"{equipment.flavor_text}\n"
            "\n"
            "장비에서는 불길한 기운이 흘러나온다.\n"
            "이걸 가져가면 분명 대가를 치르게 될 것 같다.\n"
            "\n"
            f"1. 그래도 집는다 (최대 HP -{hp_cost})\n"
            "2. 아무것도 건드리지 않고 떠난다"
        )

        choice = input("> ")

        if choice == "1":
            old_equipment = None

            if isinstance(equipment, Weapon):
                old_equipment = player.weapon
                player.weapon = equipment

            elif isinstance(equipment, Armor):
                old_equipment = player.armor
                player.armor = equipment

            elif isinstance(equipment, Ring):
                old_equipment = player.ring
                player.ring = equipment

            else:
                print("알 수 없는 장비다.")
                return

            player.max_hp = max(1, player.max_hp - hp_cost)
            player.hp = min(player.hp, calculate_max_hp(player))
            player.mp = min(player.mp, calculate_max_mp(player))

            print(
                f"{equipment.name}을(를) 집어 들었다.\n"
                "순간 검은 기운이 손끝을 타고 몸 안으로 스며든다.\n"
                "\n"
                f"{old_equipment.name} → {equipment.name}\n"
                f"최대 HP -{hp_cost}."
            )
            return

        elif choice == "2":
            print(
                "이상할 정도로 멀쩡한 장비.\n"
                "거기에 대놓고 풍기는 불길한 기운까지.\n"
                "\n"
                "굳이 위험을 감수할 필요는 없다.\n"
                "아무것도 건드리지 않고 무기고를 빠져나왔다."
            )
            return

        print("올바르지 않은 입력")


def event_suspicious_break_room(player):
    while True:
        print(
            "문을 열자 작은 휴게실이 나타났다.\n"
            "\n"
            "푹신해 보이는 소파.\n"
            "적당히 시원한 물이 나오는 정수기.\n"
            "탁자 위에는 먹어도 될 것 같은 과자까지 놓여 있다.\n"
            "\n"
            "함정도, 괴물도, 수상한 마법진도 보이지 않는다.\n"
            "\n"
            "……수상할 정도로 평범하다.\n"
            "\n"
            "1. 소파에서 쉰다. (최대 HP/MP의 25% 회복)\n"
            "2. 정수기의 물을 마신다. (최대 MP의 50% 회복)\n"
            "3. 과자를 먹는다. (최대 HP의 50% 회복)\n"
            "4. 수상하니 그냥 나간다"
        )

        choice = input("> ")

        if choice == "1":
            max_hp = calculate_max_hp(player)
            max_mp = calculate_max_mp(player)

            old_hp = player.hp
            old_mp = player.mp

            player.hp = min(
                player.hp + max_hp // 4,
                max_hp
            )
            player.mp = min(
                player.mp + max_mp // 4,
                max_mp
            )

            print(
                "조심스럽게 소파에 몸을 눕혔다.\n"
                "……………….\n"
                "아무 일도 일어나지 않았다.\n"
                "\n"
                "푹 쉬었다.\n"
                f"HP +{player.hp - old_hp}, MP +{player.mp - old_mp}."
            )
            return

        elif choice == "2":
            max_mp = calculate_max_mp(player)
            old_mp = player.mp

            player.mp = min(
                player.mp + max_mp // 2,
                max_mp
            )

            print(
                "정수기에서 물을 받아 조심스럽게 한 모금 마셨다.\n"
                "……평범한 물이다.\n"
                "한 모금 더 마셔봤다.\n"
                "역시 평범한 물이다.\n"
                "\n"
                f"MP +{player.mp - old_mp}."
            )
            return

        elif choice == "3":
            max_hp = calculate_max_hp(player)
            old_hp = player.hp

            player.hp = min(
                player.hp + max_hp // 2,
                max_hp
            )

            print(
                "과자 봉지를 뜯어 하나 집어 먹었다.\n"
                "바삭하다.\n"
                "적당히 짭짤하다.\n"
                "……그리고 그게 전부다.\n"
                "\n"
                f"HP +{player.hp - old_hp}."
            )
            return

        elif choice == "4":
            print(
                "아무리 봐도 이상하다.\n"
                "던전 한복판에 이렇게 멀쩡한 휴게실이 있을 리 없다.\n"
                "분명 뭔가 있다. 뭔지는 모르겠지만.\n"
                "\n"
                "끝까지 경계를 늦추지 않은 채 휴게실을 빠져나왔다.\n"
                "\n"
                "아무 일도 일어나지 않았다."
            )
            return

        print("올바르지 않은 입력")


def event_suspicious_exe(player):
    while True:
        print(
            "어두운 방 한가운데, 낡은 컴퓨터 한 대가 켜져 있다.\n"
            "모니터의 바탕화면에는 파일 하나만 덩그러니 놓여 있다.\n"
            "\n"
            "[무료_스탯_상승.exe]\n"
            "\n"
            "★ 다운로드 수: 8,391,204\n"
            "★ 만족도: 5.0 / 5.0\n"
            "★ 바이러스 없음!\n"
            "★ 관리자 권한 필요\n"
            "\n"
            "1. 실행한다 (무슨 일이 일어날지 모른다)\n"
            "2. 파일 정보를 확인한다\n"
            "3. 컴퓨터를 끈다"
        )

        choice = input("> ")

        if choice == "1":
            print(
                "무료_스탯_상승.exe를 실행했다.\n"
                "\n"
                "[이 앱이 디바이스를 변경할 수 있도록 허용하시겠습니까?]\n"
                "\n"
                "당연히 허용했다."
            )
            time.sleep(1)

            result = random.random()
            stat = random.choice(["attack", "magic", "speed", "defense"])

            stat_names = {
                "attack": "ATK",
                "magic": "MAG",
                "speed": "SPD",
                "defense": "DEF",
            }

            if result <= 0.5:
                setattr(player, stat, getattr(player, stat) + 4)

                print(
                    "\n설치가 완료되었습니다!\n"
                    "놀랍게도 진짜 효과가 있는 프로그램이었다.\n"
                    "\n"
                    f"{stat_names[stat]} +4."
                )

            elif result <= 0.7:
                setattr(
                    player,
                    stat,
                    max(0, getattr(player, stat) - 2)
                )

                print(
                    "\n설치 도중 알 수 없는 오류가 발생했습니다.\n"
                    "\n"
                    "뭔가 몸 상태가 전보다 나빠진 것 같다.\n"
                    "\n"
                    f"{stat_names[stat]} -2."
                )

            elif result <= 0.9:
                stolen_gold = min(player.gold, random.randint(100, 150))
                player.gold -= stolen_gold

                print(
                    "\n설치가 완료되었습니다!\n"
                    "\n"
                    "[프리미엄 서비스 결제가 완료되었습니다.]\n"
                    "\n"
                    "……결제?\n"
                    f"\nGold -{stolen_gold}."
                )

            else:
                setattr(player, stat, getattr(player, stat) + 7)

                print(
                    "\n축하합니다!\n"
                    "[프리미엄 버전이 활성화되었습니다.]\n"
                    "\n"
                    "온몸에 엄청난 힘이 솟구친다!\n"
                    "\n"
                    f"{stat_names[stat]} +7"
                )

            break

        elif choice == "2":
            print(
                "파일 정보를 확인했다.\n"
                "\n"
                "이름: 무료_스탯_상승.exe\n"
                "게시자: 알 수 없음\n"
                "크기: 4 KB\n"
                "마지막 수정일: 1970-01-01\n"
                "\n"
                "……확실히 믿음직스럽다."
            )
            input()
            continue

        elif choice == "3":
            print(
                "컴퓨터를 종료했다.\n"
                "\n"
                "종료 중……\n"
                "잠시 후 모니터가 조용히 꺼졌다.\n"
                "\n"
                "아무 일도 일어나지 않았다."
            )
            break

        print("올바르지 않은 입력")


def event_rgb_altar(player):
    while True:
        print(
            "방 한가운데, 게이밍 PC 한 대가 제단처럼 모셔져 있다.\n"
            "본체, 키보드, 마우스, 심지어 책상 밑까지 온갖 색으로 번쩍이고 있다.\n"
            "\n"
            "모니터에는 문구 하나가 떠 있다.\n"
            "\n"
            "「RGB가 많을수록 성능이 향상된다.」\n"
            "— 고대 컴퓨터 공학자의 가르침\n"
            "\n"
            "1. RGB를 더 장착한다. (Gold -50, SPD +2)\n"
            "2. 모든 RGB를 최대로 켠다. (Gold -150, SPD +6)\n"
            "3. RGB를 전부 뜯어낸다. (Gold +100, SPD -2)\n"
            "4. 그냥 지나간다"
        )

        choice = input("> ")

        if choice == "1":
            if player.gold < 50:
                print(
                    "제단에 금화를 넣으려 했지만 자금이 부족하다.\n"
                    "\n"
                )
                continue

            player.gold -= 50
            player.run_stats["gold_spent"] += 50
            player.speed += 2

            print(
                "제단에 금화를 넣자 어디선가 LED 스트립이 튀어나왔다.\n"
                "적당히 빈 곳에 붙였다.\n"
                "\n"
                "형형색색의 빛이 몸을 감싼다.\n"
                "\n"
                "……진짜로 빨라졌다.\n"
                "\n"
                "Gold -50, SPD +2."
            )
            return

        elif choice == "2":
            if player.gold < 150:
                print(
                    "모든 RGB를 최대로 켜기에는 자금이 부족하다.\n"
                    "\n"
                    "최고의 성능에는 최고의 투자가 필요한 법이다."
                )
                continue

            player.gold -= 150
            player.run_stats["gold_spent"] += 150
            player.speed += 6

            print(
                "금화를 제단에 쏟아붓고 모든 조명을 최대로 설정했다.\n"
                "\n"
                "위이이이잉――\n"
                "\n"
                "방 전체가 무지갯빛으로 물든다.\n"
                "본체와 주변기기에서 쏟아지는 빛 때문에 눈을 뜨기조차 힘들다.\n"
                "\n"
                "……그런데 성능은 확실히 향상되었다.\n"
                "아니, 생각보다 훨씬 많이 향상되었다.\n"
                "\n"
                "Gold -150, SPD +6."
            )
            return

        elif choice == "3":
            player.speed = max(0, player.speed - 2)
            player.gold += 100
            player.run_stats["gold_earned"] += 100

            print(
                "LED 스트립과 RGB 팬을 하나씩 뜯어냈다.\n"
                "\n"
                "……생각보다 중고가가 괜찮다.\n"
                "\n"
                "본체는 처참할 정도로 밋밋해졌다.\n"
                "그리고 정말로 성능도 떨어졌다.\n"
                "\n"
                "Gold +100, SPD -2."
            )
            return

        elif choice == "4":
            print(
                "RGB가 많다고 성능이 좋아질 리가 없다.\n"
                "상식적으로 생각하면 당연한 일이다.\n"
                "\n"
                "제단을 무시하고 지나갔다.\n"
                "\n"
                "등 뒤에서 RGB 팬이 서운한 듯 천천히 회전했다."
            )
            return

        print("올바르지 않은 입력")


def event_rampaging_magic_crystal(player):
    while True:
        print(
            "방 한가운데, 거대한 푸른 수정 하나가 공중에 떠 있다.\n"
            "수정 내부에서는 마력이 번개처럼 튀며 요동치고 있다.\n"
            "\n"
            "가까이 다가가기만 해도 머리카락이 곤두선다.\n"
            "……아무래도 안정된 물건은 아닌 것 같다.\n"
            "\n"
            "1. 수정에 손을 댄다. (HP -8, SPD +3)\n"
            "2. 수정에 마력을 주입한다. (MP -10, MAG +3)\n"
            "3. 수정의 힘을 무기에 흘려보낸다. (HP -5, ATK +3)\n"
            "4. 수정을 부순다. (Gold 획득)\n"
            "5. 그냥 지나간다"
        )

        choice = input("> ")

        if choice == "1":
            hp_damage, blocked_damage = take_damage(player, 8)

            player.run_stats["damage_taken"] += hp_damage
            player.run_stats["damage_blocked"] += blocked_damage

            player.speed += 3

            print(
                "조심스럽게 수정에 손을 가져다 댔다.\n"
                "\n"
                "파직――!\n"
                "\n"
                "폭주하던 마력이 온몸을 훑고 지나갔다.\n"
                "근육과 신경이 강제로 깨어나는 듯한 감각이 느껴진다.\n"
                "\n"
                "몸은 아프지만, 움직임은 이전보다 훨씬 빨라졌다.\n"
                "\n"
                f"HP -{hp_damage}, SPD +3."
            )

            if player.hp == 0:
                print("악! 이건 너무 아프다!")
                print("Game Over")
                print("다음장...")
                save_run_log(
                    player,
                    "패배 - 마력 폭주 수정을 만졌다가 감전사"
                )
                input()
                exit()

            return

        elif choice == "2":
            if player.mp < 10:
                print(
                    "수정에 마력을 흘려넣으려 했지만 마력이 부족하다.\n"
                    "\n"
                    "수정이 더 내놓으라는 듯 불길하게 번쩍였다."
                )
                continue

            player.mp -= 10
            player.magic += 3

            print(
                "수정을 향해 마력을 흘려넣었다.\n"
                "\n"
                "요동치던 수정이 마력을 집어삼키며 더욱 밝게 빛난다.\n"
                "잠시 후, 정제된 마력 일부가 몸 안으로 되돌아왔다.\n"
                "\n"
                "양은 줄었지만, 이전보다 훨씬 강한 힘이 느껴진다.\n"
                "\n"
                "MP -10, MAG +3."
            )
            return

        elif choice == "3":
            hp_damage, blocked_damage = take_damage(player, 5)

            player.run_stats["damage_taken"] += hp_damage
            player.run_stats["damage_blocked"] += blocked_damage

            player.attack += 3

            print(
                "무기를 수정 가까이 가져갔다.\n"
                "\n"
                "파지직――!\n"
                "\n"
                "푸른 마력이 무기를 타고 흘러들어가며 날카롭게 번쩍인다.\n"
                "그 순간 역류한 마력이 손끝을 태우듯 스쳐 지나갔다.\n"
                "\n"
                "무기는 한층 강해졌지만, 손은 꽤 아프다.\n"
                "\n"
                f"HP -{hp_damage}, ATK +3."
            )

            if player.hp == 0:
                print("악! 이건 너무 아프다!")
                print("Game Over")
                print("다음장...")
                save_run_log(
                    player,
                    "패배 - 마력 폭주 수정의 힘을 무기에 흘려보내다 사망"
                )
                input()
                exit()

            return

        elif choice == "4":
            gold = random.randint(100, 180)

            player.gold += gold
            player.run_stats["gold_earned"] += gold

            print(
                "이 위험한 물건을 계속 내버려두는 것보다는 부수는 편이 낫겠다.\n"
                "\n"
                "수정을 힘껏 내려쳤다.\n"
                "\n"
                "쨍그랑――!\n"
                "\n"
                "산산조각 난 수정 사이에서 반짝이는 결정 조각들을 발견했다.\n"
                "쓸모는 모르겠지만, 꽤 비싸게 팔릴 것 같다.\n"
                "\n"
                f"Gold +{gold}."
            )
            return

        elif choice == "5":
            print(
                "폭주하는 마력에 굳이 손을 댈 이유는 없다.\n"
                "\n"
                "수정이 계속 불길하게 번쩍이는 가운데,\n"
                "조용히 방을 빠져나왔다."
            )
            return

        print("올바르지 않은 입력")


def event_old_spellbook(player):
    if not player.skills:
        print(
            "낡은 독서대 위에 두꺼운 마법서 한 권이 펼쳐져 있다.\n"
            "책에서는 희미한 마력이 느껴지지만,\n"
            "대가로 바칠 만한 지식이 없다.\n"
            "\n"
            "아무것도 하지 못하고 책을 덮었다."
        )
        return

    rarity_order = [
        COMMON,
        RARE,
        EPIC,
        LEGENDARY,
    ]

    print(
        "방 한가운데 놓인 낡은 독서대 위에\n"
        "두꺼운 마법서 한 권이 펼쳐져 있다.\n"
        "\n"
        "대부분의 글자는 지워져 있지만,\n"
        "몇몇 구절만은 이상할 정도로 선명하게 읽힌다.\n"
        "\n"
        "책을 읽기 위해서는 이미 알고 있는 지식 하나를\n"
        "대가로 바쳐야 할 것 같다.\n"
        "(스킬 1개를 한 단계 높은 희귀도의 스킬 2개 중 하나로 변경)"
    )

    while True:
        print("\n어떤 스킬을 잊겠습니까?\n")

        for i, skill in enumerate(player.skills, start=1):
            print(
                f"{i}. [{skill.rarity}] {skill.name}"
            )

        print(f"{len(player.skills) + 1}. 책을 덮는다")

        choice = input("> ")

        if choice == str(len(player.skills) + 1):
            print(
                "굳이 멀쩡한 기억을 지워가며 읽을 필요는 없다.\n"
                "마법서를 조용히 덮었다."
            )
            return

        if not choice.isdigit():
            print("올바르지 않은 입력")
            continue

        skill_index = int(choice) - 1

        if not 0 <= skill_index < len(player.skills):
            print("올바르지 않은 입력")
            continue

        old_skill = player.skills[skill_index]

        if old_skill.rarity not in rarity_order:
            print(
                "이 스킬은 마법서에 바칠 수 없는 종류의 지식이다."
            )
            continue

        old_rarity_index = rarity_order.index(old_skill.rarity)

        if old_skill.rarity != LEGENDARY:
            target_rarity = rarity_order[old_rarity_index + 1]

        else:
            target_rarity = LEGENDARY

        candidates = [
            skill
            for skill in skills
            if skill.rarity == target_rarity
            and skill not in player.skills
        ]

        if not candidates:
            print(
                "마법서가 몇 번 빛을 내더니 조용해졌다.\n"
                "새롭게 얻을 수 있는 지식이 없는 것 같다."
            )
            return

        candidate_count = min(2, len(candidates))

        rewards = random.sample(
            candidates,
            candidate_count,
        )

        print(
            f"\n[{old_skill.rarity}] {old_skill.name}에 대한 기억을 "
            "마법서에 바치려 한다.\n"
            "\n"
            "책장이 저절로 넘어가며 새로운 구절들이 떠오른다.\n"
        )

        for i, skill in enumerate(rewards, start=1):
            print(
                f"{i}. [{skill.rarity}] {skill.name}\n"
                f"   MP {skill.mp_cost}\n"
                f"   {skill.description}"
            )

        print(f"{len(rewards) + 1}. 그만둔다")

        while True:
            sub_choice = input("> ")

            if not sub_choice.isdigit():
                print("올바르지 않은 입력")
                continue

            sub_choice = int(sub_choice)

            if sub_choice == len(rewards) + 1:
                print(
                    "마지막 순간 책에서 손을 뗐다.\n"
                    "\n"
                    f"{old_skill.name}에 대한 기억은 아직 남아 있다."
                )
                return

            if not 1 <= sub_choice <= len(rewards):
                print("올바르지 않은 입력")
                continue

            new_skill = rewards[sub_choice - 1]

            player.skills[skill_index] = new_skill

            print(
                f"\n{old_skill.name}에 대한 기억이 머릿속에서 흐려진다.\n"
                "\n"
                "마법서의 글자들이 검게 타오르더니,\n"
                "사라진 지식의 빈자리에 새로운 지식이 새겨졌다.\n"
                "\n"
                f"[{old_skill.rarity}] {old_skill.name}\n"
                "↓\n"
                f"[{new_skill.rarity}] {new_skill.name}\n"
                "\n"
                f"{new_skill.name}을(를) 습득했다!"
            )

            return


unknown_events_second_floor = [
    event_alchemist_table,
    event_eternal_brazier,
    event_vampire_coffin,
    event_dud_bomb,
    event_cursed_armory,
    event_suspicious_break_room,
    event_suspicious_exe,
    event_rgb_altar,
    event_rampaging_magic_crystal,
    event_old_spellbook,
    treasure,
]


def event_blackjack(player):
    starting_gold = player.gold

    def draw_card():
        return random.randint(1, 10)

    def hand_value(cards):
        value = sum(cards)

        # 1을 A로 취급
        if 1 in cards and value + 10 <= 21:
            value += 10

        return value

    def display_cards(cards):
        return [
            "A" if card == 1 else card
            for card in cards
        ]

    def display_card(card):
        return "A" if card == 1 else card

    def record_blackjack_result():
        gold_change = player.gold - starting_gold

        if gold_change > 0:
            player.run_stats["gold_earned"] += gold_change
        elif gold_change < 0:
            player.run_stats["gold_spent"] += -gold_change

    while True:
        min_bet = 50
        max_bet = min(player.gold, 500)

        print(
            "붉은 카펫이 깔린 방 안쪽에 작은 카드 테이블이 놓여 있다.\n"
            "테이블 너머에는 얼굴을 검은 천으로 가린 딜러가 앉아 있다.\n"
            "\n"
            "딜러는 말없이 카드를 섞더니 손을 내민다.\n"
            "\n"
            "「판돈을 걸어라.」\n"
            f"\n현재 골드: {player.gold}G\n"
            f"최소 판돈: {min_bet}G\n"
            f"최대 판돈: {max_bet}G\n"
            "\n"
            "0. 그만둔다"
        )

        choice = input("> ")

        if not choice.isdigit():
            print("올바르지 않은 입력")
            continue

        bet = int(choice)

        if bet == 0:
            print("당신은 카드 테이블을 뒤로하고 방을 떠났다.")
            return

        if player.gold < min_bet:
            print(
                f"최소 판돈인 {min_bet}G조차 가지고 있지 않다.\n"
                "딜러가 말없이 당신을 바라본다."
            )
            continue

        if bet < min_bet:
            print(f"최소 판돈은 {min_bet}G다.")
            continue

        if bet > max_bet:
            print(f"한 판에 걸 수 있는 최대 판돈은 {max_bet}G다.")
            continue

        player.gold -= bet

        player_cards = [
            draw_card(),
            draw_card(),
        ]

        dealer_cards = [
            draw_card(),
            draw_card(),
        ]

        print()
        print(f"{bet}G를 걸었다.")
        print()
        print("---------------------------------------------")
        print()

        player_blackjack = hand_value(player_cards) == 21
        dealer_blackjack = hand_value(dealer_cards) == 21

        if player_blackjack:
            print(
                f"당신의 카드: "
                f"{display_cards(player_cards)} "
                f"= {hand_value(player_cards)}"
            )
            print("블랙잭!")

            if dealer_blackjack:
                print(
                    f"딜러의 카드: "
                    f"{display_cards(dealer_cards)} "
                    f"= {hand_value(dealer_cards)}"
                )
                print("딜러도 블랙잭이다.")
                print("무승부.")

                player.gold += bet
                print(f"{bet}G를 돌려받았다.")

                record_blackjack_result()
                time.sleep(1.5)
                return

            reward = bet * 3
            player.gold += reward

            print(f"{reward}G를 획득했다!")
            record_blackjack_result()
            time.sleep(1.5)
            return

        while True:
            print(
                f"당신의 카드: "
                f"{display_cards(player_cards)} "
                f"= {hand_value(player_cards)}"
            )

            print(
                f"딜러의 카드: "
                f"[{display_card(dealer_cards[0])}, ?]"
            )

            print()
            print("1. 한 장 더 받는다")
            print("2. 멈춘다")

            choice = input("> ")

            if choice == "1":
                card = draw_card()
                player_cards.append(card)

                print()
                print(
                    f"{display_card(card)}을(를) 받았다."
                )

                if hand_value(player_cards) > 21:
                    print(
                        f"당신의 카드: "
                        f"{display_cards(player_cards)} "
                        f"= {hand_value(player_cards)}"
                    )
                    print("버스트!")
                    print(f"{bet}G를 잃었다...")

                    time.sleep(1.5)
                    record_blackjack_result()
                    return

            elif choice == "2":
                break

            else:
                print("올바르지 않은 입력")

        print()
        print("------------- 딜러의 차례 -------------")
        print()

        print(
            f"딜러의 카드: "
            f"{display_cards(dealer_cards)} "
            f"= {hand_value(dealer_cards)}"
        )

        while hand_value(dealer_cards) < 17:
            card = draw_card()
            dealer_cards.append(card)

            print(
                f"딜러가 {display_card(card)}을(를) 받았다."
            )

            print(
                f"딜러의 카드: "
                f"{display_cards(dealer_cards)} "
                f"= {hand_value(dealer_cards)}"
            )

            time.sleep(1)

        player_score = hand_value(player_cards)
        dealer_score = hand_value(dealer_cards)

        print()

        if dealer_score > 21:
            print("딜러 버스트!")
            reward = bet * 2

        elif player_score > dealer_score:
            print("승리!")
            reward = bet * 2

        elif player_score == dealer_score:
            print("무승부.")

            player.gold += bet
            print(f"{bet}G를 돌려받았다.")

            time.sleep(1.5)
            record_blackjack_result()
            return

        else:
            print("패배.")
            reward = 0

        if reward > 0:
            player.gold += reward
            print(f"{reward}G를 획득했다!")

        else:
            print(f"{bet}G를 잃었다.")

        record_blackjack_result()
        time.sleep(1.5)
        return


def event_vending_machine_v2(player):
    print(
        "어딘가 익숙하게 생긴 자판기가 놓여 있다.\n"
        "이번에는 상품 진열창이 검게 가려져 있다.\n"
        "\n"
        "「VENDING MACHINE Mk.2」\n"
        "\n"
        "1. 100G를 넣는다 (패키지 구매)\n"
        "2. 걷어찬다 (무슨 일이 일어날지 모른다)\n"
        "3. 무시한다"
    )

    while True:
        choice = input("> ")

        if choice == "1":
            if player.gold < 100:
                print("골드가 부족하다.")
                continue

            print(
                "\n상품 종류를 선택하십시오.\n"
                "1. 신체 강화 패키지\n"
                "2. 마력 강화 패키지\n"
                "3. 생존 패키지\n"
                "4. 취소"
            )

            sub_choice = input("> ")

            if sub_choice == "4":
                continue

            if sub_choice not in ["1", "2", "3"]:
                print("올바르지 않은 입력")
                continue

            player.gold -= 100
            player.run_stats["gold_spent"] += 100

            if sub_choice == "1":
                stat = random.choice(
                    ["attack", "speed", "defense"]
                )

                stat_names = {
                    "attack": "ATK",
                    "speed": "SPD",
                    "defense": "DEF",
                }

                setattr(
                    player,
                    stat,
                    getattr(player, stat) + 3
                )

                print(
                    "\n기계 내부에서 무언가 굉음을 내며 작동한다.\n"
                    "잠시 후 작은 캡슐 하나가 배출구로 떨어졌다.\n"
                    "\n"
                    "복용하자 몸이 눈에 띄게 강화되었다.\n"
                    "\n"
                    f"{stat_names[stat]} +3!"
                )

            elif sub_choice == "2":
                result = random.randint(1, 2)

                if result == 1:
                    player.magic += 3

                    print(
                        "\n푸른색 병 하나가 배출구로 떨어졌다.\n"
                        "마시는 순간 머릿속이 맑아지고 마력이 선명해진다.\n"
                        "\n"
                        "MAG +3!"
                    )

                else:
                    player.max_mp += 7
                    player.mp += 7

                    print(
                        "\n빛나는 액체가 담긴 병 하나가 떨어졌다.\n"
                        "마시는 순간 몸 안에 마력이 가득 차오른다.\n"
                        "\n"
                        "최대 MP +7!"
                    )

            elif sub_choice == "3":
                result = random.randint(1, 2)

                if result == 1:
                    player.max_hp += 7
                    player.hp += 7

                    print(
                        "\n붉은색 캡슐 하나가 배출구로 떨어졌다.\n"
                        "복용하자 몸이 한층 튼튼해진 느낌이 든다.\n"
                        "\n"
                        "최대 HP +7!"
                    )

                else:
                    item = random.choice(items)
                    player.items.append(item)

                    print(
                        "\n덜컹.\n"
                        "배출구에서 예상하지 못한 물건 하나가 떨어졌다.\n"
                        "\n"
                        f"{item.name}을(를) 획득했다!"
                    )

            return

        elif choice == "2":
            print("자판기를 힘껏 걷어찼다.")

            result = random.randint(1, 4)

            if result == 1:
                gold = random.randint(100, 150)
                player.gold += gold
                player.run_stats["gold_earned"] += gold

                print(
                    f"자판기에서 {gold}G가 쏟아져 나왔다!"
                )

            elif result == 2:
                item = random.choice(items)
                player.items.append(item)

                print(
                    f"{item.name}이(가) 떨어졌다!"
                )

            elif result == 3:
                hp_damage, blocked_damage = take_damage(
                    player,
                    10
                )

                player.run_stats["damage_taken"] += hp_damage
                player.run_stats["damage_blocked"] += blocked_damage

                print(
                    "어째서인지 자판기가 폭발했다!\n"
                    f"HP -{hp_damage}."
                )

                if player.hp == 0:
                    print("악! 이건 너무 아프다!")
                    print("Game Over")
                    print("다음장...")

                    save_run_log(
                        player,
                        "패배 - 자판기를 걷어찼다가 폭사"
                    )

                    input()
                    exit()

            elif result == 4:
                print(
                    "자판기를 발로 찼더니,\n"
                    "자판기가 요란한 경고음을 내며 변신했다!"
                )

                time.sleep(1)

                vending_machine_mimic_v2 = Enemy(
                    name="자판기 미믹 Ver.2",
                    max_hp=75,
                    speed=16,
                    attack=13,
                    defense=12,
                    gold=120,
                    action_pool=[
                        Action(
                            name="고속 음료수 발사",
                            effects=[
                                DamageEffect(
                                    power=1.2,
                                    stat="attack",
                                    dice_count=1,
                                    dice_sides=6,
                                )
                            ],
                            mp_cost=0,
                            flavor_text=(
                                "자판기 미믹 Ver.2는 "
                                "고속으로 음료수 병을 발사한다!"
                            ),
                        ),
                        Action(
                            name="상품 진열 방어",
                            effects=[
                                BlockEffect(
                                    power=1.5,
                                    stat="defense",
                                    flat=5,
                                )
                            ],
                            mp_cost=0,
                            flavor_text=(
                                "자판기 미믹 Ver.2는 "
                                "상품 진열대를 닫아 공격을 막는다!"
                            ),
                        ),
                        Action(
                            name="재고 떨이",
                            effects=[
                                DamageEffect(
                                    power=0.4,
                                    stat="attack",
                                    dice_count=1,
                                    dice_sides=3,
                                ),
                                DamageEffect(
                                    power=0.4,
                                    stat="attack",
                                    dice_count=1,
                                    dice_sides=3,
                                ),
                                DamageEffect(
                                    power=0.4,
                                    stat="attack",
                                    dice_count=1,
                                    dice_sides=3,
                                ),
                            ],
                            mp_cost=0,
                            flavor_text=(
                                "자판기 미믹 Ver.2가 "
                                "남아 있는 재고를 마구잡이로 쏟아낸다!"
                            ),
                        ),
                    ],
                )

                battle(
                    player,
                    [vending_machine_mimic_v2]
                )

                print()
                print(
                    f"{vending_machine_mimic_v2.name}와(과)의 전투를 마쳤다."
                )
                print()
                print("전투로부터 경험을 얻었다.")

                choose_random_stat_reward(player)

                if random.random() < 0.3:
                    print(
                        "적이 특별한 보상을 드랍했다!"
                    )

                    choose_equipment_or_skill(
                        player,
                        floor=3
                    )

            return

        elif choice == "3":
            print(
                "수상한 자판기를 무시하고 지나갔다."
            )
            return

        else:
            print("올바르지 않은 입력")


def event_wishing_fountain(player):
    def check_death():
        if player.hp <= 0:
            print("악! 이건 너무 아프다!")
            print("Game Over")
            print("다음장...")
            save_run_log(
                player,
                "패배 - 소원의 분수에 너무 많은 생명력을 바쳐 사망"
            )
            input()
            exit()

    while True:
        print(
            "기묘할 정도로 맑은 물이 고인 분수를 발견했다.\n"
            "수면을 들여다보자, 어디선가 목소리가 들려온다.\n"
            "\n"
            "「원하는 것을 말해라.」\n"
            "\n"
            "1. 힘을 원한다 (ATK +1, HP -5)\n"
            "2. 마력을 원한다 (MAG +1, HP -5)\n"
            "3. 속도를 원한다 (SPD +1, HP -5)\n"
            "4. 강인함을 원한다 (DEF +1, HP -5)\n"
            "5. 부를 원한다 (Gold +50, HP -5)\n"
            "6. 여기서 나가고 싶은데요? (HP -5)"
        )

        choice = input("> ")

        if choice == "1":
            player.hp = max(0, player.hp - 5)
            player.attack += 1
            print("HP -5!")
            print("ATK +1!")
            check_death()

        elif choice == "2":
            player.hp = max(0, player.hp - 5)
            player.magic += 1
            print("HP -5!")
            print("MAG +1!")
            check_death()

        elif choice == "3":
            player.hp = max(0, player.hp - 5)
            player.speed += 1
            print("HP -5!")
            print("SPD +1!")
            check_death()

        elif choice == "4":
            player.hp = max(0, player.hp - 5)
            player.defense += 1
            print("HP -5!")
            print("DEF +1!")
            check_death()

        elif choice == "5":
            player.hp = max(0, player.hp - 5)
            player.gold += 50
            player.run_stats["gold_earned"] += 50
            print("HP -5!")
            print("Gold +50!")
            check_death()

        elif choice == "6":
            player.hp = max(0, player.hp - 5)
            print("HP -5!")
            check_death()

            print()
            print("「...저쪽이다.」")
            print("목소리가 가리킨 방향으로 방을 빠져나왔다.")
            return

        else:
            print("올바르지 않은 입력")


def event_bloody_grail(player):
    while True:
        print(
            "어두운 제단 위에 붉은 액체가 가득 담긴 성배가 놓여 있다.\n"
            "가까이 다가가자, 성배 안에서 낮은 목소리가 울려 퍼진다.\n"
            "\n"
            "「생명을 바쳐 생명을 얻고, 생명을 빌려 생명을 되찾으라.」\n"
            "\n"
            "1. 성배에 생명을 바친다. "
            "(HP -15, MP -5 / 최대 HP +7, 최대 MP +3)\n"
            "2. 성배의 생명을 받아들인다. "
            "(최대 HP -7, 최대 MP -3 / HP·MP 완전 회복)\n"
            "3. 피를 힘으로 바꾼다. "
            "(최대 HP -5, 최대 MP -5, ATK +4, MAG +4)\n"
            "4. 성배를 건드리지 않는다."
        )

        choice = input("> ")

        if choice == "1":
            if player.hp <= 15 or player.mp < 5:
                print(
                    "성배에 바칠 생명과 마력이 부족하다."
                )
                continue

            player.hp -= 15
            player.mp -= 5

            player.max_hp += 7
            player.max_mp += 3

            print(
                "성배가 당신의 생명과 마력을 빨아들인다.\n"
                "\n"
                "잠시 후, 텅 빈 자리를 메우듯 새로운 생명력이 몸 안에 자리잡는다.\n"
                "\n"
                "HP -15, MP -5\n"
                "최대 HP +7, 최대 MP +3"
            )
            return

        elif choice == "2":
            if player.max_hp <= 7 or player.max_mp < 3:
                print(
                    "성배가 요구하는 대가를 감당할 수 없다."
                )
                continue

            player.max_hp = max(1, player.max_hp - 7)
            player.max_mp = max(0, player.max_mp - 3)

            player.hp = calculate_max_hp(player)
            player.mp = calculate_max_mp(player)

            print(
                "성배의 붉은 액체를 들이켰다.\n"
                "\n"
                "상처가 순식간에 아물고, 메말랐던 마력이 다시 차오른다.\n"
                "하지만 몸 어딘가가 영원히 비어버린 듯한 기분이 든다.\n"
                "\n"
                "최대 HP -7, 최대 MP -3\n"
                "HP와 MP를 모두 회복했다!"
            )
            return

        elif choice == "3":
            if player.max_hp <= 5:
                print(
                    "더 이상 성배에 바칠 생명력이 없다."
                )
                continue
            if player.max_mp <= 5:
                print(
                    "더 이상 성배에 바칠 마력이 없다."
                )
                continue

            player.max_hp = max(1, player.max_hp - 5)
            player.max_mp = max(1, player.max_mp - 5)
            player.hp = min(player.hp, calculate_max_hp(player))
            player.mp = min(player.mp, calculate_max_mp(player))
            player.attack += 4
            player.magic += 4

            print(
                "성배의 붉은 액체를 한 모금 들이켰다.\n"
                "\n"
                "뜨거운 피가 온몸을 타고 흐르는 듯한 감각이 퍼진다.\n"
                "생명 일부가 깎여나간 대신, 몸에는 거친 힘이 넘쳐흐른다.\n"
                "\n"
                "최대 HP -5, 최대 MP -5, ATK +4, MAG +4"
            )
            return

        elif choice == "4":
            print(
                "불길한 성배에 손대지 않고 제단을 떠났다."
            )
            return

        else:
            print("올바르지 않은 입력")


def event_emergency_clinic(player):
    print(
        "낡은 문을 열자 작은 응급 치료실이 나타났다.\n"
        "대부분의 장비는 망가져 있지만,\n"
        "비상 전력으로 아직 한 번 정도는 치료 장비를 작동시킬 수 있을 것 같다.\n"
        "\n"
        "1. 집중 치료를 받는다. (HP 완전 회복)\n"
        "2. 마력 안정화 처치를 받는다. (MP 완전 회복)\n"
        "3. 응급 처치를 받는다. (HP/MP 40% 회복)\n"
        "4. 남아 있는 의료 물품을 챙긴다.\n"
        "5. 그냥 나간다."
    )

    while True:
        choice = input("> ")

        if choice == "1":
            old_hp = player.hp
            player.hp = calculate_max_hp(player)

            print(
                "남아 있는 치료 장비를 작동시켰다.\n"
                "기계음과 함께 치료가 시작된다.\n"
                "\n"
                f"HP +{player.hp - old_hp}.\n"
                "\n"
                "치료가 끝나자 비상 전력이 완전히 소진되었다."
            )
            return

        elif choice == "2":
            old_mp = player.mp
            player.mp = calculate_max_mp(player)

            print(
                "마력 안정화 장치를 작동시켰다.\n"
                "희미한 빛이 몸을 감싸며 흐트러진 마력을 정돈한다.\n"
                "\n"
                f"MP +{player.mp - old_mp}.\n"
                "\n"
                "처치가 끝나자 비상 전력이 완전히 소진되었다."
            )
            return

        elif choice == "3":
            max_hp = calculate_max_hp(player)
            max_mp = calculate_max_mp(player)

            old_hp = player.hp
            old_mp = player.mp

            player.hp = min(
                player.hp + int(max_hp * 0.4),
                max_hp
            )
            player.mp = min(
                player.mp + int(max_mp * 0.4),
                max_mp
            )

            print(
                "남아 있는 장비를 최대한 활용해 응급 처치를 받았다.\n"
                "\n"
                f"HP +{player.hp - old_hp}, MP +{player.mp - old_mp}.\n"
                "\n"
                "처치가 끝나자 비상 전력이 완전히 소진되었다."
            )
            return

        elif choice == "4":
            medical_items = [
                item for item in items
                if "체력 포션" in item.name
            ]

            if not medical_items:
                print(
                    "치료실을 뒤져봤지만 쓸 만한 의료 물품은 남아 있지 않았다."
                )
                return

            item_1 = random.choice(medical_items)
            item_2 = random.choice(medical_items)

            player.items.append(item_1)
            player.items.append(item_2)

            print(
                "서랍과 보관함을 뒤져 남아 있는 의료 물품을 챙겼다.\n"
                "\n"
                f"{item_1.name} 획득!\n"
                f"{item_2.name} 획득!"
            )
            return

        elif choice == "5":
            print(
                "아직 쓸 수 있는 장비가 남아 있지만,\n"
                "지금 당장은 필요하지 않을 것 같다.\n"
                "\n"
                "치료실을 뒤로하고 방을 나섰다."
            )
            return

        else:
            print("올바르지 않은 입력")


def event_living_mirror(player):
    rarity_order = [
        COMMON,
        RARE,
        EPIC,
        LEGENDARY,
    ]

    print(
        "방 한쪽 벽을 가득 채운 거대한 거울을 발견했다.\n"
        "거울 앞에 서자, 비친 모습이 당신과는 다른 표정으로 이쪽을 바라본다.\n"
        "\n"
        "잠시 후, 거울 속의 당신이 먼저 입을 열었다.\n"
        "\n"
        "「마음에 들지 않는 게 있나?」\n"
        "\n"
        "1. 기술이 마음에 들지 않는다.\n"
        "  (스킬 1개를 한 단계 높은 희귀도의 스킬 3개 중 하나로 변경)\n"
        "2. 장비가 마음에 들지 않는다.\n"
        "  (장비 1개를 한 단계 높은 희귀도의 장비 3개 중 하나로 변경)\n"
        "3. 내가 마음에 들지 않는다. (스탯 1개 -5, 다른 스탯 1개 +5)\n"
        "4. 네가 마음에 들지 않는다. (전투)"
    )

    while True:
        choice = input("> ")

        if choice == "1":
            if not player.skills:
                print("「...기술이 없는데?」")
                continue

            print()
            print("어떤 기술이 마음에 들지 않습니까?")

            for i, skill in enumerate(player.skills, start=1):
                print(
                    f"{i}. [{skill.rarity}] {skill.name}"
                )

            print(f"{len(player.skills) + 1}. 그만둔다")

            while True:
                skill_choice = input("> ")

                if skill_choice == str(len(player.skills) + 1):
                    print("「그럼 됐어.」")
                    return

                if not skill_choice.isdigit():
                    print("올바르지 않은 입력")
                    continue

                skill_index = int(skill_choice) - 1

                if not 0 <= skill_index < len(player.skills):
                    print("올바르지 않은 입력")
                    continue

                old_skill = player.skills[skill_index]

                if old_skill.rarity not in rarity_order:
                    print("이 기술은 거울로 바꿀 수 없는 것 같다.")
                    continue

                rarity_index = rarity_order.index(old_skill.rarity)

                if old_skill.rarity == LEGENDARY:
                    target_rarity = LEGENDARY
                else:
                    target_rarity = rarity_order[rarity_index + 1]

                candidates = [
                    skill
                    for skill in skills
                    if skill.rarity == target_rarity
                    and skill not in player.skills
                ]

                if not candidates:
                    print(
                        "거울이 잠시 일렁였지만 아무 일도 일어나지 않았다.\n"
                        "바꿀 수 있는 기술이 없는 것 같다."
                    )
                    return

                rewards = random.sample(
                    candidates,
                    min(3, len(candidates))
                )

                print()
                print("거울 속의 당신이 손을 내민다.")
                print(
                    f"「그럼, [{old_skill.rarity}] {old_skill.name} 대신 "
                    "어떤 네가 되고 싶지?」"
                )
                print()

                for i, skill in enumerate(rewards, start=1):
                    print(
                        f"{i}. [{skill.rarity}] {skill.name}\n"
                        f"   MP {skill.mp_cost}\n"
                        f"   {skill.description}"
                    )

                print(f"{len(rewards) + 1}. 그만둔다")

                while True:
                    new_choice = input("> ")

                    if not new_choice.isdigit():
                        print("올바르지 않은 입력")
                        continue

                    new_choice = int(new_choice)

                    if new_choice == len(rewards) + 1:
                        print("「마음이 바뀌었나 보네.」")
                        return

                    if not 1 <= new_choice <= len(rewards):
                        print("올바르지 않은 입력")
                        continue

                    new_skill = rewards[new_choice - 1]
                    player.skills[skill_index] = new_skill

                    print()
                    print(
                        "거울 속의 당신이 손을 뻗는다.\n"
                        "머릿속에서 익숙한 기술 하나가 흐릿해진다."
                    )
                    print()
                    print(
                        f"[{old_skill.rarity}] {old_skill.name}\n"
                        "↓\n"
                        f"[{new_skill.rarity}] {new_skill.name}"
                    )
                    print()
                    print(f"{new_skill.name}을(를) 습득했다!")

                    return

        elif choice == "2":
            current_equipments = [
                player.weapon,
                player.armor,
                player.ring,
            ]

            print()
            print("어떤 장비가 마음에 들지 않습니까?")

            for i, equipment in enumerate(current_equipments, start=1):
                if equipment is None:
                    print(f"{i}. 없음")
                else:
                    stats = get_equipment_stats(equipment)

                    print(
                        f"{i}. [{equipment.rarity}] {equipment.name}"
                        f" - {stats}"
                    )

            print("4. 그만둔다")

            while True:
                equipment_choice = input("> ")

                if equipment_choice == "4":
                    print("「그럼 됐어.」")
                    return

                if equipment_choice not in ("1", "2", "3"):
                    print("올바르지 않은 입력")
                    continue

                old_equipment = current_equipments[
                    int(equipment_choice) - 1
                ]

                if old_equipment is None:
                    print("그 슬롯에는 장비가 없다.")
                    continue

                if old_equipment.rarity not in rarity_order:
                    print("이 장비는 거울로 바꿀 수 없는 것 같다.")
                    continue

                rarity_index = rarity_order.index(
                    old_equipment.rarity
                )

                if old_equipment.rarity == LEGENDARY:
                    target_rarity = LEGENDARY
                else:
                    target_rarity = rarity_order[
                        rarity_index + 1
                    ]

                candidates = [
                    equipment
                    for equipment in equipments
                    if equipment.slot == old_equipment.slot
                    and equipment.rarity == target_rarity
                    and equipment is not old_equipment
                ]

                if not candidates:
                    print(
                        "거울이 잠시 일렁였지만 아무 일도 일어나지 않았다.\n"
                        "바꿀 수 있는 장비가 없는 것 같다."
                    )
                    return

                rewards = random.sample(
                    candidates,
                    min(3, len(candidates))
                )

                print()
                print(
                    "거울 속의 장비가 여러 모습으로 뒤틀리기 시작한다."
                )
                print()

                for i, equipment in enumerate(rewards, start=1):
                    stats = get_equipment_stats(equipment)

                    print(
                        f"{i}. [{equipment.rarity}] "
                        f"{equipment.name}\n"
                        f"   {stats}\n"
                        f"   {equipment.flavor_text}"
                    )

                print(f"{len(rewards) + 1}. 그만둔다")

                while True:
                    new_choice = input("> ")

                    if not new_choice.isdigit():
                        print("올바르지 않은 입력")
                        continue

                    new_choice = int(new_choice)

                    if new_choice == len(rewards) + 1:
                        print("「마음이 바뀌었나 보네.」")
                        return

                    if not 1 <= new_choice <= len(rewards):
                        print("올바르지 않은 입력")
                        continue

                    new_equipment = rewards[
                        new_choice - 1
                    ]

                    if new_equipment.slot == "weapon":
                        player.weapon = new_equipment

                    elif new_equipment.slot == "armor":
                        player.armor = new_equipment

                    elif new_equipment.slot == "ring":
                        player.ring = new_equipment

                    player.hp = min(
                        player.hp,
                        calculate_max_hp(player)
                    )
                    player.mp = min(
                        player.mp,
                        calculate_max_mp(player)
                    )

                    print()
                    print(
                        "거울 속의 장비가 새로운 모습으로 굳어진다.\n"
                        "잠시 후, 당신이 들고 있던 장비도 같은 모습으로 변했다."
                    )
                    print()
                    print(
                        f"[{old_equipment.rarity}] "
                        f"{old_equipment.name}"
                    )
                    print("↓")
                    print(
                        f"[{new_equipment.rarity}] "
                        f"{new_equipment.name}"
                    )

                    return

        elif choice == "3":
            stat_map = {
                "1": ("attack", "ATK"),
                "2": ("magic", "MAG"),
                "3": ("speed", "SPD"),
                "4": ("defense", "DEF"),
            }

            print()
            print("거울 속의 당신이 고개를 기울인다.")
            print()
            print("「어떤 부분이 마음에 안 드는데?」")
            print()
            print("낮출 능력치를 선택하십시오.")
            print("1. ATK")
            print("2. MAG")
            print("3. SPD")
            print("4. DEF")
            print("5. 그만둔다")

            while True:
                down_choice = input("> ")

                if down_choice == "5":
                    print("「그럼 됐어.」")
                    return

                if down_choice not in stat_map:
                    print("올바르지 않은 입력")
                    continue

                down_stat, down_name = stat_map[down_choice]

                if getattr(player, down_stat) < 5:
                    print(
                        f"{down_name}은(는) 5만큼 낮출 수 없다."
                    )
                    continue

                break

            print()
            print("올릴 능력치를 선택하십시오.")

            for key, (stat, name) in stat_map.items():
                if stat == down_stat:
                    continue

                print(f"{key}. {name}")

            print("5. 그만둔다")

            while True:
                up_choice = input("> ")

                if up_choice == "5":
                    print("「마음이 바뀌었나 보네.」")
                    return

                if up_choice not in stat_map:
                    print("올바르지 않은 입력")
                    continue

                up_stat, up_name = stat_map[up_choice]

                if up_stat == down_stat:
                    print(
                        "같은 능력치를 낮추고 올릴 수는 없다."
                    )
                    continue

                break

            setattr(
                player,
                down_stat,
                getattr(player, down_stat) - 5
            )
            setattr(
                player,
                up_stat,
                getattr(player, up_stat) + 5
            )

            print()
            print(
                "거울 속의 모습이 천천히 일그러진다.\n"
                "잠시 후, 조금 다른 모습의 당신이 이쪽을 바라보고 있다."
            )
            print()
            print(
                f"{down_name} -5, {up_name} +5."
            )

            return

        elif choice == "4":
            print()
            print("「...그래?」")
            time.sleep(2)
            print()
            print("거울 속의 당신이 천천히 웃는다.")
            print()
            print("「나도 그래.」")
            time.sleep(1)
            print()
            print(
                "순간 거울 표면이 크게 일그러지더니,\n"
                "거대한 거울이 벽에서 떨어져 스스로 움직이기 시작했다!"
            )
            time.sleep(1)

            living_mirror = Enemy(
                name="살아있는 거울",
                max_hp=90,
                speed=18,
                attack=14,
                defense=14,
                gold=150,
                action_pool=[
                    Action(
                        name="거울 파편",
                        effects=[
                            DamageEffect(
                                power=1.2,
                                stat="attack",
                                dice_count=1,
                                dice_sides=6,
                            )
                        ],
                        mp_cost=0,
                        flavor_text=(
                            "살아있는 거울이 날카로운 파편을 쏘아낸다!"
                        ),
                    ),
                    Action(
                        name="반사광",
                        effects=[
                            DamageEffect(
                                power=0.7,
                                stat="attack",
                                dice_count=1,
                                dice_sides=4,
                            ),
                            DamageEffect(
                                power=0.7,
                                stat="attack",
                                dice_count=1,
                                dice_sides=4,
                            ),
                        ],
                        mp_cost=0,
                        flavor_text=(
                            "거울 표면에서 눈부신 빛이 두 갈래로 반사된다!"
                        ),
                    ),
                    Action(
                        name="거울 방패",
                        effects=[
                            BlockEffect(
                                power=1.5,
                                stat="defense",
                                flat=5,
                            ),
                            AddStatusEffect(
                                status_class=CounterStatus,
                                status_kwargs={},
                                target_type="self",
                            )
                        ],
                        mp_cost=0,
                        flavor_text=(
                            "살아있는 거울의 표면이 단단하게 굳어진다!"
                        ),
                    ),
                ],
            )

            battle(player, [living_mirror])

            print()
            print("살아있는 거울이 산산조각 났다.")
            print()
            print("전투로부터 경험을 얻었다.")
            choose_random_stat_reward(player)

            print()
            print("깨진 거울 속에서 무언가가 모습을 드러냈다.")
            choose_equipment_or_skill(
                player,
                floor=3
            )

            return

        else:
            print("올바르지 않은 입력")


def event_cheat_console(player):
    print(
        "방 한쪽에 오래된 컴퓨터가 놓여 있다.\n"
        "화면에는 검은 창 하나만 떠 있다.\n"
        "\n"
        "DUNGEON ADMINISTRATOR CONSOLE\n"
        'Type "help" for available commands.'
    )

    admin_reward_used = False

    while True:
        print()
        command = input("> ").strip().lower()

        if command == "":
            continue

        elif command == "help":
            print(
                "\nAvailable commands:\n"
                "help\n"
                "god\n"
                "heal\n"
                "boost [stat]\n"
                "give potion\n"
                "give gold\n"
                "exit\n"
                "shutdown\n"
            )

        elif command == "god":
            print("\nGod is currently not here.")

        elif command == "sudo god":
            print("\nRequesting administrator privileges...")
            time.sleep(1)
            print("Access denied.")
            print()
            print("Reason: User is not God.")

        elif command == "heal":
            if admin_reward_used:
                print("\nAdministrator privilege has expired.")
                continue

            old_hp = player.hp
            old_mp = player.mp

            player.hp = calculate_max_hp(player)
            player.mp = calculate_max_mp(player)

            admin_reward_used = True

            print("\nExecuting heal...")
            print(
                f"HP +{player.hp - old_hp}, "
                f"MP +{player.mp - old_mp}!"
            )
            print("\nAdministrator privilege has expired.")

        elif command == "boost":
            print("\nUsage: boost [atk/mag/spd/def]")

        elif command.startswith("boost "):
            if admin_reward_used:
                print("\nAdministrator privilege has expired.")
                continue

            stat_name = command[6:].strip()

            stat_map = {
                "atk": ("attack", "ATK"),
                "mag": ("magic", "MAG"),
                "spd": ("speed", "SPD"),
                "def": ("defense", "DEF"),
            }

            if stat_name not in stat_map:
                print(
                    f'\nUnknown stat: "{stat_name}"\n'
                    "Usage: boost [atk/mag/spd/def]"
                )
                continue

            stat, display_name = stat_map[stat_name]

            setattr(
                player,
                stat,
                getattr(player, stat) + 4
            )

            admin_reward_used = True

            print(f"\nExecuting boost {stat_name}...")
            print(f"{display_name} +4!")
            print("\nAdministrator privilege has expired.")

        elif command == "give":
            print("\nUsage: give [item]")

        elif command == "give potion":
            if admin_reward_used:
                print("\nAdministrator privilege has expired.")
                continue

            potions = [
                item
                for item in items
                if "포션" in item.name
            ]

            if not potions:
                print('\nItem "potion" not found.')
                continue

            rewards = [
                random.choice(potions)
                for _ in range(3)
            ]

            for item in rewards:
                player.items.append(item)

            admin_reward_used = True

            print("\nDispensing items...")

            for item in rewards:
                print(f"{item.name} 획득!")

            print("\nAdministrator privilege has expired.")

        elif command == "give gold":
            if admin_reward_used:
                print("\nAdministrator privilege has expired.")
                continue

            gold = 200

            player.gold += gold
            player.run_stats["gold_earned"] += gold

            admin_reward_used = True

            print("\nExecuting give gold...")
            print(f"Gold +{gold}!")
            print("\nAdministrator privilege has expired.")

        elif command.startswith("give "):
            item_name = command[5:].strip()

            print(
                f'\nItem "{item_name}" not found.'
            )

        elif command == "exit":
            print("\nConsole terminated.")
            print("컴퓨터 화면이 꺼졌다.")
            return

        elif command == "shutdown":
            print(
                "\nWARNING: This command will terminate the dungeon."
            )
            print("Continue? (y/n)")

            choice = input("> ").strip().lower()

            if choice != "y":
                print("\nShutdown cancelled.")
                continue

            print("\nUnsaved progress will be lost.")
            print("Are you sure? (y/n)")

            choice = input("> ").strip().lower()

            if choice != "y":
                print("\nShutdown cancelled.")
                continue

            print("\n진짜로? (y/n)")

            choice = input("> ").strip().lower()

            if choice != "y":
                print("\nShutdown cancelled.")
                continue

            print("\nTerminating dungeon.exe...")
            time.sleep(1)
            sys.exit(0)

        else:
            print(f"\nUnknown command: {command}")


def event_suspicious_installer(player):
    print(
        "방 한쪽에 오래된 컴퓨터가 놓여 있다.\n"
        "화면에는 알 수 없는 프로그램의 설치 화면이 떠 있다.\n"
        "\n"
        "DungeonEnhancer Setup Wizard\n"
        "\n"
        "이 프로그램은 당신의 던전 탐험 경험을 향상시킵니다.\n"
        "\n"
        "1. 빠른 설치 (권장)\n"
        "2. 사용자 지정 설치\n"
        "3. 취소"
    )

    while True:
        choice = input("> ")

        # 빠른 설치
        if choice == "1":
            print()
            print("권장 설정으로 설치를 시작합니다...")
            time.sleep(1)

            stat = random.choice(
                ["attack", "magic", "speed", "defense"]
            )

            stat_names = {
                "attack": "ATK",
                "magic": "MAG",
                "speed": "SPD",
                "defense": "DEF",
            }

            setattr(
                player,
                stat,
                getattr(player, stat) + 4
            )

            ad_count = 8
            player.hp = max(0, player.hp - ad_count)

            print()
            print("DungeonEnhancer 설치 완료!")
            print(f"{stat_names[stat]} +4!")
            print()
            print("추가 프로그램 8개가 설치되었습니다.")
            print("이런, 전부 악질 광고 프로그램이다!")
            print(f"짜증이 밀려온다. HP -{ad_count}.")
            if player.hp == 0:
                print("악! 이건 너무 아프다!")
                print("Game Over")
                save_run_log(player, "패배 - 악성 광고 프로그램에 시달리다 사망")
                input()
                exit()
            return

        elif choice == "2":
            programs = [
                {
                    "name": "플레이어 스탯 향상 프로그램",
                    "real": True,
                },
                {
                    "name": "FREE GOLD 100% REAL",
                    "real": False,
                },
                {
                    "name": "Goblin Search Toolbar",
                    "real": False,
                },
                {
                    "name": "Download More RAM",
                    "real": False,
                },
                {
                    "name": "Hot Goblins In Your Area",
                    "real": False,
                },
                {
                    "name": "Dungeon Shopping Assistant",
                    "real": False,
                },
                {
                    "name": "Free Potion Downloader",
                    "real": False,
                },
                {
                    "name": "Premium Dungeon Security",
                    "real": False,
                },
                {
                    "name": "Recommended Offers",
                    "real": False,
                },
            ]

            random.shuffle(programs)
            checked = [True] * len(programs)
            while True:
                print()
                print("설치할 구성 요소를 선택하십시오.")
                print()

                for i, program in enumerate(programs):
                    mark = "X" if checked[i] else " "
                    print(
                        f"[{mark}] {i + 1}. "
                        f"{program['name']}"
                    )

                print()
                print(
                    "숫자를 입력하여 선택/해제하십시오."
                )
                print("0. 설치")

                custom_choice = input("> ").strip()
                if custom_choice == "0":
                    break
                if not custom_choice.isdigit():
                    print("올바르지 않은 입력")
                    continue
                index = int(custom_choice) - 1
                if not 0 <= index < len(programs):
                    print("올바르지 않은 입력")
                    continue
                checked[index] = not checked[index]

            selected_programs = [
                program
                for program, is_checked in zip(
                    programs, checked
                )
                if is_checked
            ]

            print()
            print("설치를 시작합니다...")
            time.sleep(1)
            print()

            real_installed = any(
                program["real"]
                for program in selected_programs
            )

            ad_count = sum(
                1
                for program in selected_programs
                if not program["real"]
            )

            if real_installed:
                while True:
                    print()
                    print("향상할 능력치를 선택하십시오.")
                    print("1. ATK")
                    print("2. MAG")
                    print("3. SPD")
                    print("4. DEF")

                    stat_choice = input("> ")

                    stat_map = {
                        "1": ("attack", "ATK"),
                        "2": ("magic", "MAG"),
                        "3": ("speed", "SPD"),
                        "4": ("defense", "DEF"),
                    }

                    if stat_choice not in stat_map:
                        print("올바르지 않은 입력")
                        continue

                    stat, stat_name = stat_map[stat_choice]

                    setattr(
                        player,
                        stat,
                        getattr(player, stat) + 4
                    )

                    print()
                    print("DungeonEnhancer 설치 완료!")
                    print(f"{stat_name} +4!")
                    break

            if ad_count > 0:
                player.hp = max(
                    0,
                    player.hp - ad_count
                )

                print()
                print(
                    f"광고 프로그램 {ad_count}개가 함께 설치되었다."
                )
                print(
                    f"짜증이 밀려온다. HP -{ad_count}."
                )
                if player.hp == 0:
                    print("악! 이건 너무 아프다!")
                    print("Game Over")
                    save_run_log(player, "패배 - 악성 광고 프로그램에 시달리다 사망")
                    input()
                    exit()

            if not selected_programs:
                print(
                    "아무것도 설치하지 않았다."
                )

            elif not real_installed and ad_count > 0:
                print()
                print(
                    "정작 필요한 프로그램은 설치하지 않았다."
                )

            return

        elif choice == "3":
            print()
            print("설치를 취소합니다...")
            time.sleep(0.5)
            print("설치가 취소되었습니다.")
            return

        else:
            print("올바르지 않은 입력")


def event_fairy_feast(player):
    print(
        "화려한 음식으로 가득한 긴 식탁을 발견했다.\n"
        "손바닥만 한 요정들이 식탁 위를 날아다니며 떠들썩하게 연회를 벌이고 있다.\n"
        "\n"
        "당신을 발견한 요정 하나가 손을 흔든다.\n"
        "\n"
        "「손님이다! 하나 먹고 가!」\n"
        "\n"
        "1. 버섯 케이크를 먹는다. "
        "(최대 HP +12, DEF +2, SPD -2)\n"
        "2. 별빛 술을 마신다. "
        "(최대 MP +10, MAG +3, SPD -2)\n"
        "3. 요정 설탕과자를 먹는다. "
        "(SPD +5, 최대 HP -5)\n"
        "4. 요정들과 함께 연회를 즐긴다. "
        "(HP/MP 완전 회복, Gold -100)\n"
        "5. 정중히 거절한다."
    )

    while True:
        choice = input("> ")

        if choice == "1":
            player.max_hp += 12
            player.hp += 12
            player.defense += 2
            player.speed = max(0, player.speed - 2)

            print()
            print(
                "알록달록한 버섯으로 장식된 케이크를 한입 베어 물었다.\n"
                "몸이 묵직해지고, 피부가 단단해지는 듯한 감각이 퍼진다.\n"
                "\n"
                "대신 움직임이 약간 둔해졌다."
            )
            print(
                "최대 HP +12, DEF +2, SPD -2!"
            )
            return

        elif choice == "2":
            player.max_mp += 10
            player.mp += 10
            player.magic += 3
            player.speed = max(0, player.speed - 2)

            print()
            print(
                "잔 안에서 은은하게 빛나는 술을 단숨에 들이켰다.\n"
                "강한 마력이 몸 안에 차오르고, 머릿속이 이상할 정도로 선명해진다.\n"
                "\n"
                "……대신 몸이 조금 무거워진 것 같다."
            )
            print(
                "최대 MP +10, MAG +3, SPD -2!"
            )
            return

        elif choice == "3":
            player.speed += 5
            player.max_hp = max(1, player.max_hp - 5)
            player.hp = min(
                player.hp,
                calculate_max_hp(player)
            )

            print()
            print(
                "별 모양의 설탕과자를 입에 넣었다.\n"
                "순간 몸이 믿을 수 없을 정도로 가벼워졌다.\n"
                "\n"
                "대신 생명력이 조금 깎여나간 듯한 기분이 든다."
            )
            print(
                "SPD +5, 최대 HP -5!"
            )
            return

        elif choice == "4":
            if player.gold < 100:
                print()
                print(
                    "연회에 끼어들려 하자 요정 하나가 손을 내민다.\n"
                    "\n"
                    "「참가비는 100G야!」\n"
                    "\n"
                    "...생각보다 철저하다.\n"
                    "연회에 참가하기에는 돈이 모자라다."
                )
                continue

            player.gold -= 100
            player.run_stats["gold_spent"] += 100

            print()
            print("「건배!」")
            time.sleep(0.5)
            print()
            print("한 잔.")
            time.sleep(0.5)
            print("두 잔.")
            time.sleep(0.5)
            print("세 잔.")
            time.sleep(1)
            print()
            print("...")
            time.sleep(1)
            print()

            old_hp = player.hp
            old_mp = player.mp

            player.hp = calculate_max_hp(player)
            player.mp = calculate_max_mp(player)

            print(
                "정신을 차려보니 연회장은 텅 비어 있다.\n"
                "상처도 피로도 말끔히 사라져 있다.\n"
                "\n"
                "……그리고 주머니가 조금 가벼워졌다."
            )
            print()
            print(
                f"HP +{player.hp - old_hp}, "
                f"MP +{player.mp - old_mp}, "
                "Gold -100!"
            )
            return

        elif choice == "5":
            print()
            print("「그래? 다음에 또 와!」")
            print(
                "요정들은 곧바로 당신에게서 관심을 거두고 다시 연회를 시작했다."
            )
            return

        else:
            print("올바르지 않은 입력")


def event_gpu_trap(player):
    stat_map = {
        "1": ("attack", "ATK"),
        "2": ("magic", "MAG"),
        "3": ("speed", "SPD"),
        "4": ("defense", "DEF"),
    }

    while True:
        print(
            "방 한가운데 최신형 그래픽카드가 놓여 있다.\n"
            "누가 봐도 비싸 보이는 물건이다.\n"
            "\n"
            "문제는 그래픽카드 주변으로 압력판, 와이어, 수상한 구멍과 마법진이\n"
            "빼곡하게 설치되어 있다는 것이다.\n"
            "\n"
            "누가 봐도 덫이다.\n"
            "\n"
            "1. 할 수 있다 나라면! (ATK 비례 성공률)\n"
            "2. 할 수 있다 나라면! (MAG 비례 성공률)\n"
            "3. 할 수 있다 나라면! (SPD 비례 성공률)\n"
            "4. 할 수 있다 나라면! (DEF 비례 성공률)\n"
            "5. 그냥 지나간다."
        )

        choice = input("> ")

        if choice == "5":
            print()
            print("그래픽카드에서 애써 시선을 돌렸다.")
            print()
            print("목숨은 그래픽카드보다 소중하다.")
            print("...아마도.")
            return

        if choice not in stat_map:
            print("올바르지 않은 입력")
            continue

        stat, stat_name = stat_map[choice]
        stat_value = getattr(player, stat)

        success_chance = min(
            0.9,
            0.25 + stat_value * 0.015
        )

        print()

        if choice == "1":
            print(
                "복잡하게 생각할 필요가 있을까.\n"
                "그래픽카드 주변의 덫부터 하나씩 박살내기 시작했다."
            )

        elif choice == "2":
            print(
                "수상한 마법진과 장치에 역으로 마력을 흘려넣었다.\n"
                "불길하게 빛나던 장치들이 하나씩 흔들리기 시작한다."
            )

        elif choice == "3":
            print(
                "함정을 해제할 필요는 없다.\n"
                "작동하기 전에 지나가면 된다."
            )

        elif choice == "4":
            print(
                "피할 수도, 해제할 수도 없다면 방법은 하나다.\n"
                "\n"
                "그냥 간다."
            )

        time.sleep(1)

        if random.random() < success_chance:
            print()

            if choice == "1":
                print(
                    "와이어도, 압력판도, 마법 장치도 전부 박살냈다.\n"
                    "\n"
                    "...이게 해체가 맞나?"
                )

            elif choice == "2":
                print(
                    "마법진의 빛이 하나씩 꺼지고,\n"
                    "잠시 후 모든 함정이 조용해졌다."
                )

            elif choice == "3":
                print(
                    "화살과 칼날, 불꽃이 뒤늦게 쏟아졌지만\n"
                    "이미 그래픽카드는 당신 손 안에 있었다."
                )

            elif choice == "4":
                print(
                    "화살이 날아오고, 칼날이 튀어나오고,\n"
                    "마법이 쏟아졌지만――\n"
                    "\n"
                    "전부 버텼다."
                )

            print()
            print("최신형 그래픽카드를 손에 넣었다!")

            setattr(
                player,
                stat,
                stat_value + 7
            )

            print(
                "그래픽카드를 장착하자 성능이 눈에 띄게 향상되었다."
            )
            print(
                f"{stat_name} +7!"
            )

            return

        else:
            print()
            print("딸깍.")
            time.sleep(0.5)
            print()
            print("아.")
            time.sleep(0.5)

            player.hp = max(
                0,
                player.hp - 20
            )

            print(
                "온갖 덫이 한꺼번에 작동했다!"
            )
            print(
                "HP -20!"
            )

            print()
            print(
                "간신히 빠져나왔지만,\n"
                "그래픽카드는 덫 아래로 떨어져 사라져 버렸다."
            )

            if player.hp == 0:
                print("Game Over")
                save_run_log(
                    player,
                    "패배 - 그래픽카드에 눈이 멀어 덫에 걸림"
                )
                input()
                exit()

            return


unknown_events_third_floor = [
    event_blackjack,
    event_vending_machine_v2,
    event_wishing_fountain,
    event_emergency_clinic,
    event_bloody_grail,
    event_living_mirror,
    event_cheat_console,
    event_suspicious_installer,
    event_fairy_feast,
    event_gpu_trap,
    treasure,
]

def run_unknown_event(player, floor):
    if floor == 1:
        event = random.choice(unknown_events_first_floor)
    elif floor == 2:
        event = random.choice(unknown_events_second_floor)
    elif floor == 3:
        event = random.choice(unknown_events_third_floor)
    
    if event is treasure:
        event(player, floor)
    else:
        event(player)
