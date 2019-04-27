# mysql_sync
mysql数据同步简易脚本(一对多)

### 功能
由于近期的开发常需要在一些测试库之间迁移表数据，为了减少复制粘贴的工作，这个脚本正是用于<span style="color:OrangeRed;">**简单配置/快速同步mysql指定表数据**</span>.   

使用的是<span style="color:OrangeRed;">mysql 命令导入</span>，相关的导入方式还有[mysql导入数据](https://www.runoob.com/mysql/mysql-database-import.html)  
将配置文件中的source_database中的表(table)，同步到target_database中的每个库中去.  

**代码流程**  
其先将source_database中的表数据load成一个文件（bakfile_name），接着其会主动依次创建target_database中指定的db名，最后再将source_database中的表数据依次load到新建（或已存在）的db中去

**功能代码**
```sql
mysqldump -u{user} -p{pwd} -h{host} -P{port} {db} {table} > ./{bakfile_name}

mysql -u{user} -p{pwd} -h{host} -P{port} {db} < ./{bakfile_name}
```
### 使用
在target_database中依次配置好需要导入的目标群数据库，但是注意：其导入方式会直接在原始数据上insert新数据 -- **具体可以查看导出的sql文件内容** ，所以可能会导致数据库文件出现异常（新数据将老数据覆盖，两个数据库并非完全相同），最好在导入数据前，确认target_db中的表中的数据是否还需要使用（若不需要，可以直接drop表）

