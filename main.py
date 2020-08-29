from create_map import *
import time



def print_state(sensor_map):
    """모든 노드의 상태 값 출력"""
    for key, value in sorted(sensor_map.items()):
        print(key, value.distance, value.visited)

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

# 센서에 불, 연기 감지될 때 마다 돌려야 함
knu.set_state_to_0()
# print(knu.exit_node)

knu.set_distance()



print_state(knu.sensor_map)


# print(f"\n\nset_state 걸린시간 : {time.time() - start}")
# print("불난 노드 :", knu.fire_node_is().keys())



