# Shogi

## Introduction
[遊玩規則](https://zh.wikipedia.org/zh-tw/%E6%97%A5%E6%9C%AC%E5%B0%86%E6%A3%8B)
---
初始棋盤
```
9 | L| N| S| G| K| G| S| N| L|
8 |__| R|__|__|__|__|__| B|__|
7 | P| P| P| P| P| P| P| P| P|
6 |__|__|__|__|__|__|__|__|__|
5 |__|__|__|__|__|__|__|__|__|
4 |__|__|__|__|__|__|__|__|__|
3 | p| p| p| p| p| p| p| p| p|
2 |__| b|__|__|__|__|__| r|__|
1 | l| n| s| g| k| g| s| n| l|
    a  b  c  d  e  f  g  h  i

Our Captures:
Enemy Captures:
```
## Usage

開始遊戲
```bash
python game.py
```

## How to Play
### Move

Move piece a3 to a4
```
a3a4
```

Move piece h6 to h7 and promote
### Promotion move
```
h6h7+
```

### Drop
Drop "Pawn" to d4 (No case distinction)
```
P*d4
p*d4
```
Drop "Rook" to g5
```
R*g5
r*g5
```