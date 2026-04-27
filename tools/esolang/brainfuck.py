"""极简 Brainfuck 解释器。

供 provinces/brainfuck/ 等 esolang 类郡复用。
约束：
- 默认磁带 30000 字节，可自动扩展到 1 MB；
- 默认最多 5_000_000 步，超限抛 RuntimeError；
- `,` 从给定 stdin 字符串读取（不阻塞终端）。
"""
from __future__ import annotations

from typing import Tuple


TAPE_INITIAL_SIZE = 30000
TAPE_MAX_SIZE = 1_048_576
DEFAULT_MAX_STEPS = 5_000_000


def _build_bracket_map(src: str) -> dict[int, int]:
    stack: list[int] = []
    pairs: dict[int, int] = {}
    for i, ch in enumerate(src):
        if ch == "[":
            stack.append(i)
        elif ch == "]":
            if not stack:
                raise SyntaxError(f"unmatched ] at position {i}")
            j = stack.pop()
            pairs[i] = j
            pairs[j] = i
    if stack:
        raise SyntaxError(f"unmatched [ at position {stack[-1]}")
    return pairs


def run_bf(
    src: str,
    *,
    stdin: str = "",
    max_steps: int = DEFAULT_MAX_STEPS,
) -> Tuple[str, int]:
    """运行 Brainfuck 源码。

    返回 (输出字符串, 实际步数)。
    """
    # 仅保留 8 个有效指令
    src = "".join(c for c in src if c in "><+-.,[]")
    bracket = _build_bracket_map(src)

    tape = bytearray(TAPE_INITIAL_SIZE)
    ptr = 0
    pc = 0
    out: list[str] = []
    in_buf = stdin.encode("utf-8")
    in_pos = 0
    steps = 0

    while pc < len(src):
        if steps >= max_steps:
            raise RuntimeError(f"BF: 超过 {max_steps} 步")
        steps += 1

        c = src[pc]
        if c == ">":
            ptr += 1
            if ptr >= len(tape):
                if len(tape) >= TAPE_MAX_SIZE:
                    raise RuntimeError("BF: 磁带超限")
                tape.extend(b"\x00" * min(len(tape), TAPE_MAX_SIZE - len(tape)))
        elif c == "<":
            if ptr == 0:
                raise RuntimeError("BF: 指针越下界")
            ptr -= 1
        elif c == "+":
            tape[ptr] = (tape[ptr] + 1) & 0xFF
        elif c == "-":
            tape[ptr] = (tape[ptr] - 1) & 0xFF
        elif c == ".":
            out.append(chr(tape[ptr]))
        elif c == ",":
            if in_pos < len(in_buf):
                tape[ptr] = in_buf[in_pos]
                in_pos += 1
            else:
                tape[ptr] = 0
        elif c == "[":
            if tape[ptr] == 0:
                pc = bracket[pc]
        elif c == "]":
            if tape[ptr] != 0:
                pc = bracket[pc]
        pc += 1

    return "".join(out), steps


if __name__ == "__main__":
    import sys
    src = sys.stdin.read()
    output, used = run_bf(src)
    sys.stderr.write(f"[bf] {used} steps\n")
    sys.stdout.write(output)
