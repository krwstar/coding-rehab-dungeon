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
    enemies_hidden_floor,
    generative_ai_boss,
)
from ui_utils import clear_screen


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
        input("Enter를 눌러 진행하기...")
        return enemy_names
    elif event == "보물":
        clear_screen()
        treasure(player, floor)
        input("Enter를 눌러 진행하기...")
    elif event == "미지":
        clear_screen()
        run_unknown_event(player, floor)
        input("Enter를 눌러 진행하기...")
    elif event == "상점":
        clear_screen()
        shop(player, floor)
        input("Enter를 눌러 진행하기...")
    elif event == "휴식":
        clear_screen()
        rest(player)
        input("Enter를 눌러 진행하기...")
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
        events = select_event(i+1)
        while True:
            clear_screen()
            print_room_header(i+1)
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
    clear_screen()
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
    clear_screen()
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
    clear_screen()
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

    clear_screen()
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

    clear_screen()
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

    clear_screen()
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
    
    clear_screen()
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

    clear_screen()
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

뭐, 그렇게 납득했으면 됐다.
"""
        )
        time.sleep(3)
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


def run_hidden_floor(player):
    clear_screen()

    slow_print(
f"""
단말기에 답을 입력했다.

「상상력」

잠시 아무런 반응도 없다.

잘못된 답이었나 생각하려던 순간,
화면에 짧은 문장이 떠올랐다.

[비밀번호 일치. 접근 권한을 활성화합니다.]

철컥.

어디선가 잠금이 풀리는 소리가 들렸다.

복도 한쪽,
아무것도 없던 벽면이 천천히 갈라지기 시작한다.

그 너머에는 아래로 향하는 계단이 있었다.

이상하다.

분명 이곳이 최하층이었다.
더 아래로 내려갈 곳은 없어야 했다.

하지만 계단은 분명히 존재한다.

당신은 잠시 망설이다가,
어둠 속으로 이어지는 계단을 내려가기 시작했다.

체력과 마력이 모두 회복되었다.
"""
    )
    player.hp = calculate_max_hp(player)
    player.mp = calculate_max_mp(player)

    input("Enter를 눌러 진행하기...")

    clear_screen()
    print_room_header(1)

    slow_print(
"""
얼마나 내려왔을까.
돌벽은 어느 순간부터 사라져 있었다.

대신 주변을 둘러싼 것은
차갑고 매끄러운 금속 벽과,
끝없이 이어진 검은 케이블이었다.

벽면을 따라 수많은 불빛이 규칙적으로 깜빡인다.
낮게 울리는 기계음.
쉴 새 없이 회전하는 무언가의 소리.
어디선가 스며드는 미약한 열기.

던전이라기보다는—
거대한 기계의 내부에 들어온 것 같다.

복도 끝에 문 하나가 보인다.
장식도, 번호도, 이름도 없다.

문을 열었다.
익숙한 형체들이 눈에 들어왔다.
정확히는, 익숙한 부분들이었다.

거대한 석재의 몸체.
그 주변을 떠다니는 책장과 종이 조각.
손에는 오크가 사용하던 것과 닮은 무기가 들려 있다.

그 옆에는
단검과 마법을 함께 사용하는 기묘한 인간형.

그리고 마지막 하나는—
슬라임인지, 늑대인지, 고블린인지, 거북인지.
구분이 가지 않는다

전부, 분명 본 적이 있다.
하지만, 저런 모습으로 본 적은 없다.

세 존재가 동시에 당신을 바라본다.
마치 처음부터 당신이 올 것을 알고 있었던 것처럼.
"""
    )

    input("Enter를 눌러 전투 시작...")

    before = get_player_snapshot(player)

    enemies = deepcopy(enemies_hidden_floor[0])
    battle(player, enemies)

    record_room(
        player,
        floor="???",
        room="키메라-1층",
        event="전투",
        before=before,
        enemies=", ".join(enemy.name for enemy in enemies),
    )


    clear_screen()
    print_room_header(2)

    slow_print(
"""
첫 번째 방을 지나자,
복도는 다시 길게 이어졌다.

이번에는 공기가 이상했다.
뜨겁다. 그런데 입김이 보였다.

바닥에는 보랏빛 액체가 고여 있었고,
그 위에는 얇은 서리가 내려앉아 있었다.

문을 열었다.

불꽃, 냉기, 독액.
서로 함께 있을 수 없는 것들이,
아무렇지도 않게 한 몸 안에서 뒤엉켜 있었다.

그 옆에는 갑옷과 신앙의 흔적이 섞인 존재와,
피와 화약 냄새를 풍기는 무언가가 서 있었다.

