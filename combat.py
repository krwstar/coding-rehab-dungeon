import sys
import time
import random
from wcwidth import wcswidth

from models import (
    Player,
    FinalBoss,
    calculate_max_hp,
    calculate_max_mp,
    calculate_speed,
)

from player_utils import group_items, use_item
from run_log import save_run_log

GLITCH_CHARS = "▓▒░█▌▐▀▄"
# ╳×※#@$%&!?/\\|<>
def battle(player, enemies):
    if isinstance(player, Player):
        player.run_stats["battles"] += 1

    player.block = 0
    
    enemy_units = []
    for enemy in enemies:
        enemy.block = 0
        enemy.action_gauge = 0
        enemy.action_index = 0
        enemy_units.append(enemy)
    
    enemy_names = ", ".join(enemy.name for enemy in enemies)
    battle_logs = [f"{enemy_names}이(가) 나타났다!"]

    player.action_gauge = 0

    enter_battle_screen()
    
    player.trigger_battle_start_passive(battle_logs)

    try:
        while True:
            draw_battle_screen(
                player,
                enemy_units,
                player.action_gauge,
                battle_logs,
            )
            if player.action_gauge >= 200 or any_enemy_ready(enemy_units):
                while player.action_gauge >= 200 or any_enemy_ready(enemy_units):
                    ready_enemy_units = [
                        unit for unit in enemy_units
                        if unit.hp > 0 and unit.action_gauge >= 200
                    ]
                    highest_enemy_unit = max(
                        ready_enemy_units,
                        key=lambda unit: unit.action_gauge,
                        default=None,
                    )
                    
                    if (
                        player.action_gauge >= 200
                        and (
                            highest_enemy_unit is None
                            or player.action_gauge >= highest_enemy_unit.action_gauge
                        )
                    ):
                        player.action_gauge -= 200
                        player_turn(
                            player,
                            enemy_units,
                            player.action_gauge,
                            battle_logs,
                        )

                    else:
                        highest_enemy_unit.action_gauge -= 200
                        enemy_turn(
                            player,
                            highest_enemy_unit,
                            enemy_units,
                            battle_logs,
                        )
                    
                    for enemy in enemy_units:
                        if isinstance(enemy, FinalBoss):
                            old_log_count = len(battle_logs)
                            special_log = enemy.check_phase(enemy_units, battle_logs,)
                            play_new_battle_logs(
                                player,
                                enemy_units,
                                player.action_gauge,
                                battle_logs,
                                old_log_count,
                                delay=1 if special_log else 0.2,
                            )
                    
                    result = hp_check(player, enemy_units, battle_logs)
                    if result is not None:
                        draw_battle_screen(
                            player,
                            enemy_units,
                            player.action_gauge,
                            battle_logs,
                        )
                        input("\nEnter를 눌러 종료...")
                        if result == "lose":
                            save_run_log(player, f"{enemy.name}에게 패배")
                            exit()
                        return

            time.sleep(0.05)
            player.action_gauge += calculate_speed(player)
            
            for unit in enemy_units:
                if unit.hp > 0:
                    unit.action_gauge += calculate_speed(unit)
                elif unit.action_gauge != 0:
                    unit.action_gauge = 0

    finally:
        player.statuses.clear()
        exit_battle_screen()


def get_alive_enemy_units(enemy_units):
    return [
        unit
        for unit in enemy_units
        if unit.hp > 0
    ]
    
def get_alive_enemies(enemy_units):
    return [
        unit
        for unit in enemy_units
        if unit.hp > 0
    ]

def any_enemy_ready(enemy_units):
    return any(
        unit.hp > 0 and unit.action_gauge >= 200
        for unit in enemy_units
    )

def action_needs_enemy_target(action):
    return any(
        effect.target_type == "enemy"
        for effect in action.effects
    )

