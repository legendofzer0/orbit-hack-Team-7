class WebSocketService {
  private socket: WebSocket | null = null;
  private isConnected: boolean = false;
  private url: string = "ws://localhost:8765"; // WebSocket URL
  private reconnectDelay: number = 1000; // Initial reconnect delay (1 second)
  private maxReconnectDelay: number = 10000; // Maximum reconnect delay (10 seconds)
  private messageHandler: ((message: any) => void) | null = null; // Callback for received messages
  private isReconnecting: boolean = false; // Prevent concurrent reconnections

  constructor() {
    this.connect(); // Try to connect as soon as the service is instantiated
  }

  // Function to connect to the WebSocket server
  private connect() {
    if (!this.socket) {
      this.socket = new WebSocket(this.url);

      this.socket.onopen = () => {
        console.log("Connected to WebSocket server");
        this.isConnected = true;
        this.reconnectDelay = 1000; // Reset the reconnect delay
        this.isReconnecting = false;
      };

      this.socket.onclose = () => {
        console.log("Disconnected from WebSocket server");
        this.isConnected = false;
        this.socket = null;
        this.attemptReconnect();
      };

      this.socket.onerror = (error) => {
        console.error("WebSocket error:", error);
        this.isConnected = false;
        this.socket = null;
        this.attemptReconnect();
      };

      this.socket.onmessage = (event) => {
        const message = JSON.parse(event.data);
        console.log("Received message:", message);
        if (this.messageHandler) {
          this.messageHandler(message); // Pass the message to the registered handler
        }
      };
    }
  }

  // Function to attempt reconnection with exponential backoff
  private attemptReconnect() {
    if (!this.isReconnecting && !this.isConnected) {
      this.isReconnecting = true;
      console.log(`Reconnecting in ${this.reconnectDelay / 1000} seconds...`);
      setTimeout(() => {
        this.connect(); // Try to reconnect
        this.reconnectDelay = Math.min(this.reconnectDelay * 2, this.maxReconnectDelay); // Exponential backoff
      }, this.reconnectDelay);
    }
  }

  // Function to send a message to the WebSocket server
  sendMessage(message: { userId: string; userName: string; content: string }) {
    if (!this.isConnected) {
      console.warn("WebSocket is not open. Trying to reconnect...");
      this.connect(); // Attempt to reconnect if not connected
      return;
    }

    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify(message));
      console.log("Message sent:", message);
    } else {
      console.warn("WebSocket is not open. Message not sent.");
    }
  }

  // Function to register a handler for incoming messages
  onMessage(handler: (message: any) => void) {
    this.messageHandler = handler;
    return handler;
  }

  // Function to close the WebSocket connection
  close() {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
      this.isConnected = false;
      console.log("WebSocket connection closed.");
    }
  }
}

// Usage example
const webSocketService = new WebSocketService();
webSocketService.onMessage((message) => {
  console.log("Processing received message:", message);
  // Add custom logic for handling received messages here
});
export default webSocketService;
