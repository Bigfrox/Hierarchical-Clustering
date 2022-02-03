"""
Data Mining
Assignment 6, Graph Clustering by Hierarchical Approach
Myeong suhwan
"""

from datetime import datetime
import sys


def getDataFromFile(filename):
    input_file = open(filename, "r")
    graph = dict()

    line = None
    line = input_file.readline().split()

    while line != "":

        if not line[0] in graph:
            graph[line[0]] = [line[1]]

        elif line[0] in graph:
            connected = graph[line[0]]
            connected.append(line[1])
            graph[line[0]] = list(set(connected))

        if not line[1] in graph:
            graph[line[1]] = [line[0]]

        elif line[1] in graph:
            connected = graph[line[1]]
            connected.append(line[0])
            graph[line[1]] = list(set(connected))

        line = input_file.readline().split()
        if not line:
            break
    # print(graph)

    return graph


def output_to_file(filename, cluster):
    file = open(filename, "w")

    for v in cluster:
        if not v:
            continue
        file.write("{0} : {1}".format(len(v), v))
        file.write("\n")
    file.close()


def GetNeighbors(graph, vertex, node_set):

    for r in graph[vertex]:
        node_set.add(r)

    return node_set


def GetJaccardCoefficient(graph, node1, node2):

    S = len(
        GetNeighbors(graph, node1, node_set=set()).intersection(
            GetNeighbors(graph, node2, node_set=set())
        )
    ) / len(
        GetNeighbors(graph, node1, node_set=set()).union(
            GetNeighbors(graph, node2, node_set=set())
        )
    )

    return S


def K_Core_Decomposition(graph, k):
    isChanged = True
    while isChanged:
        isChanged = False
        del_list = []

        for v in graph:

            if len(graph[v]) <= k:
                del_list.append(v)
                isChanged = True
        for d in del_list:

            del graph[d]  # * delete vertex

        for d in del_list:
            for v in graph:
                if d in graph[v]:
                    # print(d," is deleted in ", graph[v])
                    graph[v].remove(d)  # * delete edge
                    # print("result = ", graph[v])

    graph = dict(sorted(graph.items(), key=lambda x: len(x[1]), reverse=True))

    # * Show degree of every node
    # for v in graph:
    #     print(v ," ::", len(graph[v]),graph[v])

    cluster = list()

    # * first of all, cluster with vertex and neighbors
    for v in graph:
        node_set = set()
        node_set.add(v)  # *(1)
        node_set = GetNeighbors(graph, vertex=v, node_set=node_set)  # *(2)

        cluster.append(node_set)

    # * Eliminate redundant case
    index = 0
    j_index = 0

    while index < len(cluster):
        v = cluster[index]

        j_index = 0
        while j_index < len(cluster):

            if index == j_index:
                j_index += 1
                continue
            if j_index >= len(cluster):
                break

            u = cluster[j_index]

            if v == u:

                # print(u," is deleted")
                cluster.remove(u)
                j_index -= 1

            j_index += 1
        index += 1

    # * Merge two clusters if common neighbor is.
    isChanged = True
    while isChanged:
        isChanged = False
        i = 0
        j = 0
        for i in range(len(cluster)):
            if not cluster[i]:
                continue
            for j in range(len(cluster)):
                if not cluster[j]:
                    continue

                if i >= j:
                    continue

                if cluster[i].intersection(cluster[j]):
                    # print(" = = = = = = == = == = == = = ")
                    # print(len(cluster[i]),"cluster i: ",cluster[i])
                    # print(len(cluster[j]),"cluster j: ",cluster[j])
                    # print("intersection : ",cluster[i].intersection(cluster[j]))
                    cluster[i] = cluster[i].union(cluster[j])
                    cluster[j] = set()
                    isChanged = True
                    # print(len(cluster[i]),"union=>>",cluster[i])

    return cluster


def GetDensity(graph, edge_list):
    vertexNum = len(graph)
    possibleEdgeNum = int(vertexNum * (vertexNum - 1) / 2)
    edges_len = len(edge_list)
    # print("edges len :", edges_len)
    # print("possible all edge len : ", possibleEdgeNum)
    density = edges_len / possibleEdgeNum
    # print("density : ", density)

    return density