def select_enemy_target(player, enemy_units, player_gauge, battle_logs):
    while True:
        alive_units = get_alive_enemy_units(enemy_units)
        
        if not alive_units:
            return None
        
        if len(alive_units) == 1:
            return alive_units[0]

        menu = "공격할 대상을 선택하세요.\n"
        
        for i, unit in enumerate(alive_units, start=1):
            enemy = unit
            menu += (f"{i}. {enemy.name}\n")
        
        menu += "0. 뒤로\n> "
        
        draw_battle_screen(
            player,
            enemy_units,
            player_gauge,
            battle_logs,
            menu,
        )
        
        choice = input()
        
        if not choice.isdigit():
            add_battle_log(battle_logs, "올바르지 않은 입력")
            continue
        choice = int(choice)

        if choice == 0:
            return None
        
        if choice not in range(1, len(alive_units) + 1):
            add_battle_log(battle_logs, "올바르지 않은 입력")
            continue
        
        return alive_units[choice-1]

def player_turn(
    player,
    enemy_units,
    player_gauge,
    battle_logs
):
    add_battle_log(battle_logs, "")
    add_battle_log(battle_logs, f"▶  {player.name}의 턴!")
    
    player.reset_block()
    player.trigger_turn_start_passive(battle_logs)
    can_act = player.trigger_turn_start_statuses(battle_logs)
    
    if player.hp == 0:
        return
    
    if not can_act:
        player.trigger_turn_end_passive(battle_logs)
        player.trigger_turn_end_statuses(battle_logs)
        player.cleanup_statuses()
        return
    
    menu = (
        f"{player.name}은 무엇을 할까?\n"
        "1. 공격\n"
        "2. 방어\n"
        "3. 스킬\n"
        "4. 아이템\n"
        "> "
    )
    
    while True:
        draw_battle_screen(player, enemy_units, player_gauge, battle_logs, menu)
        action = input()
        if action == "1":
            if action_needs_enemy_target(player.weapon.basic_attack):
                target = select_enemy_target(
                    player,
                    enemy_units,
                    player_gauge,
                    battle_logs)
                if target is None:
                    continue
            else:
                target = get_alive_enemies(enemy_units)[0]
            
            if target is None:
                continue
            
            old_log_count = len(battle_logs)
            add_battle_log(battle_logs, player.weapon.basic_attack.flavor_text)
            play_new_battle_logs(player, enemy_units, player_gauge, battle_logs, old_log_count, delay=0.5)
            execute_action(
                player,
                target,
                player.weapon.basic_attack,
                enemy_units,
                battle_logs,
                player,
                enemy_units,
            )
            break

        elif action == "2":
            old_log_count = len(battle_logs)
            add_battle_log(battle_logs, player.armor.defense_action.flavor_text)
            play_new_battle_logs(player, enemy_units, player_gauge, battle_logs, old_log_count, delay=0.5)
            execute_action(
                player,
                None,
                player.armor.defense_action,
                enemy_units,
                battle_logs,
                player,
                enemy_units,
            )
            break

        elif action == "3":
            while True:
                skill_menu = "스킬 목록\n"

                for i, skill in enumerate(player.skills, start=1):
                    skill_menu += f"{i}. {skill.name} " f"(MP {skill.mp_cost})\n"
                skill_menu += "0. 뒤로\n> "

                draw_battle_screen(
                    player, enemy_units, player_gauge, battle_logs, skill_menu
                )

                choice = input()
                if not choice.isdigit():
                    add_battle_log(battle_logs, "올바르지 않은 입력")
                    continue
                choice = int(choice)
                if choice in range(0, len(player.skills) + 1):
                    break
                add_battle_log(battle_logs, "올바르지 않은 입력")
                continue
            if choice == 0:
                continue
        
            selected_skill = player.skills[choice - 1]
            
            if selected_skill.name == "세계":
                if any(status.name == "시간의 부채" for status in player.statuses):
                    add_battle_log(battle_logs, "아직 세계를 다시 사용할 수 없다.")
                    continue
            
            if action_needs_enemy_target(selected_skill):
                target = select_enemy_target(
                    player,
                    enemy_units,
                    player_gauge,
                    battle_logs)
                if target is None:
                    continue
            else:
                target = get_alive_enemies(enemy_units)[0]
            
            if player.mp >= selected_skill.mp_cost:
                old_log_count = len(battle_logs)
                add_battle_log(battle_logs, selected_skill.flavor_text)
                play_new_battle_logs(player, enemy_units, player_gauge, battle_logs, old_log_count, delay=0.5)
            
            result = execute_action(
                player,
                target,
                selected_skill,
                enemy_units,
                battle_logs,
                player,
                enemy_units,
            )
            
            if not result:
                continue
            
            player.trigger_skill_use_passive(target, battle_logs)
            
            break

        elif action == "4":
            while True:
                print("아이템 목록: ")
                for i in range(len(player.items)):
                    print(f"{i+1}. {player.items[i].name}")
                print(f"{len(player.items)+1}. 뒤로")
                
                grouped_items = group_items(player.items)
                item_menu = "아이템 목록\n"
                for i, entry in enumerate(grouped_items, start=1):
                    item = entry["item"]
                    count = entry["count"]
                    item_menu += f"{i}. [{item.name}] x{count}\n"

                item_menu += "0. 뒤로\n> "

                draw_battle_screen(
                    player, enemy_units, player_gauge, battle_logs, item_menu
                )

                choice = input()
                if not choice.isdigit():
                    add_battle_log(battle_logs, "올바르지 않은 입력")
                    continue
                choice = int(choice)
                if choice in range(0, len(player.items) + 1):
                    break
                add_battle_log(battle_logs, "올바르지 않은 입력")
                continue
            if choice == 0:
                continue
            
            item = grouped_items[choice - 1]["item"]
            if not item.usable_in_battle:
                print("전투 중에는 사용할 수 없는 아이템이다.")
                continue

            target = None
            if item.target_type == "enemy":
                target = select_enemy_target(player, enemy_units, player_gauge, battle_logs,)
                if target is None:
                    continue
            elif item.target_type == "self":
                target = player
            elif item.target_type == "all_enemies":
                target = None
            else:
                add_battle_log(
                    battle_logs,
                    f"알 수 없는 아이템 대상 타입: {item.target_type}"
                )
                continue

            player.items.remove(item)
            use_item(player, item, target=target, enemy_units=enemy_units, battle_logs=battle_logs,)            
            break

        else:
            add_battle_log(battle_logs, "올바르지 않은 입력")
            continue
    
    player.trigger_turn_end_passive(battle_logs)
    player.trigger_turn_end_statuses(battle_logs)
    player.cleanup_statuses()


