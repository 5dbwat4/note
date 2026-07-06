import { autoContentFiles } from "#accumbens/config";
import fs from "fs";

export default {
    "dir":import.meta.url,
    "path":{
        "default":false,
        "aliases":["Schoolwork/CTF101","CS/CTF101","Featured/CTF101"], 
    },
    "entries":autoContentFiles(),
    "name":"CTF101",
    "show":false,
}