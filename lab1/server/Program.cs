using System;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

class Program
{
    static List<Socket> clientSockets = new List<Socket>(); // Listă pentru stocarea socket-urilor clienților conectați

    static void Main(string[] args)
    {
        StartServer(); // Funcția de pornire a serverului
    }

    static void StartServer()
    {
        Socket serverSocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        try
        {
            IPAddress ipAddress = IPAddress.Parse("127.0.0.1");
            serverSocket.Bind(new IPEndPoint(ipAddress, 9000)); // Legarea serverului la adresa IP și portul specificate
            serverSocket.Listen(5); // Ascultarea conexiunilor de la clienți

            Console.WriteLine("Server started. Waiting for connections...");

            while (true)
            {
                Socket connection = serverSocket.Accept(); // Așteptarea și acceptarea conexiunilor de la clienți
                Console.WriteLine("Connection accepted from " + connection.RemoteEndPoint);

                clientSockets.Add(connection); // Adăugarea socket-ului clientului în lista de clienți conectați

                // Start a new thread to handle the connection
                Thread clientThread = new Thread(() => HandleClient(connection)); // Pornirea unui fir de execuție pentru a gestiona conexiunea cu clientul
                clientThread.Start();
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"An error occurred: {ex.Message}"); // Tratarea și afișarea erorilor în cazul apariției unei excepții
        }
        finally
        {
            serverSocket.Close(); // Închiderea socketului serverului la final pentru eliberarea resurselor
        }
    }

    static void HandleClient(Socket clientSocket)
    {
        try
        {
            byte[] buffer = new byte[1024];
            while (true)
            {
                int bytesReceived = clientSocket.Receive(buffer); // Primirea datelor de la client
                string text = Encoding.UTF8.GetString(buffer, 0, bytesReceived); // Convertirea datelor primite în șir de caractere
                Console.WriteLine($"From {clientSocket.RemoteEndPoint}: {text}"); // Afișarea mesajului primit de la client

                if (text.ToLower() == "exit")
                    break;

                BroadcastMessage(text, clientSocket); // Retransmiterea mesajului către toți clienții, excludând expeditorul
            }

            clientSockets.Remove(clientSocket);
            clientSocket.Shutdown(SocketShutdown.Both); // Închiderea socketului clientului
            clientSocket.Close();
        }
        catch (Exception ex)
        {
            Console.WriteLine($"An error occurred: {ex.Message}"); // Tratarea și afișarea erorilor în cazul apariției unei excepții
        }
    }

    static void BroadcastMessage(string message, Socket sender)
    {
        foreach (Socket clientSocket in clientSockets)
        {
            if (clientSocket != sender) // Excluderea expeditorului din lista destinatarilor
            {
                try
                {
                    byte[] bytesData = Encoding.UTF8.GetBytes(message);
                    clientSocket.Send(bytesData); // Trimiterea mesajului către clienții conectați
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"An error occurred while broadcasting message to a client: {ex.Message}"); // Tratarea și afișarea erorilor în cazul apariției unei excepții
                }
            }
        }
    }
}
