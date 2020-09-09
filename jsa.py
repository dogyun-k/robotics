import numpy as np
import heapq
node_list = []
count = -1

class Node (object):
    def __init__(self, x,y,z,num):
        self.location = np.array([x,y,z])
        self.index = num
        self.forward = None
        self.backward = None
        self.left = None
        self.right = None
        self.up = None
        self.down = None

        self.distance = float('inf')
        self.direction = [0, 0, 0, 0, 0, 0] #상, 하, 좌, 우, 위, 아래

    def set_index(self, num):
        self.index = num

    def set_distance(self, num):
        if(self.distance > num):
            self.distance = num


def link_node(node1,node2):
    if(node1.location[0]+1 == node2.location[0] and node1.location[1:2]==node2.location[1:2]):
        node1.right = node2
        node2.left = node1
        node1.direction[3] = 1
        node2.direction[2] = 1
    elif (node1.location[0] - 1 == node2.location[0] and node1.location[1:2]==node2.location[1:2]):
        node1.left = node2
        node2.right = node1
        node1.direction[2] = 1
        node2.direction[3] = 1
    elif(node1.location[1]+1 == node2.location[1] and node1.location[0]==node2.location[0] and node1.location[2] == node2.location[2]):
        node1.forward = node2
        node2.backward = node1
        node1.direction[0] = 1
        node2.direction[1] = 1
    elif (node1.location[1] - 1 == node2.location[1] and node1.location[0] == node2.location[0] and node1.location[2] == node2.location[2]):
        node1.backward = node2
        node2.forward = node1
        node1.direction[1] = 1
        node2.direction[0] = 1
    elif (node1.location[2] + 1 == node2.location[2] and node1.location[0:1]==node2.location[0:1]):
        node1.up = node2
        node2.down = node1
        node1.direction[4] = 1
        node2.direction[5] = 1
    elif (node1.location[2] - 1 == node2.location[2] and node1.location[0:1]==node2.location[0:1]):
        node1.down = node2
        node2.up = node1
        node1.direction[5] = 1
        node2.direction[4] = 1
    else:
        print(node1.location, node2.location)
        print("잘못된 연결")

def AddNode(x,y,z):
    global count
    count += 1

    return Node(x,y,z, count)

def find_linked_node(Node):
    dir = Node.direction
    index_list = []
    if dir[0] == 1:
        index_list.append(Node.forward.index)
    if dir[1] == 1:
        index_list.append(Node.backward.index)
    if dir[2] == 1:
        index_list.append(Node.left.index)
    if dir[3] == 1:
        index_list.append(Node.right.index)
    if dir[4] == 1:
        index_list.append(Node.up.index)
    if dir[5] == 1:
        index_list.append(Node.down.index)
    return index_list


def dijkstra(start, linked_node_lis):
    # linked_node_list : 노드의 인접노드들의 리스트
    # 모든 노드의 디스턴스 무한대로 설정, 출구노드는 디스턴스 0
    distances = {node: float('inf') for node in range(84)}
    distances[start] = 0


    queue = []
    heapq.heappush(queue, [distances[start], start])


    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if distances[current_node] < current_distance:
            continue

        for adjacent in linked_node_list[current_node]:
            distance = current_distance + 1
 
            if distance < distances[adjacent]:
                distances[adjacent] = distance
                heapq.heappush(queue, [distance, adjacent])
                print(queue)

    return distances

