import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QPushButton,
    QLabel,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class Calculator(QWidget):
    def __init__(self):
        # 부모 클래스(QWidget)의 __init__ 호출
        super().__init__()
        self.setWindowTitle("계산기")
        # 창 크기 조절 고정
        self.setFixedSize(320, 520)
        self.setStyleSheet("background-color: #1c1c1e;")

        # 문자열 누적 저장 변수
        self.current_input = ""
        self.just_calculated = False

        # 위젯을 수직으로 쌓는 레이아웃
        main_layout = QVBoxLayout()
        # 좌, 상, 우, 하 여백
        main_layout.setContentsMargins(12, 20, 12, 12)
        # 내부 위젯 간격
        main_layout.setSpacing(10)

        # 디스플레이
        # 초기값 0
        self.display = QLabel("0")
        self.display.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom
        )
        self.display.setFont(QFont("Arial", 52, QFont.Weight.Light))
        self.display.setStyleSheet("color: white; padding: 10px 8px 0px 8px;")
        self.display.setMinimumHeight(120)
        main_layout.addWidget(self.display)

        # 버튼 그리드
        # 계산기 버튼을 5행 4열로 배치
        grid = QGridLayout()
        # 버튼 간 간격
        grid.setSpacing(10)

        # 버튼 목록을 텍스트, 행, 열, 타입 튜플로 정의
        buttons = [
            ("AC", 0, 0, "func"),
            ("+/-", 0, 1, "func"),
            ("%", 0, 2, "func"),
            ("÷", 0, 3, "op"),
            ("7", 1, 0, "num"),
            ("8", 1, 1, "num"),
            ("9", 1, 2, "num"),
            ("×", 1, 3, "op"),
            ("4", 2, 0, "num"),
            ("5", 2, 1, "num"),
            ("6", 2, 2, "num"),
            ("−", 2, 3, "op"),
            ("1", 3, 0, "num"),
            ("2", 3, 1, "num"),
            ("3", 3, 2, "num"),
            ("+", 3, 3, "op"),
            ("0", 4, 0, "num"),
            (".", 4, 2, "num"),
            ("=", 4, 3, "op"),
        ]

        colors = {
            "func": ("#a5a5a5", "#d4d4d4", "#1c1c1e"),
            "op": ("#ff9f0a", "#ffc355", "white"),
            "num": ("#333333", "#4d4d4d", "white"),
        }

        # 버튼 목록을 순회하며 그리드에 배치
        for text, row, col, btn_type in buttons:
            btn = QPushButton(text)
            # 타입 별 색상
            btn_color, hover_color, text_color = colors[btn_type]

            if text == "0":
                btn.setFixedHeight(72)
                btn.setStyleSheet(
                    f"""
                    QPushButton {{
                        background-color: {btn_color};
                        color: {text_color};
                        border-radius: 36px;
                        font-size: 26px;
                        font-weight: 400;
                        text-align: left;
                        padding-left: 26px;
                    }}
                    QPushButton:pressed {{
                        background-color: {hover_color};
                    }}
                """
                )

                # 1행 2열 차지
                grid.addWidget(btn, row, col, 1, 2)
            else:
                btn.setFixedSize(72, 72)
                btn.setStyleSheet(
                    f"""
                    QPushButton {{
                        background-color: {btn_color};
                        color: {text_color};
                        border-radius: 36px;
                        font-size: 26px;
                        font-weight: 400;
                    }}
                    QPushButton:pressed {{
                        background-color: {hover_color};
                    }}
                """
                )

                grid.addWidget(btn, row, col)

            # 버튼 클릭 시 on_button_click 메서드를 호출
            btn.clicked.connect(lambda checked, t=text: self.on_button_click(t))

        main_layout.addLayout(grid)
        self.setLayout(main_layout)

    # 버튼 클릭 이벤트 처리 메서드
    def on_button_click(self, text):
        if text == "AC":
            # 입력값 초기화
            self.current_input = ""
            self.display.setText("0")

        elif text == "+/-":
            # 맨 앞에 - 를 붙이거나 제거
            if self.current_input and self.current_input != "0":
                if self.current_input.startswith("-"):
                    self.current_input = self.current_input[1:]
                else:
                    self.current_input = "-" + self.current_input
                self.display.setText(self.current_input)

        elif text == "%":
            if self.current_input:
                self.current_input += "%"
                self.display.setText(self.current_input)

        elif text in ("÷", "×", "−", "+"):
            # 입력값이 있을 때 사칙연산 기호를 공백과 함께 추가
            if self.current_input:
                self.current_input += f" {text} "
                self.display.setText(self.current_input)

        elif text == "=":
            if self.current_input:
                # 디스플레이용 기호를 연산자로 교체
                expr = self.current_input
                expr = expr.replace("÷", "/")
                expr = expr.replace("×", "*")
                expr = expr.replace("−", "-")

                try:
                    result = eval(expr)
                    # 정수로 떨어지면 소수점 제거
                    if result == int(result):
                        result = int(result)
                    self.current_input = str(result)
                    self.just_calculated = True
                except:
                    self.current_input = "오류"
                self.display.setText(self.current_input)

        elif text == ".":
            # 이미 . 이 있으면 추가X
            parts = self.current_input.split(" ")
            last = parts[-1] if parts else ""
            if "." not in last:
                self.current_input += "."
                self.display.setText(self.current_input if self.current_input else "0.")

        else:
            # 계산 직후면 새로운 입력 시작
            if self.just_calculated:
                self.current_input = text
                self.just_calculated = False
            elif self.current_input == "0":
                self.current_input = text
            else:
                self.current_input += text
            self.display.setText(self.current_input)

        # 글자 수에 따라 폰트 크기 자동 조절
        length = len(self.display.text())
        if length <= 6:
            size = 52
        elif length <= 9:
            size = 38
        else:
            size = 28
        self.display.setFont(QFont("Arial", size, QFont.Weight.Light))


if __name__ == "__main__":

    # QApplication 객체 생성
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    app.exec()
