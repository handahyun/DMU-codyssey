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
        super().__init__()
        self.setWindowTitle("계산기")
        self.setFixedSize(320, 520)
        self.setStyleSheet("background-color: #1c1c1e;")

        # 문자열 누적 저장 변수
        self.current_input = ""
        self.just_calculated = False

        # 위젯을 수직으로 쌓는 레이아웃
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(12, 20, 12, 12)
        main_layout.setSpacing(10)

        # 디스플레이
        self.display = QLabel("0")
        self.display.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom
        )
        self.display.setFont(QFont("Arial", 52, QFont.Weight.Light))
        self.display.setStyleSheet("color: white; padding: 10px 8px 0px 8px;")
        self.display.setMinimumHeight(120)
        main_layout.addWidget(self.display)

        # 버튼 그리드
        grid = QGridLayout()
        grid.setSpacing(10)

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

        for text, row, col, btn_type in buttons:
            btn = QPushButton(text)
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

            btn.clicked.connect(lambda checked, t=text: self.on_button_click(t))

        main_layout.addLayout(grid)
        self.setLayout(main_layout)

    # ---사칙연산 메소드---

    def add(self, a, b):
        """덧셈"""
        return a + b

    def subtract(self, a, b):
        """뺄셈"""
        return a - b

    def multiply(self, a, b):
        """곱셈"""
        return a * b

    def divide(self, a, b):
        """나눗셈 (0 나눗셈 예외 처리 포함)"""
        if b == 0:
            raise ZeroDivisionError("0으로 나눌 수 없습니다.")
        return a / b

    # ---보조 기능 메소드---

    def reset(self):
        """AC: 입력값과 디스플레이 초기화"""
        self.current_input = ""
        self.just_calculated = False
        self.display.setText("0")
        self._adjust_font(1)

    def negative_positive(self):
        """+/-: 현재 마지막 피연산자의 부호 반전"""
        if not self.current_input or self.current_input == "0":
            return

        # 마지막 피연산자 위치 파악
        operators = ("÷", "×", "−", "+")
        last_op_idx = -1
        for op in operators:
            idx = self.current_input.rfind(f" {op} ")
            if idx > last_op_idx:
                last_op_idx = idx

        if last_op_idx == -1:
            # 피연산자가 하나뿐인 경우
            if self.current_input.startswith("-"):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = "-" + self.current_input
        else:
            # 연산자 뒤 마지막 피연산자만 부호 반전
            prefix = self.current_input[: last_op_idx + 3]  # " OP " 포함
            last_operand = self.current_input[last_op_idx + 3 :]
            if last_operand.startswith("-"):
                last_operand = last_operand[1:]
            else:
                last_operand = "-" + last_operand
            self.current_input = prefix + last_operand

        self.display.setText(self.current_input)
        self._adjust_font(len(self.current_input))

    def percent(self):
        """%: 현재 입력값에 % 추가 (이미 있으면 추가 안 함)"""
        if self.current_input and not self.current_input.endswith("%"):
            self.current_input += "%"
            self.display.setText(self.current_input)
            self._adjust_font(len(self.current_input))

    # ---등호 메소드---

    def equal(self):
        """수식을 파싱해 사칙연산 메소드로 계산하고 결과를 표시"""
        if not self.current_input:
            return

        # 디스플레이 기호 -> 파이썬 연산자 매핑
        op_map = {"÷": "/", "×": "*", "−": "-"}

        # 수식을 토큰으로 분리
        expr = self.current_input
        tokens = []
        current_token = ""
        i = 0
        while i < len(expr):
            ch = expr[i]
            if ch == " ":
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
            elif ch in op_map or ch == "+":
                # 연산자 앞뒤 공백으로 구분되므로 토큰으로 추가
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
                tokens.append(ch)
            else:
                current_token += ch
            i += 1
        if current_token:
            tokens.append(current_token)

        # 퍼센트 처리
        def parse_number(s):
            if s.endswith("%"):
                return float(s[:-1]) / 100
            return float(s)

        try:
            # 단일 숫자
            if len(tokens) == 1:
                result = parse_number(tokens[0])
            elif len(tokens) == 3:
                a = parse_number(tokens[0])
                op = tokens[1]
                b = parse_number(tokens[2])

                if op == "+":
                    result = self.add(a, b)
                elif op == "−":
                    result = self.subtract(a, b)
                elif op == "×":
                    result = self.multiply(a, b)
                elif op == "÷":
                    result = self.divide(a, b)
                else:
                    result = eval(f"{a}{op_map.get(op, op)}{b}")
            else:
                # 토큰이 3개를 초과하는 복합 수식은 eval 로 fallback
                safe_expr = expr
                for k, v in op_map.items():
                    safe_expr = safe_expr.replace(k, v)
                safe_expr = safe_expr.replace("%", "/100")
                result = eval(safe_expr)

            # 정수로 떨어지면 소수점 제거, 아니면 소수점 6자리 반올림
            if isinstance(result, float) and result == int(result):
                result = int(result)
            elif isinstance(result, float):
                result = round(result, 6)
                # 반올림 후 정수가 됐으면 int로
                if result == int(result):
                    result = int(result)

            self.current_input = str(result)
            self.just_calculated = True

        except ZeroDivisionError:
            self.current_input = "오류"
        except Exception:
            self.current_input = "오류"

        self.display.setText(self.current_input)
        self._adjust_font(len(self.current_input))

    # ---폰트 크기 자동 조절---

    def _adjust_font(self, length):
        """글자 수에 따라 디스플레이 폰트 크기 조정"""
        if length <= 6:
            size = 52
        elif length <= 9:
            size = 38
        else:
            size = 28
        self.display.setFont(QFont("Arial", size, QFont.Weight.Light))

    # ---버튼 클릭 이벤트---

    def on_button_click(self, text):
        if text == "AC":
            self.reset()

        elif text == "+/-":
            self.negative_positive()

        elif text == "%":
            self.percent()

        elif text in ("÷", "×", "−", "+"):
            if self.current_input:
                self.current_input += f" {text} "
                self.display.setText(self.current_input)
                self._adjust_font(len(self.current_input))
            self.just_calculated = False

        elif text == "=":
            self.equal()

        elif text == ".":
            # 마지막 피연산자에 소수점이 없을 때만 추가
            parts = self.current_input.split(" ")
            last = parts[-1] if parts else ""
            if "." not in last:
                self.current_input += "."
                display_text = self.current_input if self.current_input else "0."
                self.display.setText(display_text)
                self._adjust_font(len(display_text))

        else:
            # 숫자 입력
            if self.just_calculated:
                self.current_input = text
                self.just_calculated = False
            elif self.current_input == "0":
                self.current_input = text
            else:
                self.current_input += text
            self.display.setText(self.current_input)
            self._adjust_font(len(self.current_input))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    app.exec()
