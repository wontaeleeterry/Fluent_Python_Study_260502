from dataclasses import dataclass

@dataclass(frozen=True)
class Money:
    amount: int

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("금액은 음수가 될 수 없습니다.")