def fire_test(fire_node_num, send_node_num1, send_node_num2, node, linked_node_list):
    queue = []
    del_list = []
    fire_start = fire_node_num
    send1 = send_node_num1
    send2 = send_node_num2

    node[fire_node_num].distance = float('inf')

    if fire_node_num not in fire_place_num:
        fire_place_num.append(fire_node_num)

    for i in linked_node_list[send2]:
        if i != send1 and i not in fire_place_num:
            queue.insert(0,i)

    for i in queue:
        substract = []
        node_list = []
        shortest_node_num = []

        for j in linked_node_list[i]:
            node_list.append(j)
            if j != send2:
                substract.append(node[j].distance - node[i].distance)
            else:
                substract.append(float('inf'))

        if min(substract) != -1 or node[i].exit_diret_num != substract.count(-1):

            node[i].exit_diret = []
            shortest_distance_node_index = [i for i, value in enumerate(substract) if value == min(substract)]

            for k in shortest_distance_node_index:
                shortest_node_num.append(node_list[k])

            if node[i].forward != None and node[i].forward.index in shortest_node_num:
                node[i].exit_diret.append('forward')

            if node[i].backward != None and node[i].backward.index in shortest_node_num:
                node[i].exit_diret.append('backward')

            if node[i].right != None and node[i].right.index in shortest_node_num:
                node[i].exit_diret.append('right')

            if node[i].left != None and node[i].left.index in shortest_node_num:
                node[i].exit_diret.append('left')

            if node[i].up != None and node[i].up.index in shortest_node_num:
                node[i].exit_diret.append('up')
                
            if node[i].down != None and node[i].down.index in shortest_node_num:
                node[i].exit_diret.append('down')
            node[i].set_exit_diret_num()
        else:
            del_list.append(i)

    for i in del_list:
        queue.remove(i)
        
    for i in queue:
        fire_test(fire_start, send2, i, node, linked_node_list)


def set_weight(node, exit_list):
    for e in exit:
        result = dijkstra(e, linked_node_list)
        for i in range(84):
            node[i].set_distance(result[i])

