# dashboard-llm

A modern, responsive GUI for Large Language Model chat applications, similar to ChatGPT and Claude interfaces.

![Chat Interface](https://github.com/user-attachments/assets/4a98fa3b-f40c-4556-91d8-e9c2277dad01)

## Features

- 💬 **Clean Chat Interface**: Modern, intuitive design with user and assistant message differentiation
- 📝 **Multiple Conversations**: Create and manage multiple chat sessions
- 🎨 **Responsive Design**: Built with Tailwind CSS for a polished, responsive UI
- ⚡ **Fast Performance**: Built with Vite and React for optimal performance
- 🔄 **Auto-scroll**: Messages automatically scroll to the latest message
- ⌨️ **Keyboard Shortcuts**: Press Enter to send, Shift+Enter for new lines

## Screenshots

### Chat Conversation
![Chat with Messages](https://github.com/user-attachments/assets/ce328a49-2589-478d-8bbb-03b1dfa53ae2)

### New Chat
![New Chat](https://github.com/user-attachments/assets/4015a7df-2cd2-49aa-922a-ddef8b5bb885)

## Getting Started

### Prerequisites

- Node.js 18+ and npm

### Installation

1. Clone the repository:
```bash
git clone https://github.com/karimazizc/dashboard-llm.git
cd dashboard-llm
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open your browser and navigate to `http://localhost:5173`

### Building for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

### Preview Production Build

```bash
npm run preview
```

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling
- **PostCSS** - CSS processing

## Project Structure

```
src/
├── components/
│   ├── ChatInput.tsx      # Message input component
│   ├── Message.tsx        # Individual message display
│   ├── MessageList.tsx    # List of messages with auto-scroll
│   └── Sidebar.tsx        # Conversation sidebar
├── types.ts               # TypeScript type definitions
├── App.tsx                # Main application component
├── main.tsx               # Application entry point
└── index.css              # Global styles
```

## Usage

### Creating a New Chat

Click the "+ New Chat" button in the sidebar to start a new conversation.

### Sending Messages

1. Type your message in the input box at the bottom
2. Press Enter or click the "Send" button
3. The AI response will appear automatically (currently simulated)

### Switching Between Conversations

Click on any conversation in the sidebar to switch to it.

## Connecting to an LLM API

This is a frontend-only demo. To connect to a real LLM API:

1. Add your preferred LLM API integration (OpenAI, Anthropic, local model, etc.)
2. Update the `handleSendMessage` function in `src/App.tsx`
3. Replace the simulated response with actual API calls
4. Add error handling and loading states

Example integration points:
- OpenAI GPT API
- Anthropic Claude API
- Local models via Ollama
- Custom backend API

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Customization

- **Colors**: Modify `tailwind.config.js` to change the color scheme
- **Components**: All components are in `src/components/` and can be customized
- **Message Display**: Edit `Message.tsx` to change message appearance
- **Sidebar**: Modify `Sidebar.tsx` to add features like search or filters

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
