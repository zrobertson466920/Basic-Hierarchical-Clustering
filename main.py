import numpy as np

def dist(a,b):
    return abs(b-a)

def center(a,b):
    return (a+b)/2

# Add new cluster, remove 2 row/column & add row/column to sim matrix
def union(cluster,rcluster,sim,a,b):

    # Union Clusters
    cl = len(cluster)
    nsize = rcluster[a][1] + rcluster[b][1]
    ndata = center(rcluster[a][0],rcluster[b][0])
    cluster.append([ndata,nsize,None,[rcluster[a][0],rcluster[b][0]]])

    ra = rcluster[a]
    rb = rcluster[b]
    rcluster.remove(ra)
    rcluster.remove(rb)
    rcluster.append([ndata,nsize,None,[a,b]])

    # Update Cluster's Parent
    cluster[a][2] = cl
    cluster[b][2] = cl

    # Update Sim Matrix
    sim = np.delete(sim,(a,b),axis = 0)
    sim = np.delete(sim,(a,b),axis = 1)

    # Add new row/column (I vote this most difficult to code)
    nrow = []
    dim = np.shape(sim)
    # Construct the row
    for i in range(dim[0]):
        nrow.append(dist(rcluster[i][0],rcluster[len(rcluster)-1][0]))
    mrow = np.matrix(nrow)
    # Construct the column (We'll have to transpose)
    sim = np.append(sim,mrow,axis = 0)
    mrow = np.append(mrow,[[0]],axis = 1)
    sim = np.append(sim,mrow.T,axis = 1)

    return sim


def main():
    data = [1,2,4,5]
    dl = len(data)

    # Create Initial Clusters
    # cluster[i] = [data,size,parent,children]
    cluster = []
    rcluster = []
    for i in data:
        cluster.append([i,1,None,None])
        rcluster.append([i,1,None,None])

    # Create Similarity Matrix
    sim = np.arange(dl*dl).reshape(dl,dl)
    for i in range(dl):
        for j in range(dl):
            sim[i][j] = dist(data[i],data[j])

    # Main Loop
    print("The Data:")
    print(data)
    print("\nThe Dendrogram:")
    size = np.shape(sim)
    while (len(rcluster) > 1):
        print(rcluster)
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
    print(cluster)


main()