def GetEdgeList(graph):
    edge_list = list()

    for v in graph:
        # print(v ," ::", len(graph[v]),graph[v])
        for node2 in graph[v]:
            tmp = {v, node2}
            edge_list.append(tmp)
    # print("edge list ", edge_list)

    new_edge_list = list()

    for edge in edge_list:
        if edge not in new_edge_list:
            new_edge_list.append(edge)

    return new_edge_list


def GetSubGraph(graph, cluster):
    new_graph = dict()

    for vertex in cluster:
        if vertex in graph:
            new_graph[vertex] = graph[vertex]

    return new_graph


def DivisiveClustering(graph, cluster_):

    ret_cluster = list()

    for clst in cluster_:
        # * edge 구하고 중복제거
        cluster = clst

        subgraph = GetSubGraph(graph, clst)

        edge_list = list()
        edge_list = GetEdgeList(subgraph)

        # * jaccard 계산
        jaccard_coeff_list = list()
        for edge in edge_list:

            tmp_list = list(edge)
            node1 = tmp_list[0]
            node2 = tmp_list[1]

            if node1 not in subgraph or node2 not in subgraph:
                continue
            jaccard_coeff = GetJaccardCoefficient(subgraph, node1, node2)
            jaccard_coeff_list.append([node1, node2, jaccard_coeff])

        density = GetDensity(subgraph, edge_list)

        if density >= 0.5:
            ret_cluster.append(clst)
            continue

        if density < 0.5:
            isConnected = True  # * init value
            while isConnected:
                jaccard_coeff_list.sort()

                smallest = jaccard_coeff_list[0][2]  # * init value
                smallest_list = jaccard_coeff_list[0]  # * init value
                for v in jaccard_coeff_list:
                    tmp = v[2]
                    if tmp < smallest:
                        smallest = tmp
                        smallest_list = v
                # print("to remove : ",smallest_list)
                remove_node1 = smallest_list[0]
                remove_node2 = smallest_list[1]
                for v in jaccard_coeff_list[:]:
                    if v[0] == remove_node1 and v[1] == remove_node2:
                        # print("node1 : ",remove_node1, "is deleted.")
                        # print("node2 : ",remove_node2, "is deleted.")
                        jaccard_coeff_list.remove(v)

                subgraph[remove_node1].remove(remove_node2)
                subgraph[remove_node2].remove(remove_node1)
                edge_list = GetEdgeList(subgraph)

                for v in edge_list[:]:
                    if remove_node1 in v and remove_node2 in v:
                        # print("node1 : ",remove_node1, "is deleted. in edge list")
                        # print("node2 : ",remove_node2, "is deleted. in edge list")
                        edge_list.remove(v)

                for v in subgraph:
                    if len(subgraph[v]) == 0:
                        print(v, " is deleted in graph")  # * K-core-decomposition으로 삭제
                # * 삭제 완료
                cluster = K_Core_Decomposition(
                    subgraph, k
                )  # ?* k=0 for removing outliers
                # print("cluster : ", cluster)

                density = GetDensity(subgraph, edge_list)

                new_cluster = list()

                for v in cluster:
                    if not v:
                        continue
                    new_cluster.append(v)

                # i = 0
                # for v in new_cluster:
                #     print("div - new cluster ", i, v)
                #     i += 1
                cluster = new_cluster

                if density >= 0.5:
                    print("density >= 0.5")
                    break

                if len(cluster) > 1:
                    print("disconnected!")
                    isConnected = False

                    ret_cluster += DivisiveClustering(subgraph, cluster)

                else:
                    print("is connected!")
                    isConnected = True
                    continue

        if density >= 0.5:
            # print("density = ", density)

            for v in cluster:
                ret_cluster.append(v)
    # print("RETURN! ",ret_cluster)
    return ret_cluster