def enemy_turn(player, enemy, enemy_units, battle_logs):
    enemy.reset_block()
    
    old_log_count = len(battle_logs)
    add_battle_log(battle_logs, "")
    add_battle_log(battle_logs, f"▶  {enemy.name}의 턴!")
    play_new_battle_logs(player, enemy_units, player.action_gauge, battle_logs, old_log_count, delay=0.5)
    
    enemy.trigger_turn_start_passive(battle_logs)
    can_act = enemy.trigger_turn_start_statuses(battle_logs)

    if enemy.hp == 0:
        return

    if not can_act:
        enemy.trigger_turn_end_passive(battle_logs)
        enemy.trigger_turn_end_statuses(battle_logs)
        enemy.cleanup_statuses()
        return

    update_enemy_action_pool(enemy, enemy_units)
    action = select_enemy_action(enemy)
    
    if isinstance(enemy, FinalBoss):
        old_log_count = len(battle_logs)
        special_log = enemy.execute_developer_action(player, enemy_units, battle_logs)
        play_new_battle_logs(
            player,
            enemy_units,
            player.action_gauge,
            battle_logs,
            old_log_count,
            delay=1 if special_log else 0.2,
        )
        
    old_log_count = len(battle_logs)
    add_battle_log(battle_logs, action.flavor_text)
    play_new_battle_logs(player, enemy_units, player.action_gauge, battle_logs, old_log_count, delay=0.5)
    
    execute_action(enemy, player, action, [player], battle_logs, player, enemy_units, ally_units=enemy_units)
    enemy.trigger_turn_end_passive(battle_logs)
    enemy.trigger_turn_end_statuses(battle_logs)
    enemy.cleanup_statuses()
        
    time.sleep(0.8)


def update_enemy_action_pool(enemy, enemy_units):
    if enemy.action_pools is None:
        return

    alive_allies = [
        unit
        for unit in enemy_units
        if unit is not enemy and unit.hp > 0
    ]

    ally_count = len(alive_allies)
    new_pool = enemy.action_pools.get(ally_count)
    if new_pool is None:
        return

    if enemy.action_pool is not new_pool:
        enemy.action_pool = new_pool
        enemy.action_index = 0


