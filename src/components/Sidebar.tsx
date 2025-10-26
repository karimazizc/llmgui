import React from 'react';
import type { Conversation } from '../types';

interface SidebarProps {
  conversations: Conversation[];
  currentConversationId: string | null;
  onSelectConversation: (id: string) => void;
  onNewConversation: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({
  conversations,
  currentConversationId,
  onSelectConversation,
  onNewConversation,
}) => {
  return (
    <div className="w-64 bg-gray-900 text-white flex flex-col">
      <div className="p-4 border-b border-gray-700">
        <button
          onClick={onNewConversation}
          className="w-full px-4 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg font-medium transition-colors duration-200"
        >
          + New Chat
        </button>
      </div>
      
      <div className="flex-1 overflow-y-auto p-2">
        <div className="space-y-1">
          {conversations.map((conversation) => (
            <button
              key={conversation.id}
              onClick={() => onSelectConversation(conversation.id)}
              className={`w-full text-left px-3 py-3 rounded-lg transition-colors duration-200 ${
                currentConversationId === conversation.id
                  ? 'bg-gray-700'
                  : 'hover:bg-gray-800'
              }`}
            >
              <div className="font-medium truncate">{conversation.title}</div>
              <div className="text-xs text-gray-400 mt-1">
                {new Date(conversation.createdAt).toLocaleDateString()}
              </div>
            </button>
          ))}
        </div>
      </div>

      <div className="p-4 border-t border-gray-700">
        <div className="text-xs text-gray-400 text-center">
          LLM Chat Dashboard
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
