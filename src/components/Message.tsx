import React from 'react';
import type { Message as MessageType } from '../types';

interface MessageProps {
  message: MessageType;
}

const Message: React.FC<MessageProps> = ({ message }) => {
  const isUser = message.role === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div
        className={`max-w-[80%] rounded-lg px-4 py-3 ${
          isUser
            ? 'bg-blue-600 text-white'
            : 'bg-gray-100 text-gray-900 border border-gray-200'
        }`}
      >
        <div className="flex items-start gap-2">
          <div className="flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center text-xs font-semibold">
            {isUser ? '👤' : '🤖'}
          </div>
          <div className="flex-1">
            <div className="whitespace-pre-wrap break-words">{message.content}</div>
            <div
              className={`text-xs mt-1 ${
                isUser ? 'text-blue-100' : 'text-gray-500'
              }`}
            >
              {new Date(message.timestamp).toLocaleTimeString()}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Message;