def select_enemy_action(enemy):
    if isinstance(enemy, FinalBoss):
        return enemy.select_action()

    action = enemy.action_pool[enemy.action_index]

    enemy.action_index += 1
    if enemy.action_index >= len(enemy.action_pool):
        enemy.action_index = 0

    return action


def hp_check(player, enemy_units, battle_logs):
    alive_units = get_alive_enemy_units(enemy_units)
    
    if not alive_units:
        total_gold = sum(unit.gold for unit in enemy_units)

        player.block = 0
        player.gold += total_gold

        player.run_stats["wins"] += 1
        player.run_stats["gold_earned"] += total_gold

        add_battle_log(battle_logs, "빰빠카밤! 적을 쓰러뜨렸다!")
        add_battle_log(battle_logs, f"{total_gold}의 골드 획득!")
        return "win"
    
    if player.hp == 0:
        add_battle_log(battle_logs, "악! 이건 너무 아프다!")
        add_battle_log(battle_logs, "GAME OVER")
        add_battle_log(battle_logs, "다음장...")
        return "lose"
    return None


def reset_enemy(enemy):
    enemy.hp = enemy.max_hp
    enemy.mp = enemy.max_mp
    enemy.block = 0
    enemy.action_index = 0
    enemy.statuses.clear()


def enter_battle_screen():
    sys.stdout.write("\033[?1049h")
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()


def exit_battle_screen():
    sys.stdout.write("\033[?1049l")
    sys.stdout.flush()


def make_bar(current, maximum, length=20):
    if maximum <= 0:
        return "□" * length

    ratio = max(0, min(current / maximum, 1))
    filled = int(ratio * length)

    return "■" * filled + "□" * (length - filled)


LEFT_WIDTH = 68
LOG_COLUMN = 75
SEPARATOR = "|  "

def draw_battle_screen(
    player, enemy_units, player_gauge, battle_logs, menu=None
):
    console = sys.stdout

    glitch = (
        any(
            isinstance(unit, FinalBoss) and unit.phase == 3
            for unit in enemy_units
        )
        and random.random() < 0.8
    )

    def process_text(text):
        if glitch:
            return glitch_text(text)
        return text

    def make_status_lines(statuses, max_width):
        prefix = "  상태: "
        indent = " " * 6

        lines = []
        current = prefix

        for status in statuses:
            status_text = draw_status(status)
            test_line = current + status_text

            if wcswidth(test_line) > max_width and current != prefix:
                lines.append(current.rstrip())
                current = indent + status_text
            else:
                current += status_text

        if current != prefix:
            lines.append(current.rstrip())

        return lines

    console.write("\033[2J\033[H")

    left_lines = []

    # 플레이어
    left_lines.append("[플레이어]")
    left_lines.append(player.name)

    left_lines.append(
        f"  HP [{make_bar(player.hp, calculate_max_hp(player))}] "
        f"  {player.hp}/{calculate_max_hp(player)}  "
        f"  방어도 {player.block}"
    )

    left_lines.append(
        f"  MP [{make_bar(player.mp, calculate_max_mp(player))}] "
        f"  {player.mp}/{calculate_max_mp(player)}"
    )

    left_lines.append(
        f"  AG [{make_bar(player_gauge, 200)}] "
        f"  {player_gauge:3d}"
    )

    if player.statuses:
        left_lines.extend(
            make_status_lines(
                player.statuses,
                LEFT_WIDTH - 2
            )
        )

    left_lines.append("")

    # 적
    left_lines.append("[적]")

    for enemy in enemy_units:
        gauge = enemy.action_gauge

        if enemy.hp <= 0:
            left_lines.append(
                f"{enemy.name}  쓰러짐"
            )
            left_lines.append("")
            continue

        left_lines.append(enemy.name)

        left_lines.append(
            f"  HP [{make_bar(enemy.hp, calculate_max_hp(enemy))}] "
            f"  {enemy.hp}/{calculate_max_hp(enemy)}  "
            f"  방어도 {enemy.block}"
        )

        left_lines.append(
            f"  AG [{make_bar(gauge, 200)}] "
            f"  {gauge:3d}"
        )

        if enemy.statuses:
            left_lines.extend(
                make_status_lines(
                    enemy.statuses,
                    LEFT_WIDTH - 2
                )
            )

        left_lines.append("")

    # 메뉴
    prompt_index = None

    if menu is not None:
        left_lines.append("=" * 55)

        menu_lines = menu.rstrip("\n").split("\n")

        if (
            menu_lines
            and menu_lines[-1].strip().startswith(">")
        ):
            prompt = menu_lines.pop()

            left_lines.extend(menu_lines)

            prompt_index = len(left_lines)
            left_lines.append(prompt)

        else:
            left_lines.extend(menu_lines)

    # 오른쪽 전투 로그
    log_lines = [
        "---------------[전투 로그]---------------",
        "",
    ] + battle_logs[-30:]

    max_lines = max(
        len(left_lines),
        len(log_lines)
    )

    # 실제 화면 출력
    for i in range(max_lines):
        left = (
            left_lines[i]
            if i < len(left_lines)
            else ""
        )

        right = (
            log_lines[i]
            if i < len(log_lines)
            else ""
        )

        left = process_text(left)
        right = process_text(right)

        if i == prompt_index:
            # 입력 프롬프트 출력
            console.write(left)

            # "> " 바로 뒤 위치 저장
            console.write("\033[s")

            # 로그는 무조건 지정한 열에서 시작
            console.write(f"\033[{LOG_COLUMN}G")
            console.write(SEPARATOR + right + "\n")

        else:
            # 왼쪽 영역 출력
            console.write(left)

            # 오른쪽 로그 영역으로 강제 이동
            console.write(f"\033[{LOG_COLUMN}G")
            console.write(SEPARATOR + right + "\n")

    # 입력 위치로 복귀
    if prompt_index is not None:
        console.write("\033[u")

    console.flush()


