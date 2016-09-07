'''
Created on 25-Sep-2015
@author: suhas
'''

import logging

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
        
    def createTable_(self, tableName=None, column_family=None, prime=None):
        if not (tableName and column_family and prime):
            return None
        try:
            if prime:
                query = "CREATE TABLE "+self.keyspace+"."+tableName+" ( "+column_family+", "+" PRIMARY KEY("+prime+" ))";
                return self.Transaction(query);
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
        self.Transaction(cql);


def main(): 
    db = configDB()
    db.initialization()
    column_definition={"content_id":"uuid","userId":"uuid","location":"text"}
    db.createTable("test_table", column_definition, ["content_id"])
    
    
if __name__ == '__main__':
    main()