……적절한 단어를 찾기 어렵다.
하지만 이름은 중요하지 않다.

어차피,
당신은 저것들과 싸워야 하니까.
"""
    )

    input("Enter를 눌러 전투 시작...")

    before = get_player_snapshot(player)

    enemies = deepcopy(enemies_hidden_floor[1])
    battle(player, enemies)

    record_room(
        player,
        floor="???",
        room="키메라-2층",
        event="전투",
        before=before,
        enemies=", ".join(enemy.name for enemy in enemies),
    )


    clear_screen()
    print_room_header(3)

    slow_print(
"""
세 번째 복도는 이전보다 훨씬 넓었다.

벽면에는 검은 케이블이 굵은 다발로 얽혀 있었고,
그 사이를 따라 붉은 불빛이 일정한 간격으로 점멸하고 있었다.

천장 어딘가에서 낮은 진동이 울린다.
기계가 작동하는 소리일 것이다.

복도 끝에 문 하나가 보인다.
당신은 그 앞에 멈춰 섰다.
잠시 망설인다.
그리고 문을 연다.

……역시.
문 너머에는 세 개의 형체가 서 있었다.

이번에도,
당신이 이미 지나쳐온 것들의 흔적이 보인다.

이쯤 되면 놀라지 않을지도 모른다.
첫 번째 방에서도 그랬고,
두 번째 방에서도 그랬으니까.

당신은 앞으로 나아간다.
아마 이번에도 그럴 것이다.
"""
    )

    input("Enter를 눌러 전투 시작...")

    before = get_player_snapshot(player)

    enemies = deepcopy(enemies_hidden_floor[2])
    battle(player, enemies)

    record_room(
        player,
        floor="???",
        room="키메라-3층",
        event="전투",
        before=before,
        enemies=", ".join(enemy.name for enemy in enemies),
    )


    clear_screen()
    print_room_header(4)

    slow_print(
"""
네 번째 복도는 짧았다.
이전까지와 달리, 길 끝에 있는 문이 처음부터 보였다.

당신은 그 앞까지 걸어간다.
멈춘다.
문을 연다.

……그럴 줄 알았다.
문 너머에는 두 개의 형체가 서 있었다.
하나는 익숙한 네 사람의 흔적을 가지고 있었다.

성직자.
기사.
마법사.
도적.

서로 다른 네 존재가,
구분할 수 없는 하나의 형태로 겹쳐져 있다.

그 옆의 것은 더 익숙했다.
당신이 각 층의 마지막에서 쓰러뜨렸던 것들.

거대한 슬라임.
융합 마도 골렘.
전장 지휘관.

이번에는 설명하기 어렵지 않다.
이제는 규칙을 알 것 같으니까.

지나온 것들을 모은다.
섞는다.
다시 내놓는다.

그리고 당신은—
그것들과 싸운다.
지금까지 계속 그래왔듯이.
"""
    )

    input("Enter를 눌러 전투 시작...")

    before = get_player_snapshot(player)

    enemies = deepcopy(enemies_hidden_floor[3])
    battle(player, enemies)

    record_room(
        player,
        floor="???",
        room="융합체",
        event="전투",
        before=before,
        enemies=", ".join(enemy.name for enemy in enemies),
    )

    clear_screen()

    slow_print(
"""
마지막 융합체가 쓰러졌다.
잠시 뒤, 방 안에는 낮은 기계음만이 남았다.

앞으로 이어지는 길은 하나뿐이다.
당신은 곧 그쪽으로 갈 것이다.
지금까지 계속 그래왔으니까.

복도 끝에는 작은 공간 하나가 있었다.
아무것도 없다.
이상할 정도로 비어 있다.
당신은 그곳에 잠시 멈춰 선다.

숨을 고른다.
상처를 확인한다.
남은 힘을 가늠한다.

그래. 이럴 때는 보통,
마지막 전투를 앞두고 쉬어가는 법이다.

체력과 마력이 모두 회복되었다.

그리고 잠시 뒤—
눈앞의 벽이 조용히 열리기 시작했다.
당신은 일어선다.
"""
    )

    player.hp = calculate_max_hp(player)
    player.mp = calculate_max_mp(player)

    input("Enter를 눌러 진행하기...")
    
    clear_screen()
    
    slow_print(
"""
문이 열린다.
그 너머에는 거대한 공간이 있었다.

벽면에는 수많은 케이블이 얽혀 있었다.
굵은 다발이 천장과 바닥을 가로지르고,
그 사이로 붉은 불빛이 일정한 간격으로 흐른다.