def draw_status(status):
    name = status.name
    if name == "동결" or name == "무적":
        return f"{name} "
    elif name == "독" or name == "출혈" or name == "냉기":
        return f"{name}({status.stack}스택) "
    elif name == "화상":
        return f"{name}({status.power}데미지, {status.duration}턴) "
    elif name == "회피":
        return f"{name}({status.count}회) "
    elif getattr(status, "duration", None) is not None:
        return f"{name}({status.duration}턴) "
    else:
        return f"{name} "
        

def play_new_battle_logs(
    player, enemy_units, player_gauge, battle_logs, start_index, delay=0.2
):
    for end_index in range(start_index + 1, len(battle_logs) + 1):
        draw_battle_screen(
            player, enemy_units, player_gauge, battle_logs[:end_index]
        )
        time.sleep(delay)


def add_battle_log(battle_logs, text):
    battle_logs.append(text)


def execute_action(
    user,
    target,
    action,
    enemy_units,
    battle_logs,
    player,
    display_enemy_units,
    ally_units=None,
):
    if ally_units is None:
        ally_units = [user]
    if user.mp < action.mp_cost:
        add_battle_log(battle_logs, f"MP가 부족해 {action.name}을 사용할 수 없다!")
        return False

    user.mp -= action.mp_cost

    if isinstance(user, Player):
        user.run_stats["mp_spent"] += action.mp_cost

        action_uses = user.run_stats["actions_used"]
        action_uses[action.name] = action_uses.get(action.name, 0) + 1

    for effect in action.effects:
        if user.hp <= 0:
            break
        
        old_log_count = len(battle_logs)
        
        if effect.target_type == "self":
            effect.apply(user, user, battle_logs)
            
        elif effect.target_type == "all_enemies":
            for unit in get_alive_enemy_units(enemy_units):
                effect.apply(user, unit, battle_logs)
                
        elif effect.target_type == "ally":
            allies = [
                unit for unit in ally_units
                if unit.hp > 0 and unit is not user
            ]

            if allies:
                ally = random.choice(allies)
            else:
                ally = user

            effect.apply(user, ally, battle_logs)

        elif effect.target_type == "all_allies":
            for unit in ally_units:
                if unit.hp > 0:
                    effect.apply(user, unit, battle_logs)
                    
        else:
            effect.apply(user, target, battle_logs)
        
        play_new_battle_logs(
            player,
            display_enemy_units,
            player.action_gauge,
            battle_logs,
            old_log_count,
        )

    return True


def glitch_text(text, intensity=0.05):
    result = []

    for char in text:
        if char == "\n" or char.isspace():
            result.append(char)
            continue

        if random.random() < intensity:
            result.append(random.choice(GLITCH_CHARS))
        else:
            result.append(char)

    return "".join(result)