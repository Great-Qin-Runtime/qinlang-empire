// 锈铁郡 · Rust 主程序
//
// 角色：producer
// 产出：bing-qi（兵器）
//
// 没有外部依赖：手写最小 JSON 字段提取与字符串转义。

use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).expect("read stdin");

    let tick: i64 = find_int(&input, "\"tick\"").unwrap_or(0);
    let dispatch_id = find_string(&input, "\"dispatch_id\"").unwrap_or_default();
    let seed = find_string(&input, "\"random_seed\"").unwrap_or_default();
    let season = find_string(&input, "\"season\"").unwrap_or_else(|| "春".into());
    let weather = find_string(&input, "\"weather\"").unwrap_or_else(|| "晴".into());
    let level: i64 = find_int(&input, "\"level\"").unwrap_or(1);

    // 由 seed 确定 3..=6，再叠加等级加成；产出至少 3
    let base = 3 + (sum_bytes(&seed) % 4) as i64;
    let n = (base + (level - 1)).max(3);

    let weather_phrase = match weather.as_str() {
        "晴" => "炉火映甲",
        "雨" => "淬铁带湿",
        "雪" => "雪打铜砧",
        "雾" => "烟笼工坊",
        "霾" => "尘掩工事",
        "异象" => "异光照锻",
        _ => "",
    };
    let season_phrase = match season.as_str() {
        "春" => "春试新刃",
        "夏" => "夏伏鼓风",
        "秋" => "秋点甲胄",
        "冬" => "冬日炼器",
        _ => "",
    };

    let text = if weather_phrase.is_empty() {
        format!("锈铁郡 {}，献兵器 {} 件。", season_phrase, n)
    } else {
        format!("锈铁郡 {}，{}，献兵器 {} 件。", season_phrase, weather_phrase, n)
    };

    let mut out = String::new();
    out.push_str("{");
    out.push_str(&kv_str("language", "Rust"));
    out.push_str(",");
    out.push_str(&kv_str("province", "锈铁郡"));
    out.push_str(",\"ok\":true,");
    out.push_str(&format!("\"tick\":{}", tick));
    out.push_str(",");
    out.push_str(&kv_str("dispatch_id", &dispatch_id));
    out.push_str(",\"deltas\":{");
    out.push_str(&format!("\"treasury\":{{\"bing-qi\":{}}},", n));
    out.push_str(&format!("\"self\":{{\"produced\":{}}}", n));
    out.push_str("},");
    out.push_str("\"events\":[{");
    out.push_str(&kv_str("type", "produce"));
    out.push_str(",");
    out.push_str(&kv_str("text", &text));
    out.push_str(",");
    out.push_str(&kv_str("severity", "info"));
    out.push_str("}]");
    out.push_str("}");

    let stdout = io::stdout();
    let mut handle = stdout.lock();
    handle.write_all(out.as_bytes()).expect("write stdout");
    handle.write_all(b"\n").expect("newline");
}

fn kv_str(key: &str, value: &str) -> String {
    format!("\"{}\":\"{}\"", escape(key), escape(value))
}

fn escape(s: &str) -> String {
    let mut out = String::with_capacity(s.len());
    for c in s.chars() {
        match c {
            '"' => out.push_str("\\\""),
            '\\' => out.push_str("\\\\"),
            '\n' => out.push_str("\\n"),
            '\r' => out.push_str("\\r"),
            '\t' => out.push_str("\\t"),
            c if (c as u32) < 0x20 => out.push_str(&format!("\\u{:04x}", c as u32)),
            c => out.push(c),
        }
    }
    out
}

fn sum_bytes(s: &str) -> u32 {
    s.bytes().map(|b| b as u32).sum()
}

/// 在原始 JSON 文本中按 key 抓 `"key": <value>` 的字符串值；只解析 ASCII 引号内的简单字符串。
fn find_string(src: &str, key: &str) -> Option<String> {
    let pos = src.find(key)?;
    let after = &src[pos + key.len()..];
    let colon = after.find(':')?;
    let rest = &after[colon + 1..];
    let mut chars = rest.chars();
    // 跳过空白
    let mut consumed = 0usize;
    let mut start = None;
    for c in &mut chars {
        consumed += c.len_utf8();
        if c == '"' {
            start = Some(consumed);
            break;
        }
        if !c.is_whitespace() {
            return None;
        }
    }
    let start = start?;
    let value_part = &rest[start..];
    let mut buf = String::new();
    let mut iter = value_part.chars().peekable();
    while let Some(c) = iter.next() {
        match c {
            '"' => return Some(buf),
            '\\' => match iter.next() {
                Some('"') => buf.push('"'),
                Some('\\') => buf.push('\\'),
                Some('n') => buf.push('\n'),
                Some('r') => buf.push('\r'),
                Some('t') => buf.push('\t'),
                Some('/') => buf.push('/'),
                Some(other) => buf.push(other),
                None => return None,
            },
            c => buf.push(c),
        }
    }
    None
}

/// 抓 `"key": <int>`；遇到第一个数字开始读到非数字字符。
fn find_int(src: &str, key: &str) -> Option<i64> {
    let pos = src.find(key)?;
    let after = &src[pos + key.len()..];
    let colon = after.find(':')?;
    let rest = after[colon + 1..].trim_start();
    let mut end = 0usize;
    for (idx, c) in rest.char_indices() {
        if idx == 0 && (c == '-' || c.is_ascii_digit()) {
            end = idx + c.len_utf8();
            continue;
        }
        if c.is_ascii_digit() {
            end = idx + c.len_utf8();
        } else {
            break;
        }
    }
    if end == 0 {
        None
    } else {
        rest[..end].parse::<i64>().ok()
    }
}
