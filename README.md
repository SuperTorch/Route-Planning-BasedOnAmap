# Route-Planning-BasedOnAmap 

### 基于Dijkstra算法的高德地图简单路径规划

##### Step1，数据采集

获取不同城市的地点名称，比如北京，351个地铁站名称，所属的地铁线路。

工具：requests + BeautifulSoup

##### Step2，获取地点的坐标（经度、维度）

使用高德地图API，获取指定地点的所在经度、纬度，比如五道口的坐标。

工具：requests + 正则表达式

##### Step3，计算两点之间的距离

使用高德地图API，获取指定两点之间的距离，比如从五道口到知春路。

###### 距离的定义可以有两种：

1）distance: 距离

2）duration: 时间

##### Step4，使用Dijkstra计算从start（五道口）到end（北京南站）的最优路径

找到开销最小的节点

def find_lowest_cost_node(costs):



找到最短路径

def find_shortest_path():



计算图中从start到end的最短路径

def dijkstra():

##### Step5，进行测试验证

### 工具介绍

1. subway_location.ipynb 采集地铁数据信息，保存到subway.csv。
2. route_planning.ipynb 基于地铁站的路径规划，路径起始地址只能是北京的地铁站。
3. route_api.py 将route_planning.ipynb中的路径规划算法进行api封装。
4. route_planning2.ipynb 优化后的路径规划，使用自己封装的route_api.py, 计算距离路径起始地址最近的地铁站，进行路径规划，将起始地址添加到路径的头和尾。
5. graph.pkl 用于存储北京地铁的图信息。
6. test_api.py 用于测试route_api.py 。