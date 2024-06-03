using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

class Program
{
    static void Main(string[] args)
    {
        StartClient(); // Funcția de pornire a clientului
    }

    static void StartClient()
    {
        try
        {
            IPAddress serverIp = IPAddress.Parse("127.0.0.1");
            int serverPort = 9000;

            Socket client = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            client.Connect(new IPEndPoint(serverIp, serverPort)); // Conectarea clientului la server

            Console.WriteLine("Connected to the server");

            // Start a new thread to receive messages from the server
            Thread receiveThread = new Thread(() => ReceiveMessages(client)); // Pornirea unui fir de execuție pentru a primi mesaje de la server
            receiveThread.Start();

            while (true)
            {
                Console.Write("Enter message to send (type 'exit' to close connection): ");
                string text = Console.ReadLine();
                byte[] bytesData = Encoding.UTF8.GetBytes(text);
                client.Send(bytesData); // Trimiterea mesajului către server

                if (text.ToLower() == "exit")
                    break;
            }

            client.Shutdown(SocketShutdown.Both); // Închiderea conexiunii cu serverul
            client.Close();
        }
        catch (Exception ex)
        {
            Console.WriteLine($"An error occurred: {ex.Message}"); // Tratarea și afișarea erorilor în cazul apariției unei excepții
        }
    }

    static void ReceiveMessages(Socket client)
    {
        try
        {
            while (true)
            {
                byte[] buffer = new byte[1024];
                int bytesReceived = client.Receive(buffer); // Primirea mesajelor de la server
                string text = Encoding.UTF8.GetString(buffer, 0, bytesReceived); // Convertirea datelor primite în șir de caractere
                Console.WriteLine($"Server: {text}"); // Afișarea mesajului primit de la server

                if (text.ToLower() == "exit")
                    break;
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"An error occurred: {ex.Message}"); // Tratarea și afișarea erorilor în cazul apariției unei excepții
        }
    }
}
