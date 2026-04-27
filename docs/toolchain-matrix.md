# 工具链矩阵

> 工部之责：使天下郡县所用工具，皆有所出，皆有所版。

本文档列出每种 Runner 所依赖的核心工具链、推荐版本、Docker 镜像。

## 1. 概览

| Runner | 主要依赖 | 平台 | 离线可行 |
|---|---|---|:---:|
| `direct` | 各语言官方解释器 | L/M/W | ✅ |
| `compiled` | C/C++/Rust/Go 等编译器 | L/M/W | ✅ |
| `vm` | JDK 17+ / .NET 8+ / BEAM | L/M/W | ✅ |
| `docker` | Docker / Podman | L/M/W | 镜像缓存后 ✅ |
| `nix` | Nix（multi-user） | L/M | ✅ |
| `query` | sqlite / jq / xmllint / graphql-cli | L/M/W | ✅ |
| `render` | mermaid-cli / graphviz / plantuml.jar | L/M/W | ✅ |
| `proof` | Lean / Coq / Agda / TLA+ Tools | L/M | 镜像 ✅ |
| `shader` | glslangValidator / DXC / naga | L/M/W | ✅ |
| `hdl` | iverilog / verilator / ghdl | L/M | ✅ |
| `esolang` | tools/esolang/*.py（自带） | L/M/W | ✅ |
| `manual` | 由 manifest 标注 | - | ❌ |

> L=Linux  M=macOS  W=Windows

## 2. Direct Runner 工具链

| ID | 工具 | 推荐版本 | 安装提示 |
|---|---|---|---|
| python | CPython | 3.11+ | python.org / pyenv |
| ruby | Ruby | 3.2+ | rbenv |
| php | PHP | 8.2+ | system / brew |
| perl | Perl | 5.36+ | system |
| lua | Lua | 5.4 | brew / apt |
| tcl | Tcl | 8.6 | system |
| javascript | Node.js | 20 LTS | nvm |
| typescript | tsx / ts-node | 最新 | npm i -g tsx |
| dart | Dart SDK | 3.x | dart.dev |
| bash | Bash | 5.x | system |
| powershell | PowerShell | 7.x | github releases |
| awk | gawk | 5.x | apt / brew |

## 3. Compiled Runner 工具链

| ID | 编译器 | 推荐版本 |
|---|---|---|
| c | gcc / clang | gcc 13 / clang 17 |
| cpp | g++ / clang++ | -std=c++20 |
| rust | rustc | 1.79+ (stable) |
| go | go | 1.22+ |
| zig | zig | 0.13+ |
| nim | nim | 2.0+ |
| crystal | crystal | 1.10+ |
| fortran | gfortran | 13+ |
| pascal | fpc | 3.2+ |
| nasm-x86 | nasm + ld | 2.16+ |

## 4. VM Runner 工具链

| ID | 工具 | 版本 |
|---|---|---|
| java | JDK | 17 LTS / 21 LTS |
| kotlin | Kotlin CLI | 2.0+ |
| scala | scala-cli | 1.4+ |
| clojure | Clojure CLI | 1.11+ |
| csharp | .NET SDK | 8 LTS |
| fsharp | .NET SDK | 8 LTS |
| erlang | Erlang/OTP | 26+ |
| elixir | Elixir | 1.16+ |
| gleam | gleam | 1.x |

## 5. Docker Runner 镜像

镜像统一发布到 `qinlang/<id>` 命名空间。  
基线规则：

1. 基础镜像优先 `debian:stable-slim` 或 `alpine`；
2. 镜像必须固定版本号，不允许 `latest`；
3. ENTRYPOINT 必须以 `/usr/local/bin/qinlang-province` 包装器调用，统一处理 stdin/stdout；
4. 镜像内置非 root 用户 `qin:qin (uid=10000)`。

| ID | 镜像 | 大小目标 |
|---|---|---|
| cobol | `qinlang/cobol:1.0` | < 200 MB |
| ada | `qinlang/ada:1.0` | < 250 MB |
| haskell | `qinlang/haskell:9.8` | < 400 MB |
| ocaml | `qinlang/ocaml:5.1` | < 300 MB |
| prolog | `qinlang/prolog:9.2` | < 150 MB |
| racket | `qinlang/racket:8.12` | < 250 MB |
| smalltalk | `qinlang/pharo:11` | < 200 MB |

## 6. Render Runner 工具链

| ID | 工具 | 版本 |
|---|---|---|
| mermaid | mermaid-cli (mmdc) | 10.x |
| dot | Graphviz | 9.x |
| plantuml | plantuml.jar | 1.2024+ |
| asciidoc | asciidoctor | 2.0+ |
| markdown | pandoc / cmark-gfm | 最新 |
| tikz | TeX Live (latex/pdflatex) | 2024 |
| vega | vega-cli | 5.x |
| vega-lite | vega-lite-cli | 5.x |

## 7. Proof Runner 工具链

| ID | 工具 | 版本 |
|---|---|---|
| lean4 | Lean | 4.10+ |
| coq | Rocq / Coq | 8.19+ |
| agda | Agda | 2.6.4+ |
| idris2 | Idris 2 | 0.7+ |
| isabelle | Isabelle | 2024 |
| tlaplus | TLA+ Tools | 1.8+ |
| alloy | Alloy | 6.x |
| dafny | Dafny | 4.x |
| z3-smt | z3 | 4.13+ |

## 8. HDL Runner 工具链

| ID | 工具 | 备注 |
|---|---|---|
| verilog | iverilog + vvp | 仿真 |
| systemverilog | verilator | 仅子集 |
| vhdl | ghdl | LLVM 后端 |
| chisel | sbt + firtool | 走 vm runner 链 |
| amaranth | python | 走 direct runner |

## 9. Shader Runner 工具链

| ID | 工具 | 备注 |
|---|---|---|
| glsl | glslangValidator | 编译验证 |
| hlsl | DXC | dxc.exe |
| wgsl | naga | wgpu 项目 |
| spirv-asm | spirv-as | spirv-tools |
| msl | metal compiler | macOS 限定 |

## 10. Esolang Runner 工具链

`tools/esolang/` 自带轻量解释器（Python 实现）：

| ID | 解释器 | 来源 |
|---|---|---|
| brainfuck | `tools/esolang/brainfuck.py` | 自研 |
| whitespace | `tools/esolang/whitespace.py` | 自研 |
| lolcode | `tools/esolang/lolcode.py` | 包装 lci |
| befunge | `tools/esolang/befunge.py` | 自研 |
| piet | `tools/esolang/piet.py` | 自研 + PIL |
| rockstar | `npx rockstar-lang` | npm |
| arnoldc | `tools/esolang/arnoldc/` | jar |

> 所有自研解释器必须有单元测试，覆盖率 ≥ 70%。

## 11. 平台兼容性矩阵

> 仅列出与平台强相关的语言。

| ID | Linux | macOS | Windows | 说明 |
|---|:---:|:---:|:---:|---|
| powershell | ✅ | ✅ | ✅ | 全平台 |
| batch | ❌ | ❌ | ✅ | Windows 限定 |
| applescript | ❌ | ✅ | ❌ | macOS 限定 |
| msl | ❌ | ✅ | ❌ | Metal 限定 |
| labview | ❌ | ❌ | ⚠️ | 商业平台 |
| abap | ❌ | ❌ | ⚠️ | SAP 平台 |
| apex | ❌ | ❌ | ⚠️ | Salesforce 平台 |
| objective-c | ⚠️ | ✅ | ❌ | macOS 优先 |

> ⚠️ 表示需要专有平台或商业授权。

## 12. CI 矩阵建议

```yaml
matrix:
  os: [ubuntu-22.04, macos-14, windows-2022]
  bundle:
    - core            # 20 主流语言
    - extended        # 50 种
    - exotic          # esolang + historical
    - heavy           # docker / proof / hdl
exclude:
  - { os: windows-2022, bundle: heavy }   # 重镜像跳过 Windows
  - { os: macos-14, bundle: heavy }
```
