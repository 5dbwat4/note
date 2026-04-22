```js
/**
 * @param {character[][]} grid
 * @return {number}
 */
var numIslands = function(grid) {
    const moveTillNoEdge=(x,y)=>{
        if(grid[x][y]=='1'){
            grid[x][y]='0';
        }
        if(grid[x+1]&&grid[x+1][y]=='1'){
            moveTillNoEdge(x+1,y);
        }
        if(grid[x-1]&&grid[x-1][y]=='1'){
            moveTillNoEdge(x-1,y);
        }
                if(grid[x][y+1]=='1'){
            moveTillNoEdge(x,y+1);
                }
                      if(grid[x][y-1]=='1'){
            moveTillNoEdge(x,y-1);
                }          
    }
    let n=0;
    for(let i=0;i<grid.length;i++){
        for(let j=0;j<grid[i].length;j++){
            if(grid[i][j]=='1'){
                moveTillNoEdge(i,j);
n++
            }
        }
    }
    return n;
};
```