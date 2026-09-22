import time
from datetime import datetime

from models import (
    calculate_max_hp,
    calculate_max_mp,
    calculate_speed,
    calculate_attack_power,
    calculate_magic_power,
    calculate_defense,
)


def save_run_log(player, result):

    elapsed_seconds = int(time.time() - player.run_start_time)
    minutes, seconds = divmod(elapsed_seconds, 60)

    lines = []

    lines.append("===== 플레이 결과 =====")
    lines.append(f"결과: {result}")
    lines.append(f"플레이어: {player.name}")
    lines.append(f"플레이 시간: {minutes}분 {seconds}초")
    lines.append("")

    lines.append("===== 진행 기록 =====")
    lines.append(f"완료한 방: {player.run_stats['rooms_cleared']}")
    lines.append(f"전투: {player.run_stats['battles']}")
    lines.append(f"승리: {player.run_stats['wins']}")
    lines.append("")

    lines.append("===== 최종 스테이터스 =====")
    lines.append(f"HP: {player.hp}/{calculate_max_hp(player)}")
    lines.append(f"MP: {player.mp}/{calculate_max_mp(player)}")
    lines.append(f"ATK: {calculate_attack_power(player)}")
    lines.append(f"MAG: {calculate_magic_power(player)}")
    lines.append(f"SPD: {calculate_speed(player)}")
    lines.append(f"DEF: {calculate_defense(player)}")
    lines.append(f"Gold: {player.gold}")
    lines.append("")

    lines.append("===== 장비 =====")
    lines.append(f"무기: {player.weapon.name}")
    lines.append(f"방어구: {player.armor.name}")
    lines.append(f"반지: {player.ring.name}")
    lines.append("")

    lines.append("===== 보유 스킬 =====")
    for skill in player.skills:
        lines.append(f"- {skill.name} " f"(MP {skill.mp_cost})")
    lines.append("")

    lines.append("===== 아이템 =====")
    for item in player.items:
        lines.append(f"- {item.name}")
    lines.append("")

    lines.append("===== 전투 통계 =====")
    lines.append(f"가한 데미지: " f"{player.run_stats['damage_dealt']}")
    lines.append(f"독 데미지: " f"{player.run_stats['poison_damage']}")
    lines.append(f"화상 데미지: " f"{player.run_stats['burn_damage']}")
    lines.append(f"출혈 데미지: " f"{player.run_stats['bleed_damage']}")
    lines.append(f"받은 데미지: " f"{player.run_stats['damage_taken']}")
    lines.append(f"방어한 데미지: " f"{player.run_stats['damage_blocked']}")
    lines.append(f"획득한 방어도: " f"{player.run_stats['block_gained']}")
    lines.append(f"회복량: " f"{player.run_stats['healing']}")
    lines.append(f"소비 MP: " f"{player.run_stats['mp_spent']}")
    lines.append("")

    lines.append("===== 행동 사용 횟수 =====")
    for name, count in sorted(player.run_stats["actions_used"].items()):
        lines.append(f"- {name}: {count}회")
    lines.append("")

    lines.append("===== 아이템 사용 횟수 =====")
    if player.run_stats["items_used"]:
        for name, count in sorted(player.run_stats["items_used"].items()):
            lines.append(f"- {name}: {count}회")
    else:
        lines.append("- 사용하지 않음")
    lines.append("")

    lines.append("===== 경제 =====")
    lines.append(f"획득 골드: " f"{player.run_stats['gold_earned']}")
    lines.append(f"소비 골드: " f"{player.run_stats['gold_spent']}")

    lines.append("")
    lines.append("===== 방 진행 기록 =====")

    for record in player.run_stats["room_history"]:
        before = record["before"]
        after = record["after"]

        lines.append(room_title(record))
        
        if record["enemies"]:
            lines.append(f"적: {record['enemies']}")

        def change(key):
            diff = after[key] - before[key]

            if diff > 0:
                return f" (+{diff})"
            elif diff < 0:
                return f" ({diff})"
            return ""

        max_hp_change = change("max_hp")
        max_mp_change = change("max_mp")

        lines.append(
            f"HP: {after['hp']}/{after['max_hp']}"
            f"{change('hp')}"
            f"{f' / Max HP{max_hp_change}' if max_hp_change else ''}"
        )

        lines.append(
            f"MP: {after['mp']}/{after['max_mp']}"
            f"{change('mp')}"
            f"{f' / Max MP{max_mp_change}' if max_mp_change else ''}"
        )

        lines.append(
            f"ATK {after['attack']}{change('attack')} / "
            f"MAG {after['magic']}{change('magic')} / "
            f"SPD {after['speed']}{change('speed')} / "
            f"DEF {after['defense']}{change('defense')}"
        )

        lines.append(
            f"Gold: {after['gold']}{change('gold')}"
        )

        lines.append(
            f"장비: {after['weapon']} / "
            f"{after['armor']} / "
            f"{after['ring']}"
        )

        lines.append(
            "스킬: " + ", ".join(after["skills"])
        )

        lines.append("")
        if record["event"] == "전투":
            damage_dealt = after["damage_dealt"] - before["damage_dealt"]
            damage_taken = after["damage_taken"] - before["damage_taken"]
            damage_blocked = after["damage_blocked"] - before["damage_blocked"]
            block_gained = after["block_gained"] - before["block_gained"]
            healing = after["healing"] - before["healing"]
            mp_spent = after["mp_spent"] - before["mp_spent"]

            poison_damage = after["poison_damage"] - before["poison_damage"]
            burn_damage = after["burn_damage"] - before["burn_damage"]
            bleed_damage = after["bleed_damage"] - before["bleed_damage"]

            lines.append(
                f"전투 통계: "
                f"가한 데미지 {damage_dealt} / "
                f"받은 데미지 {damage_taken} / "
                f"방어한 데미지 {damage_blocked} / "
                f"획득한 방어도 {block_gained} / "
                f"회복 {healing} / "
                f"MP {mp_spent}"
            )
            status_parts = []

            if poison_damage > 0:
                status_parts.append(f"독 {poison_damage}")
            if burn_damage > 0:
                status_parts.append(f"화상 {burn_damage}")
            if bleed_damage > 0:
                status_parts.append(f"출혈 {bleed_damage}")
            if status_parts:
                lines.append(
                    "상태이상 데미지: " + " / ".join(status_parts)
                )
            lines.append("")
        
    with open("run_log.txt", "a", encoding="utf-8") as f:
        f.write("\n")
        f.write("=" * 60 + "\n")
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {result}\n")
        f.write("=" * 60 + "\n\n")
        f.write("\n".join(lines))
        f.write("\n")
        f.write("=" * 60 + "\n")


