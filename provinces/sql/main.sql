-- 簿录郡 · 户籍数据库逻辑
-- 用 SQLite 在内存中完成一次"编户齐民"的清查
--
-- run.py 会把 :delta_huji / :year 替换为实际数字后整个执行。
-- 输出最后一条 SELECT 的结果，作为本次 census 的统计。

CREATE TABLE IF NOT EXISTS households (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    year_added   INTEGER NOT NULL,
    member_count INTEGER NOT NULL DEFAULT 1
);

CREATE INDEX IF NOT EXISTS idx_year ON households(year_added);

-- 籍记元年三户，作为先祖底色
INSERT INTO households (year_added, member_count)
VALUES (0, 3), (0, 4), (0, 5);

-- 本次新增 :delta_huji 户，每户 1~5 口
WITH RECURSIVE counter(n) AS (
    SELECT 1
    UNION ALL
    SELECT n + 1 FROM counter WHERE n < :delta_huji
)
INSERT INTO households (year_added, member_count)
SELECT :year, 1 + ((n + :year) % 5) FROM counter;

-- 输出本郡当下统计
SELECT
    COUNT(*)            AS total_households,
    COALESCE(SUM(member_count), 0) AS total_members,
    COALESCE(MAX(year_added), 0)   AS latest_year
FROM households;
