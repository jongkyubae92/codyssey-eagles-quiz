def display_menu():
    print("\n--- [ 프로그램 메뉴 ] ---")
    print("1. 환영 인사하기")
    print("2. 프로그램 정보 보기")
    print("3. 종료하기")
    print("-----------------------")

def main():
    while True:
        display_menu()
        choice = input("원하는 기능의 번호를 입력하세요: ")

        if choice == '1':
            print("\n-> 안녕하세요! 프로그램에 오신 것을 환영합니다.")
        elif choice == '2':
            print("\n-> 이 프로그램은 메뉴 선택 기능을 테스트하기 위해 만들어졌습니다.")
        elif choice == '3':
            print("\n-> 프로그램을 종료합니다. 이용해 주셔서 감사합니다!")
            break  # 반복문을 빠져나가 프로그램을 종료합니다.
        else:
            # 잘못된 입력(숫자가 아니거나 범위를 벗어난 경우) 처리
            print("\n[오류] 잘못된 입력입니다. 1, 2, 3 중에서 선택해 주세요.")

if __name__ == "__main__":
    main()