def get_player_snapshot(player):
    return {
        "hp": player.hp,
        "max_hp": calculate_max_hp(player),
        "mp": player.mp,
        "max_mp": calculate_max_mp(player),

        "attack": calculate_attack_power(player),
        "magic": calculate_magic_power(player),
        "speed": calculate_speed(player),
        "defense": calculate_defense(player),

        "gold": player.gold,

        "weapon": player.weapon.name,
        "armor": player.armor.name,
        "ring": player.ring.name,

        "skills": [skill.name for skill in player.skills],
        "items": [item.name for item in player.items],
        
        # 전투 통계
        "damage_dealt": player.run_stats["damage_dealt"],
        "damage_taken": player.run_stats["damage_taken"],
        "damage_blocked": player.run_stats["damage_blocked"],
        "block_gained": player.run_stats["block_gained"],
        "healing": player.run_stats["healing"],
        "mp_spent": player.run_stats["mp_spent"],

        "poison_damage": player.run_stats["poison_damage"],
        "burn_damage": player.run_stats["burn_damage"],
        "bleed_damage": player.run_stats["bleed_damage"],
    }


def record_room(player, floor, room, event, before, enemies=None):
    after = get_player_snapshot(player)

    player.run_stats["room_history"].append({
        "floor": floor,
        "room": room,
        "event": event,
        "enemies": enemies,
        "before": before,
        "after": after,
    })


def room_title(record):
    floor = record["floor"]
    room = record["room"]
    event = record["event"]

    if floor == "최하층":
        return f"[최하층 - {room} - {event}]"

    if room == "보스":
        return f"[{floor}층 보스전 - {event}]"

    return f"[{floor}층 {room}번방 - {event}]"