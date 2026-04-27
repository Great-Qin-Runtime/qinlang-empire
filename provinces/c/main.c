/*
 * 始源郡 · C 主程序
 *
 * 角色：producer
 * 产出：gong-ju（工具）
 *
 * 直接读 stdin 上的 dispatch JSON，简单字段提取后产出工具，
 * 写一份合规 JSON 到 stdout。源码以 UTF-8 保存。
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

static long find_int(const char *buf, const char *key) {
    char pat[64];
    snprintf(pat, sizeof(pat), "\"%s\"", key);
    const char *p = strstr(buf, pat);
    if (!p) return 0;
    p = strchr(p, ':');
    if (!p) return 0;
    p++;
    while (*p && !(isdigit((unsigned char)*p) || *p == '-')) p++;
    return atol(p);
}

static void find_str(const char *buf, const char *key, char *out, size_t outlen) {
    out[0] = 0;
    char pat[64];
    snprintf(pat, sizeof(pat), "\"%s\"", key);
    const char *p = strstr(buf, pat);
    if (!p) return;
    p = strchr(p, ':');
    if (!p) return;
    p = strchr(p, '"');
    if (!p) return;
    p++;
    const char *end = strchr(p, '"');
    if (!end) return;
    size_t len = (size_t)(end - p);
    if (len >= outlen) len = outlen - 1;
    memcpy(out, p, len);
    out[len] = 0;
}

int main(void) {
    static char buf[262144];
    size_t got = fread(buf, 1, sizeof(buf) - 1, stdin);
    buf[got] = 0;

    long tick = find_int(buf, "tick");
    long level = find_int(buf, "level");
    if (level < 1) level = 1;

    char dispatch_id[256] = {0};
    find_str(buf, "dispatch_id", dispatch_id, sizeof(dispatch_id));
    char season[16] = {0};
    find_str(buf, "season", season, sizeof(season));
    char weather[24] = {0};
    find_str(buf, "weather", weather, sizeof(weather));

    /* 2 ~ 5 件工具，由 tick 决定，等级加成 */
    long yield = 2 + ((tick * 7) % 4) + (level - 1);
    if (yield < 1) yield = 1;

    /* 季节叙事，全部 UTF-8 字面量 */
    const char *season_phrase = "时";
    if (strcmp(season, "春") == 0) season_phrase = "春日";
    else if (strcmp(season, "夏") == 0) season_phrase = "夏日";
    else if (strcmp(season, "秋") == 0) season_phrase = "秋日";
    else if (strcmp(season, "冬") == 0) season_phrase = "冬日";

    printf("{"
           "\"language\":\"C\","
           "\"province\":\"始源郡\","
           "\"ok\":true,"
           "\"tick\":%ld,"
           "\"dispatch_id\":\"%s\","
           "\"deltas\":{\"treasury\":{\"gong-ju\":%ld},\"self\":{\"produced\":%ld}},"
           "\"events\":[{\"type\":\"produce\","
           "\"text\":\"始源郡 %s 鼓风炼铁，铸工具 %ld 件。\","
           "\"severity\":\"info\"}]"
           "}\n",
           tick, dispatch_id, yield, yield, season_phrase, yield);

    fflush(stdout);
    return 0;
}