if __name__ == "__main__":

    node = []
    node.append(AddNode(0, 0, 2)), node.append(AddNode(1, 0, 2)), node.append(AddNode(2,0,2)),
    node.append(AddNode(3, 0, 2)), node.append(AddNode(4, 0, 2)), node.append(AddNode(4,1,2)),
    node.append(AddNode(4, 2, 2)), node.append(AddNode(4, 3, 2)), node.append(AddNode(3,3,2)),
    node.append(AddNode(2, 3, 2)), node.append(AddNode(1, 3, 2)), node.append(AddNode(0,3,2)),
    node.append(AddNode(0, 2, 2)), node.append(AddNode(0, 1, 2)) #2호관 1층 Node_num = 1 ~ 14

    node.append(AddNode(0, 0, 3)), node.append(AddNode(1, 0, 3)), node.append(AddNode(2, 0, 3)),
    node.append(AddNode(3, 0, 3)), node.append(AddNode(4, 0, 3)), node.append(AddNode(4, 1, 3)),
    node.append(AddNode(4, 2, 3)), node.append(AddNode(4, 3, 3)), node.append(AddNode(3, 3, 3)),
    node.append(AddNode(2, 3, 3)), node.append(AddNode(1, 3, 3)), node.append(AddNode(0, 3, 3)),
    node.append(AddNode(0, 2, 3)), node.append(AddNode(0, 1, 3)), node.append(AddNode(1, 1, 3)),
    node.append(AddNode(2, 1, 3)), node.append(AddNode(3, 1, 3)), node.append(AddNode(3, 2, 3)),
    node.append(AddNode(2, 2, 3)), node.append(AddNode(1, 2, 3))  # 2호관 2층 Node num = 15 ~ 34

    node.append(AddNode(0, 0, 4)), node.append(AddNode(1, 0, 4)), node.append(AddNode(2, 0, 4)),
    node.append(AddNode(3, 0, 4)), node.append(AddNode(4, 0, 4)), node.append(AddNode(4, 1, 4)),
    node.append(AddNode(4, 2, 4)), node.append(AddNode(4, 3, 4)), node.append(AddNode(3, 3, 4)),
    node.append(AddNode(2, 3, 4)), node.append(AddNode(1, 3, 4)), node.append(AddNode(0, 3, 4)),
    node.append(AddNode(0, 2, 4)), node.append(AddNode(0, 1, 4))  #2호관 3층 Node_num = 35 ~ 48

    node.append(AddNode(5, 3, 3)), node.append(AddNode(6, 3, 3)), node.append(AddNode(7, 3, 3)) #구름다리 4층 Node_num = 49 ~ 51
    node.append(AddNode(5, 3, 4)), node.append(AddNode(6, 3, 4)), node.append(AddNode(7, 3, 4)) #구름다리 5층 Node_num = 52 ~ 54

    node.append(AddNode(8, 3, 0)), node.append(AddNode(9, 3, 0)), node.append(AddNode(10, 3, 0)),
    node.append(AddNode(11, 3, 0)), node.append(AddNode(12, 3, 0)) # 1호관 1층 Node_num = 55 ~ 59

    node.append(AddNode(8, 3, 1)), node.append(AddNode(9, 3, 1)), node.append(AddNode(10, 3, 1)),
    node.append(AddNode(11, 3, 1)), node.append(AddNode(12, 3, 1))  # 1호관 2층 Node_num = 60 ~ 64

    node.append(AddNode(8, 3, 2)), node.append(AddNode(9, 3, 2)), node.append(AddNode(10, 3, 2)),
    node.append(AddNode(11, 3, 2)), node.append(AddNode(12, 3, 2))  # 1호관 3층 Node_num = 65 ~ 69

    node.append(AddNode(8, 3, 3)), node.append(AddNode(9, 3, 3)), node.append(AddNode(10, 3, 3)),
    node.append(AddNode(11, 3, 3)), node.append(AddNode(12, 3, 3))  # 1호관 4층 Node_num = 70 ~ 74

    node.append(AddNode(8, 3, 4)), node.append(AddNode(9, 3, 4)), node.append(AddNode(10, 3, 4)),
    node.append(AddNode(11, 3, 4)), node.append(AddNode(12, 3, 4))  # 1호관 5층 Node_num = 75 ~ 79

    node.append(AddNode(8, 3, 5)), node.append(AddNode(9, 3, 5)), node.append(AddNode(10, 3, 5)),
    node.append(AddNode(11, 3, 5)), node.append(AddNode(12, 3, 5))  # 1호관 6층 Node_num = 80 ~ 84

    #2호관 1층 연결
    for i in range(13):
       link_node(node[i],node[i+1])
    link_node(node[13], node[0]), link_node(node[1], node[15]),link_node(node[7], node[21]),link_node(node[11], node[25])

    #2호관 2층 연결
    for i in range(14,27):
       link_node(node[i], node[i + 1])
    link_node(node[27], node[14]),link_node(node[15], node[35]),link_node(node[21], node[41]),link_node(node[25], node[45])

    for i in range(28,33):
        link_node(node[i], node[i + 1])
    link_node(node[33], node[28]), link_node(node[23], node[32]), link_node(node[29], node[16])

    #2화관 3층 연결
    for i in range(34,47):
        link_node(node[i], node[i + 1])
    link_node(node[47], node[34])

    #구름다리 연결
    link_node(node[21], node[48]),link_node(node[48], node[49]), link_node(node[49], node[50]),link_node(node[50], node[69]),
    link_node(node[41], node[51]),link_node(node[51], node[52]),link_node(node[52], node[53]),link_node(node[53], node[74]),

    #1호관 연결
    for i in range(54,58):
        link_node(node[i], node[i + 1])
    for i in range(59,64,2):
        link_node(node[i], node[i - 5])

    for i in range(59,63):
        link_node(node[i], node[i + 1])
    for i in range(64, 69, 2):
        link_node(node[i], node[i - 5])

    for i in range(64,68):
        link_node(node[i], node[i + 1])
    for i in range(69,74,2):
        link_node(node[i], node[i - 5])

    for i in range(69,73):
        link_node(node[i], node[i + 1])
    for i in range(74,79,2):
        link_node(node[i], node[i - 5])

    for i in range(74,78):
        link_node(node[i], node[i + 1])
    for i in range(79,84,2):
        link_node(node[i], node[i - 5])

    for i in range(79,83):
        link_node(node[i], node[i + 1])


    #다익스트라 알고리즘
    linked_node_list = []
    for i in range(84):
        linked_node_list.append([])
        for j in find_linked_node(node[i]):
            linked_node_list[i].append(j)

    '''print(linked_node_list)
    result = dijkstra(0,linked_node_list)
    for i in range(84):
        node[i].set_distance(result[i])'''
    exit = [2,7,11,56,58,64]
    set_weight(node,exit)
    for i in range(84):
        print(i,':',node[i].distance, end= "  ")
