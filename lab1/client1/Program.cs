using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

class Program
{
    static void Main(string[] args)
    {
        StartClient();
    }

    static void StartClient()
    {
        Socket client = null;
        try
        {
            IPAddress serverIp = IPAddress.Parse("127.0.0.1");
            int serverPort = 9000;

            client = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            client.Connect(new IPEndPoint(serverIp, serverPort));
            Console.WriteLine("Connected to the server");

            // Start a new thread to receive messages from the server
            Thread receiveThread = new Thread(() => ReceiveMessages(client));
            receiveThread.Start();

            while (true)
            {
                Console.Write("Enter message to send (type 'exit' to close connection): ");
                string text = Console.ReadLine();
                byte[] bytesData = Encoding.UTF8.GetBytes(text);
                client.Send(bytesData);

                if (text.ToLower() == "exit")
                    break;
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"An error occurred: {ex.Message}");
        }
        finally
        {
            if (client != null)
            {
                if (client.Connected)
                {
                    client.Shutdown(SocketShutdown.Both);
                    client.Close();
                }
            }
        }
    }

    static void ReceiveMessages(Socket client)
    {
        try
        {
            while (true)
            {
                byte[] buffer = new byte[1024];
                int bytesReceived = client.Receive(buffer);
                string text = Encoding.UTF8.GetString(buffer, 0, bytesReceived);
                Console.WriteLine($"Server: {text}");

                if (text.ToLower() == "exit")
                    break;
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"An error occurred: {ex.Message}");
        }
    }
}
