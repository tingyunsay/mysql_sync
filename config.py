#!/usr/bin/env python3
# -*- coding:utf-8 -*-


#源表需多填一项--表名
source_database = {
    "user":"root",
    "pwd":"123456",
    "host":"192.168.217.10",
    "port":3306,
    "db":"music_ugc",
    "table":"magazine_label"
}

target_database = [{
    "user":"tingyun",
    "pwd":"tingyun",
    "host":"127.0.0.1",
    "port":3306,
    "db":"music_ugc"
    }

]


bakfile_name = "tingyun.sql"



