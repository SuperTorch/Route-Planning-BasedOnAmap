# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 16:46:29 2020

@author: EDZ
"""


# 高德地图路径规划

# 计算图中从start到end的最短距离
# graph, cost开销字典, parents记录路径, processed已经执行过

def dijkstra():
    # 找到目前开销最小的节点
    node = find_lowest_cost_node(costs)
    #print('当前cost最小节点：', node)
    
    # 找到开销最小的节点就进行路径规划，如果所有节点都放到processed中，就结束
    while node is not None:
        # 获取节点目前的cost
        cost = costs[node]
        # 获取节点的邻居
        neighbors = graph[node]
        # 遍历所有邻居，看看是否通过node节点，比之前cost更少
        for neighbor in neighbors.keys():
            # 计算经过当前节点到达相邻节点的开销， 即当前节点cost + 当前节点到邻居的cost
            new_cost = cost + neighbors[neighbor]
            # 通过node是否可以更新start到neighbor的cost  
            if neighbor not in costs or new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
                # 经过node到达neighbor的节点cost更少
                parents[neighbor] = node
        # 将当前节点放入processed
        processed.append(node)
        # 找到接下来要处理的节点， 并且继续循环
        node = find_lowest_cost_node(costs)
        #print('当前cost最小节点：', node)   
    #print(parents)
    # 循环完毕说明所有节点都已经处理完
    shortest_path = find_shortest_path()
    print('从{}到{}的最短路径：{}'.format(start,end,shortest_path))
    return shortest_path

def find_shortest_path():
    node = end
    shortest_path = [end]
    while parents[node] != start:
        shortest_path.append(parents[node])
        node = parents[node]
    shortest_path.append(start)
    shortest_path.reverse()
    return shortest_path

# 找到开销最小的节点
def find_lowest_cost_node(costs):
    # 初始化数据
    lowest_cost = float('inf')
    lowest_cost_node = None
    # 遍历所有节点
    for node in costs:
        # 找到非processed集合中最小节点
        if not node in processed:
            # 如果当前节点开销比已经存在的开销小，则更新该节点为开销最下的节点
            if costs[node] < lowest_cost:
                lowest_cost = costs[node]
                lowest_cost_node = node
    return lowest_cost_node

# 计算两点之间的距离
import re
key =  'd31ca20f3fc9f31d76e20359404a0783'
import requests
def compute_distance(longitude1, latitude1, longitude2, latitude2):
    request_url = 'http://restapi.amap.com/v3/distance?key='+ key+ '&origins=' + str(longitude1) +','\
                    +str(latitude1) +'&destination='+str(longitude2) +','+str(latitude2)+'&type=1'
    
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    data = requests.get(request_url, headers=headers, timeout=10)
    data.encoding='utf-8'
    data = data.text
    #print(data)
    pattern = 'distance":"(.*?)","duration":"(.*?)"'
    result = re.findall(pattern, data)
    
    return int(result[0][0])

import pickle
file = open('./graph.pkl', 'rb')
graph = pickle.load(file)

start = None
end = None
# 查看start的邻居节点
#graph[start].keys()
#graph[start].values()

# costs创建节点的开销表， cost是指从start到这个节点的距离
costs = {}
# parents存储父节点的Hash表， 用于记录路径
parents = {}
#parents[end] = None
# processed记录处理过的节点list
processed = []

def compute(site1, site2):
    global start ,end, parents, costs, processed
    start, end = site1, site2
    parents[end] = None
    
    # 获取该节点相邻节点
    for node in graph[start].keys():
        costs[node] = float(graph[start][node])
        parents[node] = start
    costs[end] = float('inf')
    # 完成计算
    shortest_path = dijkstra()
    return shortest_path

def get_location(keyword, city):
    request_url = 'http://restapi.amap.com/v3/place/text?key=' + key + \
        '&keywords=' + keyword + '&types=&city=' + city + '&children=1&offset=1&page=1&extensions=all'
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    data = requests.get(request_url, headers=headers, timeout=10)
    data.encoding='utf-8'
    data = data.text
    
    #print(data)
    """
        后面多一个？表示懒惰模式
        .*具有贪婪的性质，首先匹配到不能匹配为止
        .*?则相反，一个匹配以后，就往下执行后续的正则
    """
    pattern = 'location":"(.*?),(.*?)"'
    # 得到经纬度
    result = re.findall(pattern, data)
    # 如果有多个，取第一位置
    try:
        return result[0][0], result[0][1]
    except:
        return get_location(keyword.replace('站', ''),city)

if __name__ == '__main__':
    site1 = '五道口站'
    site2 = '北京南站'
    compute(site1, site2)