def main():
    # inputfile = 'assignment5_input.txt' #! sys
    # inputfile = 'test_input.txt'

    if len(sys.argv) != 2:
        print("No input file.")
        print("<Usage> as6.py assignment6_input.txt")
        # * inputfile = 'test_input.txt'
        return -1

    if len(sys.argv) == 2:
        inputfile = sys.argv[1]
    output_filename = "output.txt"

    graph = getDataFromFile(inputfile)
    start_time = datetime.now()
    global k
    k = 0
    # global CLUSTER
    # CLUSTER = list()

    main_cluster = list()

    cluster = K_Core_Decomposition(graph, k)
    # * show cluster number and nodes in the cluster
    new_cluster = list()

    for v in cluster:
        if not v:
            continue
        new_cluster.append(v)

    # * 클러스터가 connected되어있는지를 K-core로 확인.
    cluster = list()
    cluster = new_cluster

    i = 0
    for v in new_cluster:

        print("cluster ", i, v)
        print("cluster!")
        i += 1

    # i=0
    # for v in cluster:
    #     print("cluster ",i, v)
    #     i+=1
    #! first clustering 부분. connected 여부와 상관 없이 첫 번째 클러스터(가장 큰 클러스터)를 선택함
    first_cluster = cluster[0]

    original_graph = GetSubGraph(graph, first_cluster)  #! cluster[0]

    graph = original_graph.copy()  # * 가장 큰 클러스터 -> 서브그래프로 시작

    # * edge 구하고 중복제거
    edge_list = GetEdgeList(graph)
    # print("edge list : ",edge_list)
    # * jaccard 계산
    jaccard_coeff_list = list()
    for edge in edge_list:
        # print("jaccard : edge " ,edge)
        tmp_list = list(edge)
        node1 = tmp_list[0]
        node2 = tmp_list[1]
        jaccard_coeff = GetJaccardCoefficient(graph, node1, node2)
        jaccard_coeff_list.append([node1, node2, jaccard_coeff])

    density = GetDensity(graph, edge_list)

    if density >= 0.5:
        # print("[1]density is ", density)
        print("first cluster's density is over 0.5")
        # print("cluster ",first_cluster )
        return 0

    if density < 0.5:  # * density < 0.5
        isConnected = True  # * init value
        while isConnected:
            # print("[1] density is ",density)

            # * remove
            jaccard_coeff_list.sort()

            smallest = jaccard_coeff_list[0][2]  # * init value
            smallest_list = jaccard_coeff_list[0]  # * init value
            for v in jaccard_coeff_list:
                tmp = v[2]
                if tmp < smallest:
                    smallest = tmp
                    smallest_list = v
            # print("to remove : ",smallest_list)

            remove_node1 = smallest_list[0]
            remove_node2 = smallest_list[1]
            # print("jaccard coeff list length : ",len(jaccard_coeff_list))
            for v in jaccard_coeff_list[:]:

                if v[0] == remove_node1 and v[1] == remove_node2:
                    # print("node1 : ",remove_node1, "is deleted.")
                    # print("node2 : ",remove_node2, "is deleted.")
                    jaccard_coeff_list.remove(v)
                    # print("제거 후 jaccard list : ",jaccard_coeff_list)

            graph[remove_node1].remove(remove_node2)
            graph[remove_node2].remove(remove_node1)

            # print("remove node1 ", remove_node1,"의 edge들 ", graph[remove_node1])
            # print("length1 : ",len(graph[remove_node1]))
            # print("remove node2 ", remove_node2,"의 edge들 ", graph[remove_node2])
            # print("length2 : ",len(graph[remove_node2]))
            for v in edge_list[:]:
                if remove_node1 in v and remove_node2 in v:
                    # print("node1 : ",remove_node1, "is deleted. in edge list")
                    # print("node2 : ",remove_node2, "is deleted. in edge list")
                    edge_list.remove(v)

            for v in graph:

                if len(graph[v]) == 0:
                    print(v, " is deleted in graph")
            # * 삭제
            cluster = K_Core_Decomposition(graph, k)  # ?* k=0 for removing outliers

            density = GetDensity(graph, edge_list)

            new_cluster = list()

            for v in cluster:
                if not v:
                    continue
                new_cluster.append(v)

            # i = 0
            # for v in new_cluster:
            #     print(">new cluster ", i, v)
            #     i += 1
            cluster = new_cluster

            if density >= 0.5:
                break

            if len(cluster) > 1:
                isConnected = False
                # print("disconnected!")
                main_cluster += DivisiveClustering(graph, cluster)

            else:
                isConnected = True
                # print("is connected!")
                continue

    # print("main cluster : ",main_cluster)
    result_cluster = list()

    for v in main_cluster:
        if v not in result_cluster:
            result_cluster.append(v)

    result_cluster.sort(key=len, reverse=True)
    for v in result_cluster:
        print("cluster ", v)

    print("[+] Time Elapsed : ", datetime.now() - start_time, "microseconds")

    # * save to output file with size : nodes in a cluster
    output_to_file(output_filename, result_cluster)


if __name__ == "__main__":
    main()
