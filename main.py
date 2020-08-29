from create_map import *
import time


def print_state(sensor_map):
    """모든 노드의 상태 값 출력"""

    for key, value in sorted(sensor_map.items()):
        direction_list = []
        adjacent_list = []
        for direction, boolean in value.direction_of_exit.items():
            if boolean:
                direction_list.append(direction)
            
        for adjacent, boolean in value.adjacent_node.items():
            if boolean:
                adjacent_list.append(adjacent)

        print("노드번호 :", key, value.distance)
        print("출구방향 :", direction_list)
        print("연결된 노드 :", adjacent_list)
        print()


def print_all_adjacent_node(sensor_map):
    """모든 노드의 인접노드 출력"""
    for key in sensor_map:
        print(key, adjacent_node_is(sensor_map[key]).keys())


""" 테스트 라인 """
print('\n\n')
knu = Map()
knu.create_sensor_map("length.txt", "width.txt", "stairs.txt", "exit.txt")
knu.set_fire('2208')


start = time.time()


knu.set_distance_dijkstra()
knu.direction_of_exit()


print("출구노드 :", knu.exit_node.keys(), "\n")
print_state(knu.sensor_map)


print(f"\n\nset_state 걸린시간 : {time.time() - start}")
print("불난 노드 :", knu.fire_node_is().keys())



