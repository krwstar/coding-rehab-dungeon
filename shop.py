import random

from models import Equipment, Item, Action
from data import equipments, items, skills
from player_utils import (
    show_status,
    add_skill,
    get_equipment_stats,
    equip,
    get_random_reward_by_rarity,
    SHOP_FLOOR_RARITY_WEIGHTS,
)


def get_shop_item_text(item):
    if isinstance(item, Equipment):
        stats = get_equipment_stats(item)
        return (
            f"[장비] [{item.rarity}] {item.name} - {item.price}G\n"
            f"{stats}\n"
            f"{item.flavor_text}"
        )

    elif isinstance(item, Item):
        return f"[아이템] {item.name} - {item.price}G\n" f"{item.flavor_text}"

    elif isinstance(item, Action):
        return (
            f"[스킬] [{item.rarity}] {item.name} - {item.price}G\n"
            f"MP {item.mp_cost}\n"
            f"{item.description}"
        )

    return "[알 수 없는 상품]"


def shop(player, floor):
    rarity_weights = SHOP_FLOOR_RARITY_WEIGHTS[floor]
    reroll_cost = 30
    shop_items = (
        [get_random_reward_by_rarity(equipments, rarity_weights) for _ in range(2)] +
        [get_random_reward_by_rarity(skills, rarity_weights) for _ in range(2)] +
        random.sample(items, 2)
    )

    while True:
        print()
        print("=" * 45)
        print("                    상점")
        print("=" * 45)
        print(f"보유 골드: {player.gold}G")
        print("-" * 45)

        for i, item in enumerate(shop_items, start=1):
            print(f"{i}. {get_shop_item_text(item)}")
            print()

        status_num = len(shop_items) + 1
        reroll_num = status_num + 1

        print("-" * 45)
        print(f"{status_num}. 스테이터스 확인")
        print(f"{reroll_num}. 상점 새로고침({reroll_cost}G)")
        print("0. 상점에서 나간다")
        print("=" * 45)

        choice = input("> ")

        if not choice.isdigit():
            print("올바르지 않은 입력")
            continue

        choice = int(choice)

        if choice == 0:
            print("상점을 나섰다.")
            return
        
        if choice == status_num:
            show_status(player)
            continue
        
        if choice == reroll_num:
            if player.gold < reroll_cost:
                print("골드가 부족합니다")
                continue
            player.gold -= reroll_cost
            player.run_stats["gold_spent"] += reroll_cost
            reroll_cost *= 2
            shop_items = (
                [get_random_reward_by_rarity(equipments, rarity_weights) for _ in range(2)] +
                [get_random_reward_by_rarity(skills, rarity_weights) for _ in range(2)] +
                random.sample(items, 2)
            )
            print("상점을 새로고침했다.")
            continue

        if choice not in range(1, len(shop_items) + 1):
            print("올바르지 않은 입력")
            continue

        selected_item = shop_items[choice - 1]

        print()
        print("-" * 45)
        print("선택한 상품")
        print(get_shop_item_text(selected_item))
        print("-" * 45)

        while True:
            confirm = input("구매하시겠습니까? y/n: ").lower()

            if confirm in ("y", ""):
                if buy_shop_item(player, selected_item):
                    shop_items.pop(choice - 1)
                break

            elif confirm == "n":
                print("구매를 취소했다.")
                break

            else:
                print("y 또는 n을 입력해주세요.")


def buy_shop_item(player, item):
    if isinstance(item, Equipment):
        return buy_equipment(player, item)

    elif isinstance(item, Item):
        if buy_item(player, item):
            player.items.append(item)
            return True
        return False

    elif isinstance(item, Action):
        return buy_skill(player, item)

    print("구매할 수 없는 상품입니다.")
    return False


def buy_skill(player, skill):
    if player.gold < skill.price:
        print("골드가 부족합니다")
        return False

    if not add_skill(player, skill):
        return False

    player.gold -= skill.price
    player.run_stats["gold_spent"] += skill.price
    print(f"{skill.name}을(를) 구매했습니다.")
    return True


def buy_item(player, item):
    if player.gold >= item.price:
        player.gold -= item.price
        player.run_stats["gold_spent"] += item.price
        print(f"{item.name}을(를) 구매했습니다.")
        return True
    else:
        print("골드가 부족합니다")
        return False


def buy_equipment(player, equipment):
    if player.gold >= equipment.price:
        if not equip(player, equipment):
            return False

        player.gold -= equipment.price
        player.run_stats["gold_spent"] += equipment.price

        print(f"{equipment.name}을(를) 구매했습니다.")
        return True
    else:
        print("골드가 부족합니다")
        return False
