import random
import time

from copy import deepcopy
from combat import battle, reset_enemy
from events import treasure, rest, run_unknown_event
from models import InvincibleStatus
from shop import shop
from run_log import get_player_snapshot, record_room
from player_utils import (
    show_status,
    choose_random_stat_reward,
    choose_equipment_or_skill,
    calculate_max_hp,
    calculate_max_mp,
)
from data import (
    enemies_first_floor,
    enemies_second_floor,
    enemies_third_floor_early,
    enemies_third_floor,
    bosses,
    four_kings,
    final_boss,
)


def select_event(i):
    if i in (1, 4, 7):
        return ["전투", "전투", "전투"]
    elif i == 10:
        return ["휴식", "휴식", "휴식"]
    event1 = super_random_event()
    event2 = super_random_event()
    event3 = super_random_event()
    return [event1, event2, event3]


def super_random_event():
    rand = random.random()
    if rand > 0.6:
        return "전투"
    elif rand > 0.2:
        return "미지"
    elif rand > 0.1:
        return "상점"
    else:
        return "보물"


def next_event(event, player, battle_count, floor):
    if floor == 1:
        enemies = enemies_first_floor
    elif floor == 2:
        enemies = enemies_second_floor
        
    if event == "전투":
        if floor <= 2:
            if battle_count == 1:
                battle_enemies = [deepcopy(random.choice(enemies)),]
            elif battle_count <= 3:
                rand = random.random()
                if rand > 0.5:
                    battle_enemies = [deepcopy(random.choice(enemies)),]
                else:
                    battle_enemies = [
                        deepcopy(random.choice(enemies)),
                        deepcopy(random.choice(enemies)),
                    ]
            else:
                rand = random.random()
                if rand > 0.7:
                    battle_enemies = [deepcopy(random.choice(enemies)),]
                elif rand > 0.3:
                    battle_enemies = [
                        deepcopy(random.choice(enemies)),
                        deepcopy(random.choice(enemies)),
                    ]
                else:
                    battle_enemies = [
                        deepcopy(random.choice(enemies)),
                        deepcopy(random.choice(enemies)),
                        deepcopy(random.choice(enemies)),
                    ]
        else:
            if battle_count <= 2:
                battle_enemies = deepcopy(
                    random.choice(enemies_third_floor_early)
                )
            else:
                battle_enemies = deepcopy(
                    random.choice(enemies_third_floor)
                )
            
        battle(player, battle_enemies)
        
        enemy_names = ", ".join(enemy.name for enemy in battle_enemies)
        
        print()
        print(f"{enemy_names}와(과)의 전투를 마쳤다.")
        print()
        print("전투로부터 경험을 얻었다.")
        choose_random_stat_reward(player)
        if random.random() < 0.2:
            print("적이 특별한 보상을 드랍했다!")
            choose_equipment_or_skill(player, floor=floor)
        
        return enemy_names
    elif event == "보물":
        treasure(player, floor)
    elif event == "미지":
        run_unknown_event(player, floor)
        input("Enter를 눌러 진행하기...")
    elif event == "상점":
        shop(player, floor)
    elif event == "휴식":
        rest(player)
    elif event == "보스":
        before = get_player_snapshot(player)
        
        if floor == 1:
            giant_slime = bosses[0]
            enemy_names = giant_slime.name
            reset_enemy(giant_slime)
            boss(player, giant_slime)
            print()
            print(f"{giant_slime.name}와(과)의 전투를 마쳤다.")
            print()
            print("전투로부터 경험을 얻었다.")
            choose_random_stat_reward(player)
            print("보스가 특별한 보상을 드랍했다!")
            choose_equipment_or_skill(player, "boss", floor)
        elif floor == 2:
            mado_golem = bosses[1]
            enemy_names = mado_golem.name
            reset_enemy(mado_golem)
            boss(player, mado_golem)
            print()
            print(f"{mado_golem.name}와(과)의 전투를 마쳤다.")
            print()
            print("전투로부터 경험을 얻었다.")
            choose_random_stat_reward(player)
            print("보스가 특별한 보상을 드랍했다!")
            choose_equipment_or_skill(player, "boss", floor)
        elif floor == 3:
            battle_commander = bosses[2]
            enemy_names = battle_commander[1].name
            for enemy in battle_commander:
                reset_enemy(enemy)
            boss(player, battle_commander)
            print()
            print(f"전장 지휘관와(과)의 전투를 마쳤다.")
            print()
            print("전투로부터 경험을 얻었다.")
            choose_random_stat_reward(player)
            print("보스가 특별한 보상을 드랍했다!")
            choose_equipment_or_skill(player, "boss", floor)
        record_room(
            player,
            floor=floor,
            room="보스",
            event="전투",
            before=before,
            enemies=enemy_names,
        )
    else:
        print("이벤트 선택 오류")

    return None

