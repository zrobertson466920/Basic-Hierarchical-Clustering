import numpy as np
import matplotlib.pyplot as plt
import tree
from tree import Tree

def dist(a,b):
    return abs(b.data-a.data)

def center(a,b):
    return (a.data+b.data)/2

def merge(atree,btree):
    return Tree(center(atree,btree),[atree,btree])

# Add new cluster, remove 2 row/column & add row/column to sim matrix
def union(cluster,rcluster,sim,a,b):

    # Union Clusters
    ta = rcluster[a]
    tb = rcluster[b]
    tab = merge(rcluster[a],rcluster[b])
    rcluster.append(tab)
    cluster.append(tab)
    rcluster.remove(ta)
    rcluster.remove(tb)

    # Update Sim Matrix
    sim = np.delete(sim,(a,b),axis = 0)
    sim = np.delete(sim,(a,b),axis = 1)

    # Add new row/column (I vote this most difficult to code)
    nrow = []
    dim = np.shape(sim)
    # Construct the row
    for i in range(dim[0]):
        nrow.append(dist(rcluster[i],rcluster[len(rcluster)-1]))
    mrow = np.matrix(nrow)
    # Construct the column (We'll have to transpose)
    sim = np.append(sim,mrow,axis = 0)
    mrow = np.append(mrow,[[0]],axis = 1)
    sim = np.append(sim,mrow.T,axis = 1)

    return sim

def create_sim(trees):
    dl = len(trees)
    sim = np.arange(dl*dl).reshape(dl,dl)
    for i in range(dl):
        for j in range(dl):
            sim[i][j] = dist(trees[i],trees[j])
    return sim

def cluster(values):
    data = []
    for i in values:
        data.append(Tree(i))
    dl = len(data)

    # Create Initial Clusters
    # cluster[i] = [data,size,parent,children]
    cluster = []
    rcluster = []
    for datum in data:
        cluster.append(datum)
        rcluster.append(datum)

    # Create Similarity Matrix
    sim = create_sim(data)

    # Main Loop
    #print("The Data:")
    #print(data)
    print("\nThe Dendrogram:")
    size = np.shape(sim)
    while (len(rcluster) > 1):
        #print(cluster)
        min = (0,1)
        min_d = sim.item(min)
        for i in range(size[0]):
            for j in range(size[1]):
                    if (i != j) & (sim.item((i,j)) < min_d):
                        min = (i,j)
                        min_d = sim.item(min)
        sim = union(cluster,rcluster,sim,min[0],min[1])
        size = np.shape(sim)

    print("\nFull Cluster:")
    tree.print_tree(cluster[-1],5)

    plt.hist(values, bins = 20)
    plt.show()