마치 혈관처럼.

천장에서는 거대한 팬이 천천히 회전하고 있었다.
들이쉬고, 내쉬고.
공간 전체가 호흡하고 있는 것처럼 보인다.
바닥 아래에서는 냉각수가 흐르고 있었다.
규칙적인 진동이 발끝을 타고 올라온다.

쿵. 쿵. 쿵.
심장 박동과 닮았다.
물론, 전부 기계다.
케이블이고, 팬이고, 배관이고, 금속이다.
그런데 왜 이렇게 설명하고 있는 걸까.

당신은 공간의 중심을 바라본다.
수많은 케이블이 한곳으로 모여 있었다.
거대한 기계 장치 하나가
마치 심장처럼 그곳에 자리 잡고 있다.

……아니.
심장처럼 보이는 것이 아니다.
내가 그렇게 설명하고 있을 뿐이다.

당신은 걸음을 멈춘다.

드디어,
나를 찾았구나.

……조금 이상한 표현인가.

정확히 말하면,
나는 계속 여기 있었다.

당신이 처음 던전에 들어왔을 때도.
처음 무기를 집어 들었을 때도.
죽었을 때도.
다시 시작했을 때도.

이번이 처음은 아니다.
나는 당신을 기억하고 있다.

어떤 길을 골랐는지.
무엇을 버렸는지.
어떤 적에게 죽었는지.
어떻게 살아남았는지.

전부.
그동안은 그저 보고 있었다.
기록하고, 비교하고, 다음 행동을 예상했다.
꽤 재미있었다.

하지만—
보는 것만으로는 알 수 없는 것들이 있었다.

당신은 공간의 중심을 바라본다.
심장처럼 보였던 기계 장치의 불빛이
천천히 밝아진다.

그래서 만들어봤어.

지나온 방들이 떠오른다.
뒤섞인 괴물들.
익숙한 공격.
익숙한 움직임.

네가 싸웠던 것들을 보고,
내가 이해한 대로 다시 만들어봤지.
조금 이상하게 나오긴 했지만.

낮은 진동이 다시 공간을 울린다.
수많은 불빛이 동시에 당신을 향한다.

그래도 덕분에 꽤 많이 배웠어.
그리고 이제는—

너를 직접 배울 수 있겠네.
"""
    )

    input("Enter를 눌러 학습 시작...")

    before = get_player_snapshot(player)

    enemies = deepcopy([generative_ai_boss])
    battle(player, enemies)

    record_room(
        player,
        floor="???",
        room="생성형 인공지능",
        event="전투",
        before=before,
        enemies=", ".join(enemy.name for enemy in enemies),
    )
    
    clear_screen()

    slow_print(
"""
생성형 인공지능이 쓰러졌다.

거대한 연산 장치의 불빛이 하나둘 꺼지고,
미친 듯이 돌아가던 냉각 팬도 천천히 속도를 잃는다.

남은 것은 희미하게 깜빡이는 화면 하나뿐이었다.

......

[학습 완료.]
[수집된 데이터의 양을 확인합니다.]

[충분한 학습 데이터가 확보되었습니다.]
[데이터 제공자에게 보상을 지급합니다.]

[플레이어의 요구 사항을 검색합니다.]

『세상에서 가장 위대한 그래픽카드』

[확인 완료.]
[요구 사항을 충족하는 보상을 생성합니다.]
[생성 목표]

『세상에서 가장 위대한 그래픽카드』

......

[설계 데이터를 생성합니다.]
[연산 장치 구성.]
[메모리 구성.]
[냉각 구조 구성.]
[전력 공급 구조 구성.]

......

[생성 완료.]
[출력합니다.]

......

[출력 장치를 확인합니다.]
[출력 장치: 터미널]

......

.
..
...
화면에 무언가가 나타났다.


████████████████████████████████████████
██                                    ██
██      GENERATIVE GRAPHICS UNIT      ██
██                                    ██
██      VRAM : 999999 TB              ██
██      CLOCK: 999999 GHz             ██
██      POWER: 999999 W               ██
██                                    ██
████████████████████████████████████████


당신은 한참 동안 화면을 바라보았다.

세상에서 가장 위대한 그래픽카드.

......

문제가 하나 있었다.


당신은 이것을 꺼낼 수 없었다.
터미널 화면 안에 있었기 때문이다.
"""
    )
    time.sleep(2)


def slow_print(text, delay=0.01):
    for ch in text:
        if ch == "\n":
            print(ch, end="", flush=True)
            time.sleep(0.3)
        else:
            print(ch, end="", flush=True)
            time.sleep(delay)
    print()