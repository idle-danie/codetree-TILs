from collections import deque

MAX_L = 70

R, C, K = 0, 0, 0
forest_map = [[0] * MAX_L for _ in range(MAX_L + 3)]  # 숲에 들어오기 전을 고려하여 3만큼의 rows 추가
dy = [-1, 0, 1, 0]
dx = [0, 1, 0, -1]
is_exit = [[False] * MAX_L for _ in range(MAX_L + 3)]
answer = 0  # 각 정령들이 도달한 최종 행의 총합


# (y, x)가 숲의 범위 안에 있는지 확인하는 function
def in_range(y, x):
    return 3 <= y <= R + 2 and 0 <= x <= C - 1


# 숲에 있는 골렘을 모두 빠져나가게 하는 초기화 function
def reset_forest_map():
    for i in range(R + 3):
        for j in range(C):
            forest_map[i][j] = 0
            is_exit[i][j] = False


# 골렘이 (y, x)에 위치할 수 있는지 확인하는 function
def can_move(y, x):
    # 먼저 (y,x)의 범위를 확인
    if not (y + 1 <= R + 2 and 0 <= x - 1 and x + 1 <= C - 1):
        return False

    # 남쪽으로 내려올 때, 좌우 회전을 통해 내려올 때의 위치가 0일 때
    if (forest_map[y][x + 1] == 0 and forest_map[y][x - 1] == 0 and forest_map[y + 1][x] == 0 and 
        forest_map[y - 1][x - 1] == 0 and forest_map[y][x] == 0 and forest_map[y - 2][x] == 0 and
        forest_map[y - 1][x + 1] == 0):
            return True

    return False


# 정령이 움직일 수 있는 모든 범위를 확인 및 최하단 행 반환하는 function
def bfs(y, x):
    result = y
    q = deque([(y,x)])
    visit = [[False] * C for _ in range(R + 3)]
    visit[y][x] = True
    while q:
        cur_y, cur_x = q.popleft()
        for k in range(4):
            ny, nx = cur_y + dy[k], cur_x + dx[k]
            # 정령의 움직임은 골렘 내부이거나
            # 골렘의 탈출구에 위치하고 있다면 다른 골렘으로 옮겨 갈 수 있다
            if in_range(ny, nx) and not visit[ny][nx] and (forest_map[ny][nx] == forest_map[cur_y][cur_x] or (forest_map[ny][nx] != 0 and is_exit[cur_y][cur_x])):
                q.append((ny, nx))
                visit[ny][nx] = True
                result = max(result, ny)
    return result

# 골렘id가 중심 (y, x), 출구의 방향이 d일때 규칙에 따라 움직임을 취하는 function
def down(y, x, d, id):
    if can_move(y + 1, x):
        down(y + 1, x, d, id)
    elif can_move(y + 1, x - 1):
        down(y + 1, x - 1, (d + 3) % 4, id)
    elif can_move(y + 1, x + 1):
        down(y + 1, x + 1, (d + 1) % 4, id)
    else:
        # 1, 2, 3의 움직임이 불가능할 때
        if not in_range(y - 1, x - 1) or not in_range(y + 1, x + 1):
            reset_forest_map()
        else:
            # 골렘이 숲 안에 정착
            forest_map[y][x] = id
            for k in range(4):
                forest_map[y + dy[k]][x + dx[k]] = id
            # 골렘의 출구를 기록하고
            is_exit[y + dy[d]][x + dx[d]] = True
            global answer
            # bfs를 통해 정령이 최대로 내려갈 수 있는 행를 계산하여 누적합니다
            answer += bfs(y, x) - 3 + 1

def main():
    global R, C, k
    R, C, K = map(int, input().split())
    for id in range(1, K + 1):
        x, d = map(int, input().split())
        down(0, x - 1, d, id)
    print(answer)

if __name__ == "__main__":
    main()