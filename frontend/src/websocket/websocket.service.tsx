class WebSocketService {
  private socket: WebSocket | null = null;
  private isConnected: boolean = false;
  private url: string = "ws://localhost:8765"; // WebSocket URL
  private reconnectDelay: number = 1000; // Initial reconnect delay (1 second)
  private maxReconnectDelay: number = 10000; // Maximum reconnect delay (10 seconds)

  constructor() {
    this.connect(); // Try to connect as soon as the service is instantiated
  }

  // Function to connect to the WebSocket server
  connect() {
    if (!this.socket) {
      this.socket = new WebSocket(this.url);

      this.socket.onopen = () => {
        console.log("Connected to WebSocket server");
        this.isConnected = true; // Mark as connected
        this.reconnectDelay = 1000; // Reset the reconnect delay
      };

      this.socket.onclose = () => {
        console.log("Disconnected from WebSocket server");
        this.isConnected = false; // Mark as disconnected
        this.socket = null; // Reset socket for reconnection
        this.attemptReconnect(); // Try to reconnect
      };

      this.socket.onerror = (error) => {
        console.error("WebSocket error:", error);
        this.isConnected = false; // Mark as disconnected on error
        this.attemptReconnect(); // Try to reconnect
      };
    }
  }

  // Function to attempt reconnection with exponential backoff
  private attemptReconnect() {
    if (!this.isConnected) {
      console.log(`Reconnecting in ${this.reconnectDelay / 1000} seconds...`);
      setTimeout(() => {
        this.connect(); // Try to reconnect
        this.reconnectDelay = Math.min(
          this.reconnectDelay * 2,
          this.maxReconnectDelay
        ); // Exponential backoff
      }, this.reconnectDelay);
    }
  }

  // Function to send a message to the WebSocket server
  sendMessage(message: { userId: string; userName: string; content: string }) {
    if (!this.isConnected) {
      console.warn("WebSocket is not open. Trying to reconnect...");
      this.connect(); // Attempt to reconnect if not connected
    }

    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify(message)); // Send message if connected
      console.log("Message sent:", message);
    } else {
      console.warn("WebSocket is not open. Message not sent.");
    }
  }

  // Function to close the WebSocket connection
  close() {
    if (this.socket) {
      this.socket.close();
      console.log("WebSocket connection closed.");
    }
  }
}

const webSocketService = new WebSocketService();
export default webSocketService;
