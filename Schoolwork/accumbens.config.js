import phy from "./Physics/dir.js"
import other from "./Others/dir.js"
import cs from "./CS/dir.js"
import math from "./Math/dir.js"



export default {
    "dir":import.meta.url,
    "path":"",
    "name":"课程笔记",
    "subcategories":[
        ...cs,
        ...math,
        ...phy,
        ...other,
    ],
    "entries":"auto"
}
