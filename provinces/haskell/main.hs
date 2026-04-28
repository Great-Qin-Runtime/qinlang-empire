-- 函郡 · Haskell 主程序
--
-- 角色：producer
-- 产出：xue-wen（学问）
--
-- 仅依赖 GHC base：手写最小 JSON 字段提取与字符串转义。

module Main where

import Data.Char (chr, ord)
import Data.List (isPrefixOf, stripPrefix)
import Data.Maybe (fromMaybe)
import qualified System.IO as IO

-- 抽取 "key": "value" 字符串值
findString :: String -> String -> Maybe String
findString src key = go src
  where
    go [] = Nothing
    go s@(_:rest)
      | needle `isPrefixOf` s = readVal (drop (length needle) s)
      | otherwise = go rest
    needle = "\"" ++ key ++ "\""
    readVal s =
      let s1 = dropWhile (\c -> c == ' ' || c == ':' || c == '\t' || c == '\n') s
       in case s1 of
            ('"':rest) -> Just (takeStr rest)
            _ -> Nothing
    takeStr [] = []
    takeStr ('\\':c:rest) = case c of
      '"' -> '"' : takeStr rest
      '\\' -> '\\' : takeStr rest
      'n' -> '\n' : takeStr rest
      't' -> '\t' : takeStr rest
      'r' -> '\r' : takeStr rest
      _ -> c : takeStr rest
    takeStr ('"':_) = []
    takeStr (c:rest) = c : takeStr rest

-- 抽取 "key": <int>
findInt :: String -> String -> Maybe Integer
findInt src key = go src
  where
    go [] = Nothing
    go s@(_:rest)
      | needle `isPrefixOf` s = readVal (drop (length needle) s)
      | otherwise = go rest
    needle = "\"" ++ key ++ "\""
    readVal s =
      let s1 = dropWhile (\c -> c == ' ' || c == ':' || c == '\t' || c == '\n') s
          (digits, _) = span (\c -> c == '-' || (c >= '0' && c <= '9')) s1
       in case digits of
            "" -> Nothing
            "-" -> Nothing
            d -> Just (read d)

escape :: String -> String
escape = concatMap esc
  where
    esc '"' = "\\\""
    esc '\\' = "\\\\"
    esc '\n' = "\\n"
    esc '\r' = "\\r"
    esc '\t' = "\\t"
    esc c
      | ord c < 0x20 = "\\u" ++ pad4 (showHex (ord c))
      | otherwise = [c]
    pad4 s = replicate (4 - length s) '0' ++ s
    showHex 0 = "0"
    showHex n = go n ""
      where
        go 0 acc = acc
        go x acc = let (q, r) = x `divMod` 16 in go q (digit r : acc)
        digit d
          | d < 10 = chr (ord '0' + d)
          | otherwise = chr (ord 'a' + d - 10)

kvStr :: String -> String -> String
kvStr k v = "\"" ++ escape k ++ "\":\"" ++ escape v ++ "\""

main :: IO ()
main = do
  IO.hSetBuffering IO.stdout IO.NoBuffering
  raw <- getContents
  let !_ = length raw
  let tick = fromMaybe 0 (findInt raw "tick")
      dispatchId = fromMaybe "" (findString raw "dispatch_id")
      seed = fromMaybe "" (findString raw "random_seed")
      season = fromMaybe "春" (findString raw "season")
      weather = fromMaybe "晴" (findString raw "weather")
      level = fromMaybe 1 (findInt raw "level")
      base = 3 + (sumBytes seed `mod` 4)
      n = max 3 (base + (level - 1))
      seasonPhrase = case season of
        "春" -> "春诵新简"
        "夏" -> "夏暑校书"
        "秋" -> "秋录入函"
        "冬" -> "冬日抄经"
        _ -> ""
      weatherPhrase = case weather of
        "晴" -> "明窗对简"
        "雨" -> "听雨披卷"
        "雪" -> "雪夜读经"
        "雾" -> "雾里寻章"
        "霾" -> "尘窗寡言"
        "异象" -> "灵光照册"
        _ -> ""
      txt =
        "函郡 " ++ seasonPhrase
          ++ (if null weatherPhrase then "" else "，" ++ weatherPhrase)
          ++ "，献学问 " ++ show n ++ " 编。"
      out =
        "{" ++ kvStr "language" "Haskell"
          ++ "," ++ kvStr "province" "函郡"
          ++ ",\"ok\":true"
          ++ ",\"tick\":" ++ show tick
          ++ "," ++ kvStr "dispatch_id" dispatchId
          ++ ",\"deltas\":{\"treasury\":{\"xue-wen\":" ++ show n ++ "},\"self\":{\"produced\":" ++ show n ++ "}}"
          ++ ",\"events\":[{" ++ kvStr "type" "produce" ++ "," ++ kvStr "text" txt ++ "," ++ kvStr "severity" "info" ++ "}]"
          ++ "}"
  putStrLn out
  where
    sumBytes :: String -> Integer
    sumBytes = fromIntegral . sum . map ord
