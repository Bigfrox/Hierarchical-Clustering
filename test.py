def GetSubGraph(graph,cluster):
    new_graph = dict()
    print("cluster : ", cluster)
    print("graph: ",graph)
    for vertex in cluster:
        if vertex in graph:
            new_graph[vertex] = graph[vertex]
            print("new graph of ", vertex, new_graph[vertex])

    return new_graph


def K_Core_Decomposition(graph,k):
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

def GetNeighbors(graph, vertex, node_set):

    for r in graph[vertex]:
        node_set.add(r)

    return node_set


def DivisiveClustering(graph,cluster):
    #global CLUSTER
    
    print("DIVISIVE!")
    print("\n")
    ret_cluster = list()
    
    for clst in cluster:
        #* edge 구하고 중복제거
        # clst_num = cluster.index(clst)
        #print("clst : ", clst)
        # print("clst num ; ",clst_num)
        print("cluster len ", len(cluster))
        print("clst len : ", len(clst))
        # if 'YBR258C' in subgraph:
        #     print("YBR258C는 subgraph 안에 있습니다.")
        # if 'YBR258C' in clst:
        #     print("YBR258C는 clst 안에 있습니다.")
        # else:
        #     print("clst에 없습니다.")
            #!!!!!!!!!!!!!!클러스터에 없는걸 찾으려는게 문제임.
        print(len(cluster) , "is len of cluster ")
        print("====================")
        print(len(clst), "len of clst")
        tmp_graph = GetSubGraph(graph,clst)#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        subgraph = tmp_graph.copy()
        # if 'YBR258C' in graph:
        #     print("YBR258C는 graph안에 있습니다.")
        # else:
        #     print("YBR258C는 graph안에 없습니다.")
        print("graph length : ", len(subgraph))
        edge_list = list()
        edge_list = GetEdgeList(subgraph)
        
        #* jaccard 계산
        jaccard_coeff_list = list()
        for edge in edge_list:
            print("=============================\n\n")
            tmp_list = list(edge)
            node1 = tmp_list[0]
            node2 = tmp_list[1]
            print("edge(node1,node2) : ", edge)
            if node1 not in subgraph or node2 not in subgraph:
                print("여기 subgraph : ", subgraph)
            jaccard_coeff = GetJaccardCoefficient(subgraph,node1,node2)
            jaccard_coeff_list.append([node1,node2,jaccard_coeff])
        
        density = GetDensity(subgraph, edge_list)

        
        if density < 0.5:
            isConnected = True #* init value
            while isConnected:
                jaccard_coeff_list.sort()
                
                # print("jaccard list ", jaccard_coeff_list)
                # for v in jaccard_coeff_list:
                #     print("jac : ",v)
                        
                smallest = jaccard_coeff_list[0][2] #* init value
                smallest_list = jaccard_coeff_list[0] #* init value
                for v in jaccard_coeff_list:
                    tmp = v[2]
                    if tmp < smallest:
                        smallest = tmp
                        smallest_list = v
                #print("to remove : ",smallest_list)
                remove_node1 = smallest_list[0]
                remove_node2 = smallest_list[1]
                for v in jaccard_coeff_list[:]:
                    if v[0] == remove_node1 and v[1] == remove_node2:
                        print("node1 : ",remove_node1, "is deleted.")
                        print("node2 : ",remove_node2, "is deleted.")
                        jaccard_coeff_list.remove(v)
                
                
                graph[remove_node1].remove(remove_node2)
                graph[remove_node2].remove(remove_node1)
                subgraph[remove_node1].remove(remove_node2)
                subgraph[remove_node2].remove(remove_node1)
                edge_list = GetEdgeList(subgraph)
                
                
                
                for v in edge_list[:]:
                    if remove_node1 in v and remove_node2 in v:
                        print("node1 : ",remove_node1, "is deleted. in edge list")
                        print("node2 : ",remove_node2, "is deleted. in edge list")
                        edge_list.remove(v)


                for v in subgraph:
                    
                    if len(subgraph[v]) == 0:
                        #if v == 'YBR258C':
                            # print("YBR258C발견 : ", graph[v])
                            # input("pause!")
                        print(v, " is deleted in graph")
                #* 삭제 완료
                
                cluster = K_Core_Decomposition(subgraph,k) #?* k=0 for removing outliers
                #?graph = GetSubGraph(graph,cluster)
                
                density = GetDensity(subgraph,edge_list)
                
                new_cluster = list()
                
                for v in cluster:
                    if not v:
                        
                        continue
                    new_cluster.append(v)
                    
                    #print(v,"is added in new cluster")
                
                # i = 0
                # for v in new_cluster:
                #     print("new cluster ", i, v)
                #     i += 1
                cluster = new_cluster
                
                if density >= 0.5:
                    break
                
                
                if len(cluster) > 1:
                    #print("disconnected!")
                    isConnected = False
                    ret_cluster += DivisiveClustering(subgraph,cluster)
                    
                else:
                    #print("is connected!")
                    isConnected = True
                    continue

                
        if density >= 0.5:
            #print("density = ", density)
            
            for v in cluster:
                ret_cluster.append(v)
    #print("RETURN! ",ret_cluster)
    return ret_cluster
def GetEdgeList(graph):
    edge_list = list()
    print("GetEdgeList 함수")
    # if 'YBR258C' in graph:
    #     print("'YBR258C'는 GetEdgeList의 인자인 graph안에 있습니다.")
    #     print("'YBR258C' : ", graph['YBR258C'])
    for v in graph:
        #print(v ," ::", len(graph[v]),graph[v])
        for node2 in graph[v]:
            tmp = {v,node2}
            edge_list.append(tmp)
    #print("edge list ", edge_list)
    for edge in edge_list:
        if 'YBR258C' in edge:
            print("edge ; ", edge)
    new_edge_list = list()

    for edge in edge_list:
        if edge not in new_edge_list:
            new_edge_list.append(edge)
    
    return new_edge_list

    
def GetDensity(graph, edge_list):
    vertexNum = len(graph)
    possibleEdgeNum = int(vertexNum * (vertexNum-1) / 2)
    edges_len = len(edge_list)
    #print("edges len :", edges_len)
    #print("possible all edge len : ", possibleEdgeNum)
    density = edges_len / possibleEdgeNum
    # print("density : ", density)
    
    return density

def GetJaccardCoefficient(graph, node1, node2):
    if node1 not in graph or node2 not in graph:
        print("jaccard graph: ", graph) #! 여기 graph랑 여기 전 subgraph랑 다르다.
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


graph = dict()
graph['A'] = {'B', 'C', 'D'}
graph['B'] = {'A', 'C', 'D'}
graph['C'] = {'B', 'A', 'D'}
graph['D'] = {'B', 'C', 'A'}

graph['A1'] = {'B1', 'C1'}
graph['B1'] = {'A1', 'C1'}
graph['C1'] = {'B1', 'A1'}


print(graph)

cluster = K_Core_Decomposition(graph,k=0)
new_cluster = list()
for v in cluster:
    if v:
        new_cluster.append(v)
print(new_cluster)

new = DivisiveClustering(graph,new_cluster)
print(new)


new.sort(key=len,reverse=True)
#*graph = dict(sorted(graph.items(), key=lambda x: len(x[1]), reverse=True))
print(new)