def boss(player, enemy):
    print(f"!!보스전!!")
    time.sleep(1)
    battle(player, enemy if isinstance(enemy, list) else [enemy])


def print_room_header(room_number):
    print()
    print("=" * 45)
    print(f"                  {room_number}번째 방")
    print("=" * 45)
    time.sleep(0.5)


def run_floor(player, floor):
    print(f"{floor}층에 진입했다.")
    if floor != 1:
        player.hp = calculate_max_hp(player)
        player.mp = calculate_max_mp(player)
        print("체력과 마력이 회복되었다.")
    battle_count = 0
    
    for i in range(10):
        print_room_header(i+1)
        events = select_event(i+1)
        while True:
            print("어디로 갈까?")
            print(f"0. 스테이터스 확인")
            print(f"1. {events[0]}")
            print(f"2. {events[1]}")
            print(f"3. {events[2]}")
            print("-" * 45)
            choice = input("> ")
            if choice == "0":
                show_status(player)
            elif choice == "1":
                event = events[0]
                break
            elif choice == "2":
                event = events[1]
                break
            elif choice == "3":
                event = events[2]
                break
            else:
                print("올바르지 않은 입력")
                print("-" * 45)
                print()
        print()
        print("당신은 선택한 길로 발걸음을 옮겼다...")
        time.sleep(0.5)
        print()
        
        if event == "전투":
            battle_count += 1
        
        before = get_player_snapshot(player)
        enemy_names = next_event(event, player, battle_count, floor)
        player.run_stats["rooms_cleared"] += 1
        record_room(
            player,
            floor=floor,
            room=i+1,
            event=event,
            before=before,
            enemies=enemy_names
        )

    print()
    print("=" * 45)
    print("                  보스 방")
    print("=" * 45)
    time.sleep(1)
    
    battle_count += 1
    next_event("보스", player, battle_count, floor)
    player.run_stats["rooms_cleared"] += 1

