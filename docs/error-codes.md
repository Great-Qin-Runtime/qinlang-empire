# 错误码与状态码规范

> 凡郡县奉诏不力，必有所归。  
> 错有其名，名有其码，码有其档。

本文档定义 QinLang Empire 中所有可能出现的状态、错误码、退出码。

## 1. 结果状态（Result Status）

每条 `results.status` 必为以下之一：

| 状态 | 含义 | 是否计入 `passed` |
|---|---|:---:|
| `passed` | 通过：构建 + 运行 + schema 全部成功 | ✅ |
| `failed` | 失败：明确语义错误（构建错、断言错、退出码非零等） | ❌ |
| `timeout` | 超过 `timeout_ms` 限制 | ❌ |
| `oom` | 内存超限 | ❌ |
| `protocol-violation` | 输出不符合 schema | ❌ |
| `setup-error` | 工具链 / 环境缺失，调度器无法启动子进程 | ❌ |
| `skipped` | 被显式跳过（例如平台不支持） | ❌（计入 skipped） |
| `blocked` | manifest 显式标记 `blocked` | ❌（计入 skipped） |

> `oom` 与 `timeout` 在排行榜中独立计数，不污染失败原因统计。

## 2. 子进程退出码（建议）

| 退出码 | 含义 |
|---|---|
| 0 | 成功 |
| 1 | 业务失败（自定义） |
| 2 | 输入格式错误（无法解析诏书） |
| 3 | 协议错误（自检发现自身输出会违反协议） |
| 4 | 工具链错误（依赖缺失） |
| 64-78 | 兼容 BSD `sysexits.h`（可选） |
| 124 | 调度器观察到的超时（由调度器写入） |
| 137 | 进程被 SIGKILL（128+9，调度器写入） |

> 自身退出码 ≥ 200 视为非法，调度器会重写为 1 并报 `failed`。

## 3. 错误码（`error.code`）

错误码格式：`E` + 4 位数字。区段约定：

| 区段 | 类别 |
|---|---|
| E0001-E0099 | 协议 / 输入 / 输出 |
| E0100-E0199 | 调度器 / 中央朝廷 |
| E0200-E0299 | 户籍 / Registry |
| E0300-E0399 | Runner |
| E0400-E0499 | 构建 / 工具链 |
| E0500-E0599 | 运行时 |
| E0600-E0699 | 安全 |
| E0700-E0799 | Docker / 容器 |
| E0800-E0899 | 渲染 / 证明 / HDL |
| E0900-E0999 | 业务自定义保留 |

### 协议类（E0001-E0099）

| 码 | 名 | 描述 |
|---|---|---|
| E0001 | INVALID_INPUT_JSON | stdin 不是合法 JSON |
| E0002 | INPUT_SCHEMA_FAIL | 输入不符合 input.schema.json |
| E0003 | INVALID_OUTPUT_JSON | stdout 不是合法 JSON |
| E0004 | OUTPUT_SCHEMA_FAIL | 输出不符合 output.schema.json |
| E0005 | OUTPUT_TOO_LARGE | 输出超过 output_limit_kb |
| E0006 | LANGUAGE_MISMATCH | 输出 language 与 manifest.name 不一致 |
| E0007 | PROVINCE_MISMATCH | 输出 province 与 manifest.province 不一致 |
| E0008 | MISSING_OK_FALSE_ERROR | ok=false 时未提供 error 字段 |
| E0009 | NON_JSON_ON_STDOUT | stdout 中混入了非 JSON 文本 |

### 调度器类（E0100-E0199）

| 码 | 名 | 描述 |
|---|---|---|
| E0100 | EMPEROR_BOOT_FAIL | 调度器自身启动失败 |
| E0101 | UNKNOWN_MODE | mode 不是 parade/chain/graph |
| E0102 | UNKNOWN_PROVINCE | --province 指定了未登记 ID |
| E0103 | EMPTY_PARADE | 没有任何可运行的 province |
| E0104 | CHAIN_PLAN_INVALID | chain plan 文件不合规 |

### 户籍类（E0200-E0299）

