import heapq

INF = float('inf')

class Node:
    """센서 노드 클래스"""
    def __init__(self, sensor_num):
        # 센서 위치값
        self.data = sensor_num

        # 인접 노드 레퍼런스
        self.adjacent_node = {'up':None, 'down':None, 'right':None, 'left':None, 'upstair':None, 'downstair':None}
        self.adjacent_node_distance = {'up':float('inf'), 'down':float('inf'), 'right':float('inf'), 'left':float('inf'), 'upstair':float('inf'), 'downstair':float('inf')}
        self.state = 0  # 불 : F | 연기 : G | 출구 : E

        self.distance = float('inf')

    def set_distance(self, num):
        """노드에서 인접노드까지의 거리"""
        if(self.distance > num):
            self.distance = num



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
                            current_sensor.distance = 0
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


    def dijkstra_to_set_state(self, exit_node):
        """하나의 출구로부터 모든 노드의 최단거리를 찾는 알고리즘 
            다익스트라로 노드 디스턴스 설정"""
        distances ={}
        for sensor_num in self.sensor_map:
            distances[sensor_num] = self.sensor_map[sensor_num].distance

        queue = []
        # 시작노드(출구노드)의 번호를 우선순위 큐에 넣는다.
        heapq.heappush(queue, [distances[exit_node], exit_node])


        while queue:

            # 힙에서 가장 우선순위가 높은 데이터 꺼내옴
            current_distance, current_node_num = heapq.heappop(queue)

            if distances[current_node_num] < current_distance:
                continue

            for adjacent_node_num in self.adjacent_node_is(self.sensor_map[current_node_num]):
                distance = current_distance + 1

                if distance < distances[adjacent_node_num]:
                    distances[adjacent_node_num] = distance
                    heapq.heappush(queue, [distance, adjacent_node_num])
                    print(queue)

        return distances    # 딕셔너리


    # def set_weight(self):
    #     for exit_num, exit_node in self.exit_node:
    #         result = self.dijkstra_to_set_state(exit_num, self.adjacent_node_is(exit_node))

    #         for sensor_num in self.sensor_map:
    #             self.sensor_map[sensor_num].state = sensor_map[sensor_num].set_distance(result[i])


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