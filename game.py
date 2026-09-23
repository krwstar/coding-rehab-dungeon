import time

from colorama import just_fix_windows_console

from data import prologue_text, early_access
from dungeon import run_floor, run_last_floor, slow_print
from player_utils import create_player, select_job
from run_log import save_run_log

just_fix_windows_console()

def main():
    print("코딩 재활치료 목적 로그라이크 던전 돌파 게임!")
    start = input("Enter A button... ")
    if start.lower() == "a":
        print("==== GAME OVER ====")
        print("거기서는 B버튼이 정석이잖아?")
        input()
        exit()
    elif start.lower() != "b":
        print("==== GAME OVER ====")
        print("A를 입력하세요.")
        input()
        exit()
    if input("프롤로그를 보시겠습니까? y/n: ").lower() == "y":
        slow_print(prologue_text)
        time.sleep(1)
    player = create_player()
    select_job(player)

    print()
    print("=" * 45)
    print("                  게임 시작")
    print("=" * 45)
    print()

    run_floor(player, 1)
    
    print()
    print("=" * 45)
    print("                  1층 클리어!")
    print("=" * 45)
    print()
    
    run_floor(player, 2)
    
    print()
    print("=" * 45)
    print("                  2층 클리어!")
    print("=" * 45)
    print()
    
    run_floor(player, 3)
    
    print()
    print("=" * 45)
    print("                  3층 클리어!")
    print("=" * 45)
    print()
    
    run_last_floor(player)
    
    print("\033[2J\033[H", end="")
    save_run_log(player, "클리어")
    slow_print(
f"""


=====================================
『코딩재활치료 그래픽카드 던전(가제)』
=====================================


디렉터

krwstar


프로그래밍

krwstar


보조 프로그래밍

ChatGPT


게임 디자인

krwstar


시나리오

krwstar


밸런스 디자인

{player.name}


QA

{player.name}


플레이테스트

{player.name}


아트

{player.name}


사운드

{player.name}




Special Thanks

{player.name}




Thank you for playing!
"""
    )


if __name__ == "__main__":
    main()
    time.sleep(2)
