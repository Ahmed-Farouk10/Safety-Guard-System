import socket
import ssl

def test_connection():
    host = "broker.emqx.io"
    port = 1883
    
    print(f"Testing connection to {host}:{port}")
    
    try:
        # Create a socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        
        # Try to connect
        sock.connect((host, port))
        print("Successfully connected to the server!")
        
        # Close the connection
        sock.close()
        return True
    except Exception as e:
        print(f"Connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_connection() 