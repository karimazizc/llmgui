import { useState } from 'react';
import type { Conversation, Message as MessageType } from './types';
import Sidebar from './components/Sidebar';
import MessageList from './components/MessageList';
import ChatInput from './components/ChatInput';

function App() {
  const [conversations, setConversations] = useState<Conversation[]>([
    {
      id: '1',
      title: 'Welcome Chat',
      messages: [
        {
          id: 'm1',
          role: 'assistant',
          content: 'Hello! I\'m your AI assistant. How can I help you today?',
          timestamp: new Date(),
        },
      ],
      createdAt: new Date(),
    },
  ]);
  const [currentConversationId, setCurrentConversationId] = useState<string>('1');

  const currentConversation = conversations.find(
    (conv) => conv.id === currentConversationId
  );

  const handleSendMessage = (content: string) => {
    if (!currentConversationId) return;

    const newUserMessage: MessageType = {
      id: `m${Date.now()}`,
      role: 'user',
      content,
      timestamp: new Date(),
    };

    setConversations((prevConversations) =>
      prevConversations.map((conv) =>
        conv.id === currentConversationId
          ? {
              ...conv,
              messages: [...conv.messages, newUserMessage],
              title:
                conv.messages.length === 1
                  ? content.slice(0, 30) + (content.length > 30 ? '...' : '')
                  : conv.title,
            }
          : conv
      )
    );

    // Simulate AI response
    setTimeout(() => {
      const aiResponse: MessageType = {
        id: `m${Date.now()}`,
        role: 'assistant',
        content: `This is a demo response. In a real application, this would connect to an LLM API (like OpenAI, Anthropic, or a local model) to generate intelligent responses to: "${content}"`,
        timestamp: new Date(),
      };

      setConversations((prevConversations) =>
        prevConversations.map((conv) =>
          conv.id === currentConversationId
            ? { ...conv, messages: [...conv.messages, aiResponse] }
            : conv
        )
      );
    }, 1000);
  };

  const handleNewConversation = () => {
    const newConv: Conversation = {
      id: `conv${Date.now()}`,
      title: 'New Chat',
      messages: [],
      createdAt: new Date(),
    };
    setConversations((prev) => [...prev, newConv]);
    setCurrentConversationId(newConv.id);
  };

  const handleSelectConversation = (id: string) => {
    setCurrentConversationId(id);
  };

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar
        conversations={conversations}
        currentConversationId={currentConversationId}
        onSelectConversation={handleSelectConversation}
        onNewConversation={handleNewConversation}
      />
      <div className="flex-1 flex flex-col">
        <header className="bg-white border-b border-gray-200 px-6 py-4">
          <h1 className="text-2xl font-bold text-gray-800">
            {currentConversation?.title || 'Chat'}
          </h1>
        </header>
        <MessageList messages={currentConversation?.messages || []} />
        <ChatInput onSendMessage={handleSendMessage} />
      </div>
    </div>
  );
}

export default App;

