
interface SendMessageResponse {
  conversation_id: number;
  response: string;
  tool_calls?: Array<any>;
}

/**
 * Sends a message to the chat API and returns the AI response
 * @param message The user's message to send
 * @param userId The authenticated user's ID (required)
 * @param accessToken The user's authentication token (required)
 * @param conversationId Optional conversation ID for continuing conversations
 * @returns Promise resolving to the AI response
 */
export const sendMessage = async (
  message: string,
  userId: string,  // User ID is now required
  accessToken: string,  // Access token is now required
  conversationId?: string
): Promise<SendMessageResponse> => {
  try {
    console.log("API call details:");
    console.log("  - User ID:", userId);
    console.log("  - Has access token:", !!accessToken);
    console.log("  - Conversation ID:", conversationId);
    console.log("  - API URL:", `${process.env.NEXT_PUBLIC_API_URL}/api/${userId}/chat`);

    // Verify that both user ID and access token are provided
    if (!userId) {
      throw new Error("User ID is required for chat operations");
    }
    
    if (!accessToken) {
      throw new Error("Authentication token is required for chat operations");
    }

    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${accessToken}`,  // Always include the authorization header
    };

    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/${userId}/chat`, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        message,
        conversation_id: conversationId, // Optional conversation ID for continuing conversations
      }),
    });

    console.log("Response status:", response.status);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: 'Unknown error' }));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error sending message:', error);
    throw error;
  }
};

/**
 * Gets conversation history for a specific conversation
 * @param conversationId The ID of the conversation to retrieve
 * @param accessToken The user's authentication token
 * @returns Promise resolving to the conversation history
 */
export const getConversationHistory = async (
  userId: string,
  conversationId: number,
  accessToken: string
): Promise<any> => {
  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/${userId}/conversations/${conversationId}/history`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: 'Unknown error' }));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error getting conversation history:', error);
    throw error;
  }
};