| 码 | 名 | 描述 |
|---|---|---|
| E0200 | MANIFEST_NOT_FOUND | provinces/<id>/manifest.json 缺失 |
| E0201 | MANIFEST_SCHEMA_FAIL | manifest 不符合 manifest.schema.json |
| E0202 | DUPLICATE_ID | 多个目录使用同一 ID |
| E0203 | DIR_ID_MISMATCH | 目录名与 manifest.id 不一致 |
| E0204 | UNKNOWN_CATEGORY | category 不在 21 类之中 |
| E0205 | UNKNOWN_RUNNER | runner 不在 12 种之中 |
| E0206 | INVALID_PROVINCE_NAME | 郡名不以「郡」结尾或重复 |
| E0207 | SOURCE_NOT_FOUND | manifest.source 指向的文件不存在 |

### Runner 类（E0300-E0399）

| 码 | 名 | 描述 |
|---|---|---|
| E0300 | RUNNER_NOT_AVAILABLE | runner 实现未注册 |
| E0301 | RUNNER_INTERNAL_ERROR | runner 内部异常 |
| E0302 | INTERPRETER_NOT_FOUND | esolang.interpreter 文件缺失 |
| E0303 | DOCKER_IMAGE_MISSING | docker.image 不存在 |
| E0304 | NIX_FLAKE_FAIL | Nix flake 评估失败 |

### 构建类（E0400-E0499）

| 码 | 名 | 描述 |
|---|---|---|
| E0400 | BUILD_COMMAND_FAIL | build 命令退出码非零 |
| E0401 | BUILD_TIMEOUT | build 超时 |
| E0402 | TOOLCHAIN_MISSING | 找不到编译器 / 解释器 |
| E0403 | LINK_ERROR | 链接阶段失败 |
| E0404 | DEPENDENCY_FETCH_FAIL | 依赖下载失败 |

### 运行时类（E0500-E0599）

| 码 | 名 | 描述 |
|---|---|---|
| E0500 | RUN_NONZERO_EXIT | 子进程退出码非零 |
| E0501 | RUN_TIMEOUT | 运行超时 |
| E0502 | RUN_OOM | 内存超限 |
| E0503 | RUN_KILLED | 进程被信号杀死 |
| E0504 | STDIN_WRITE_FAIL | 调度器写 stdin 失败 |
| E0505 | STDOUT_READ_FAIL | 调度器读 stdout 失败 |

### 安全类（E0600-E0699）

| 码 | 名 | 描述 |
|---|---|---|
| E0600 | UNAUTHORIZED_NETWORK | 未授权的网络访问 |
| E0601 | UNAUTHORIZED_FS_WRITE | 未授权的文件系统写入 |
| E0602 | UNAUTHORIZED_FS_READ | 未授权的文件系统读取 |
| E0603 | SUSPICIOUS_RUN_COMMAND | run 命令包含可疑模式（rm -rf 等） |
| E0604 | EXEC_OUTSIDE_PROVINCE | 子进程试图执行 province 外文件 |

### Docker 类（E0700-E0799）

| 码 | 名 | 描述 |
|---|---|---|
| E0700 | DOCKER_NOT_AVAILABLE | 宿主机无 docker 命令 |
| E0701 | DOCKER_PULL_FAIL | 镜像拉取失败 |
| E0702 | DOCKER_BUILD_FAIL | 镜像构建失败 |
| E0703 | DOCKER_RUN_FAIL | 容器启动失败 |
| E0704 | DOCKER_NETWORK_DENIED | 容器违反网络隔离策略 |

### 渲染 / 证明 / HDL（E0800-E0899）

| 码 | 名 | 描述 |
|---|---|---|
| E0800 | RENDER_FAIL | 渲染产物生成失败 |
| E0801 | RENDER_OUTPUT_INVALID | 产物文件无效（非 SVG/PNG） |
| E0810 | PROOF_FAIL | 证明检查失败 |
| E0811 | PROOF_TIMEOUT | 证明超时 |
| E0820 | HDL_ELABORATION_FAIL | HDL 综合阶段失败 |
| E0821 | HDL_SIM_FAIL | HDL 仿真失败 |

## 4. 错误码使用建议

1. 语言模块自身遇到业务错误时，应在 stdout 输出 `ok=false`，并填写最贴近的 error 码；
2. 调度器一律使用 `E01xx`-`E08xx` 区段，不允许使用 `E09xx`；
3. 业务自定义错误一律使用 `E09xx`；
4. 错误描述必须使用人类可读语言（中英文皆可），但不得包含 secret；
5. 详细栈信息放 `error.detail`，避免污染 `error.message`。
