import socket
import pymysql.cursors

# 数据库配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'zzk123456789',
    'database': 'atm',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def handle_client(client_socket):
    try:
        # 接收客户端发送的用户名
        username = client_socket.recv(1024).decode()
        # 数据库连接和查询
        with pymysql.connect(**db_config).cursor() as cursor:
            if check_username(cursor, username):
                if handle_password(cursor, username, client_socket):
                    process_transaction(cursor, username, client_socket)
            else:
                client_socket.sendall(b"ID not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()

def check_username(cursor, username):
    # 检查用户名是否存在
    sql = "SELECT username, balance FROM accounts WHERE username = %s"
    cursor.execute(sql, (username,))
    return cursor.fetchone()

def handle_password(cursor, username, client_socket):
    # 发送密码请求并验证
    client_socket.sendall(b"500 sp AUTH REQUIRED!")
    password = client_socket.recv(1024).decode()
    sql = "SELECT balance FROM accounts WHERE username = %s AND password = %s"
    cursor.execute(sql, (username, password))
    result = cursor.fetchone()
    if result:
        client_socket.sendall(b"525 OK!")
        return True
    else:
        client_socket.sendall(b"Invalid password.")
        return False

def process_transaction(cursor, username, client_socket):
    # 处理取款
    user_withdraw = int(client_socket.recv(1024).decode())
    balance = cursor.fetchone()['balance']
    if balance >= user_withdraw:
        update_balance(cursor, username, balance - user_withdraw)
        client_socket.sendall(f"SUCCESS:you have {balance - user_withdraw} left in your balance!".encode())
        handle_final_response(client_socket)
    else:
        client_socket.sendall(b"401 sp ERROR!")

def update_balance(cursor, username, new_balance):
    # 更新数据库中的余额
    sql = "UPDATE accounts SET balance=%s WHERE username=%s"
    cursor.execute(sql, (new_balance, username))
    cursor.connection.commit()

def handle_final_response(client_socket):
    # 接收和处理结束语
    user_over = client_socket.recv(1024).decode()
    if user_over in ["确认", "取消"]:
        client_socket.sendall(b"BYE!")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('', 2525))
        server_socket.listen(5)
        print("Server is listening on port 2525...")
        while True:
            client_socket, _ = server_socket.accept()
            handle_client(client_socket)

if __name__ == "__main__":
    main()