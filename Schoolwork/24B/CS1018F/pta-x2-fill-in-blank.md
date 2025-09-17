40282.FILL_IN_THE_BLANK_FOR_PROGRAMMING:Topological sorting

The function of the following code is to perform topological ordering on a given graph 'g', where 'topnum [] records topological ordering from 1.
```c++
void Topsort( Graph G )
{
    Queue Q;
    Vertex V, W;
    NodePtr ptr;
    int counter = 0;
    Q = CreateEmptyQueue(NumVertex);
    for ( V=0;  VNumV;  V++ )
        if ( Indegree[V] == 0 )
            Enqueue(V, Q);
    while ( ! IsEmpty(Q) ){
        V = Dequeue( Q );
        TopNum[V] = @@[++counter](3);
        for ( ptr=G->List[V];  ptr;  ptr=ptr->Next) {
            W = ptr->Vertex;
            if ( @@[--Indegree[W]](3) == 0 )
                Enqueue(W, Q);
        }
        if ( counter !=  NumVertex )
            printf("ERROR: Graph has a cycle.\n");
        DisposeQueue(Q);
    }
}
```

answer：First null: + + counter
Second null: - - indegree [w]

## 希尔排序(shell sort)

39761.FILL_IN_THE_BLANK_FOR_PROGRAMMING:The implementation of Shellsort Algorithm with increment sequence {1,3,7,11}

Following function Shellsort(int A[], int N) is the implementation of Shellsort Algorithm with increment sequence {1,3,7,11}. Please fill in the blanks.
```c++
void Shellsort( int A[ ], int N )
{     int  i, j, k, Increment, Inc[]={1,3,7,11};
int  Tmp;
for ( k=3;   k>=0;   k--) {
@@[Increment = Inc[k]](3);
for ( i = Increment;  i < N;  i++ ) {
Tmp = A[ i ];
for ( j = i;  j >= Increment;  j -= Increment )
if( Tmp < A[ j - Increment ] )
@@[A[ j ] = A[ j - Increment ]](3);
else   break;
A[ j ] = Tmp;
}
```

answer：The first blank: increment = Inc [k]
The second blank: a [J] = a [J - increment]


## 39911.
The function `Unweighted` is to find the unweighted shortest path from `Vertex S` to every other vertices in a given `Graph`. The distances are stored in `dist[]`, and `path[]` records the paths. The `Graph` is defined as the following:
```c
typedef struct GNode *PtrToGNode;
struct GNode{
int Nv;          /*  Number of vertices */
int Ne;          /*  Number of edges    */
AdjList List;    /*  adjacency matrix */
};
typedef PtrToGNode Graph;
void Unweighted( Graph G, Queue Q, int dist[], int path[], Vertex S )
{
    Vertex V, W;
    NodePtr ptr;
    dist[S] = 0;
    Enqueue(S, Q);
    while ( ! IsEmpty(Q) ) {
    V = Dequeue( Q );
    for ( ptr=G->List[V].FirstEdge;  ptr;  ptr=ptr->Next) {
    W = ptr->AdjV;
    if ( dist[W] == INFINITY ) {
    @@[dist[W] = dist[V] + 1](3);
    path[W] = V;
    @@[Enqueue(W, Q)](3);
}
```

answer：The first empty: dist [w] = dist [v] + 1
The second empty: enqueue (W, q)