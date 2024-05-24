from socket import *


def send_and_receive(socket, message=None):
    """ 发送消息并接收响应的简化函数 """
    if message is not None:
        socket.sendall(message.encode())
    return socket.recv(1024).decode()


def main():
    server_address = ('localhost', 2525)

    try:
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect(server_address)

        # 第一步：发送ID并接收响应
        user_id = input("Enter your ID: ")
        response = send_and_receive(client_socket, user_id)
        print(response)

        if response == "500 sp AUTH REQUIRED!":
            # 第二步：发送密码并接收响应
            user_password = input("Enter your password: ")
            response = send_and_receive(client_socket, user_password)
            print(response)

            if response == "525 OK!":
                # 第三步：发送取款金额并接收响应
                user_withdraw = input("Enter withdraw amount: ")
                response = send_and_receive(client_socket, user_withdraw)
                print(response)

                if response.startswith("SUCCESS"):
                    # 最终步骤：发送结束语并接收响应
                    user_over = input("Enter final command: ")
                    response = send_and_receive(client_socket, user_over)
                    print(response)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()


if __name__ == "__main__":
    main()