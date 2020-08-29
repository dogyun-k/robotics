import heapq

INF = float('inf')

class Node:
    """센서 노드 클래스"""
    def __init__(self, sensor_num):
        # 센서 번호
        self.data = sensor_num

        # 인접 노드 레퍼런스
        self.adjacent_node = {'up':None, 'down':None, 'right':None, 'left':None, 'upstair':None, 'downstair':None}

        # 다익스트라 알고리즘 쓰기위한 변수
        self.distance = float('inf')
        self.weight = {'up':1, 'down':1, 'right':1, 'left':1, 'upstair':1, 'downstair':1}
        self.visited = False

        # BFS 쓰기위한 변수
        self.state = 0  # 불 : F | 연기 : G | 출구 : E


class Map:
    """센서 맵 클래스"""
    def __init__(self):
        self.sensor_map = {}
        self.exit_node = {}

    def create_sensor_map(self, length_file, width_file, stairs_file, exit_file):
        """센서의 고유번호, 관계, 위치가 저장된 파일을 전달하면 그래프화 하고 sensor_map에 저장."""
        self.sensor_map = {}
        file_list = [length_file, width_file, stairs_file, exit_file]

        for file_name in file_list:

            with open(file_name) as sensor_file:

                for line in sensor_file:
                    
                    raw_data = line.strip().split("-")
                    prev_sensor = None

                    for sensor_num in raw_data:
                        sensor_num = sensor_num.strip()

                        if sensor_num not in self.sensor_map:   # 센서 정보가 센서 딕셔너리에 없으면
                            current_sensor = Node(sensor_num)
                            self.sensor_map[sensor_num] = current_sensor
                        else:
                            current_sensor = self.sensor_map[sensor_num]


                        if file_name == "exit.txt": # 출구 센서 지정
                            # current_sensor.is_exit = True
                            # current_sensor.distance = 0
                            current_sensor.state = 'E'
                            self.exit_node[sensor_num] = current_sensor


                        if prev_sensor is not None:

                            if file_name == "width.txt":# 가로 연결된 센서 
                                current_sensor.adjacent_node['right'] = prev_sensor
                                prev_sensor.adjacent_node['left'] = current_sensor

                            elif file_name == "length.txt":   # 세로 연결된 센서
                                current_sensor.adjacent_node['up'] = prev_sensor
                                prev_sensor.adjacent_node['down'] = current_sensor

                            elif file_name == "stairs.txt": # 계단 센서
                                current_sensor.adjacent_node['downstair'] = prev_sensor
                                prev_sensor.adjacent_node['upstair'] = current_sensor

                        
                        prev_sensor = current_sensor


    def adjacent_node_is(self, node):
        """인접노드 리턴"""
        adjacent = node.adjacent_node
        adjacent_node = {}

        for check in adjacent:
            if adjacent[check] is not None:
                adjacent_node[adjacent[check].data] = adjacent[check]

        return adjacent_node


    def fire_node_is(self):
        """불난노드 리턴"""
        fired_node = {}

        for node in self.sensor_map.values():
            if node.state == 'F' or node.state == 'G':
                fired_node[node.data] = node
        
        return fired_node
        

    def set_state_to_0(self):
        """모든 노드 state 0으로"""
        for num in self.sensor_map:
            if self.sensor_map[num].state != 'E' and self.sensor_map[num].state != 'F' and self.sensor_map[num].state != 'G':
                self.sensor_map[num].state = 0


    def set_state(self):
        """각 노드 state 값 지정"""
        current_nodes = self.exit_node
        
        while current_nodes:
            temp = []
            for num in current_nodes:
                
                adjacent_nodes = self.adjacent_node_is(self.sensor_map[num])

                for ad_num in adjacent_nodes:
                    
                    if self.sensor_map[ad_num].state == 0:
                        temp.append(ad_num)

                        if self.sensor_map[num].state == 'E':
                            self.sensor_map[ad_num].state += 1
                        else:
                            self.sensor_map[ad_num].state = self.sensor_map[num].state + 1
                        
            current_nodes = temp


    def set_visited_false(self):
        for node in self.sensor_map.values():
            node.visited = False


    def dijkstra(self, start_num):
        self.set_visited_false()
        queue = []

        # 우선순위 큐에 들어가는 우선순위는 노드의 distance 값으로 한다.
        # 시작 노드를 큐에 넣고 distance는 0으로 한다. 큐에 넣었으니 visited = True로 한다.
        start_node = self.sensor_map[start_num]
        start_node.distance = 0
        heapq.heappush(queue, (start_node.distance, start_node.data))
        start_node.visited = True

        print("출구 노드 :", start_node.data, start_node.visited)

        while queue:    # 큐가 빌 때 까지 -> 모든 노드를 방문할 때 까지

            # 현재 노드에 큐에서 우선순위가 가장 높은 큐를 넣는다.
            current_node = self.sensor_map[heapq.heappop(queue)[1]]

            # 현재 노드의 인접노드 중 방문하지 않은 노드를 불러온다.

            for adjacent_direction, adjacent_node in current_node.adjacent_node.items():
                
                if adjacent_node is not None and adjacent_node.visited is False and adjacent_node.distance > current_node.distance + current_node.weight[adjacent_direction]:
                    adjacent_node.distance = current_node.distance + current_node.weight[adjacent_direction]

                    heapq.heappush(queue, (adjacent_node.distance, adjacent_node.data))
                    adjacent_node.visited = True


    def set_distance(self):
        for exit_node in self.exit_node:
            self.dijkstra(exit_node)


    def set_fire(self, sensor_num):
        """센서에서 불 감지 시 실행"""
        self.sensor_map[sensor_num].state = 'F'


    def set_gass(self, sensor_num):
        """센서에서 가스 감지 시 실행"""
        self.sensor_map[sensor_num].state = 'G'


    def __str__(self):
        """센서맵의 센서들 문자열 리턴"""
        res_str = "|"

        for data in sorted(self.sensor_map.keys()):
            res_str += f" {data} |"

        return res_str