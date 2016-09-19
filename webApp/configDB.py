'''
Created on 25-Sep-2015
@author: suhas
'''

import logging
import uuid
from cassandra.cluster import Cluster

class configDB:
    cluster=None
    session=None
    log = None
    keyspace = "configdbkeyspace"
    
    
    def __init__(self):
        return
  
        
    def initialization(self):
        try:
            logging.basicConfig(filename='/var/log/configDB.log', filemode='w', format='%(asctime)-15s:%(levelname)s:%(message)s', 
                            level=logging.DEBUG)
            self.Connect(["127.0.0.1"])
            if self.keyspace not in self.cluster.metadata.keyspaces.keys():
                self.createNameSpace(self.keyspace)
            logging.info("Cassandra DB is successfully initialized")
        except Exception as err:
                raise Exception(err)
        return


    """Connect to cassandra cluster"""
    def Connect(self, nodes):
        try:
            self.cluster = Cluster(nodes)
            metadata = self.cluster.metadata 
            self.session = None
            self.session = self.cluster.connect()
            logging.info('Connected to cluster: ' + metadata.cluster_name)
            for host in metadata.all_hosts():
                logging.info('Datacenter: %s; Host: %s; Rack: %s', host.datacenter, host.address, host.rack)
            #self.session.execute("USE \"%s\"", self.keyspace)
        except Exception as err:
            raise Exception(err)
    
    
    """Terminate Cassandra cluster connection"""
    def Close(self):
        self.session.cluster.shutdown()
        self.session.shutdown()


    """Executes Cassandra cqlsh query. Namespace is configDbKeyspace"""
    def Transaction(self,query):
        try:    
            result = self.session.execute(query);
            return result
        except Exception as err:
            raise Exception(err)
    
    
    def createNameSpace(self, keyspace=None):
        try:
            if keyspace:
                self.keyspace=keyspace
                query = "CREATE KEYSPACE "+keyspace+" WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3}"	
                return self.Transaction(query)
            else:
                logging.ERROR("Create keyspace failed due to keyspace value:%s",keyspace)
                return None
        except Exception as err:
            raise Exception(err)
        
        
    def createTable(self,tableName=None,column_definition=dict(),primary_keys=[]):
        if len(column_definition):
            col_def=""
            for key in column_definition.keys():
                col_def+=""+key+" "+column_definition[key]+","
            cql="CREATE TABLE "+self.keyspace+"."+tableName+" ( "+col_def
            if primary_keys:
                prim=""
                for key in primary_keys[0:-1]:
                    prim+=" "+key+","
                prim+=primary_keys[-1]
                cql+=" PRIMARY KEY ("+prim+") );"
                print cql
                try:
                    return self.Transaction(cql);
                except Exception as err:
                    raise Exception(err)
                
    """Method to retrieve tuple"""        
    def get(self, tableName=None, condition=None):
        if not condition:
            cql = "SELECT * from "+self.keyspace+"."+tableName+""
            try:
                return self.Transaction(cql)
            except Exception as err:
                raise Exception(err)
        if not tableName:
            raise Exception("Table name is must")
        
        cql = "SELECT * from "+self.keyspace+"."+tableName+" WHERE "+condition+""
        try:
            return self.Transaction(cql)
        except Exception as err:
            raise Exception(err)
    
    """Method to save a tuple"""
    def save(self, tableName=None,column_list=[],value_list=[]):
        
        if not tableName:
            raise Exception("Table name is must")
        if not column_list:
            raise Exception("Column name is must")
        if not value_list:
            raise Exception("Column values are must")
        
        columns=""
        for item in column_list[0:-1]:
            columns+=item+","
        columns+=column_list[-1]
        value=""
        for item in value_list[0:-1]:
            if type(item)==uuid.UUID:
                value+=""+str(item)+","
            else:
                value+="'"+item+"',"
            
        if type(value_list[-1])==uuid.UUID:
            value+=""+str(item)+","
        else:
            value+="'"+value_list[-1]+"'" 
        
        cql = "INSERT into "+self.keyspace+"."+tableName+" ( "+columns+" )"+" \
                VALUES ( "+value+" )" 
        
        print cql
        try:
            self.Transaction(cql)
        except Exception as err:
            raise Exception(err)
      
    def delete(self, tableName=None,condition=None):
        if not tableName:
            raise Exception("Table name is must")
        if not condition:
            raise Exception("A condition is must in order to delete a tuple \
                            from table")
        cql = "DELETE from "+self.keyspace+"."+tableName+" WHERE "+condition
        print cql
        try:
            self.Transaction(cql)
        except Exception as err:
            raise Exception(err)
        
class contentSystems(configDB):
    content_id = "user_id"
    user_id = "user_id"
    location = "text"
    type = "varchar"
    category = "varchar"
    description = "text"
    column_field = {"content_id":content_id,
                    "user_id":user_id,
                    "location":location,
                    "type":type,
                    "category":category,
                    "description":description
                    }
    table_name="contentSystems"
    primaryKeys=["content_id"]
    column_list=['content_id','user_id','category','description','location',
                 'type' ]
    value_list =[user_id.uuid4(),user_id.uuid4(),'movies','About a movie',
                'x/y/z.mp4','video']
    db = configDB()
    db.initialization()
    import pdb
    pdb.set_trace()
    #db.createTable(table_name, column_field, primaryKeys)
    db.save(table_name, column_list, value_list)
    row=db.get(table_name,"content_id=4683a3fc-a8b9-46d0-8f9e-269f8f5dffc5")
    
def main():
    '''
        Example of creating a table
        column_definition={"content_id":"user_id","userId":"user_id","location":"text"}
        db.createTable("test_table", column_definition, ["content_id"])
    '''
    contentSystems()
    
    
if __name__ == '__main__':
    main()
