from database.DB_connect import DBConnect
from model.order import Order


class DAO():

    @staticmethod
    def getStores():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)

        query = """select * 
                from stores s 
                order by S.store_id asc """

        cursor.execute(query)

        for row in cursor:
            result.append(row["store_id"])

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def getNodes(store):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)

        query = """ select * from orders o
                    where o.store_id = %s """

        cursor.execute(query, (store,))

        for row in cursor:
            result.append(Order(**row))

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def getEdges(idMap, store, store2, k):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)

        query = """select t1.order_id as node1, t2.order_id as node2, t1.order_date as date1, t2.order_date as date2,
                    SUM(oi1.quantity) + SUM(oi2.quantity) AS edge_weight 
                    from (select * from orders o
                    where o.store_id = %s) t1, 
                    (select * from orders o
                    where o.store_id = %s) t2, 
                    order_items oi1, order_items oi2 
                    where t1.order_id != t2.order_id and 
                    t1.order_date > t2.order_date
                    AND  datediff( t1.order_date, t2.order_date) < %s 
                    and oi1.order_id = t1.order_id 
                    and oi2.order_id = t2.order_id
                    GROUP BY t1.order_id, t2.order_id, t1.order_date, t2.order_date"""

        cursor.execute(query, (store, store2, k))

        for row in cursor:
            if row["node1"] in idMap and row["node2"] in idMap:
                result.append((idMap[row["node1"]], idMap[row["node2"]], row["edge_weight"]))

        cursor.close()
        conn.close()

        return result
