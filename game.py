import time

from colorama import just_fix_windows_console

from data import prologue_text, early_access
from dungeon import run_floor, run_last_floor, run_hidden_floor, slow_print
from player_utils import create_player, select_job
from run_log import save_run_log

just_fix_windows_console()

import time

from colorama import just_fix_windows_console

from data import prologue_text
from dungeon import run_floor, run_last_floor, slow_print
from player_utils import create_player, select_job
from run_log import save_run_log
from meta_save import all_jobs_cleared, register_job_clear

just_fix_windows_console()


def clear_screen():
    print("\033[2J\033[H", end="")


def title_screen():
    clear_screen()

    print("=" * 55)
    print()
    print("        『코딩재활치료 그래픽카드 던전(가제)』")
    print()
    print("          코딩 재활치료 목적 로그라이크")
    print("              던전 돌파 게임!")
    print()
    print("=" * 55)
    print()
    print("                 Enter A button...")
    print()

    start = input("> ").strip().lower()

    if start == "a":
        clear_screen()
        print("==== GAME OVER ====")
        print()
        print("거기서는 B버튼이 정석이잖아?")
        input("\nEnter를 눌러 종료...")
        return False

    if start != "b":
        clear_screen()
        print("==== GAME OVER ====")
        print()
        print("A를 입력하세요.")
        input("\nEnter를 눌러 종료...")
        return False

    return True


def prologue_screen():
    clear_screen()

    print("=" * 55)
    print("                      프롤로그")
    print("=" * 55)
    print()
    print("프롤로그를 보시겠습니까?")
    print()
    print("[1] 예")
    print("[2] 아니오")
    print()

    while True:
        choice = input("> ").strip()

        if choice == "1":
            clear_screen()
            slow_print(prologue_text)
            time.sleep(1)
            input("\nEnter를 눌러 계속...")
            return

        if choice == "2":
            return

        print("올바른 번호를 입력하세요.")

def main():
    if not title_screen():
        return
    
    prologue_screen()

    clear_screen()
    player = create_player()
    select_job(player)

    clear_screen()
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
    input("\nEnter를 눌러 다음 층으로...")
    
    run_floor(player, 2)
    
    print()
    print("=" * 45)
    print("                  2층 클리어!")
    print("=" * 45)
    print()
    input("\nEnter를 눌러 다음 층으로...")
    
    run_floor(player, 3)
    
    print()
    print("=" * 45)
    print("                  3층 클리어!")
    print("=" * 45)
    print()
    input("\nEnter를 눌러 다음 층으로...")
    
    while True:
        print(
"""
복도 한쪽 벽면에 작은 단말기가 박혀 있다.
화면에는 단 한 문장만 떠 있었다.

「세상에서 가장 위대한 그래픽카드는?」

0. 무시하고 지나간다
"""
        )

        answer = input("> ").strip()

        if answer == "상상력":
            run_hidden_floor(player)
            break

        elif answer == "0":
            run_last_floor(player)
            break

        else:
            print("아무 일도 일어나지 않았다")
    
    
    register_job_clear(player.job)
    
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