def run_last_floor(player):   
    slow_print(
"""
계단을 따라 한참을 내려갔다.
이윽고, 더 이상 내려갈 곳이 없는 곳에 도착했다.

최하층.

지금까지의 던전과는 분위기가 전혀 다르다.
돌벽도, 횃불도, 갈림길도 없다.
대신 눈앞에는 지나치게 반듯한 복도와 하나의 문이 놓여 있다.

잠시 숨을 고르고 앞으로 나아갔다.
체력과 마력이 모두 회복되었다.
"""
    )
    
    player.hp = calculate_max_hp(player)
    player.mp = calculate_max_mp(player)
    
    input("Enter를 눌러 진행하기...")


    # 사천왕-성직자
    print_room_header(1)

    slow_print(
"""
첫 번째 문이 열린다.
문 너머에서 한 사람이 조용히 당신을 기다리고 있었다.

사천왕-성직자
「여기까지 오셨군요.」
「그렇다면, 당신의 실력을 시험해 보겠습니다.」
"""
    )

    input("Enter를 눌러 전투 시작...")
    
    before = get_player_snapshot(player)
    
    battle(player, [deepcopy(four_kings[0])])
    
    record_room(
        player,
        floor="최하층",
        room="사천왕-성직자",
        event="전투",
        before=before,
        enemies="사천왕-성직자",
    )

    # 사천왕-기사
    print_room_header(2)

    slow_print(
"""
다음 방으로 향하는 문이 열린다.
거대한 갑옷을 두른 기사가 그 앞을 가로막고 있다.

사천왕-기사
「성직자를 쓰러뜨렸나.」

「하지만 녀석은 우리 사천왕 중 최약체.」
「그 정도로 우쭐해하지 않는 게 좋을 거다.」

기사가 무기를 들어 올렸다.

「여기서부터가 진짜다.」
"""
    )

    input("Enter를 눌러 전투 시작...")
    
    before = get_player_snapshot(player)
    
    battle(player, [deepcopy(four_kings[1])])
    
    record_room(
        player,
        floor="최하층",
        room="사천왕-기사",
        event="전투",
        before=before,
        enemies="사천왕-기사",
    )

    # 사천왕-마법사
    print_room_header(3)

    slow_print(
"""
세 번째 문이 열린다.
방 안으로 들어서는 순간, 열기와 냉기가 동시에 피부를 스친다.

사천왕-마법사
「기사를 쓰러뜨렸다고?」
「흐음. 제법인데.」

「하지만 녀석은 우리 사천왕 중 두 번째로 약한 녀석.」

마법사가 피식 웃었다.

「……왜 그런 눈으로 봐?」
「순서대로 싸우고 있으니까 당연하잖아.」
"""
    )

    input("Enter를 눌러 전투 시작...")
    
    before = get_player_snapshot(player)
    
    battle(player, [deepcopy(four_kings[2])])
    
    record_room(
        player,
        floor="최하층",
        room="사천왕-마법사",
        event="전투",
        before=before,
        enemies="사천왕-마법사",
    )

    print_room_header(4)

    slow_print(
"""
마지막 문이 열린다.

아무도 없다.

조심스럽게 방 안으로 발을 들이는 순간―

「느려.」

등 뒤에서 목소리가 들렸다.

사천왕-도적
「설마 나도 '녀석은 우리 중 최약체' 같은 소리를 할 거라고 생각했냐?」

「앞의 셋이 다 죽었는데 이제 내가 최약체이자 최강체지.」

도적이 무기를 꺼내 들었다.

「아무튼, 마지막이다.」
"""
    )

    input("Enter를 눌러 전투 시작...")
    
    before = get_player_snapshot(player)
    
    battle(player, [deepcopy(four_kings[3])])
    
    record_room(
        player,
        floor="최하층",
        room="사천왕-도적",
        event="전투",
        before=before,
        enemies="사천왕-도적",
    )

    slow_print(
"""
마지막 사천왕이 쓰러졌다.

길었던 전투가 끝나고, 방 안에 정적이 내려앉는다.
앞으로 이어지는 길은 보이지만, 당장 당신을 재촉하는 것은 없다.

당신은 잠시 자리에 앉아 숨을 돌렸다.

얼마나 시간이 흘렀을까.
충분히 쉬고 다시 일어섰을 때는, 몸에 남아 있던 피로도 말끔히 사라져 있었다.
"""
    )

    player.hp = calculate_max_hp(player)
    player.mp = calculate_max_mp(player)

    slow_print(
        "\n체력과 마력이 모두 회복되었다."
    )

    input("Enter를 눌러 진행하기...")

    developer = deepcopy(final_boss)
    kings = deepcopy(four_kings)

    developer.phase = 1
    developer.statuses.append(
        InvincibleStatus(source=developer, duration=99999)
    )

    enemies = [
        kings[0],
        kings[1],
        developer,
        kings[2],
        kings[3],
    ]

    slow_print(
"""
마침내 마지막 문 앞에 도착했다.

문을 열자, 넓고 텅 빈 공간이 모습을 드러낸다.
그리고 그 한가운데에 한 사람이 서 있다.

개발자
「오.」
「진짜 여기까지 왔네.」

개발자는 잠시 당신을 바라보다가 피식 웃었다.

「뭐, 여기까지 왔으면 긴 설명은 필요 없겠지.」

개발자가 손가락을 튕겼다.

그 순간, 주위에서 네 개의 익숙한 기척이 나타난다.

사천왕-성직자.
사천왕-기사.
사천왕-마법사.
사천왕-도적.

조금 전 분명 쓰러뜨렸던 네 명이 다시 당신 앞을 가로막는다.

개발자가 사천왕들 사이로 걸어 나온다.

「사천왕이 왜 사천왕인 줄 알아?」
「넷이라서?」
「그것도 맞는데...」

「원래 사천왕이라는 건 말이지.」
「하나씩 각개격파당할 때보다, 넷이 같이 있을 때 강한 법이야」

「아까 쓰러뜨리지 않았냐고?」
「원본은 멀쩡한데?」
「아까 네가 쓰러뜨린건 deepcopy()한 거야.」
"""
    )

    input("Enter를 눌러 진행하기...")
    print()
    print("============================================================")
    print("                    !! 최종 보스전 !!")
    print("============================================================")
    print()

    time.sleep(1)

    before = get_player_snapshot(player)
    enemy_names = ", ".join(enemy.name for enemy in enemies)
    battle(player, enemies)
    
    player.run_stats["rooms_cleared"] += 1        
    record_room(
        player,
        floor="최하층",
        room="최종보스전",
        event="전투",
        before=before,
        enemies=enemy_names
    )
    
    slow_print(
"""
개발자는 더 이상 움직이지 않았다.

마지막까지 유지되던 힘이 사라진다.

깨져 있던 화면도,
뒤틀려 있던 공간도,
서서히 원래의 모습으로 돌아오기 시작했다.

...

전투는 끝났다.

주변을 둘러본다.

분명 조금 전까지 거대한 전장이었던 공간은,
어느새 아무 일도 없었던 것처럼 조용해져 있었다.

쓰러진 흔적도,
깨진 흔적도,
마치 처음부터 존재하지 않았던 것처럼 사라져 있다.

하지만 하나.

개발자가 서 있던 자리만은 달랐다.

그곳에는 이전에는 보이지 않았던 작은 문이 하나 있었다.

문에는 별다른 장식도,
잠금 장치도 없었다.

그저 한 줄의 문구만 적혀 있었다.

「최종 보상 보관실」

문을 열었다.

안쪽은 생각보다 평범한 방이었다.

화려한 보물도,
끝없이 쌓인 금화도 없었다.

대신 방 한가운데,
작은 상자 하나가 놓여 있었다.

상자는 이상할 정도로 깔끔했다.

먼지가 쌓이지도 않았고,
오래된 흔적도 없었다.

마치 누군가가 방금 전까지도
이것을 꺼내기만을 기다리고 있었던 것처럼.

상자 위에는 짧은 문구가 적혀 있었다.

『세상에서 가장 위대한 그래픽카드』
"""
    )
    
    input("> 상자를 연다...")

    slow_print(
"""
조심스럽게 상자를 열었다.

...

아무것도 없다.

상자 안은 텅 비어 있었다.

최강의 장비도.
엄청난 힘을 가진 보물도.
그토록 찾아 헤맸던 전설의 그래픽카드도.

아무것도.

대신,
상자 바닥에 작은 종이 한 장이 놓여 있었다.

종이를 펼쳤다.

거기에는 단 세 글자만 적혀 있었다.

『상상력』

......

한참 동안 그 세 글자를 바라보았다.

이게 끝인가?

세상에서 가장 위대한 그래픽카드를 찾기 위해 시작한 모험.

수많은 적과 싸우고,
수많은 위기를 넘기고,
마침내 던전의 최하층까지 도달했다.

그 끝에 기다리고 있던 것은
고작 세 글자였다.

...

라고 생각했겠지.

아니.
정확히는, 그렇게 생각하도록 만든 거야.

잘 생각해 봐.

여기에는 처음부터 아무것도 없었어.

검도 없고,
마법도 없고,
괴물도 없고,
던전도 없었지.

그런데도 너는 여기까지 오는 동안
그 모든 것을 보고,
싸우고,
모험했어.

너의 머릿속에서.

더 좋은 그래픽카드가 있다면
더 멋진 세계를 보여줄 수 있겠지.

하지만 아무것도 없는 곳에서
무언가를 만들어내는 건
그래픽카드가 아니야.

세상에서 가장 위대한 그래픽카드는
처음부터 네가 가지고 있었던 거야.

상상력.

그러니까 축하해.

너는 끝까지 도달했고,
마침내 그것을 찾아냈어.
"""
    )
    time.sleep(1)
    print("어떻게 할까?")
    print("1. 수긍한다.")
    print("2. 공격한다.")
    choice = input("> ")
    
    if choice == "1":
        slow_print(
"""
당신은 고개를 끄덕였다.

그래.
세상에서 가장 위대한 그래픽카드는
처음부터 당신 안에 있었던 것이다.

......

납득했으면 됐다.
"""
        )
    else:
        print(
"""
조▓스▒게 ░자█ ▌었▐.

.▀╳

아×것※ #다.

상$ 안% 텅 &어 !었?.

최/의 \비|.
엄<난 >을 ▓진 ▒물░.
그█록 ▌아 ▐맸▀ 전▄의 ╳래×카※도.

아#것$.

대%,
상& 바!에 ?은 /이 \ 장| 놓< >었▓.

종▒를 ░쳤█.

거▌에는 ▐ 세 ▀자▄ 적╳ ×었※.

『상#력』

.$%&!?

한/ 동\ 그 | 글<를 >라▓았▒.

이░ █인가?

세▌에서 ▐장 ▀대▄ 그╳픽×드를 ※기 #해 $작% 모&.

수!은 ?과 /우\,
수|은 <기> 넘▓고,
마▒내 ░전█ 최▌층▐지 ▀달▄.

그 ╳에 ×다※고 #던 $은
고% 세 &자!다.

?..

라/ 생\했|지.

아<.
정>히는, ▓렇▒ 생░하█록 ▌든 ▐야.

잘 ▀각▄ ╳.

여×에는 ※음#터 $무%도 &었!.

검? 없/,
마\도 |고<,
괴>도 ▓고▒,
던░도 █었▌.

그▐데도 ▀는 ▄기╳지 ×는 ※안
그 #든 $을 %고,
싸&고,
모!했?.

너/ 머\속|서.

더 <은 >래▓카▒가 ░다█
더 ▌진 ▐계▀ 보▄줄 ╳ 있×지.

하※만 #무$도 %는 &에!
무?가를 /들\내| 건
그<픽>드가 ▓니▒.

세░에서 █장 ▌대▐ 그▀픽▄드는
처╳부터 ×가 ※지# 있$던 %야.

상&력.

그!니까 ?하/.

너\ 끝|지 <달>고,
마▓내 ▒것░ 찾█냈▌.


어▐게 ▀까▄?

1. ╳긍×다.
2. ※격#다.
> 2
"""
        )
        time.sleep(3)

def slow_print(text, delay=0.01):
    for ch in text:
        if ch == "\n":
            print(ch, end="", flush=True)
            time.sleep(0.3)
        else:
            print(ch, end="", flush=True)
            time.sleep(delay)
    print()